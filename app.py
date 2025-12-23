import streamlit as st
import pandas as pd
import helper

st.set_page_config(page_title="Olympic Analysis", layout="wide")

# Load data safely
@st.cache_data
def load_data():
    df = pd.read_csv("athlete_events.csv")
    region_df = pd.read_csv("noc_regions.csv")
    df = df.merge(region_df, on="NOC", how="left")
    return df

df = load_data()

st.sidebar.title("Olympic Analysis")

user_menu = st.sidebar.radio(
    "Select an option",
    (
        "Medal Tally",
        "Overall Analysis",
        "Country-wise Analysis",
        "Athlete-wise Analysis"
    )
)

# ---------------- Medal Tally ----------------
if user_menu == "Medal Tally":
    st.title("🏅 Medal Tally")

    years, countries = helper.year_country_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", countries)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    st.table(medal_tally)

# ---------------- Overall Analysis ----------------
elif user_menu == "Overall Analysis":
    st.title("📊 Overall Analysis")

    editions = df["Year"].nunique()
    cities = df["City"].nunique()
    sports = df["Sport"].nunique()
    events = df["Event"].nunique()
    athletes = df["Name"].nunique()
    nations = df["region"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Editions", editions)
    col2.metric("Hosts", cities)
    col3.metric("Sports", sports)

    col4, col5, col6 = st.columns(3)
    col4.metric("Events", events)
    col5.metric("Athletes", athletes)
    col6.metric("Nations", nations)

# ---------------- Country-wise Analysis ----------------
elif user_menu == "Country-wise Analysis":
    st.title("🌍 Country-wise Analysis")

    country_list = helper.country_list(df)
    selected_country = st.sidebar.selectbox("Select Country", country_list)

    medal_df = helper.fetch_medal_tally(df, "Overall", selected_country)
    st.subheader(f"{selected_country} Medal Tally")
    st.table(medal_df)

    st.subheader("Top 10 Athletes")
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

# ---------------- Athlete-wise Analysis ----------------
elif user_menu == "Athlete-wise Analysis":
    st.title("🏃 Athlete-wise Analysis")

    athlete_df = helper.most_successful(df)
    st.table(athlete_df)
