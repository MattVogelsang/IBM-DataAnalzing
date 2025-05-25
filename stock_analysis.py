import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import time
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import urllib3

# Suppress SSL warnings
warnings.filterwarnings('ignore', category=urllib3.exceptions.InsecureRequestWarning)

def get_stock_data(ticker):
    """Get stock data using yfinance with retry mechanism"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="max")
            if not data.empty:
                data.reset_index(inplace=True)
                return data
            print(f"Warning: No data found for {ticker}, attempt {attempt + 1}/{max_retries}")
        except Exception as e:
            print(f"Error getting stock data for {ticker}: {str(e)}, attempt {attempt + 1}/{max_retries}")
    return None

def get_revenue_data(ticker):
    """Get revenue data using yfinance"""
    try:
        stock = yf.Ticker(ticker)
        revenue = stock.financials
        if not revenue.empty:
            return revenue
        print(f"Warning: No revenue data found for {ticker}")
    except Exception as e:
        print(f"Error getting revenue data for {ticker}: {str(e)}")
    return None

def create_dashboard(stock_data, revenue_data, title):
    """Create an interactive dashboard comparing stock price and revenue"""
    if stock_data is None or revenue_data is None:
        print(f"Warning: Cannot create dashboard for {title} due to missing data")
        return None
        
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add stock price line
    fig.add_trace(
        go.Scatter(x=stock_data.index, y=stock_data['Close'],
                  name="Stock Price"),
        secondary_y=False,
    )
    
    # Add revenue bars
    fig.add_trace(
        go.Bar(x=revenue_data['Date'], y=revenue_data['Revenue'],
               name="Revenue"),
        secondary_y=True,
    )
    
    # Set titles
    fig.update_layout(
        title_text=title,
        xaxis_title="Date",
    )
    
    # Set y-axes titles
    fig.update_yaxes(title_text="Stock Price ($)", secondary_y=False)
    fig.update_yaxes(title_text="Revenue ($)", secondary_y=True)
    
    return fig

def make_graph(data, title):
    """Create a stock price graph"""
    if data is None or data.empty:
        print(f"Warning: No data available to create graph for {title}")
        return
        
    plt.figure(figsize=(12, 6))
    plt.plot(data['Date'], data['Close'])
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Stock Price ($)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    # Create a directory for the dashboards if it doesn't exist
    if not os.path.exists('dashboards'):
        os.makedirs('dashboards')
    
    # Question 1: Tesla Stock Data
    print("\nFetching Tesla Stock Data...")
    tesla_data = get_stock_data("TSLA")
    if tesla_data is not None:
        print("\nTesla Stock Data (First 5 rows):")
        print(tesla_data.head())
    
    # Question 2: Tesla Revenue Data
    print("\nFetching Tesla Revenue Data...")
    tesla_revenue = get_revenue_data("TSLA")
    if tesla_revenue is not None:
        print("\nTesla Revenue Data (Last 5 rows):")
        print(tesla_revenue.tail())
    
    # Question 3: GME Stock Data
    print("\nFetching GameStop Stock Data...")
    gme_data = get_stock_data("GME")
    if gme_data is not None:
        print("\nGME Stock Data (First 5 rows):")
        print(gme_data.head())
    
    # Question 4: GME Revenue Data
    print("\nFetching GameStop Revenue Data...")
    gme_revenue = get_revenue_data("GME")
    if gme_revenue is not None:
        print("\nGME Revenue Data (Last 5 rows):")
        print(gme_revenue.tail())
    
    # Question 5: Create Tesla Dashboard
    if tesla_data is not None:
        print("\nCreating Tesla Dashboard...")
        tesla_dashboard = create_dashboard(tesla_data, tesla_revenue, "Tesla Stock Price vs Revenue")
        if tesla_dashboard is not None:
            tesla_dashboard.write_html("dashboards/tesla_dashboard.html")
            tesla_dashboard.show()
    
    # Question 6: Create GameStop Dashboard
    if gme_data is not None:
        print("\nCreating GameStop Dashboard...")
        gme_dashboard = create_dashboard(gme_data, gme_revenue, "GameStop Stock Price vs Revenue")
        if gme_dashboard is not None:
            gme_dashboard.write_html("dashboards/gamestop_dashboard.html")
            gme_dashboard.show()
    
    # Question 5: Plot Tesla Stock Graph
    if tesla_data is not None:
        make_graph(tesla_data, 'Tesla Stock Price Over Time')
    
    print("\nProcess completed. Check the 'dashboards' directory for saved HTML files.")

if __name__ == "__main__":
    main() 