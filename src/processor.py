import logging

logger = logging.getLogger(__name__)

from collections import defaultdict
from datetime import datetime


def clean_certifications(certifications):
    """Validate, clean and deduplicate certification records."""
    cleaned = []
    seen = set()

    for cert in certifications:
        name = cert.get("name")
        completed_date = cert.get("date")

        if not name or not completed_date:
            continue

        try:
            parsed_date = datetime.strptime(completed_date, "%Y-%m-%d")
        except (ValueError, TypeError):
            continue

        # Identify the person as part of the duplicate check.
        profile_identifier = (
            cert.get("profile_url")
            or cert.get("profile_name")
            or ""
        )

        unique_key = (
            profile_identifier.strip().lower(),
            name.strip().lower(),
            completed_date,
        )

        if unique_key in seen:
            continue

        seen.add(unique_key)

        cleaned_cert = cert.copy()
        cleaned_cert["date"] = parsed_date.strftime("%Y-%m-%d")
        cleaned_cert["year"] = parsed_date.year
        cleaned.append(cleaned_cert)

    logger.info("Certifications after cleaning: %d", len(cleaned))
    return cleaned


def group_by_year(certifications):
    """Group certification records by completion year."""
    grouped = defaultdict(list)

    for cert in certifications:
        grouped[cert["year"]].append(cert)

    return dict(sorted(grouped.items()))


def print_report(grouped):
    """Display a certification report grouped by year."""
    print("\n" + "=" * 60)
    print("TRAILBLAZER CERTIFICATION REPORT")
    print("=" * 60)

    total = 0

    for year, certifications in grouped.items():
        print("\n{}".format(year))
        print("-" * 40)

        for cert in certifications:
            print("  {}".format(cert["name"]))
            print("  Completed: {}".format(cert["date"]))
            print("  Status: {}".format(cert.get("status", "Unknown")))
            print()

        total += len(certifications)

    print("=" * 60)
    print("TOTAL CERTIFICATIONS: {}".format(total))
    print("=" * 60)

