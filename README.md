# Trailblazer Certification Scraper

A Python application that retrieves publicly available Salesforce Trailblazer certification data for multiple profiles, processes the results, and exports consolidated CSV and Excel reports.

## Features

- Reads multiple Trailblazer profiles from an input CSV file.
- Retrieves public certification data through the Trailblazer GraphQL API.
- Saves the raw API response as a separate JSON file for each profile.
- Extracts and normalizes certification information.
- Removes duplicate certification records without losing certifications belonging to different profiles.
- Groups certifications by completion year.
- Exports consolidated results to CSV and Excel.
- Creates a separate Excel worksheet for each certification year.
- Includes automated tests for the main project components.

## Project Structure

```text
trailblazer-certification-scraper/
├── config/
│   ├── __init__.py
│   └── settings.py
├── input/
│   ├── profiles.csv
│   └── profiles.example.csv
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── __init__.py
│   ├── scraper.py
│   ├── extractor.py
│   ├── processor.py
│   └── exporter.py
├── tests/
│   ├── __init__.py
│   ├── test_extractor.py
│   ├── test_processor.py
│   ├── test_exporter.py
│   ├── test_main.py
│   └── test_scraper.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.11 or later
- Internet connection
- Access to publicly available Trailblazer profile data

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone <repository-url>
cd trailblazer-certification-scraper
```

Install the dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Input Configuration

Create a file named `input/profiles.csv`.

The file must contain two columns:

| Column | Description |
|---|---|
| `profile_name` | Name associated with the Trailblazer profile |
| `profile_url` | Public Salesforce Trailblazer profile URL |

Example:

```csv
profile_name,profile_url
Example User,https://www.salesforce.com/trailblazer/exampleuser
```

An example input file is available at `input/profiles.example.csv`.

The actual `input/profiles.csv` file is excluded from Git to avoid committing personal or project-specific profile lists.

## How to Run

From the project root directory, execute:

```bash
python3 main.py
```

The application will:

1. Load the profiles from the input CSV.
2. Retrieve the public certification data for each profile.
3. Save the raw GraphQL response as a JSON file.
4. Extract and clean certification records.
5. Remove duplicate records.
6. Group certifications by completion year.
7. Generate consolidated CSV and Excel reports.

If a profile cannot be processed, the application logs the error and continues with the remaining profiles.

## Output Files

### Raw API responses

Each profile gets its own JSON file in:

```text
data/raw/
```

Example:

```text
chiara_tardioli_trailblazer_api.json
```

### Processed reports

The application generates two consolidated files in:

```text
data/processed/
```

- `all_trailblazer_certifications.csv`
- `all_trailblazer_certifications.xlsx`

The Excel workbook contains:
- An **All Certifications** worksheet with all retrieved records.
- One worksheet for each certification completion year.

## Running Tests

Run the complete test suite from the project root:

```bash
python3 -m pytest -v
```

The tests cover:
- Certification extraction and date parsing.
- Data cleaning, deduplication, and yearly grouping.
- CSV and Excel exports.
- Input profile loading and validation.
- API requests and error handling.

## Technical Notes and Limitations

- The application retrieves publicly available profile data only.
- Results depend on the information exposed by the Trailblazer GraphQL API.
- Profiles with no publicly available certifications may return no certification records.
- API availability and response structure may change over time.
- Raw API responses are retained separately to support inspection and troubleshooting.
- Generated raw and processed data files are excluded from Git.

## Technologies

- Python
- Requests
- Pandas
- OpenPyXL
- Pytest
- GraphQL

