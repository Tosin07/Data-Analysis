import pytest
import pandas as pd
from io import StringIO
from sales_data import process_data  # Replace with your actual filename (without .py)

def test_process_data_adds_total_column():
    csv_data = StringIO("""Date,Product,Quantity,Price
2025-01-01,Widget A,2,10.0
2025-01-02,Widget B,3,15.0
""")
    df = pd.read_csv(csv_data)
    result_df = process_data(df)

    # Check if "Total" column exists
    assert "Total" in result_df.columns

    # Check calculated totals
    assert result_df.loc[0, "Total"] == 20.0
    assert result_df.loc[1, "Total"] == 45.0




