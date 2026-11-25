
import json
import logging
from pathlib import Path

import requests

from src.scraper import API_URL, safe_filename

STAMPS_API_URL = "https://mobile.api.trailhead.com/graphql"

logger = logging.getLogger(__name__)

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Origin": "https://www.salesforce.com",
    "Referer": "https://www.salesforce.com/",
    "x-idp": "iis",
}


RANK_QUERY = """
query GetTrailheadRank($slug: String, $hasSlug: Boolean!) {
  profile(slug: $slug) @include(if: $hasSlug) {
    __typename
    ... on PublicProfile {
      trailheadStats {
        earnedPointsSum
        earnedBadgesCount
        completedTrailCount
        rank {
          title
          requiredPointsSum
          requiredBadgesCount
          imageUrl
        }
        nextRank {
          title
          requiredPointsSum
          requiredBadgesCount
          imageUrl
        }
        learnerStatusLevels {
          statusName
          title
          level
          imageUrl
          completedAt
          progress
          edition
        }
      }
    }
  }
}
"""


BADGES_QUERY = """
query GetTrailheadBadges(
  $slug: String,
  $hasSlug: Boolean!,
  $count: Int = 8,
  $after: String = null,
  $filter: AwardTypeFilter = null
) {
  profile(slug: $slug) @include(if: $hasSlug) {
    __typename
    ... on PublicProfile {
      trailheadStats {
        earnedBadgesCount
        superbadgeCount
      }
      earnedAwards(
        first: $count,
        after: $after,
        awardType: $filter
      ) {
        edges {
          node {
            ... on EarnedAwardBase {
              id
              award {
                id
                title
                type
                icon
                content {
                  webUrl
                  description
                }
              }
            }
            ... on EarnedAwardSelf {
              earnedAt
              earnedPointsSum
            }
          }
        }
        pageInfo {
          endCursor
          hasNextPage
          startCursor
          hasPreviousPage
        }
      }
    }
  }
}
"""

AGENTBLAZER_QUERY = """
query GetAgentblazerStatus($slug: String, $hasSlug: Boolean!) {
  profile(slug: $slug) @include(if: $hasSlug) {
    __typename
    ... on PublicProfile {
      trailheadStats {
        learnerStatusLevels {
          statusName
          title
          level
          imageUrl
          completedAt
          progress
          edition
          medalImageUrl
          active
        }
      }
    }
  }
}
"""

STAMPS_QUERY = """
query EarnedStamps($slug: String!, $first: Int, $after: String) {
  earnedStamps(slug: $slug, first: $first, after: $after) {
    __typename
    count
    totalCount
    edges {
      __typename
      cursor
      node {
        __typename
        rewardId
        kind
        apiName
        name
        description
        eventDate
        eventLocation
        iconUrl
        linkUrl
      }
    }
    pageInfo {
      endCursor
      hasNextPage
      __typename
    }
  }
}
"""

