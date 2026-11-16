
import json
import logging
import re
from pathlib import Path
from urllib.parse import urlparse

import requests

logger = logging.getLogger(__name__)

API_URL = "https://profile.api.trailhead.com/graphql"

QUERY = """
query GetUserCertifications($slug: String, $hasSlug: Boolean!) {
  profile(slug: $slug) @include(if: $hasSlug) {
    __typename
    id
    ... on PublicProfile {
      credential {
        messages {
          __typename
          body
          header
          location
          image
          cta {
            __typename
            label
            url
          }
          orientation
        }
        messagesOnly
        certificationsHistoryUrl
        certificationsPrivacy
        brands {
          __typename
          id
          name
          logo
        }
        certifications {
          cta {
            __typename
            label
            url
          }
          dateCompleted
          dateExpired
          downloadLogoUrl
          logoUrl
          infoUrl
          maintenanceDueDate
          product
          publicDescription
          status {
            __typename
            title
            expired
            date
            color
            order
          }
          title
          certificationUserLegalName
          certificationId
        }
      }
    }
  }
}
"""


def safe_filename(name):
    """Convert a person's name into a safe filename."""
    filename = re.sub(r"[^a-zA-Z0-9]+", "_", name.lower())
    return filename.strip("_")


def scrape_profile(profile_url, profile_name, output_dir="data/raw"):
    """Retrieve and save public Trailblazer certification data through GraphQL."""

    slug = urlparse(profile_url).path.rstrip("/").split("/")[-1]

    if not slug:
        raise ValueError("Could not extract profile slug from URL.")

    payload = {
        "operationName": "GetUserCertifications",
        "variables": {
            "hasSlug": True,
            "slug": slug
        },
        "query": QUERY
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://www.salesforce.com",
        "Referer": "https://www.salesforce.com/",
        "x-idp": "iis"
    }

    logger.info("Requesting certifications for profile: %s", slug)

    response = requests.post(
        API_URL,
        json=payload,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()
    data = response.json()

    if data.get("errors"):
        raise RuntimeError(
            "GraphQL returned errors: {}".format(data["errors"])
        )

    certifications = (
        data.get("data", {})
            .get("profile", {})
            .get("credential", {})
            .get("certifications", [])
    )

    if not certifications:
        logger.warning("No public certifications found for %s", slug)

    # Create the output directory if it does not exist.
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate a filename using the person's name.
    filename = safe_filename(profile_name) + "_trailblazer_api.json"
    json_path = output_path / filename

    # Save the API response.
    with json_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    logger.info("Saved GraphQL response to %s", json_path)
    logger.info("Found %d certifications", len(certifications))

    return data
