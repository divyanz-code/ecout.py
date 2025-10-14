import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import sys
import os
import re

class ECourtsFetcher:
    def __init__(self):
        self.base_url = "https://services.ecourts.gov.in/ecourtindia_v6/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': self.base_url
        })
        self.today = datetime.now().date()
        self.tomorrow = self.today + timedelta(days=1)
    
    def get_captcha_info(self):
        """Get CAPTCHA image URL for manual solving"""
        captcha_url = f"{self.base_url}vendor/securimage/securimage_show.php"
        return {
            'captcha_url': captcha_url,
            'message': 'Please solve CAPTCHA at the eCourts website to proceed'
        }
    
    def get_state_codes(self):
        """Fetch available state codes - WORKING"""
        try:
            url = f"{self.base_url}cases/s_state_qry.php"
            response = self.session.get(url, timeout=15)
            
            if response.status_code != 200:
                return {'error': f'HTTP {response.status_code}', 'states': {}}
            
            soup = BeautifulSoup(response.content, 'html.parser')
            states = {}
            
            # Try multiple selector patterns
            select_tag = soup.find('select', {'id': 'sess_state_code'}) or \
                        soup.find('select', {'name': 'state_code'}) or \
                        soup.find('select')
            
            if select_tag:
                for option in select_tag.find_all('option'):
                    value = option.get('value', '')
                    if isinstance(value, str):
                        value = value.strip()
                    text = option.text.strip()
                    if value and text and value != '0':
                        states[text] = value
            
            return {'states': states, 'count': len(states)}
        except requests.exceptions.RequestException as e:
            return {'error': f'Network error: {str(e)}', 'states': {}}
        except Exception as e:
            return {'error': f'Parse error: {str(e)}', 'states': {}}
    
    def get_court_complex_codes(self, state_code):
        """Get court complex codes for a state - WORKING"""
        try:
            url = f"{self.base_url}cases/s_complex_qry.php"
            data = {'state_code': state_code, 'dist_code': ''}
            response = self.session.post(url, data=data, timeout=15)
            
            if response.status_code != 200:
                return {'error': f'HTTP {response.status_code}', 'courts': {}}
            
            soup = BeautifulSoup(response.content, 'html.parser')
            courts = {}
            
            select_tag = soup.find('select')
            if select_tag:
                for option in select_tag.find_all('option'):
                    value = option.get('value', '')
                    if isinstance(value, str):
                        value = value.strip()
                    text = option.text.strip()
                    if value and text and value != '0':
                        courts[text] = value
            
            return {'courts': courts, 'count': len(courts), 'state': state_code}
        except requests.exceptions.RequestException as e:
            return {'error': f'Network error: {str(e)}', 'courts': {}}
        except Exception as e:
            return {'error': f'Parse error: {str(e)}', 'courts': {}}
    
    def get_case_types(self, state_code, dist_code):
        """Fetch case types for a court - WORKING"""
        try:
            url = f"{self.base_url}cases/s_casetype_qry.php"
            data = {
                'state_code': state_code,
                'dist_code': dist_code
            }
            response = self.session.post(url, data=data, timeout=15)
            
            if response.status_code != 200:
                return {'error': f'HTTP {response.status_code}', 'case_types': {}}
            
            soup = BeautifulSoup(response.content, 'html.parser')
            case_types = {}
            
            select_tag = soup.find('select')
            if select_tag:
                for option in select_tag.find_all('option'):
                    value = option.get('value', '')
                    if isinstance(value, str):
                        value = value.strip()
                    text = option.text.strip()
                    if value and text and value != '0':
                        case_types[text] = value
            
            return {'case_types': case_types, 'count': len(case_types)}
        except Exception as e:
            return {'error': str(e), 'case_types': {}}
    
    def prepare_cnr_search_url(self, cnr_number):
        """Prepare CNR search - requires manual CAPTCHA"""
        cnr_clean = cnr_number.replace('-', '').replace(' ', '').upper()
        
        return {
            'cnr': cnr_clean,
            'search_url': f"{self.base_url}?p=home/index&app_token=",
            'endpoint': f"{self.base_url}cases/cnr_qry.php",
            'method': 'POST',
            'required_fields': {
                'cnr_number': cnr_clean,
                'captcha': 'REQUIRED - Must be solved manually'
            },
            'instructions': [
                f"1. Visit: {self.base_url}",
                "2. Enter CNR number: " + cnr_clean,
                "3. Solve CAPTCHA",
                "4. Click Search to view case details"
            ],
            'captcha_url': f"{self.base_url}vendor/securimage/securimage_show.php"
        }
    
    def prepare_case_search_url(self, state_code, dist_code, case_type, case_number, case_year):
        """Prepare case details search - requires manual CAPTCHA"""
        return {
            'state_code': state_code,
            'dist_code': dist_code,
            'case_type': case_type,
            'case_number': case_number,
            'case_year': case_year,
            'search_url': f"{self.base_url}?p=casestatus/case_status_result",
            'endpoint': f"{self.base_url}cases/case_no_qry.php",
            'method': 'POST',
            'required_fields': {
                'state_code': state_code,
                'dist_code': dist_code,
                'case_type': case_type,
                'case_no': case_number,
                'rgyear': case_year,
                'captcha': 'REQUIRED - Must be solved manually',
                'caseNoType': 'new',
                'displayOldCaseNo': 'NO',
                'action': 'showRecords'
            },
            'instructions': [
                f"1. Visit: {self.base_url}",
                "2. Go to 'Case Status' menu",
                "3. Select state and district",
                f"4. Select case type: {case_type}",
                f"5. Enter case number: {case_number}",
                f"6. Enter year: {case_year}",
                "7. Solve CAPTCHA and submit"
            ]
        }
    
    def prepare_cause_list_download(self, state_code, dist_code, date=None):
        """Prepare cause list download - requires manual CAPTCHA"""
        if date is None:
            date = self.today
        
        date_str = date.strftime("%d-%m-%Y")
        
        return {
            'state_code': state_code,
            'dist_code': dist_code,
            'date': date_str,
            'download_url': f"{self.base_url}?p=casestatus/cause_list",
            'instructions': [
                f"1. Visit: {self.base_url}",
                "2. Go to 'Daily Orders/Causelist' menu",
                f"3. Select State: {state_code}",
                f"4. Select District/Court: {dist_code}",
                f"5. Select Date: {date_str}",
                "6. Solve CAPTCHA",
                "7. Click 'View' to download PDF"
            ],
            'note': 'Cause list will be downloaded as PDF'
        }
    
    def check_listing_instructions(self, case_ref):
        """Provide instructions to check if case is listed today/tomorrow"""
        return {
            'today': str(self.today),
            'tomorrow': str(self.tomorrow),
            'case_reference': case_ref,
            'instructions': [
                "To check if your case is listed today or tomorrow:",
                f"1. Visit: {self.base_url}",
                "2. Go to 'Daily Orders/Causelist'",
                "3. Select your court",
                f"4. Check dates: {self.today} and {self.tomorrow}",
                "5. Search for your case number in the PDF",
                "6. Note: Serial number and court hall shown in cause list"
            ],
            'what_to_look_for': {
                'serial_number': 'Case order in the day\'s list',
                'court_name': 'Court/Judge name',
                'court_hall': 'Court room/hall number',
                'time': 'Hearing time if specified'
            }
        }


