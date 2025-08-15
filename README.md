# Vahan Investor Dashboard (Streamlit)


A clean investor-focused dashboard for India's vehicle registration data from the public **Vahan** portal.

The dashboard shows:
- **Year-over-Year (YoY)** and **Quarter-over-Quarter (QoQ)** growth
- By **vehicle category** (2W, 3W, 4W)
- By **manufacturer**
- Interactive date range & filters
- Trend graphs and % change KPIs

---



## Quickstart

```bash
# Create and activate virtual environment
python -m venv .venv
. .venv/Scripts/activate   # Windows
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run src/app.py


Project Structure

vahan_investor_dashboard/
├── data/                  # Sample dataset (CSV)
├── sql/                   # SQL schema (optional SQLite path)
├── src/                   # All source code
│   ├── data_collection.py
│   ├── load_to_sqlite.py
│   ├── processing.py
│   └── app.py
└── requirements.txt



Features

Date range selection

Filters by category/manufacturer

YoY & QoQ growth KPIs

Category and manufacturer trends

Ready-to-run with included sample dataset

Deployment

You can deploy this on Streamlit Cloud:

Push the repo to GitHub

Go to https://vahan-investor-dashboard-36nukfjeemqs4k4c66sul5.streamlit.app/

Link your repo and set src/app.py as the main file



Requirements

Python 3.9+

Streamlit

Pandas

Plotly

(Optional) SQLite3
