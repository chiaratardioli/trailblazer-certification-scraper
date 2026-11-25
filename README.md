# Trailblazer Certification & Achievement Scraper

A Python application that retrieves publicly available Salesforce Trailblazer certification and achievement data for multiple profiles, processes the results, and exports consolidated CSV and Excel reports.

The application collects certifications, badges, superbadges, Trailblazer rank and points, Agentblazer status levels, and earned event stamps.

## Features

### Profile and certification data
- Reads multiple Trailblazer profiles from an input CSV file.
- Retrieves publicly available certification data through the Trailblazer GraphQL API.
- Saves raw API responses as separate JSON files.
- Extracts and normalizes certification information.
- Removes duplicate certification records without losing records belonging to different profiles.
- Groups certifications by completion year.
- Exports consolidated certification results to CSV and Excel.
- Creates a separate Excel worksheet for each certification year.

### Trailblazer achievements
- Retrieves Trailblazer rank and points.
- Collects total badge counts and completed trail statistics.
- Retrieves earned badges, including badge names, types, descriptions, and earning dates.
- Identifies and exports superbadges separately.
- Retrieves Agentblazer status levels, including level, edition, completion date, and progress.
- Retrieves earned event stamps, including event names, dates, locations, and related information.
- Supports paginated retrieval of badges and earned stamps.

### Reporting and reliability
- Generates individual CSV reports for each achievement category.
- Creates a consolidated Excel workbook containing five achievement worksheets.
- Handles individual profile retrieval errors without stopping the entire scraping process.
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
│   ├── exporter.py
│   ├── achievement_scraper.py
│   ├── achievement_extractor.py
│   └── achievement_exporter.py
├── tests/
│   ├── __init__.py
│   ├── test_extractor.py
│   ├── test_processor.py
│   ├── test_exporter.py
│   ├── test_main.py
│   ├── test_scraper.py
│   ├── test_achievement_extractor.py
│   ├── test_achievement_scraper.py
│   └── test_achievement_exporter.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.11 or later
- Internet connection
- Access to publicly available Salesforce Trailblazer profile data

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

1. Load profiles from the input CSV.
2. Retrieve certification data for each profile.
3. Retrieve Trailblazer rank, points, and profile statistics.
4. Retrieve earned badges and identify superbadges.
5. Retrieve Agentblazer status levels.
6. Retrieve earned event stamps.
7. Save raw API responses as JSON files.
8. Extract and normalize the collected data.
9. Generate consolidated CSV and Excel reports.

If an individual data retrieval operation fails, the application logs the error and continues with the remaining operations and profiles where possible.

## Output Files

All generated files are stored in:

```text
data/
├── raw/
└── processed/
```

### Raw API responses

Raw API responses are saved as JSON files in:

```text
data/raw/
```

These files preserve the retrieved data for inspection and troubleshooting.

### Processed reports

The application generates the following files in `data/processed/`:

| File | Description |
|---|---|
| `all_trailblazer_certifications.csv` | Consolidated certification records |
| `all_trailblazer_certifications.xlsx` | Certification workbook, including yearly worksheets |
| `profile_summary.csv` | Profile rank, points, badge counts, and trail statistics |
| `badges.csv` | All retrieved earned badges |
| `superbadges.csv` | Earned superbadges |
| `agentblazer.csv` | Agentblazer status and level records |
| `stamps.csv` | Earned event stamps |
| `all_trailblazer_achievements.xlsx` | Consolidated achievement workbook |

### Excel workbooks

**Certification workbook — `all_trailblazer_certifications.xlsx`**

Contains:
- An **All Certifications** worksheet with all retrieved certification records.
- Separate worksheets for each certification completion year.

**Achievement workbook — `all_trailblazer_achievements.xlsx`**

Contains five worksheets:
- **Profile Summary** — rank, points, badge counts, superbadge counts, and completed trails.
- **Badges** — all retrieved badges.
- **Superbadges** — earned superbadges only.
- **Agentblazer** — Agentblazer levels and completion information.
- **Stamps** — earned event stamps.

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
- GraphQL API requests and error handling.
- Achievement extraction and classification.
- Badge and stamp pagination.
- Agentblazer data extraction.
- Achievement CSV and Excel exports.

## Technical Notes and Limitations

- The application retrieves publicly available Trailblazer profile data only.
- It relies on Salesforce Trailblazer GraphQL endpoints, which are not documented as a stable public API for this project.
- API availability, endpoint behavior, and response structures may change over time.
- Some achievement data, such as earned event stamps, is retrieved through a separate Trailhead API endpoint.
- Profiles with restricted visibility may return incomplete or unavailable information.
- Not every profile has earned certifications, superbadges, Agentblazer levels, or event stamps.
- Badge and stamp retrieval supports pagination to collect multiple pages of results.
- Raw API responses are retained separately to support inspection and troubleshooting.
- Generated raw and processed data files, as well as the local profile list, are excluded from Git.

## Technologies

- Python 3.11+
- Requests
- Pandas
- OpenPyXL
- Pytest
- GraphQL

## Project Status

The project currently includes certification and achievement collection, CSV and Excel reporting, and automated test coverage.

The latest verified test run completed successfully with **39 passing tests**.
