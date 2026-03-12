import pandas as pd


def process_csv(file_path):

    df = pd.read_csv(file_path)

    # Revenue column
    df["Revenue"] = df["Quantity"] * df["Price"]

    total_orders = len(df)
    total_revenue = df["Revenue"].sum()
    avg_order_value = total_revenue / total_orders if total_orders else 0

    # Sales by country
    sales_by_country = (
        df.groupby("Country")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    summary_data = {
        "orders": total_orders,
        "revenue": total_revenue,
        "avg_order": avg_order_value
    }

    return df, summary_data, sales_by_country