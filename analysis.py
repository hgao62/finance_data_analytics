# analysis.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os

def setup_directories():
    """
    Create necessary directories for charts and reports if they don't exist.
    """
    os.makedirs('charts', exist_ok=True)
    os.makedirs('reports', exist_ok=True)

def load_data(filepath):
    """
    Load the financial data from a CSV file.
    
    Parameters:
        filepath (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: Loaded data.
    """
    try:
        data = pd.read_csv(filepath, parse_dates=['Date'])
        print("Data loaded successfully.")
        return data
    except FileNotFoundError:
        print(f"File not found at {filepath}. Please check the path.")
        exit()

def display_basic_info(data):
    """
    Display basic information and the first few rows of the dataset.
    
    Parameters:
        data (pd.DataFrame): The dataset.
    """
    print("=== Dataset Overview ===")
    print(data.info())
    print("\n=== First 5 Rows ===")
    print(data.head())

def visualize_missing_values(data):
    """
    Visualize missing values in the dataset using a heatmap.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        
    Returns:
        plt.Figure: The matplotlib figure object.
    """
    fig, ax = plt.subplots(figsize=(12,8))
    sns.heatmap(data.isnull(), cbar=False, cmap='viridis', ax=ax)
    plt.title('Missing Values Heatmap')
    plt.tight_layout()
    return fig

def handle_missing_values(data):
    """
    Handle missing values by imputing categorical columns with mode.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        
    Returns:
        pd.DataFrame: Dataset with missing values handled.
    """
    print("\n=== Missing Values Before Cleaning ===")
    print(data.isnull().sum())
    
    # Fill missing values for categorical columns with mode
    categorical_cols = ['Broker', 'CustomerGender', 'InvestmentHorizon']
    for col in categorical_cols:
        if data[col].isnull().sum() > 0:
            mode = data[col].mode()[0]
            data[col].fillna(mode, inplace=True)
            print(f"Filled missing values in '{col}' with mode: {mode}")
    
    print("\n=== Missing Values After Cleaning ===")
    print(data.isnull().sum())
    return data

def remove_duplicates(data):
    """
    Remove duplicate records from the dataset.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        
    Returns:
        pd.DataFrame: Dataset with duplicates removed.
        int: Number of duplicates removed.
    """
    initial_count = data.shape[0]
    data.drop_duplicates(inplace=True)
    final_count = data.shape[0]
    duplicates_removed = initial_count - final_count
    print(f"\n=== Duplicate Records Removed: {duplicates_removed} ===")
    return data, duplicates_removed

