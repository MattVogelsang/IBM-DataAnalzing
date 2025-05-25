# Stock Analysis Project

This project uses the yfinance library to analyze stock data for Tesla (TSLA) and GameStop (GME). It provides functionality to:

- Fetch historical stock data
- Retrieve financial information
- Generate stock price graphs
- Display revenue data

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script:
```bash
python stock_analysis.py
```

The script will:
- Display Tesla stock data (first 5 rows)
- Show Tesla revenue data (last 5 rows)
- Display GME stock data (first 5 rows)
- Show GME revenue data (last 5 rows)
- Generate a graph of Tesla's stock price over time

## Dependencies

- yfinance==0.2.36
- pandas==2.0.0
- matplotlib==3.7.0
- seaborn==0.12.0
- urllib3<2.0.0 