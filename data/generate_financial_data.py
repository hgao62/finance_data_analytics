# scripts/generate_financial_data.py

import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

# Initialize random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define parameters
num_records = 100
stock_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'JPM', 'TSLA', 'BABA', 'V', 'FB', 'NFLX',
                'BAC', 'DIS', 'NVDA', 'PFE', 'KO', 'INTC', 'PYPL', 'ADBE', 'CRM', 'ORCL',
                'UBER', 'LYFT', 'SNAP', 'TWTR', 'SQ', 'ZM', 'SHOP', 'BA', 'GE', 'IBM']
company_names = ['Apple Inc.', 'Microsoft Corp.', 'Alphabet Inc.', 'Amazon.com Inc.',
                'JPMorgan Chase & Co.', 'Tesla Inc.', 'Alibaba Group Holding Ltd.',
                'Visa Inc.', 'Meta Platforms Inc.', 'Netflix Inc.',
                'Bank of America Corp.', 'The Walt Disney Company',
                'NVIDIA Corporation', 'Pfizer Inc.', 'The Coca-Cola Company',
                'Intel Corporation', 'PayPal Holdings Inc.', 'Adobe Inc.',
                'Salesforce.com Inc.', 'Oracle Corporation',
                'Uber Technologies Inc.', 'Lyft Inc.', 'Snap Inc.', 'Twitter Inc.',
                'Square Inc.', 'Zoom Video Communications Inc.',
                'Shopify Inc.', 'Boeing Co.', 'General Electric Company', 'International Business Machines Corporation']
sectors = ['Technology', 'Consumer Discretionary', 'Financials', 'Communication Services',
           'Healthcare', 'Consumer Staples', 'Industrials', 'Utilities', 'Real Estate', 'Materials']
transaction_types = ['Buy', 'Sell']
brokers = ['Fidelity', 'Charles Schwab', 'TD Ameritrade', 'E*TRADE', 'Robinhood', 'Vanguard']
portfolio_names = ['Retirement', 'Education', 'Emergency Fund', 'Wealth Growth', 'Short-Term Goals']
genders = ['M', 'F', 'Non-binary', 'Prefer not to say']
investment_horizons = ['Short-Term', 'Medium-Term', 'Long-Term']

# Generate data
data = []
for i in range(5001, 5001 + num_records):
    transaction_id = i
    date = fake.date_between(start_date='-3y', end_date='today')
    stock_symbol = random.choice(stock_symbols)
    company_name = company_names[stock_symbols.index(stock_symbol)]
    sector = random.choice(sectors)
    transaction_type = random.choices(transaction_types, weights=[70, 30])[0]  # More buys than sells
    quantity = random.randint(1, 100)
    # Assign price per share based on sector to add realism
    price_per_share = {
        'Technology': round(random.uniform(50, 3000), 2),
        'Consumer Discretionary': round(random.uniform(20, 500), 2),
        'Financials': round(random.uniform(10, 200), 2),
        'Communication Services': round(random.uniform(30, 600), 2),
        'Healthcare': round(random.uniform(10, 250), 2),
        'Consumer Staples': round(random.uniform(10, 150), 2),
        'Industrials': round(random.uniform(15, 300), 2),
        'Utilities': round(random.uniform(5, 100), 2),
        'Real Estate': round(random.uniform(50, 500), 2),
        'Materials': round(random.uniform(20, 400), 2)
    }[sector]
    total_amount = round(quantity * price_per_share, 2)
    broker = random.choice(brokers)
    portfolio_name = random.choice(portfolio_names)
    customer_age = random.randint(25, 65)
    customer_gender = random.choice(genders)
    investment_horizon = random.choice(investment_horizons)
    
    data.append([
        transaction_id, date, stock_symbol, company_name, sector, transaction_type,
        quantity, price_per_share, total_amount, broker, portfolio_name,
        customer_age, customer_gender, investment_horizon
    ])

# Create DataFrame
df = pd.DataFrame(data, columns=[
    'TransactionID', 'Date', 'StockSymbol', 'CompanyName', 'Sector',
    'TransactionType', 'Quantity', 'PricePerShare', 'TotalAmount',
    'Broker', 'PortfolioName', 'CustomerAge', 'CustomerGender', 'InvestmentHorizon'
])

# Introduce some missing values
for _ in range(5):
    idx = random.randint(0, num_records - 1)
    col = random.choice(['Broker', 'CustomerGender', 'InvestmentHorizon'])
    df.at[idx, col] = np.nan

# Introduce some duplicate records
duplicates = df.sample(5)
df = df.append(duplicates, ignore_index=True)

# Save to CSV
df.to_csv('data/financial_data.csv', index=False)

print("financial_data.csv generated successfully with {} records.".format(len(df)))
