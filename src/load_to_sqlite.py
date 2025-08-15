import sqlite3, argparse, pandas as pd, os

def ensure_schema(conn: sqlite3.Connection, schema_path: str):
    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

def load_csv(conn: sqlite3.Connection, csv_path: str):
    df = pd.read_csv(csv_path, parse_dates=["date"])
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    df.to_sql("registrations", conn, if_exists="append", index=False)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="data/vahan.db")
    ap.add_argument("--csv", default="data/vahan_registrations.csv")
    ap.add_argument("--schema", default="sql/schema.sql")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.db), exist_ok=True)
    conn = sqlite3.connect(args.db)
    ensure_schema(conn, args.schema)
    load_csv(conn, args.csv)
    conn.commit()
    conn.close()
    print(f"Loaded data from {args.csv} into {args.db}")

if __name__ == "__main__":
    main()