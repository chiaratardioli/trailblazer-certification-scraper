
import json
from unittest.mock import patch

import pytest
import requests

from src.scraper import scrape_profile, API_URL


@pytest.fixture
def mock_api_response():
    return {
        "data": {
            "profile": {
                "credential": {
                    "certifications": [
                        {
                            "title": "Salesforce Certified Administrator",
                            "dateCompleted": "2023-05-10",
                        }
                    ]
                }
            }
        }
    }


def test_scrape_profile_sends_correct_graphql_request(
    tmp_path, mock_api_response
):
    mock_response = patch("src.scraper.requests.post").start()
    mock_response.return_value.json.return_value = mock_api_response
    mock_response.return_value.raise_for_status.return_value = None

    try:
        result = scrape_profile(
            "https://www.salesforce.com/trailblazer/vinaegg",
            "Vina Egg",
            str(tmp_path),
        )

        assert result == mock_api_response

        mock_response.assert_called_once()

        args, kwargs = mock_response.call_args

        assert args[0] == API_URL
        assert kwargs["json"]["operationName"] == "GetUserCertifications"
        assert kwargs["json"]["variables"]["slug"] == "vinaegg"
        assert kwargs["json"]["variables"]["hasSlug"] is True
        assert kwargs["timeout"] == 30
        assert kwargs["headers"]["x-idp"] == "iis"

    finally:
        patch.stopall()


def test_scrape_profile_saves_raw_json(tmp_path, mock_api_response):
    with patch("src.scraper.requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_api_response
        mock_post.return_value.raise_for_status.return_value = None

        scrape_profile(
            "https://www.salesforce.com/trailblazer/vinaegg",
            "Vina Egg",
            str(tmp_path),
        )

    json_file = tmp_path / "vina_egg_trailblazer_api.json"

    assert json_file.exists()

    with json_file.open("r", encoding="utf-8") as file:
        saved_data = json.load(file)

    assert saved_data == mock_api_response


def test_scrape_profile_creates_output_directory(
    tmp_path, mock_api_response
):
    output_dir = tmp_path / "new_folder"

    with patch("src.scraper.requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_api_response
        mock_post.return_value.raise_for_status.return_value = None

        scrape_profile(
            "https://www.salesforce.com/trailblazer/chiarat",
            "Chiara Tardioli",
            str(output_dir),
        )

    assert output_dir.exists()
    assert (
        output_dir / "chiara_tardioli_trailblazer_api.json"
    ).exists()


def test_scrape_profile_rejects_invalid_url(tmp_path):
    with pytest.raises(ValueError):
        scrape_profile("/", "Invalid Profile", str(tmp_path))


def test_scrape_profile_handles_http_error(tmp_path):
    with patch("src.scraper.requests.post") as mock_post:
        mock_post.return_value.raise_for_status.side_effect = (
            requests.exceptions.HTTPError("HTTP error")
        )

        with pytest.raises(requests.exceptions.HTTPError):
            scrape_profile(
                "https://www.salesforce.com/trailblazer/vinaegg",
                "Vina Egg",
                str(tmp_path),
            )

    assert not (tmp_path / "vina_egg_trailblazer_api.json").exists()


def test_scrape_profile_handles_graphql_errors(tmp_path):
    graphql_error_response = {
        "errors": [
            {"message": "Profile not found"}
        ]
    }

    with patch("src.scraper.requests.post") as mock_post:
        mock_post.return_value.json.return_value = graphql_error_response
        mock_post.return_value.raise_for_status.return_value = None

        with pytest.raises(RuntimeError, match="GraphQL returned errors"):
            scrape_profile(
                "https://www.salesforce.com/trailblazer/unknownprofile",
                "Unknown Profile",
                str(tmp_path),
            )

    assert not (
        tmp_path / "unknown_profile_trailblazer_api.json"
    ).exists()

