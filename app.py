import streamlit as st
from src.load import load_csv, combine
from src.variance import add_variance, flag_material

st.set_page_config(page_title="Variance Analyzer", layout="wide")
st.title("Budget vs. Actual Variance Analyzer")
st.caption("SYNTHETIC data for a hypothetical photography business. Not real financials.")


@st.cache_data
def load_data():
    return combine(load_csv("data/budget.csv"), load_csv("data/actuals.csv"))


raw = load_data()

# Sidebar controls
st.sidebar.header("Materiality")
pct = st.sidebar.slider("Percent threshold (%)", 0, 100, 10)
dollars = st.sidebar.slider("Dollar threshold ($)", 0, 2000, 500, step=50)
mode = st.sidebar.radio(
    "Flag when",
    ["and", "or"],
    format_func=lambda m: "BOTH thresholds exceeded" if m == "and" else "EITHER threshold exceeded",
)
months = sorted(raw["month"].unique())
selected = st.sidebar.multiselect("Months", months, default=months)

df = flag_material(add_variance(raw), pct, dollars, mode)
df = df[df["month"].isin(selected)]

# Summary numbers
c1, c2, c3 = st.columns(3)
c1.metric("Flagged items", int(df["flagged"].sum()))
c2.metric("Rows shown", len(df))
c3.metric("Missing actuals", int((df["status"] == "missing").sum()))

if (df["status"] == "missing").any():
    st.warning("Some actuals are missing. They are shown as 'missing' and not flagged.")

# Flagged table
st.subheader("Flagged for review")
cols = ["month", "line_item", "type", "budget", "actual", "variance", "variance_pct", "status"]
flagged = df[df["flagged"]]
if flagged.empty:
    st.info("Nothing exceeds the current thresholds.")
else:
    st.dataframe(flagged[cols], hide_index=True)

# Top variances chart
st.subheader("Top 10 variances ($)")
top = df.dropna(subset=["variance"]).copy()
top["label"] = top["month"] + " " + top["line_item"]
top["abs_variance"] = top["variance"].abs()
top = top.nlargest(10, "abs_variance").set_index("label")["variance"]
st.bar_chart(top)

# Monthly trend
st.subheader("Total variance by month")
trend = df.groupby(["month", "type"])["variance"].sum().unstack()
st.line_chart(trend)

# Full table
with st.expander("All rows"):
    st.dataframe(df[cols + ["flagged"]], hide_index=True)