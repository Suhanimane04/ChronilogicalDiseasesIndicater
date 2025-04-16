import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
def load_data():
    file_path = "U.S._Chronic_Disease_Indicators.csv"
    df = pd.read_csv(file_path)

    # Show column names for reference
    st.write("Available Columns:", df.columns.tolist())

    # Convert relevant columns
    df["YearStart"] = pd.to_numeric(df["YearStart"], errors='coerce')
    df["YearEnd"] = pd.to_numeric(df["YearEnd"], errors='coerce')
    df["DataValue"] = pd.to_numeric(df["DataValue"], errors='coerce')

    return df

df = load_data()

# Apply custom styling
st.markdown("""
    <style>
        body {
            background-color: black;
            color: white;
        }
        .stTitle {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar filters with toggle
st.sidebar.header("Filters")
show_filters = st.sidebar.checkbox("Show Filters")
if show_filters:
    year_filter = st.sidebar.multiselect("Select Year", sorted(df["YearStart"].dropna().unique()))
    state_filter = st.sidebar.multiselect("Select State", sorted(df["LocationDesc"].dropna().unique()))
    topic_filter = st.sidebar.multiselect("Select Topic", sorted(df["Topic"].dropna().unique()))
    question_filter = st.sidebar.multiselect("Select Question", sorted(df["Question"].dropna().unique()))

    # Apply filters
    filtered_df = df.copy()
    if year_filter:
        filtered_df = filtered_df[filtered_df["YearStart"].isin(year_filter)]
    if state_filter:
        filtered_df = filtered_df[filtered_df["LocationDesc"].isin(state_filter)]
    if topic_filter:
        filtered_df = filtered_df[filtered_df["Topic"].isin(topic_filter)]
    if question_filter:
        filtered_df = filtered_df[filtered_df["Question"].isin(question_filter)]
else:
    filtered_df = df.copy()

# Dashboard Title
st.title("U.S. Chronic Disease Indicators Dashboard")

st.header("Most Prevalent Questions")
most_common = filtered_df.groupby("Question")["DataValue"].mean().nlargest(10).reset_index()
fig_most = px.bar(most_common, x="DataValue", y="Question", color="Question", orientation='h', height=500)
st.plotly_chart(fig_most, use_container_width=True)

st.header("Least Prevalent Questions")
least_common = filtered_df.groupby("Question")["DataValue"].mean().nsmallest(5).reset_index()
fig_least = px.pie(least_common, names="Question", values="DataValue")
st.plotly_chart(fig_least, use_container_width=True)

st.header("Average Values per Topic")
avg_topic = filtered_df.groupby("Topic")["DataValue"].mean().reset_index()
fig_topic = px.bar(avg_topic, x="DataValue", y="Topic", color="Topic", orientation='h', height=500)
st.plotly_chart(fig_topic, use_container_width=True)

st.header("Yearly Trends in Data Values")
yearly_trend = filtered_df.groupby("YearStart")["DataValue"].mean().reset_index()
fig_yearly = px.line(yearly_trend, x="YearStart", y="DataValue", markers=True, height=500)
st.plotly_chart(fig_yearly, use_container_width=True)

st.header("State-wise Averages")
state_avg = filtered_df.groupby("LocationDesc")["DataValue"].mean().reset_index()
fig_state = px.bar(state_avg, x="DataValue", y="LocationDesc", color="LocationDesc", orientation='h', height=500)
st.plotly_chart(fig_state, use_container_width=True)

st.header("Question vs Value Comparison")
fig_scatter = px.scatter(filtered_df, x="YearStart", y="DataValue", color="Topic", size_max=10, height=500)
st.plotly_chart(fig_scatter, use_container_width=True)
