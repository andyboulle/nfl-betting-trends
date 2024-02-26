# NFL Trends Analyzer

## Overview

The NFL Trends Analyzer is a Python tool designed to analyze historical data from every NFL game since 2006. It generates trends related to both game information and betting information, providing insights into home/away and favorite/underdog trends for moneylines, spreads, and totals.

## Installation

To use the NFL Trends Analyzer, follow these steps:

1. Clone the repository:
```bash
   git clone https://github.com/andyboulle/NFLTrendsAnalyzer.git
   cd NFLTrendsAnalyzer
```
2. Create a virtual environment:
```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv/Scripts/activate      # Windows
``` 
3. Install requirements:
```bash
   pip install -r requirements.txt
```
## Usage
1. Adjust `db.py` with the details from your PostgreSQL database:
```python
   conn = psycopg2.connect(
      host = 'localhost',
      dbname = 'postgres',
      user = 'postgres',
      password = 'pass',
      port = 5432
   )
```
3. Run `db.py` to create PostgreSQL database for Games and Trends. NOTE: This will take a very long time (took me ~13 hours).
```bash
   python db.py
```

## Contributions

Contributions are welcome! If you have any suggestions, bug reports, or enhancements, please open an issue or submit a pull request.
