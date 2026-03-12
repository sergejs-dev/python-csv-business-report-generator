import pandas as pd


def export_excel(df, summary_data, country_sales, file_path):

    writer = pd.ExcelWriter(file_path, engine="xlsxwriter")

    workbook = writer.book

    # ---------- RAW DATA ----------
    df.to_excel(writer, sheet_name="Raw Data", index=False)

    # ---------- SUMMARY ----------
    summary_df = pd.DataFrame({
        "Metric": ["Total Orders", "Total Revenue", "Average Order Value"],
        "Value": [
            summary_data["orders"],
            summary_data["revenue"],
            summary_data["avg_order"]
        ]
    })

    summary_df.to_excel(writer, sheet_name="Summary", index=False)

    # ---------- SALES BY COUNTRY ----------
    country_sales_df = country_sales.reset_index()
    country_sales_df.columns = ["Country", "Revenue"]

    country_sales_df.to_excel(writer, sheet_name="Sales by Country", index=False)

    worksheet = writer.sheets["Sales by Country"]

    # ---------- BAR CHART ----------
    chart = workbook.add_chart({"type": "column"})

    rows = len(country_sales_df)

    chart.add_series({
        "name": "Revenue by Country",
        "categories": ["Sales by Country", 1, 0, rows, 0],
        "values":     ["Sales by Country", 1, 1, rows, 1],
    })

    chart.set_title({"name": "Revenue by Country"})
    chart.set_x_axis({"name": "Country"})
    chart.set_y_axis({"name": "Revenue"})

    worksheet.insert_chart("D2", chart)

    writer.close()