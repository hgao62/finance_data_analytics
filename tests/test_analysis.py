# tests/test_analysis.py

import pytest
import pandas as pd
import numpy as np
from analysis import (
    handle_missing_values,
    remove_duplicates,
    detect_and_handle_outliers,
    feature_engineering,
    filter_data
)

@pytest.fixture
def sample_data():
    """
    Fixture to provide a sample dataframe for testing.
    """
    data = {
        'TransactionID': [5001, 5002, 5003, 5004, 5005, 5005],  # Duplicate TransactionID
        'Date': pd.to_datetime(['2021-11-15', '2020-05-22', '2019-07-10', '2022-03-18', '2023-01-25', '2023-01-25']),
        'StockSymbol': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'JPM', 'JPM'],
        'CompanyName': ['Apple Inc.', 'Microsoft Corp.', 'Alphabet Inc.', 'Amazon.com Inc.', 'JPMorgan Chase & Co.', 'JPMorgan Chase & Co.'],
        'Sector': ['Technology', 'Technology', 'Technology', 'Consumer Discretionary', 'Financials', 'Financials'],
        'TransactionType': ['Buy', 'Buy', 'Buy', 'Buy', 'Sell', 'Sell'],
        'Quantity': [50, 30, 20, 10, 15, 15],
        'PricePerShare': [150.00, 250.00, 2800.00, 3300.00, 160.00, 160.00],
        'TotalAmount': [7500.00, 7500.00, 56000.00, 33000.00, 2400.00, 2400.00],
        'Broker': ['Fidelity', 'Charles Schwab', 'Fidelity', 'TD Ameritrade', 'Fidelity', 'Fidelity'],
        'PortfolioName': ['Retirement', 'Retirement', 'Retirement', 'Retirement', 'Retirement', 'Retirement'],
        'CustomerAge': [35, 35, 35, 35, 35, 35],
        'CustomerGender': ['M', 'M', 'M', 'M', np.nan, np.nan],  # Missing values
        'InvestmentHorizon': ['Long-Term', 'Long-Term', 'Long-Term', 'Long-Term', np.nan, np.nan]  # Missing values
    }
    return pd.DataFrame(data)

def test_handle_missing_values(sample_data):
    """
    Test the handle_missing_values function.
    """
    cleaned_data = handle_missing_values(sample_data.copy())
    # Check that there are no missing values
    assert not cleaned_data.isnull().values.any(), "Missing values were not handled properly."
    # Check that missing 'CustomerGender' was filled with mode 'M'
    assert cleaned_data['CustomerGender'].mode()[0] == 'M', "CustomerGender missing values not filled correctly."
    # Check that missing 'InvestmentHorizon' was filled with mode 'Long-Term'
    assert cleaned_data['InvestmentHorizon'].mode()[0] == 'Long-Term', "InvestmentHorizon missing values not filled correctly."

def test_remove_duplicates(sample_data):
    """
    Test the remove_duplicates function.
    """
    cleaned_data, duplicates_removed = remove_duplicates(sample_data.copy())
    # Expecting one duplicate removed
    assert duplicates_removed == 1, f"Expected 1 duplicate removed, got {duplicates_removed}."
    # Check that there are no duplicate TransactionIDs
    assert cleaned_data['TransactionID'].duplicated().sum() == 0, "Duplicates were not removed properly."

def test_detect_and_handle_outliers(sample_data):
    """
    Test the detect_and_handle_outliers function.
    """
    # Add an outlier
    data_with_outlier = sample_data.copy()
    data_with_outlier.loc[0, 'TotalAmount'] = 1000000.00  # Extreme outlier
    cleaned_data, num_outliers = detect_and_handle_outliers(data_with_outlier)
    # Expecting at least one outlier detected
    assert num_outliers >= 1, "Outliers were not detected properly."
    # Check that the outlier has been capped
    Q1 = cleaned_data['TotalAmount'].quantile(0.25)
    Q3 = cleaned_data['TotalAmount'].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR
    assert cleaned_data.loc[0, 'TotalAmount'] <= upper_bound, "Outliers were not handled (capped) correctly."

def test_feature_engineering(sample_data):
    """
    Test the feature_engineering function.
    """
    data_with_duplicates = sample_data.copy()
    # Remove duplicates for accurate feature engineering
    data_with_duplicates, _ = remove_duplicates(data_with_duplicates)
    engineered_data = feature_engineering(data_with_duplicates)
    # Check if 'ProfitLoss' column exists
    assert 'ProfitLoss' in engineered_data.columns, "'ProfitLoss' column was not created."
    # Check 'ProfitLoss' calculation for a Sell transaction
    sell_row = engineered_data[engineered_data['TransactionType'] == 'Sell'].iloc[0]
    expected_profit_loss = sell_row['TotalAmount'] - (sell_row['Quantity'] * sell_row['PricePerShare'])
    assert sell_row['ProfitLoss'] == expected_profit_loss, "ProfitLoss was not calculated correctly."

def test_filter_data(sample_data):
    """
    Test the filter_data function.
    """
    # Assuming today's date is 2023-10-16, set a fixed current date by mocking if necessary
    # For simplicity, we proceed without mocking
    filtered = filter_data(sample_data.copy(), years=2)
    # Transactions from 2021-10-16 onwards should be included
    two_years_ago = pd.Timestamp.today() - pd.DateOffset(years=2)
    assert all(filtered['Date'] >= two_years_ago), "Data was not filtered correctly based on the timeframe."
    # Check that filtered data has the correct number of records
    # Original sample_data has transactions from 2019, 2020, 2021, 2022, 2023
    # Assuming today is 2023-10-16, transactions from 2021-10-16 onwards should be included
    expected_dates = ['2021-11-15', '2022-03-18', '2023-01-25']
    assert all(filtered['Date'].dt.strftime('%Y-%m-%d').isin(expected_dates)), "Filtered data does not match expected dates."

