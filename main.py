
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

from src.achievement_scraper import (
    fetch_profile_rank,
    fetch_profile_badges,
    fetch_agentblazer_status,
    fetch_profile_stamps,
)

from src.achievement_extractor import (
    extract_profile_summary,
    extract_badges,
    extract_superbadges,
    extract_agentblazer,
    extract_stamps,
)

from src.achievement_exporter import export_achievements


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

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
    """Run the certification and achievement scraping workflow."""

    try:
        # 1. Create project data folders
        create_directories()

        logger.info("Starting Trailblazer scraper")

        # 2. Load profiles
        profiles = load_profiles()

        if not profiles:
            logger.warning("No profiles found in the input CSV.")
            return

        logger.info("Found %d profiles to process", len(profiles))

        # 3. Prepare datasets
        all_certifications = []
        all_profile_summaries = []
        all_badges = []
        all_superbadges = []
        all_agentblazer = []
        all_stamps = []

        successful_profiles = 0
        failed_profiles = 0

        # 4. Process each profile
        for profile in profiles:

            profile_name = str(profile["profile_name"]).strip()
            profile_url = str(profile["profile_url"]).strip()

            logger.info("Processing profile: %s", profile_name)

            # --------------------------------
            # CERTIFICATIONS
            # --------------------------------
            try:
                response = scrape_profile(
                    profile_url,
                    profile_name,
                    RAW_DATA_DIR,
                )

                certifications = extract_certifications(response)

                for cert in certifications:
                    cert["profile_name"] = profile_name
                    cert["profile_url"] = profile_url

                certifications = clean_certifications(certifications)

                all_certifications.extend(certifications)

                successful_profiles += 1

                logger.info(
                    "Retrieved %d certifications for %s",
                    len(certifications),
                    profile_name,
                )

            except Exception:
                failed_profiles += 1
                logger.exception(
                    "Certification retrieval failed for %s",
                    profile_name,
                )

            # --------------------------------
            # PROFILE RANK AND SUMMARY
            # --------------------------------
            try:
                rank_data = fetch_profile_rank(
                    profile_url,
                    profile_name,
                    RAW_DATA_DIR,
                )

            except Exception:
                rank_data = None
                logger.exception(
                    "Rank retrieval failed for %s",
                    profile_name,
                )

            # --------------------------------
            # BADGES AND SUPERBADGES
            # --------------------------------
            profile_badges = []
            profile_superbadges = []

            try:
                badge_edges = fetch_profile_badges(
                    profile_url,
                    profile_name,
                    RAW_DATA_DIR,
                )

                profile_badges = extract_badges(
                    badge_edges,
                    profile_name,
                    profile_url,
                )

                profile_superbadges = extract_superbadges(
                    profile_badges
                )

                all_badges.extend(profile_badges)
                all_superbadges.extend(profile_superbadges)

                logger.info(
                    "Retrieved %d badges and %d superbadges for %s",
                    len(profile_badges),
                    len(profile_superbadges),
                    profile_name,
                )

            except Exception:
                logger.exception(
                    "Badge retrieval failed for %s",
                    profile_name,
                )

            # --------------------------------
            # PROFILE SUMMARY
            # --------------------------------
            if rank_data is not None:
                try:
                    summary = extract_profile_summary(
                        rank_data,
                        profile_name,
                        profile_url,
                        superbadge_count=len(profile_superbadges),
                    )

                    all_profile_summaries.append(summary)

                except Exception:
                    logger.exception(
                        "Profile summary extraction failed for %s",
                        profile_name,
                    )

            # --------------------------------
            # AGENTBLAZER
            # --------------------------------
            try:
                levels = fetch_agentblazer_status(
                    profile_url,
                    profile_name,
                    RAW_DATA_DIR,
                )

                agentblazer_records = extract_agentblazer(
                    levels,
                    profile_name,
                    profile_url,
                )

                all_agentblazer.extend(agentblazer_records)

                logger.info(
                    "Retrieved %d Agentblazer levels for %s",
                    len(agentblazer_records),
                    profile_name,
                )

            except Exception:
                logger.exception(
                    "Agentblazer retrieval failed for %s",
                    profile_name,
                )

         
            # --------------------------------
            # EARNED STAMPS
            # --------------------------------
            try:
                stamp_edges = fetch_profile_stamps(
                    profile_url,
                    profile_name,
                    RAW_DATA_DIR,
                )

                stamp_records = extract_stamps(
                    stamp_edges,
                    profile_name,
                    profile_url,
                )

                all_stamps.extend(stamp_records)

                logger.info(
                    "Retrieved %d stamps for %s",
                    len(stamp_records),
                    profile_name,
                )

            except Exception as error:
                logger.warning(
                    "Stamp retrieval unavailable for %s: %s",
                    profile_name,
                    error,
                )


        # --------------------------------
        # CERTIFICATION EXPORTS
        # --------------------------------
        if all_certifications:

            grouped = group_by_year(all_certifications)

            print_report(grouped)

            export_certifications(
                all_certifications,
                output_dir=PROCESSED_DATA_DIR,
                filename="all_trailblazer_certifications",
            )

        else:
            logger.warning("No certifications were retrieved.")

        # --------------------------------
        # ACHIEVEMENT EXPORTS
        # --------------------------------
        export_achievements(
            profile_summaries=all_profile_summaries,
            badges=all_badges,
            superbadges=all_superbadges,
            agentblazer=all_agentblazer,
            stamps=all_stamps,
            output_dir=PROCESSED_DATA_DIR,
        )

        # --------------------------------
        # FINAL REPORT
        # --------------------------------
        logger.info("------------------------------------")
        logger.info("TRAILBLAZER SCRAPING COMPLETED")
        logger.info("------------------------------------")

        logger.info(
            "Certification profiles successful: %d",
            successful_profiles,
        )

        logger.info(
            "Certification profiles failed: %d",
            failed_profiles,
        )

        logger.info("Total certifications: %d", len(all_certifications))
        logger.info("Total badges: %d", len(all_badges))
        logger.info("Total superbadges: %d", len(all_superbadges))
        logger.info("Total Agentblazer records: %d", len(all_agentblazer))
        logger.info("Total stamps: %d", len(all_stamps))

    except Exception:
        logger.exception("The scraper failed.")
        raise


if __name__ == "__main__":
    main()