# eCourts India - Case Listing Fetcher Tools

A Python command-line tool to help interact with eCourts India services. This tool fetches metadata and provides structured instructions for case searches that require CAPTCHA                  verification.

## What This Tool Does

### ✅ Working Features (No CAPTCHA Required)
- **Fetch State Codes** - Get list of all Indian states and their codes
- **Fetch Court Codes** - Get district/court complex codes for any state  
- **Fetch Case Types** - Get available case type codes for specific courts
- **Prepare Search URLs** - Generate properly formatted search URLs

### 📋 Instruction Features (Manual CAPTCHA Required)
- **CNR Search Preparation** - Get step-by-step instructions to search by CNR
- **Case Details Search** - Instructions for case type/number/year searches
- **Cause List Download** - Instructions to download daily cause lists
- **Listing Check Guide** - How to verify if case is listed today/tomorrow

## Important Limitations

⚠️ **CAPTCHA Requirement**: The official eCourts website requires CAPTCHA verification for all case searches and downloads. This tool:
- **CAN** fetch publicly available metadata (state codes, court codes, case types)
- **CANNOT** bypass CAPTCHA or fully automate searches
- **PROVIDES** detailed instructions and URLs for manual completion

This is an instructional and preparation tool, not a fully automated scraper.

## Requirements

- Python 3.11+
- Internet connection
- Dependencies: `requests`, `beautifulsoup4`, `python-dateutil`

## Installation

Dependencies are managed via uv:
```bash
# Already installed in this environment
uv add requests beautifulsoup4 python-dateutil
```

## Usage

Run the script:
```bash
python ecourts_fetcher.py
```

### Available Options

#### 1. View State Codes
Fetches and displays all Indian state codes from eCourts.
```
Example Output:
  [7 ] Delhi
  [12] Maharashtra
  [32] Kerala
```

#### 2. View Court/District Codes
Get court complex codes for a specific state.
```
Input: State Code (e.g., 7 for Delhi)
Output: List of courts with their codes
```

#### 3. View Case Types
Get case type codes for a specific court.
```
Input: State Code + District Code
Output: Available case types (CRL, CIV, etc.)
```

#### 4. Prepare CNR Search
Generates instructions and URLs for CNR-based case search.
```
Input: CNR Number (e.g., MHAU019999992015)
Output: Step-by-step manual search instructions
```

#### 5. Prepare Case Details Search
Provides instructions for searching by case details.
```
Input: State, District, Case Type, Number, Year
Output: Manual search workflow
```

#### 6. Prepare Cause List Download
Instructions to download daily court cause lists.
```
Input: State, District, Date (optional)
Output: Download instructions with proper URLs
```

#### 7. Get Listing Check Instructions
Learn how to check if a case is listed today or tomorrow.
```
Output: Instructions on finding serial number and court details
```

## Example Workflows

### Get Metadata for Delhi Courts
```
1. Select option 1 → View State Codes
   Note: Delhi = 7
2. Select option 2 → Enter state code: 7
   View all Delhi court codes
3. Select option 3 → Enter state: 7, district: [your code]
   View case types for that court
```

### Prepare Case Search
```
1. Use options 1-3 to get correct codes
2. Select option 5 → Enter all case details
3. Follow printed instructions to search on eCourts website
4. Complete CAPTCHA manually
5. View results on eCourts portal
```

### Check Today's Listings
```
1. Select option 7 → Enter your case reference
2. Follow instructions to access cause list
3. Download PDF and search for your case number
4. Note serial number and court hall from PDF
```

## What You'll Need to Do Manually

1. **CAPTCHA Solving** - All eCourts searches require CAPTCHA verification
2. **Case Search Submission** - Use provided URLs and parameters on eCourts website
3. **PDF Downloads** - Download cause lists and case documents through browser
4. **Result Viewing** - View case details on the official eCourts portal

## Output Examples

### State Codes Output
```json
{
  "states": {
    "Delhi": "7",
    "Maharashtra": "12",
    "Karnataka": "14"
  },
  "count": 37
}
```

### CNR Search Preparation
```
CNR: MHAU019999992015

📍 Manual Steps Required:
  1. Visit: https://services.ecourts.gov.in/ecourtindia_v6/
  2. Enter CNR number: MHAU019999992015
  3. Solve CAPTCHA
  4. Click Search to view case details

🔗 Direct URL: https://services.ecourts.gov.in/...
```

### Listing Check Instructions
```
To check if your case is listed today or tomorrow:
  1. Visit: https://services.ecourts.gov.in/ecourtindia_v6/
  2. Go to 'Daily Orders/Causelist'
  3. Select your court
  4. Check dates: 2025-10-14 and 2025-10-15
  5. Search for your case number in the PDF

🔍 What to Look For:
  • Serial Number: Case order in the day's list
  • Court Name: Court/Judge name
  • Court Hall: Court room/hall number
```

## Alternative Solutions

For **fully automated** access, consider:

1. **Official eCourts Mobile App** (Android/iOS)
   - Free, official, no CAPTCHA for logged-in users
   
2. **Third-Party APIs** (Paid Services)
   - Kleopatra E-Courts API: https://court-api.kleopatra.io
   - Surepass eCourts API: https://surepass.io
   - CrimeCheck API: https://crimecheck.in
   
3. **Manual Portal Access**
   - Most reliable for legal work
   - Official website: https://services.ecourts.gov.in/

## Technical Details

### Endpoints Used
- `/cases/s_state_qry.php` - State codes (working)
- `/cases/s_complex_qry.php` - Court codes (working)
- `/cases/s_casetype_qry.php` - Case types (working)
- `/cases/cnr_qry.php` - CNR search (requires CAPTCHA)
- `/cases/case_no_qry.php` - Case search (requires CAPTCHA)

### Why CAPTCHA Cannot Be Automated
- Legal compliance - eCourts terms of service
- Security measure to prevent abuse
- Protects judicial data integrity
- Ethical scraping practices

## Legal & Ethical Use

✅ **Appropriate Uses:**
- Personal case tracking
- Legal research
- Understanding court procedures
- Educational purposes

❌ **Inappropriate Uses:**
- Bulk data scraping
- Bypassing security measures
- Commercial resale of data
- Overloading court servers

## Support

For eCourts website issues:
- **Official Portal**: https://services.ecourts.gov.in/
- **Helpdesk**: Available on eCourts website
- **Mobile Apps**: Google Play / App Store

For this tool:
- Check code comments
- Review printed instructions
- Follow manual verification steps

## License

Educational and research purposes only. Respect eCourts terms of service and Indian judicial system guidelines.
