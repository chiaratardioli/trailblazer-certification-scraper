
import pandas as pd

from src.achievement_exporter import export_achievements


def test_export_achievements_creates_all_files(tmp_path):
    profile_summaries = [
        {"profile_name": "Chiara Tardioli", "rank": "All Star Ranger"}
    ]

    badges = [
        {"profile_name": "Chiara Tardioli", "badge_name": "Python Basics"}
    ]

    superbadges = [
        {"profile_name": "Chiara Tardioli", "badge_name": "Advanced Apex"}
    ]

    agentblazer = [
        {"profile_name": "Chiara Tardioli", "title": "Legend"}
    ]

    stamps = [
        {"profile_name": "Chiara Tardioli", "name": "Dreamforce '26"}
    ]

    excel_path = export_achievements(
        profile_summaries=profile_summaries,
        badges=badges,
        superbadges=superbadges,
        agentblazer=agentblazer,
        stamps=stamps,
        output_dir=tmp_path,
    )

    expected_files = [
        "profile_summary.csv",
        "badges.csv",
        "superbadges.csv",
        "agentblazer.csv",
        "stamps.csv",
        "all_trailblazer_achievements.xlsx",
    ]

    for filename in expected_files:
        assert (tmp_path / filename).exists()

    assert excel_path.exists()


def test_export_achievements_excel_sheets(tmp_path):
    export_achievements(
        profile_summaries=[{"rank": "All Star Ranger"}],
        badges=[{"badge_name": "Python Basics"}],
        superbadges=[{"badge_name": "Advanced Apex"}],
        agentblazer=[{"title": "Legend"}],
        stamps=[{"name": "Dreamforce '26"}],
        output_dir=tmp_path,
    )

    excel_path = tmp_path / "all_trailblazer_achievements.xlsx"

    excel_file = pd.ExcelFile(excel_path)

    assert excel_file.sheet_names == [
        "Profile Summary",
        "Badges",
        "Superbadges",
        "Agentblazer",
        "Stamps",
    ]


def test_export_achievements_empty_datasets(tmp_path):
    export_achievements(
        profile_summaries=[],
        badges=[],
        superbadges=[],
        agentblazer=[],
        stamps=[],
        output_dir=tmp_path,
    )

    assert (tmp_path / "profile_summary.csv").exists()
    assert (tmp_path / "all_trailblazer_achievements.xlsx").exists()
