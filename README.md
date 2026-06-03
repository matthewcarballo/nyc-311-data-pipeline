# NYC 311 Data Pipeline

An end-to-end data engineering and analytics project that ingests, stores, transforms, and visualizes NYC 311 service request data using Python, PostgreSQL, Airflow, dbt, and pandas.

## Architecture

```text
NYC Open Data API
↓
Python Ingestion (fetch_311_data.py)
↓
PostgreSQL Database (raw_311)
↓
Apache Airflow Daily Schedule
↓
dbt Transformations (stg_311 → fct_311)
↓
Python Analysis & Visualizations
```

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.13 | Data ingestion, API calls, analysis |
| PostgreSQL 15 | Data storage |
| Apache Airflow 3 | Pipeline orchestration |
| dbt 1.8 | Data transformation |
| pandas + matplotlib | Analysis and visualization |
| Git + GitHub | Version control |

## Project Structure

```text
nyc-311-data-pipeline/
├── ingestion/
│   └── fetch_311_data.py      # Pulls data from NYC Open Data API
├── orchestration/
│   └── dag_311_pipeline.py    # Airflow DAG for daily scheduling
├── nyc_311/
│   └── models/
│       ├── staging/
│       │   └── stg_311.sql    # Cleans raw data
│       └── marts/
│           └── fct_311.sql    # Final analysis-ready table
├── analysis/
│   ├── explore.ipynb          # Analysis notebook
│   └── nyc_311_analysis.png   # Output charts
└── requirements.txt
```

## Key Findings

- **Brooklyn** has the most 311 complaints of any borough.
- **Noise - Residential** is the most common complaint type citywide.
- **53%** of complaints remain open.
- **Queens** has the longest average resolution time.

## Setup Instructions

### Prerequisites

- Python 3.13+
- PostgreSQL 15
- Apache Airflow 3
- dbt-postgres 1.8

### Installation

1. Clone the repository.

```bash
git clone https://github.com/matthewcarballo/nyc-311-data-pipeline.git
cd nyc-311-data-pipeline
```

2. Install dependencies.

```bash
pip install requests pandas psycopg2-binary python-dotenv apache-airflow dbt-postgres matplotlib seaborn jupyter
```

3. Create the database.

```bash
createdb nyc_311
```

4. Run the ingestion script.

```bash
python ingestion/fetch_311_data.py
```

5. Run dbt transformations.

```bash
cd nyc_311
dbt run
```

6. Start Airflow.

```bash
export AIRFLOW_HOME=~/airflow
airflow standalone
```

## Data Source

[NYC Open Data: 311 Service Requests from 2010 to Present](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9)

## Author

Matthew Carballo — [GitHub](https://github.com/matthewcarballo)