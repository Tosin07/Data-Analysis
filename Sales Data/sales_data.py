import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
def load_data(filename):
    try:
        df = pd.read_csv(filename, parse_dates=["Date"])
        return df
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None

# Add a "Total" column to the data
def process_data(df):
    df["Total"] = df["Quantity"] * df["Price"]
    return df
def quantity_total(df):
    quantity_total = df[["Product", "Quantity"]]
    quantity_total.plot(kind ="bar", title = "Quantity sales")
    plt.show()
# Visualize total sales over time
def plot_sales_over_time(df):
    daily_sales = df.groupby("Date")["Total"].sum()
    daily_sales.plot(kind="line", title="Total Sales Over Time", ylabel="Sales ($)", xlabel="Date", figsize=(10,5))
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Visualize total sales by product
def plot_sales_by_product(df):
    product_sales = df.groupby("Product")["Total"].sum().sort_values(ascending=False)
    product_sales.plot(kind="bar", title="Sales by Product", ylabel="Sales ($)", xlabel="Product", figsize=(8,5), color='skyblue')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Visualize quantity sold by product
def plot_quantity_by_product(df):
    product_quantity = df.groupby("Product")["Quantity"].sum().sort_values(ascending=False)
    product_quantity.plot(kind="bar", title="Quantity Sold by Product", ylabel="Units Sold", xlabel="Product", color="salmon", figsize=(8,5))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    filename = "sales.csv"
    df = load_data(filename)
    if df is not None:
        df = process_data(df)
        quantity_total(df)
        plot_sales_over_time(df)
        plot_sales_by_product(df)
        plot_quantity_by_product(df)

if __name__ == "__main__":
    main()