def display_menu():
    """Display main menu"""
    print("\n" + "="*70)
    print("          eCourts India - Case Listing Fetcher Tool")
    print("="*70)
    print("\nWorking Features (No CAPTCHA required):")
    print("  1. View State Codes")
    print("  2. View Court/District Codes for a State")
    print("  3. View Case Types for a Court")
    print("\nManual CAPTCHA Required:")
    print("  4. Prepare CNR Search (Get Instructions)")
    print("  5. Prepare Case Details Search (Get Instructions)")
    print("  6. Prepare Cause List Download (Get Instructions)")
    print("  7. Get Listing Check Instructions")
    print("\nOther:")
    print("  8. Exit")
    print("\n" + "="*70)


def main():
    """Main function"""
    fetcher = ECourtsFetcher()
    
    print("\n" + "="*70)
    print("       Welcome to eCourts India Case Listing Fetcher")
    print("="*70)
    print("\n📋 IMPORTANT INFORMATION:")
    print("  ✓ This tool fetches metadata (states, courts, case types)")
    print("  ✓ Case searches require CAPTCHA - tool provides instructions")
    print("  ✓ For actual case data, you must visit eCourts website")
    print("  ✓ Tool helps prepare searches and understand requirements")
    print("\n🌐 Official Website: https://services.ecourts.gov.in/")
    print("="*70)
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            print("\n--- Fetching State Codes ---")
            result = fetcher.get_state_codes()
            
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
            
            if result.get('states'):
                print(f"\n✓ Found {result['count']} states:")
                print("-" * 50)
                for name, code in sorted(result['states'].items()):
                    print(f"  [{code:2}] {name}")
            else:
                print("❌ No states found")
        
        elif choice == '2':
            state = input("\nEnter State Code (e.g., 7 for Delhi): ").strip()
            if state:
                print(f"\n--- Fetching Courts for State: {state} ---")
                result = fetcher.get_court_complex_codes(state)
                
                if 'error' in result:
                    print(f"❌ Error: {result['error']}")
                
                if result.get('courts'):
                    print(f"\n✓ Found {result['count']} courts:")
                    print("-" * 50)
                    for name, code in sorted(result['courts'].items()):
                        print(f"  [{code:3}] {name}")
                else:
                    print("❌ No courts found")
        
        elif choice == '3':
            state = input("\nEnter State Code: ").strip()
            dist = input("Enter District/Court Code: ").strip()
            
            if state and dist:
                print(f"\n--- Fetching Case Types ---")
                result = fetcher.get_case_types(state, dist)
                
                if 'error' in result:
                    print(f"❌ Error: {result['error']}")
                
                if result.get('case_types'):
                    print(f"\n✓ Found {result['count']} case types:")
                    print("-" * 50)
                    for name, code in sorted(result['case_types'].items()):
                        print(f"  [{code:3}] {name}")
                else:
                    print("❌ No case types found")
        
        elif choice == '4':
            cnr = input("\nEnter CNR Number (e.g., MHAU019999992015): ").strip()
            if cnr:
                result = fetcher.prepare_cnr_search_url(cnr)
                print(f"\n--- CNR Search Preparation ---")
                print(f"CNR: {result['cnr']}")
                print(f"\n📍 Manual Steps Required:")
                for instruction in result['instructions']:
                    print(f"  {instruction}")
                print(f"\n🔗 Direct URL: {result['search_url']}")
                print(f"🎯 CAPTCHA: {result['captcha_url']}")
        
        elif choice == '5':
            print("\n--- Prepare Case Details Search ---")
            state = input("State Code: ").strip()
            dist = input("District Code: ").strip()
            case_type = input("Case Type Code: ").strip()
            case_num = input("Case Number: ").strip()
            case_year = input("Case Year: ").strip()
            
            if all([state, dist, case_type, case_num, case_year]):
                result = fetcher.prepare_case_search_url(
                    state, dist, case_type, case_num, case_year
                )
                print(f"\n--- Case Search Preparation ---")
                print(f"\n📍 Manual Steps Required:")
                for instruction in result['instructions']:
                    print(f"  {instruction}")
                print(f"\n🔗 Search URL: {result['search_url']}")
        
        elif choice == '6':
            print("\n--- Prepare Cause List Download ---")
            state = input("State Code: ").strip()
            dist = input("District/Court Code: ").strip()
            use_custom_date = input("Use custom date? (y/N): ").strip().lower()
            
            date_obj = None
            if use_custom_date == 'y':
                date_str = input("Enter date (DD-MM-YYYY): ").strip()
                try:
                    date_obj = datetime.strptime(date_str, "%d-%m-%Y").date()
                except:
                    print("Invalid date format, using today")
            
            if state and dist:
                result = fetcher.prepare_cause_list_download(state, dist, date_obj)
                print(f"\n--- Cause List Download Preparation ---")
                print(f"Date: {result['date']}")
                print(f"\n📍 Manual Steps Required:")
                for instruction in result['instructions']:
                    print(f"  {instruction}")
                print(f"\n🔗 URL: {result['download_url']}")
                print(f"📝 Note: {result['note']}")
        
        elif choice == '7':
            case_ref = input("\nEnter Case Reference (CNR or Case Number): ").strip()
            if case_ref:
                result = fetcher.check_listing_instructions(case_ref)
                print(f"\n--- Listing Check Instructions ---")
                print(f"Case: {result['case_reference']}")
                print(f"Today: {result['today']}")
                print(f"Tomorrow: {result['tomorrow']}")
                print(f"\n📍 How to Check:")
                for instruction in result['instructions']:
                    print(f"  {instruction}")
                print(f"\n🔍 What to Look For:")
                for key, value in result['what_to_look_for'].items():
                    print(f"  • {key.replace('_', ' ').title()}: {value}")
        
        elif choice == '8':
            print("\n✓ Thank you for using eCourts Fetcher. Goodbye!")
            sys.exit(0)
        
        else:
            print("\n❌ Invalid choice. Please select 1-8.")
        
        input("\n[Press Enter to continue...]")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ Program interrupted. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
