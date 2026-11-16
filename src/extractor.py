
import logging

logger = logging.getLogger(__name__)

from datetime import date

def normalize_key(value):
    """Normalize a text value for consistent comparison."""
    if not value:
        return ""

    return " ".join(str(value).lower().strip().split())

def parse_date(value):
    """Parse a certification completion date into ISO format."""

    if not value:
        return None

    try:
        parts = value[:10].split("-")

        if len(parts) != 3:
            return None

        year, month, day = map(int, parts)

        return date(year, month, day).isoformat()

    except (ValueError, TypeError):
        return None


def extract_certifications(payload):
    """Extract and normalize certification records from a GraphQL response."""

    if not isinstance(payload, dict):
        logger.warning("Payload is not a dictionary")
        return []

    data = payload.get("data", payload)
    profile = data.get("profile", {})
    credential = profile.get("credential", {})
    certifications = credential.get("certifications", [])

    logger.debug("Certifications received: %d", len(certifications))

    results = []

    for cert in certifications:
        title = cert.get("title")
        completed_date = parse_date(cert.get("dateCompleted"))

        logger.debug("Certification: %s | API date: %s | Parsed date: %s", title, cert.get("dateCompleted"), completed_date)

        if not title or not completed_date:
            continue

        status = cert.get("status") or {}

        results.append({
            "name": title,
            "date": completed_date,
            "year": int(completed_date[:4]),
            "status": status.get("title"),
            "product": cert.get("product"),
            "expiration_date": cert.get("dateExpired"),
            "info_url": cert.get("infoUrl"),
        })

    logger.info("Certifications extracted: %d", len(results))

    return results

