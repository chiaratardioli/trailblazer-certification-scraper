
from src.processor import (
    clean_certifications,
    group_by_year,
)


def sample_certifications():
    return [
        {
            "name": "Salesforce Certified Administrator",
            "date": "2023-05-10",
            "status": "Active",
            "product": "Platform",
        },
        {
            "name": "Salesforce Certified Developer",
            "date": "2024-06-20",
            "status": "Active",
            "product": "Platform",
        },
        {
            "name": "Salesforce Certified Consultant",
            "date": "2023-08-15",
            "status": "Active",
            "product": "Service",
        },
    ]


def test_clean_certifications():
    result = clean_certifications(sample_certifications())

    assert len(result) == 3
    assert result[0]["year"] == 2023
    assert result[0]["date"] == "2023-05-10"
    assert result[0]["name"] == "Salesforce Certified Administrator"


def test_remove_duplicate_certifications():
    data = sample_certifications()
    data.append(data[0].copy())

    result = clean_certifications(data)

    assert len(result) == 3


def test_group_by_year():
    cleaned = clean_certifications(sample_certifications())

    grouped = group_by_year(cleaned)

    assert list(grouped.keys()) == [2023, 2024]
    assert len(grouped[2023]) == 2
    assert len(grouped[2024]) == 1


def test_invalid_date_is_ignored():
    data = [
        {
            "name": "Salesforce Certified Administrator",
            "date": "not-a-date",
        }
    ]

    result = clean_certifications(data)

    assert result == []


def test_missing_certification_name_is_ignored():
    data = [
        {
            "name": "",
            "date": "2023-05-10",
        },
        {
            "date": "2023-05-10",
        },
    ]

    result = clean_certifications(data)

    assert result == []


def test_multiple_profiles_are_preserved():
    data = [
        {
            "name": "Salesforce Certified Administrator",
            "date": "2023-05-10",
            "profile_name": "Chiara Tardioli",
        },
        {
            "name": "Salesforce Certified Developer",
            "date": "2023-05-10",
            "profile_name": "John Smith",
        },
    ]

    result = clean_certifications(data)

    assert len(result) == 2
    assert result[0]["profile_name"] == "Chiara Tardioli"
    assert result[1]["profile_name"] == "John Smith"


def test_same_certification_for_different_profiles_is_preserved():
    data = [
        {
            "name": "Salesforce Certified Administrator",
            "date": "2023-05-10",
            "profile_name": "Chiara Tardioli",
        },
        {
            "name": "Salesforce Certified Administrator",
            "date": "2023-05-10",
            "profile_name": "John Smith",
        },
    ]

    result = clean_certifications(data)

    assert len(result) == 2
    
    
def test_same_certification_on_different_dates_is_preserved():
    data = [
        {
            "name": "Salesforce Certified Administrator",
            "date": "2023-05-10",
            "profile_name": "Vina Egg",
        },
        {
            "name": "Salesforce Certified Administrator",
            "date": "2024-05-10",
            "profile_name": "Vina Egg",
        },
    ]

    result = clean_certifications(data)

    assert len(result) == 2
    assert result[0]["date"] == "2023-05-10"
    assert result[1]["date"] == "2024-05-10"
