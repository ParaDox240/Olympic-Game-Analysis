import pandas as pd


def fetch_medal_tally(df, year, country):
    medal_df = df.dropna(subset=["Medal"])

    if year != "Overall":
        medal_df = medal_df[medal_df["Year"] == year]

    if country != "Overall":
        medal_df = medal_df[medal_df["region"] == country]

    medal_tally = (
        medal_df.groupby("region")[["Gold", "Silver", "Bronze"]]
        .sum()
        .reset_index()
        .sort_values(by=["Gold", "Silver", "Bronze"], ascending=False)
    )

    return medal_tally


def year_country_list(df):
    years = sorted(df["Year"].unique().tolist())
    years.insert(0, "Overall")

    countries = sorted(df["region"].dropna().unique().tolist())
    countries.insert(0, "Overall")

    return years, countries


def country_list(df):
    return sorted(df["region"].dropna().unique().tolist())


def most_successful(df, sport=None):
    temp_df = df.dropna(subset=["Medal"])

    if sport:
        temp_df = temp_df[temp_df["Sport"] == sport]

    top_athletes = (
        temp_df["Name"]
        .value_counts()
        .reset_index(name="Medals")
        .rename(columns={"index": "Name"})
        .head(10)
    )

    return top_athletes


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df = temp_df[temp_df["region"] == country]

    top_players = (
        temp_df["Name"]
        .value_counts()
        .reset_index(name="Medals")
        .rename(columns={"index": "Name"})
    )

    final_df = (
        top_players
        .merge(temp_df, on="Name", how="left")
        [["Name", "Sport", "Team", "Medals"]]
        .drop_duplicates()
        .head(10)
    )

    return final_df