def save_raw_response(data, profile_name, operation_name, output_dir="data/raw"):
    """Save a raw GraphQL response as a JSON file."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    filename = (
        f"{safe_filename(profile_name)}_{operation_name.lower()}.json"
    )
    json_path = output_path / filename

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    logger.info("Saved GraphQL response to %s", json_path)


def graphql_request(operation_name, query, variables, api_url=API_URL):
    """Send a GraphQL request and return the JSON response."""

    payload = {
        "operationName": operation_name,
        "variables": variables,
        "query": query,
    }

    logger.info("Requesting GraphQL operation: %s", operation_name)

    response = requests.post(
        api_url,
        json=payload,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("errors"):
        raise RuntimeError(
            f"GraphQL returned errors for {operation_name}: {data['errors']}"
        )

    return data


def extract_profile_slug(profile_url):
    """Extract the profile slug from a Trailblazer profile URL."""

    from urllib.parse import urlparse

    slug = urlparse(profile_url).path.rstrip("/").split("/")[-1]

    if not slug:
        raise ValueError("Could not extract profile slug from URL.")

    return slug


def fetch_paginated_data(
    profile_slug,
    profile_name,
    operation_name,
    query,
    connection_path,
    variables,
    output_dir="data/raw",
    api_url=API_URL,
):
    """Fetch all pages of a GraphQL connection."""

    all_edges = []
    after = None
    seen_cursors = set()

    while True:
        page_variables = {
            **variables,
            "slug": profile_slug,
            "after": after,
        }

        data = graphql_request(
            operation_name,
            query,
            page_variables,
            api_url=api_url,
        )

        save_raw_response(
            data,
            profile_name,
            f"{operation_name}_page_{len(all_edges)}",
            output_dir,
        )

        connection = data.get("data", {})

        for key in connection_path:
            connection = connection.get(key, {})

        edges = connection.get("edges", [])
        all_edges.extend(edges)

        page_info = connection.get("pageInfo", {})
        has_next_page = page_info.get("hasNextPage", False)
        end_cursor = page_info.get("endCursor")

        if not has_next_page:
            break

        if not end_cursor or end_cursor in seen_cursors:
            raise RuntimeError(
                f"Pagination stopped unexpectedly for {operation_name}."
            )

        seen_cursors.add(end_cursor)
        after = end_cursor

    logger.info(
        "Retrieved %d records for %s",
        len(all_edges),
        operation_name,
    )

    return all_edges


def fetch_profile_rank(profile_url, profile_name, output_dir="data/raw"):
    """Fetch Trailhead rank, points, badges and completed trails."""

    slug = extract_profile_slug(profile_url)

    data = graphql_request(
        operation_name="GetTrailheadRank",
        query=RANK_QUERY,
        variables={
            "hasSlug": True,
            "slug": slug,
        },
    )

    save_raw_response(
        data,
        profile_name,
        "get_trailhead_rank",
        output_dir,
    )

    logger.info("Successfully retrieved rank information for %s", slug)

    return data


def fetch_profile_badges(profile_url, profile_name, output_dir="data/raw"):
    """Fetch all earned badges, including superbadges, using pagination."""

    slug = extract_profile_slug(profile_url)

    edges = fetch_paginated_data(
        profile_slug=slug,
        profile_name=profile_name,
        operation_name="GetTrailheadBadges",
        query=BADGES_QUERY,
        connection_path=["profile", "earnedAwards"],
        variables={
            "hasSlug": True,
            "count": 8,
            "filter": None,
        },
        output_dir=output_dir,
    )

    logger.info(
        "Retrieved %d earned awards for %s",
        len(edges),
        slug,
    )

    return edges


def fetch_agentblazer_status(profile_url, profile_name, output_dir="data/raw"):
    """Fetch all Agentblazer status levels for a Trailblazer profile."""

    slug = extract_profile_slug(profile_url)

    data = graphql_request(
        operation_name="GetAgentblazerStatus",
        query=AGENTBLAZER_QUERY,
        variables={
            "hasSlug": True,
            "slug": slug,
        },
    )

    save_raw_response(
        data,
        profile_name,
        "get_agentblazer_status",
        output_dir,
    )

    levels = (
        data.get("data", {})
        .get("profile", {})
        .get("trailheadStats", {})
        .get("learnerStatusLevels", [])
    )

    logger.info(
        "Retrieved %d Agentblazer levels for %s",
        len(levels),
        slug,
    )

    return levels


def fetch_profile_stamps(profile_url, profile_name, output_dir="data/raw"):
    """Fetch all earned stamps for a Trailblazer profile."""

    slug = extract_profile_slug(profile_url)

    edges = fetch_paginated_data(
        profile_slug=slug,
        profile_name=profile_name,
        operation_name="EarnedStamps",
        query=STAMPS_QUERY,
        connection_path=["earnedStamps"],
        variables={
            "first": 8,
        },
        output_dir=output_dir,
        api_url=STAMPS_API_URL,
    )

    logger.info(
        "Retrieved %d earned stamps for %s",
        len(edges),
        slug,
    )

    return edges
