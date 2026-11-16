
import os
import pandas as pd


def export_certifications(
    certifications,
    output_dir="data/processed",
    filename="all_trailblazer_certifications",
):
    """Export certification records to consolidated CSV and Excel files."""

    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame(certifications)

    # Select and order the columns available in the extracted data.
    columns = [
        "profile_name",
        "profile_url",
        "name",
        "date",
        "year",
        "status",
        "product",
        "expiration_date",
        "info_url",
    ]

    df = df[[column for column in columns if column in df.columns]]

    csv_path = os.path.join(output_dir, filename + ".csv")
    excel_path = os.path.join(output_dir, filename + ".xlsx")

    # Export CSV
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    # Export Excel with a separate worksheet for each year.
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="All Certifications", index=False)

        for year in sorted(df["year"].unique()):
            year_df = df[df["year"] == year]
            year_df.to_excel(
                writer,
                sheet_name=str(year),
                index=False,
            )

    print("\nExport completed successfully!")
    print("CSV file:", csv_path)
    print("Excel file:", excel_path)

    return csv_path, excel_path

