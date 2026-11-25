
from pathlib import Path

import pandas as pd


def export_achievements(
    profile_summaries,
    badges,
    superbadges,
    agentblazer,
    stamps,
    output_dir="data/processed",
):
    """Export achievement datasets to individual CSV files and one Excel workbook."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    datasets = {
        "profile_summary": profile_summaries,
        "badges": badges,
        "superbadges": superbadges,
        "agentblazer": agentblazer,
        "stamps": stamps,
    }

    for name, records in datasets.items():
        dataframe = pd.DataFrame(records)
        csv_path = output_path / f"{name}.csv"
        dataframe.to_csv(csv_path, index=False, encoding="utf-8-sig")

        print(f"Exported {csv_path}")

    excel_path = output_path / "all_trailblazer_achievements.xlsx"

    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        for name, records in datasets.items():
            dataframe = pd.DataFrame(records)
            sheet_name = name.replace("_", " ").title()
            dataframe.to_excel(
                writer,
                sheet_name=sheet_name,
                index=False,
            )

    print(f"Exported {excel_path}")

    return excel_path
