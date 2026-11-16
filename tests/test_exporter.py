
import pandas as pd

from src.exporter import export_certifications


def sample_certifications():
    return [
        {
            "profile_name": "Chiara Tardioli",
            "profile_url": "https://www.salesforce.com/trailblazer/chiarat",
            "name": "Salesforce Certified Administrator",
            "date": "2023-05-10",
            "year": 2023,
            "status": "Active",
            "product": "Platform",
            "expiration_date": None,
            "info_url": "https://example.com/admin",
        },
        {
            "profile_name": "Vina Egg",
            "profile_url": "https://www.salesforce.com/trailblazer/vinaegg",
            "name": "Salesforce Certified Developer",
            "date": "2024-06-20",
            "year": 2024,
            "status": "Active",
            "product": "Platform",
            "expiration_date": None,
            "info_url": "https://example.com/developer",
        },
    ]


def test_export_creates_csv_and_excel(tmp_path):
    csv_path, excel_path = export_certifications(
        sample_certifications(),
        output_dir=str(tmp_path),
        filename="test_certifications",
    )

    assert tmp_path.joinpath("test_certifications.csv").exists()
    assert tmp_path.joinpath("test_certifications.xlsx").exists()


def test_export_includes_profile_information(tmp_path):
    csv_path, excel_path = export_certifications(
        sample_certifications(),
        output_dir=str(tmp_path),
        filename="test_certifications",
    )

    df = pd.read_csv(csv_path)

    assert "profile_name" in df.columns
    assert "profile_url" in df.columns
    assert len(df) == 2
    assert df.iloc[0]["profile_name"] == "Chiara Tardioli"
    assert df.iloc[1]["profile_name"] == "Vina Egg"


def test_export_creates_separate_year_sheets(tmp_path):
    csv_path, excel_path = export_certifications(
        sample_certifications(),
        output_dir=str(tmp_path),
        filename="test_certifications",
    )

    excel_file = pd.ExcelFile(excel_path)

    assert "All Certifications" in excel_file.sheet_names
    assert "2023" in excel_file.sheet_names
    assert "2024" in excel_file.sheet_names

    df_2023 = pd.read_excel(excel_path, sheet_name="2023")
    df_2024 = pd.read_excel(excel_path, sheet_name="2024")

    assert len(df_2023) == 1
    assert len(df_2024) == 1

