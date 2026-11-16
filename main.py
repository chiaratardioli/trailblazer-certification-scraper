
import logging
import pandas as pd

from config.settings import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    create_directories,
)

from src.scraper import scrape_profile
from src.extractor import extract_certifications
from src.processor import (
    clean_certifications,
    group_by_year,
    print_report,
)
from src.exporter import export_certifications


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Input CSV containing the Trailblazer profiles
PROFILES_FILE = "input/profiles.csv"


def load_profiles():
    """Load and validate Trailblazer profiles from the input CSV."""

    try:
        profiles_df = pd.read_csv(PROFILES_FILE)

        required_columns = {"profile_name", "profile_url"}

        if not required_columns.issubset(profiles_df.columns):
            raise ValueError(
                "The CSV must contain profile_name and profile_url columns."
            )

        profiles_df = profiles_df.dropna(
            subset=["profile_name", "profile_url"]
        )

        return profiles_df.to_dict("records")

    except FileNotFoundError:
        raise FileNotFoundError(
            "Profiles CSV not found: {}".format(PROFILES_FILE)
        )


def main():
    """Run the multi-profile scraping, processing and export workflow."""

    try:
        # 1. Create the project data folders
        create_directories()

        logger.info("Starting Trailblazer certification scraper")

        # 2. Load profiles from CSV
        profiles = load_profiles()

        if not profiles:
            logger.warning("No profiles found in the input CSV.")
            return

        logger.info("Found %d profiles to process", len(profiles))

        all_certifications = []
        successful_profiles = 0
        failed_profiles = 0

        # 3. Process each profile
        for profile in profiles:

            profile_name = str(profile["profile_name"]).strip()
            profile_url = str(profile["profile_url"]).strip()

            logger.info("Processing profile: %s", profile_name)

            try:
                # Retrieve API response and save individual JSON file
                response = scrape_profile(
                    profile_url,
                    profile_name,
                    RAW_DATA_DIR,
                )

                # Extract certifications
                certifications = extract_certifications(response)

                # Add profile information to every certification
                for cert in certifications:
                    cert["profile_name"] = profile_name
                    cert["profile_url"] = profile_url

                # Clean certifications
                certifications = clean_certifications(certifications)

                all_certifications.extend(certifications)

                successful_profiles += 1

                logger.info(
                    "Successfully processed %s: %d certifications",
                    profile_name,
                    len(certifications),
                )

            except Exception:
                failed_profiles += 1

                logger.exception(
                    "Failed to process profile: %s",
                    profile_name,
                )

                # Continue with the next profile
                continue

        # 4. Check whether any certifications were retrieved
        if not all_certifications:
            logger.warning("No certifications were retrieved.")
            logger.info(
                "Successful profiles: %d | Failed profiles: %d",
                successful_profiles,
                failed_profiles,
            )
            return

        # 5. Group all certifications by year
        grouped = group_by_year(all_certifications)

        # 6. Print the consolidated report
        print_report(grouped)

        # 7. Export consolidated CSV and Excel files
        export_certifications(
            all_certifications,
            output_dir=PROCESSED_DATA_DIR,
            filename="all_trailblazer_certifications",
        )

        logger.info(
            "Processing completed. Successful profiles: %d | Failed profiles: %d",
            successful_profiles,
            failed_profiles,
        )

        logger.info("Scraping and export completed successfully!")

    except Exception:
        logger.exception("The scraper failed.")
        raise


if __name__ == "__main__":
    main()
