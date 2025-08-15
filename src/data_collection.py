import argparse
import time
import pandas as pd

# Optional Selenium imports (only used if --scrape is passed)
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
except Exception:
    webdriver = None

VAHAN_URL = "https://vahan.parivahan.gov.in/vahan4dashboard/"

def scrape_vahan(delay: float = 1.0) -> pd.DataFrame:
    """
    Headless Selenium scraper template to extract vehicle category/manufacturer registrations.
    You MUST update the CSS/XPath selectors to match Vahan's DOM.
    Returns a normalized DataFrame with columns:
      date (YYYY-MM-01), vehicle_category (2W/3W/4W), manufacturer, registrations
    """
    if webdriver is None:
        raise RuntimeError("Selenium is not installed; install extras in requirements.txt")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(VAHAN_URL)
    wait = WebDriverWait(driver, 20)

    # --- EXAMPLE FLOW (update selectors specific to the page/table you need) ---
    # 1) Wait for a chart/table container to render
    #    Replace the CSS selector below with the real one from DevTools.
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.dashboard-container")))
    time.sleep(delay)

    # TODO: Example extraction logic — replace:
    # Find table elements for category-wise and manufacturer-wise data and build data rows.
    # rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")  # <- update selector
    # Parse text, infer date context, vehicle category, manufacturer, registrations.
    # For demonstration we return an empty DataFrame and ask the user to fill selectors.
    df = pd.DataFrame(columns=["date", "vehicle_category", "manufacturer", "registrations"])

    driver.quit()
    return df

def main():
    parser = argparse.ArgumentParser(description="Fetch/prepare Vahan data")
    parser.add_argument("--out", default="data/vahan_registrations.csv", help="Output CSV path")
    parser.add_argument("--scrape", action="store_true", help="Use Selenium to scrape live site")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay seconds between actions")

    args = parser.parse_args()

    if args.scrape:
        df = scrape_vahan(delay=args.delay)
    else:
        # Fallback: load sample; replace with your own CSV once available
        df = pd.read_csv("data/sample_registrations.csv", parse_dates=["date"])

    # Basic sanity
    df["date"] = pd.to_datetime(df["date"]).dt.to_period("M").dt.to_timestamp()
    df["vehicle_category"] = df["vehicle_category"].astype(str)
    df["manufacturer"] = df["manufacturer"].astype(str)
    df["registrations"] = pd.to_numeric(df["registrations"], errors="coerce").fillna(0).astype(int)

    df.to_csv(args.out, index=False)
    print(f"Wrote {len(df)} rows to {args.out}")

if __name__ == "__main__":
    main()