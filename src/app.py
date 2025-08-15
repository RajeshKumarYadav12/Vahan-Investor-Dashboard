import os
import pandas as pd
import streamlit as st
import plotly.express as px

from processing import normalize_df, filter_df, aggregate_time_series, growth_rates, latest_kpis

st.set_page_config(page_title="Vahan Investor Dashboard", layout="wide")

@st.cache_data
def load_data() -> pd.DataFrame:
    # Priority: user-provided CSV > scraped CSV > sample CSV
    candidates = [
        st.session_state.get("data_path", ""),
        "data/vahan_registrations.csv",
        "data/sample_registrations.csv",
    ]
    for p in candidates:
        if p and os.path.exists(p):
            df = pd.read_csv(p, parse_dates=["date"])
            return normalize_df(df)
    st.stop()

# Sidebar – data path
with st.sidebar:
    st.title("Vahan Investor Dashboard")
    st.caption("Filters and controls")
    data_path = st.text_input("CSV path (optional)", value="")
    if data_path:
        st.session_state["data_path"] = data_path

df = load_data()

# Sidebar – filters
min_date, max_date = df["date"].min(), df["date"].max()
date_range = st.sidebar.slider(
    "Date range",
    min_value=min_date.to_pydatetime(),
    max_value=max_date.to_pydatetime(),
    value=(min_date.to_pydatetime(), max_date.to_pydatetime()),
    format="YYYY-MM",
)

categories = sorted(df["vehicle_category"].unique().tolist())
manufacturers = sorted(df["manufacturer"].unique().tolist())

sel_categories = st.sidebar.multiselect("Vehicle category", categories, default=categories)
sel_manufacturers = st.sidebar.multiselect("Manufacturer", manufacturers)

# Filtered DF
fdf = filter_df(df, date_range, sel_categories, sel_manufacturers)

# Time series (by category) for totals
ts_cat = aggregate_time_series(fdf, ["vehicle_category"])
ts_cat = growth_rates(ts_cat, ["vehicle_category"])

# Time series (by manufacturer)
ts_mfr = aggregate_time_series(fdf, ["manufacturer"])
ts_mfr = growth_rates(ts_mfr, ["manufacturer"])

# KPIs – latest
latest_cat = latest_kpis(ts_cat, ["vehicle_category"])
latest_mfr = latest_kpis(ts_mfr, ["manufacturer"])

# --- Layout ---
st.subheader("Overview KPIs (latest period in range)")
col1, col2, col3 = st.columns(3)
total_latest = (
    ts_cat.loc[ts_cat["date"] == ts_cat["date"].max(), "registrations"].sum()
    if not ts_cat.empty else 0
)
yoy_latest = (
    ts_cat.loc[ts_cat["date"] == ts_cat["date"].max(), "YoY_%"].mean()
    if not ts_cat.empty else float("nan")
)
qoq_latest = (
    ts_cat.loc[ts_cat["date"] == ts_cat["date"].max(), "QoQ_%"].mean()
    if not ts_cat.empty else float("nan")
)

col1.metric("Total registrations (latest month)", f"{total_latest:,.0f}")
col2.metric("Avg YoY (categories)", f"{yoy_latest:,.1f}%")
col3.metric("Avg QoQ (categories)", f"{qoq_latest:,.1f}%")

st.markdown("---")

# Trends – categories
st.markdown("### Category Trends")
if not ts_cat.empty:
    fig_cat = px.line(
        ts_cat,
        x="date",
        y="registrations",
        color="vehicle_category",
        markers=True,
        title="Monthly registrations by category",
    )
    st.plotly_chart(fig_cat, use_container_width=True)

    # Growth heatmap-ish table
    st.dataframe(
        latest_cat.rename(columns={
            "vehicle_category": "Category",
            "registrations": "Latest Registrations",
            "YoY_%": "YoY %",
            "QoQ_%": "QoQ %",
        }).style.format({"Latest Registrations": ",", "YoY %": "{:.1f}%", "QoQ %": "{:.1f}%"}),
        use_container_width=True,
    )
else:
    st.info("No data after filters for categories.")

st.markdown("---")

# Trends – manufacturers
st.markdown("### Manufacturer Trends")
if not ts_mfr.empty:
    # Optional top-N manufacturers selector for clarity
    top_n = st.slider("Show top N manufacturers by latest registrations", 3, 25, 10)
    top_latest = latest_mfr.head(top_n)["manufacturer"].tolist()
    ts_mfr_top = ts_mfr[ts_mfr["manufacturer"].isin(top_latest)]

    fig_mfr = px.line(
        ts_mfr_top,
        x="date",
        y="registrations",
        color="manufacturer",
        markers=True,
        title=f"Monthly registrations – top {len(top_latest)} manufacturers",
    )
    st.plotly_chart(fig_mfr, use_container_width=True)

    # Bar chart for latest market share
    latest_date = ts_mfr["date"].max()
    latest_slice = ts_mfr[ts_mfr["date"] == latest_date].sort_values("registrations", ascending=False)
    fig_share = px.bar(
        latest_slice.head(top_n),
        x="manufacturer",
        y="registrations",
        title=f"Market share (latest month: {latest_date.strftime('%Y-%m')})",
    )
    st.plotly_chart(fig_share, use_container_width=True)

    st.dataframe(
        latest_mfr.rename(columns={
            "manufacturer": "Manufacturer",
            "registrations": "Latest Registrations",
            "YoY_%": "YoY %",
            "QoQ_%": "QoQ %",
        }).style.format({"Latest Registrations": ",", "YoY %": "{:.1f}%", "QoQ %": "{:.1f}%"}),
        use_container_width=True,
    )
else:
    st.info("No data after filters for manufacturers.")

st.markdown("---")
st.caption("Tip: Provide your own CSV via the sidebar input to analyze fresh Vahan exports.")