# Scraping Vahan Dashboard (Documented Steps)

The Vahan dashboard loads data via client-side JavaScript. A reliable way to extract tables is using **Selenium**.
This repo includes `src/data_collection.py` with a **template** that:
- Launches a headless Chrome via `webdriver-manager`.
- Navigates to Vahan dashboard pages.
- Waits for target tables to render.
- Parses HTML tables into Pandas DataFrames.
- Saves a normalized CSV for the Streamlit app.

## How to run

```bash
python src/data_collection.py --out data/vahan_registrations.csv
```

If you face loading issues due to dynamic widgets or CAPTCHA/rate limits, run slower with `--delay 2`
or export manually from any official download link if available, then place the CSV in `data/`.

## Target Columns

- `date` (YYYY-MM-01 for monthly), `vehicle_category` in {2W,3W,4W}, `manufacturer`, `registrations` (int),
  and optionally `state`.

## Notes

- The Vahan site may change DOM structure; update the CSS/XPath selectors in the scraper accordingly.
- Respect robots.txt and usage policies. Use caching; avoid heavy repeated scraping.