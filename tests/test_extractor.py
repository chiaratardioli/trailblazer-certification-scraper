
from src.extractor import (
    extract_certifications,
    parse_date,
    normalize_key,
)


def test_normalize_key():
    assert normalize_key("earnedDate") == "earneddate"
    assert normalize_key("  Certification Name  ") == "certification name"
    assert normalize_key(None) == ""


def test_parse_date():
    assert parse_date("2024-05-15") == "2024-05-15"
    assert parse_date("2022-8-21") == "2022-08-21"
    assert parse_date("2025-1-9") == "2025-01-09"
    assert parse_date("invalid-date") is None
    assert parse_date(None) is None


def test_extract_certifications():
    sample_data = {
        "data": {
            "profile": {
                "credential": {
                    "certifications": [
                        {
                            "title": "Salesforce Certified Administrator",
                            "dateCompleted": "2023-05-10",
                            "dateExpired": None,
                            "product": "Platform",
                            "status": {"title": "Active"},
                            "infoUrl": "https://example.com/admin"
                        },
                        {
                            "title": "Salesforce Certified Platform Developer I",
                            "dateCompleted": "2024-06-20",
                            "dateExpired": None,
                            "product": "Platform",
                            "status": {"title": "Active"},
                            "infoUrl": "https://example.com/developer"
                        }
                    ]
                }
            }
        }
    }

    result = extract_certifications(sample_data)

    assert len(result) == 2

    assert result[0]["name"] == "Salesforce Certified Administrator"
    assert result[0]["date"] == "2023-05-10"
    assert result[0]["year"] == 2023
    assert result[0]["status"] == "Active"

    assert result[1]["name"] == (
        "Salesforce Certified Platform Developer I"
    )
    assert result[1]["year"] == 2024


def test_extract_ignores_invalid_certifications():
    sample_data = {
        "data": {
            "profile": {
                "credential": {
                    "certifications": [
                        {
                            "title": None,
                            "dateCompleted": "2024-01-01"
                        },
                        {
                            "title": "Salesforce Certified Administrator",
                            "dateCompleted": "invalid-date"
                        }
                    ]
                }
            }
        }
    }

    result = extract_certifications(sample_data)

    assert result == []


def test_extract_empty_certifications():
    sample_data = {
        "data": {
            "profile": {
                "credential": {
                    "certifications": []
                }
            }
        }
    }

    result = extract_certifications(sample_data)

    assert result == []