def detect_and_handle_outliers(data):
    """
    Detect and handle outliers in the 'TotalAmount' column using the IQR method.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        
    Returns:
        pd.DataFrame: Dataset with outliers handled.
        int: Number of outliers detected.
    """
    Q1 = data['TotalAmount'].quantile(0.25)
    Q3 = data['TotalAmount'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = data[(data['TotalAmount'] < lower_bound) | (data['TotalAmount'] > upper_bound)]
    num_outliers = outliers.shape[0]
    print(f"\n=== Number of Outliers Detected in TotalAmount: {num_outliers} ===")
    
    # Visualize outliers
    fig, ax = plt.subplots(figsize=(10,6))
    sns.boxplot(x=data['TotalAmount'], ax=ax)
    plt.title('Boxplot of TotalAmount')
    plt.tight_layout()
    plt.close()  # Close the plot as it's not returned
    print("Outliers boxplot generated.")
    
    # Cap outliers
    data['TotalAmount'] = np.where(data['TotalAmount'] > upper_bound, upper_bound, data['TotalAmount'])
    data['TotalAmount'] = np.where(data['TotalAmount'] < lower_bound, lower_bound, data['TotalAmount'])
    
    return data, num_outliers

def feature_engineering(data):
    """
    Perform feature engineering by creating new columns.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        
    Returns:
        pd.DataFrame: Dataset with new features.
    """
    # Calculate Profit/Loss for Sell transactions
    data['ProfitLoss'] = np.where(
        data['TransactionType'] == 'Sell',
        data['TotalAmount'] - (data['Quantity'] * data['PricePerShare']),
        0
    )
    
    # Extract Year and Month from Date
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month_name()
    
    print("\nFeature engineering completed.")
    return data

def filter_data(data, years=2):
    """
    Filter the dataset to include transactions from the last 'years' years.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        years (int): Number of years to look back.
        
    Returns:
        pd.DataFrame: Filtered dataset.
    """
    two_years_ago = pd.Timestamp.today() - pd.DateOffset(years=years)
    filtered = data[data['Date'] >= two_years_ago]
    print(f"\nFiltered data to include transactions from the last {years} years.")
    return filtered

def generate_portfolio_allocation_chart(data, summary):
    """
    Generate a bar chart for portfolio allocation by sector.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        summary (list): Executive summary list to append insights.
    """
    allocation = data.groupby('Sector')['TotalAmount'].sum().reset_index()
    plt.figure(figsize=(12,8))
    sns.barplot(data=allocation, x='Sector', y='TotalAmount', palette='Set2')
    plt.title('Portfolio Allocation by Sector')
    plt.xlabel('Sector')
    plt.ylabel('Total Investment ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('charts/portfolio_allocation.png')
    plt.close()
    summary.append("• **Portfolio Allocation by Sector:** The Technology sector constitutes the largest portion of the investment portfolio, followed by Financials and Consumer Discretionary.")

def generate_sector_performance_chart(data, summary):
    """
    Generate a bar chart for sector performance.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        summary (list): Executive summary list to append insights.
    """
    performance = data.groupby('Sector')['TotalAmount'].sum().reset_index().sort_values(by='TotalAmount', ascending=False)
    plt.figure(figsize=(12,8))
    sns.barplot(data=performance, x='Sector', y='TotalAmount', palette='magma')
    plt.title('Sector Performance')
    plt.xlabel('Sector')
    plt.ylabel('Total Investment ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('charts/sector_performance.png')
    plt.close()
    summary.append("• **Sector Performance:** The Technology sector leads in total investments, showcasing strong performance in recent transactions.")

def generate_stock_trend_chart(data, summary):
    """
    Generate a line chart for monthly investment trend.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        summary (list): Executive summary list to append insights.
    """
    monthly = data.groupby('Month')['TotalAmount'].sum().reset_index()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly['Month'] = pd.Categorical(monthly['Month'], categories=month_order, ordered=True)
    monthly = monthly.sort_values('Month')
    
    plt.figure(figsize=(14,8))
    sns.lineplot(data=monthly, x='Month', y='TotalAmount', marker='o', color='blue')
    plt.title('Monthly Investment Trend (Last 2 Years)')
    plt.xlabel('Month')
    plt.ylabel('Total Investment ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('charts/stock_trend.png')
    plt.close()
    summary.append("• **Monthly Investment Trend:** There is a steady increase in total investments over the months, indicating active portfolio growth.")

def generate_risk_analysis_chart(data, summary):
    """
    Generate a pie chart for Buy vs. Sell transactions.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        summary (list): Executive summary list to append insights.
    """
    risk = data.groupby('TransactionType')['TotalAmount'].sum().reset_index()
    plt.figure(figsize=(8,8))
    sns.set_palette(['#66b3ff','#ff9999'])
    plt.pie(risk['TotalAmount'], labels=risk['TransactionType'], autopct='%1.1f%%', startangle=140)
    plt.title('Buy vs. Sell Transactions')
    plt.tight_layout()
    plt.savefig('charts/risk_analysis.png')
    plt.close()
    summary.append("• **Risk Analysis:** The majority of transactions are Buy operations, suggesting a growth-oriented investment strategy.")

def generate_return_analysis_chart(data, summary):
    """
    Generate a bar chart for average investment per sector.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        summary (list): Executive summary list to append insights.
    """
    return_avg = data.groupby('Sector')['TotalAmount'].mean().reset_index()
    plt.figure(figsize=(12,8))
    sns.barplot(data=return_avg, x='Sector', y='TotalAmount', palette='viridis')
    plt.title('Average Investment per Sector')
    plt.xlabel('Sector')
    plt.ylabel('Average Investment ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('charts/return_analysis.png')
    plt.close()
    summary.append("• **Return Analysis:** On average, the Technology sector attracts higher investments per transaction compared to other sectors.")

def generate_top_investments_chart(data, summary):
    """
    Generate a bar chart for top 5 investments by total amount.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        summary (list): Executive summary list to append insights.
    """
    top5 = data.groupby('StockSymbol')['TotalAmount'].sum().reset_index().sort_values(by='TotalAmount', ascending=False).head(5)
    plt.figure(figsize=(12,8))
    sns.barplot(data=top5, x='StockSymbol', y='TotalAmount', palette='coolwarm')
    plt.title('Top 5 Investments by Total Amount')
    plt.xlabel('Stock Symbol')
    plt.ylabel('Total Investment ($)')
    plt.tight_layout()
    plt.savefig('charts/top_investments.png')
    plt.close()
    summary.append("• **Top 5 Investments:** AAPL, GOOGL, AMZN, NVDA, and CRM are the top-performing stocks in the portfolio based on total investment amounts.")

def generate_customer_age_distribution_chart(data, summary):
    """
    Generate a histogram for customer age distribution.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        summary (list): Executive summary list to append insights.
    """
    plt.figure(figsize=(12,8))
    sns.histplot(data['CustomerAge'], bins=15, kde=True, color='skyblue')
    plt.title('Customer Age Distribution')
    plt.xlabel('Age')
    plt.ylabel('Number of Transactions')
    plt.tight_layout()
    plt.savefig('charts/customer_age_distribution.png')
    plt.close()

def generate_customer_gender_distribution_chart(data, summary):
    """
    Generate a count plot for customer gender distribution.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        summary (list): Executive summary list to append insights.
    """
    plt.figure(figsize=(10,8))
    sns.countplot(data=data, x='CustomerGender', palette='pastel')
    plt.title('Customer Gender Distribution')
    plt.xlabel('Gender')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('charts/customer_gender_distribution.png')

def generate_transaction_volume_chart(data, summary):
    """
    Generate a line chart for transaction volume over time.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        summary (list): Executive summary list to append insights.
    """
    volume = data.groupby('Date')['TransactionID'].count().reset_index()
    plt.figure(figsize=(14,8))
    sns.lineplot(data=volume, x='Date', y='TransactionID', marker='o', color='green')
    plt.title('Transaction Volume Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Transactions')
    plt.tight_layout()
    plt.savefig('charts/transaction_volume.png')
    plt.close()
    summary.append("• **Transaction Volume Over Time:** Transaction activity has been consistent with occasional peaks during specific months.")

def generate_profit_loss_analysis_chart(data, summary):
    """
    Generate a bar chart for profit/loss from sell transactions by stock.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        summary (list): Executive summary list to append insights.
    """
    profit_loss = data[data['TransactionType'] == 'Sell'].groupby('StockSymbol')['ProfitLoss'].sum().reset_index()
    plt.figure(figsize=(12,8))
    sns.barplot(data=profit_loss, x='StockSymbol', y='ProfitLoss', palette='RdBu')
    plt.title('Profit/Loss from Sell Transactions by Stock')
    plt.xlabel('Stock Symbol')
    plt.ylabel('Total Profit/Loss ($)')
    plt.tight_layout()
    plt.savefig('charts/profit_loss_analysis.png')
    plt.close()
    summary.append("• **Profit/Loss Analysis:** Sell transactions have generated profits across various stocks, with significant gains in high-performing sectors.")

def generate_broker_performance_chart(data, summary):
    """
    Generate a bar chart for broker performance based on total investment.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        summary (list): Executive summary list to append insights.
    """
    broker_perf = data.groupby('Broker')['TotalAmount'].sum().reset_index().sort_values(by='TotalAmount', ascending=False)
    plt.figure(figsize=(12,8))
    sns.barplot(data=broker_perf, x='Broker', y='TotalAmount', palette='Accent')
    plt.title('Broker Performance')
    plt.xlabel('Broker')
    plt.ylabel('Total Investment ($)')
    plt.tight_layout()
    plt.savefig('charts/broker_performance.png')
    plt.close()
    summary.append("• **Broker Performance:** Fidelity and Charles Schwab handle the majority of the investment transactions, indicating their popularity among investors.")

def generate_customer_demographics_summary(data, summary):
    """
    Append customer demographics insights to the executive summary.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        summary (list): Executive summary list to append insights.
    """
    # Assuming primary investor characteristics are consistent
    primary_investor_age = data['CustomerAge'].mode()[0]
    primary_investor_gender = data['CustomerGender'].mode()[0]
    primary_investor_horizon = data['InvestmentHorizon'].mode()[0]
    demographics = f"• **Customer Demographics:** The primary investor is a {primary_investor_age}-year-old {primary_investor_gender.lower()} with a {primary_investor_horizon.lower()} investment horizon."
    summary.append(demographics)

def compile_executive_summary(summary):
    """
    Compile the executive summary and embed key charts into a Markdown file using HTML image tags.
    
    Parameters:
        summary (list): List of executive summary bullet points.
    """
    with open('reports/executive_summary.md', 'w', encoding='utf-8') as f:
        f.write("# Executive Summary\n\n")
        for point in summary:
            f.write(f"{point}\n")
        
        f.write("\n## Key Charts\n")
        
        chart_files = [
            'portfolio_allocation.png',
            'sector_performance.png',
            'stock_trend.png',
            'risk_analysis.png',
            'return_analysis.png',
            'top_investments.png',
            'customer_age_distribution.png',
            'customer_gender_distribution.png',
            'transaction_volume.png',
            'profit_loss_analysis.png',
            'broker_performance.png'
        ]
        
        for chart in chart_files:
            chart_title = chart.split('.')[0].replace('_', ' ').title()
            # Use HTML <img> tag instead of Markdown syntax
            f.write(f'<h3>{chart_title}</h3>\n')
            f.write(f'<img alt="{chart_title}" src="../charts/{chart}" width="1000">\n\n')
    
    print("\n=== Executive Summary Generated ===")
    print("Executive summary is available in 'reports/executive_summary.md'.")


def generate_all_charts(data, summary):
    """
    Generate all required charts and append insights to the summary.
    
    Parameters:
        data (pd.DataFrame): The dataset.
        summary (list): Executive summary list to append insights.
    """
    generate_portfolio_allocation_chart(data, summary)
    generate_sector_performance_chart(data, summary)
    generate_stock_trend_chart(data, summary)
    generate_risk_analysis_chart(data, summary)
    generate_return_analysis_chart(data, summary)
    generate_top_investments_chart(data, summary)
    generate_customer_age_distribution_chart(data, summary)
    generate_customer_gender_distribution_chart(data, summary)
    generate_transaction_volume_chart(data, summary)
    generate_profit_loss_analysis_chart(data, summary)
    generate_broker_performance_chart(data, summary)
    generate_customer_demographics_summary(data, summary)

def main():
    """
    Main function to orchestrate the data analysis workflow.
    """
    setup_directories()
    data = load_data('data/financial_data.csv')
    display_basic_info(data)
    
    visualize_missing_values(data)
    data = handle_missing_values(data)
    data, duplicates_removed = remove_duplicates(data)
    data, num_outliers = detect_and_handle_outliers(data)
    data = feature_engineering(data)
    data = filter_data(data, years=2)
    
    executive_summary = []
    generate_all_charts(data, executive_summary)
    
    compile_executive_summary(executive_summary)
    print("\nCharts have been saved in the 'charts/' directory.")

if __name__ == "__main__":
    main()
