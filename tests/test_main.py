
import pandas as pd
import pytest

import main


def test_load_profiles_reads_multiple_profiles(tmp_path, monkeypatch):
    profiles_file = tmp_path / "profiles.csv"

    pd.DataFrame([
        {
            "profile_name": "Chiara Tardioli",
            "profile_url": "https://www.salesforce.com/trailblazer/chiarat",
        },
        {
            "profile_name": "Vina Egg",
            "profile_url": "https://www.salesforce.com/trailblazer/vinaegg",
        },
    ]).to_csv(profiles_file, index=False)

    monkeypatch.setattr(main, "PROFILES_FILE", str(profiles_file))

    profiles = main.load_profiles()

    assert len(profiles) == 2
    assert profiles[0]["profile_name"] == "Chiara Tardioli"
    assert profiles[1]["profile_name"] == "Vina Egg"


def test_load_profiles_rejects_missing_columns(tmp_path, monkeypatch):
    profiles_file = tmp_path / "profiles.csv"

    pd.DataFrame([
        {"name": "Chiara Tardioli"}
    ]).to_csv(profiles_file, index=False)

    monkeypatch.setattr(main, "PROFILES_FILE", str(profiles_file))

    with pytest.raises(ValueError):
        main.load_profiles()


def test_load_profiles_ignores_empty_rows(tmp_path, monkeypatch):
    profiles_file = tmp_path / "profiles.csv"

    pd.DataFrame([
        {
            "profile_name": "Chiara Tardioli",
            "profile_url": "https://www.salesforce.com/trailblazer/chiarat",
        },
        {
            "profile_name": None,
            "profile_url": "https://www.salesforce.com/trailblazer/vinaegg",
        },
    ]).to_csv(profiles_file, index=False)

    monkeypatch.setattr(main, "PROFILES_FILE", str(profiles_file))

    profiles = main.load_profiles()

    assert len(profiles) == 1
    assert profiles[0]["profile_name"] == "Chiara Tardioli"

