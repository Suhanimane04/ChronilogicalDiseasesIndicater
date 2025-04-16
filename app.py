import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- Load and clean dataset ----------
csv_path = "U.S._Chronic_Disease_Indicators.csv"
try:
    df = pd.read_csv(csv_path, usecols=[
        "Topic", "LocationDesc", "YearStart", "Stratification1", "DataValue"
    ])
    df["DataValue"] = pd.to_numeric(df["DataValue"], errors="coerce")
    df.dropna(subset=["DataValue"], inplace=True)
except FileNotFoundError:
    st.error("❌ Dataset file not found. Please check the file path.")
    st.stop()

# ---------- Dashboard UI ----------
st.set_page_config(page_title="Chronic Disease Dashboard", layout="wide")
st.title("📊 U.S. Chronic Disease Indicators Dashboard")
st.markdown("""
Analyze chronic disease trends across the U.S.  
Use the controls on the left to explore the data from various angles.
""")

# ---------- Sidebar Controls ----------
with st.sidebar:
    st.header("🔧 Controls")
    topic_list = sorted(df["Topic"].unique())
    selected_topic = st.selectbox("🩺 Choose a Topic", topic_list)

    attribute_options = ["LocationDesc", "YearStart", "Stratification1"]
    x_attr = st.selectbox("📊 X-axis Attribute", attribute_options)
    group_attr = st.selectbox("🎨 Grouping/Color", attribute_options)

    chart_types = [
        "Bar Chart", "Pie Chart", "Scatter Plot", "Line Chart",
        "Histogram", "Box Plot", "Area Chart", "Heatmap"
    ]
    chart_type = st.selectbox("📈 Chart Type", chart_types)

# ---------- Filter by topic ----------
filtered_df = df[df["Topic"] == selected_topic]

# ---------- Chart Drawing ----------
st.subheader(f"{chart_type} for '{selected_topic}' by {x_attr}")

fig, ax = plt.subplots(figsize=(12, 6))

if chart_type == "Bar Chart":
    bar_df = filtered_df.groupby(x_attr)["DataValue"].mean().sort_values(ascending=False).reset_index()
    sns.barplot(data=bar_df, x=x_attr, y="DataValue", ax=ax, palette="coolwarm")
    plt.xticks(rotation=90)

elif chart_type == "Pie Chart":
    pie_df = filtered_df.groupby(x_attr)["DataValue"].sum().sort_values(ascending=False).head(10)
    pie_df.plot(kind="pie", y="DataValue", autopct='%1.1f%%', ax=ax, legend=False)
    ax.set_ylabel("")

elif chart_type == "Scatter Plot":
    sns.scatterplot(data=filtered_df, x=x_attr, y="DataValue", hue=group_attr, ax=ax, palette="Set2", alpha=0.7, edgecolor="black")
    plt.xticks(rotation=45)

elif chart_type == "Line Chart":
    line_df = filtered_df.groupby([x_attr, group_attr])["DataValue"].mean().reset_index()
    sns.lineplot(data=line_df, x=x_attr, y="DataValue", hue=group_attr, ax=ax)
    plt.xticks(rotation=45)

elif chart_type == "Histogram":
    sns.histplot(data=filtered_df, x="DataValue", bins=30, kde=True, ax=ax, color='teal')

elif chart_type == "Box Plot":
    sns.boxplot(data=filtered_df, x=group_attr, y="DataValue", ax=ax, palette="Pastel1")
    plt.xticks(rotation=45)

elif chart_type == "Area Chart":
    area_df = filtered_df.groupby(["YearStart", group_attr])["DataValue"].mean().reset_index()
    for name, group in area_df.groupby(group_attr):
        ax.fill_between(group["YearStart"], group["DataValue"], label=name, alpha=0.4)
    ax.legend()
    ax.set_xlabel("YearStart")
    ax.set_ylabel("DataValue")

elif chart_type == "Heatmap":
    heat_df = filtered_df.pivot_table(values="DataValue", index="YearStart", columns="LocationDesc", aggfunc="mean")
    sns.heatmap(heat_df, cmap="YlGnBu", ax=ax)
    plt.xticks(rotation=90)

st.pyplot(fig)

# ---------- Footer ----------
st.markdown("### ℹ️ Notes")
st.markdown("""
- Use the sidebar to switch between chart types and grouping methods.
- Pie chart shows top 10 groups.
- Line/Area charts are best for Year-based visualizations.
- Heatmap requires both Year and Location data.
""")
