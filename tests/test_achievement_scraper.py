
from unittest.mock import Mock, patch

from src.achievement_scraper import (
    extract_profile_slug,
    graphql_request,
    fetch_profile_rank,
    fetch_profile_badges,
    fetch_agentblazer_status,
    fetch_profile_stamps,
)


PROFILE_URL = "https://www.salesforce.com/trailblazer/chiarat"


def test_extract_profile_slug():
    assert extract_profile_slug(PROFILE_URL) == "chiarat"


@patch("src.achievement_scraper.requests.post")
def test_graphql_request(mock_post):
    mock_response = Mock()
    mock_response.json.return_value = {"data": {"profile": {}}}
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    result = graphql_request(
        "TestOperation",
        "query TestOperation { profile { id } }",
        {"slug": "chiarat"},
    )

    assert result == {"data": {"profile": {}}}
    mock_post.assert_called_once()


@patch("src.achievement_scraper.save_raw_response")
@patch("src.achievement_scraper.graphql_request")
def test_fetch_profile_rank(mock_request, mock_save):
    mock_request.return_value = {
        "data": {
            "profile": {
                "trailheadStats": {
                    "earnedPointsSum": 1000
                }
            }
        }
    }

    result = fetch_profile_rank(PROFILE_URL, "Chiara Tardioli")

    assert result["data"]["profile"]["trailheadStats"]["earnedPointsSum"] == 1000
    mock_save.assert_called_once()


@patch("src.achievement_scraper.save_raw_response")
@patch("src.achievement_scraper.graphql_request")
def test_fetch_profile_badges_pagination(mock_request, mock_save):
    mock_request.side_effect = [
        {
            "data": {
                "profile": {
                    "earnedAwards": {
                        "edges": [{"node": {"id": "badge-1"}}],
                        "pageInfo": {
                            "endCursor": "cursor-1",
                            "hasNextPage": True,
                        },
                    }
                }
            }
        },
        {
            "data": {
                "profile": {
                    "earnedAwards": {
                        "edges": [{"node": {"id": "badge-2"}}],
                        "pageInfo": {
                            "endCursor": "cursor-2",
                            "hasNextPage": False,
                        },
                    }
                }
            }
        },
    ]

    result = fetch_profile_badges(PROFILE_URL, "Chiara Tardioli")

    assert len(result) == 2
    assert result[0]["node"]["id"] == "badge-1"
    assert result[1]["node"]["id"] == "badge-2"
    assert mock_request.call_count == 2


@patch("src.achievement_scraper.save_raw_response")
@patch("src.achievement_scraper.graphql_request")
def test_fetch_agentblazer_status(mock_request, mock_save):
    mock_request.return_value = {
        "data": {
            "profile": {
                "trailheadStats": {
                    "learnerStatusLevels": [
                        {"title": "Legend", "level": 3}
                    ]
                }
            }
        }
    }

    result = fetch_agentblazer_status(PROFILE_URL, "Chiara Tardioli")

    assert len(result) == 1
    assert result[0]["title"] == "Legend"
    mock_save.assert_called_once()


@patch("src.achievement_scraper.save_raw_response")
@patch("src.achievement_scraper.graphql_request")
def test_fetch_profile_stamps(mock_request, mock_save):
    mock_request.return_value = {
        "data": {
            "earnedStamps": {
                "edges": [{"node": {"name": "Dreamforce '26"}}],
                "pageInfo": {
                    "endCursor": None,
                    "hasNextPage": False,
                },
            }
        }
    }

    result = fetch_profile_stamps(PROFILE_URL, "Chiara Tardioli")

    assert len(result) == 1
    assert result[0]["node"]["name"] == "Dreamforce '26"
    mock_save.assert_called_once()
