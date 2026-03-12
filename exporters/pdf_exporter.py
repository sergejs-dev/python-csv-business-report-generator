from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

import matplotlib.pyplot as plt
import tempfile


def export_pdf(summary_data, country_sales, file_path):

    c = canvas.Canvas(file_path, pagesize=letter)

    width, height = letter

    y = height - 50

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Business Revenue Report")

    y -= 40

    # Summary
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Summary")

    y -= 20

    c.setFont("Helvetica", 11)

    c.drawString(60, y, f"Total Orders: {summary_data['orders']}")
    y -= 20

    c.drawString(60, y, f"Total Revenue: {summary_data['revenue']}")
    y -= 20

    c.drawString(60, y, f"Average Order Value: {summary_data['avg_order']}")
    y -= 40

    # Country sales table
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Revenue by Country")

    y -= 20

    c.setFont("Helvetica", 11)

    for country, revenue in country_sales.items():
        c.drawString(60, y, f"{country}: {revenue}")
        y -= 18

    # Chart
    countries = list(country_sales.index)
    values = list(country_sales.values)

    fig, ax = plt.subplots(figsize=(6,3))

    ax.bar(countries, values)

    ax.set_title("Revenue by Country")
    ax.set_xlabel("Country")
    ax.set_ylabel("Revenue")

    plt.tight_layout()

    temp_chart = tempfile.NamedTemporaryFile(delete=False, suffix=".png")

    fig.savefig(temp_chart.name)

    c.drawImage(temp_chart.name, 50, 200, width=500, height=200)

    c.save()