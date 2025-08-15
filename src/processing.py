from __future__ import annotations
import pandas as pd
from typing import List, Tuple, Optional

def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.to_period("M").dt.to_timestamp()
    df["vehicle_category"] = df["vehicle_category"].astype(str)
    df["manufacturer"] = df["manufacturer"].astype(str)
    df["registrations"] = pd.to_numeric(df["registrations"], errors="coerce").fillna(0).astype(int)
    return df

def filter_df(
    df: pd.DataFrame,
    date_range: Tuple[pd.Timestamp, pd.Timestamp],
    categories: Optional[List[str]] = None,
    manufacturers: Optional[List[str]] = None,
) -> pd.DataFrame:
    start, end = date_range
    m = (df["date"] >= start) & (df["date"] <= end)
    if categories:
        m &= df["vehicle_category"].isin(categories)
    if manufacturers:
        m &= df["manufacturer"].isin(manufacturers)
    return df.loc[m].copy()

def aggregate_time_series(df: pd.DataFrame, group_cols: List[str]) -> pd.DataFrame:
    g = df.groupby(group_cols + ["date"], as_index=False)["registrations"].sum()
    g = g.sort_values("date")
    return g

def growth_rates(ts_df: pd.DataFrame, group_cols: List[str]) -> pd.DataFrame:
    """
    Computes YoY and QoQ growth for each time series.
    Assumes monthly frequency. YoY = pct_change(12), QoQ = pct_change(3).
    """
    ts_df = ts_df.copy().sort_values("date")
    ts_df["YoY_%"] = (
        ts_df.groupby(group_cols)["registrations"].pct_change(periods=12) * 100
    )
    ts_df["QoQ_%"] = (
        ts_df.groupby(group_cols)["registrations"].pct_change(periods=3) * 100
    )
    return ts_df

def latest_kpis(ts_df: pd.DataFrame, group_cols: List[str]) -> pd.DataFrame:
    """
    Returns latest period value and YoY/QoQ for each group.
    """
    idx = ts_df.groupby(group_cols)["date"].transform("max") == ts_df["date"]
    latest = ts_df.loc[idx].copy()
    latest = latest[group_cols + ["date", "registrations", "YoY_%", "QoQ_%"]]
    latest = latest.sort_values(by="registrations", ascending=False)
    return latest