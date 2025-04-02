import streamlit as st
import pandas as pd
import plotly.express as px

# Load datasets
india_emissions = pd.read_csv("CarbonEmissionIndia.csv")
country_emissions = pd.read_csv("co2_emissions_kt_by_country.csv")
sector_emissions = pd.read_csv("dataset.csv")

st.set_page_config(page_title="ESG Dashboard - India", layout="wide")
st.title("🌿 ESG Carbon Emissions Dashboard - India")

# State-wise Per Capita CO₂ Emissions (Horizontal Bar Chart)
st.subheader("State-wise Per Capita CO₂ Emissions in India")
fig1 = px.bar(
    india_emissions.sort_values(by="per capita CO2 (kg per person)", ascending=True),
    x="per capita CO2 (kg per person)",
    y="States",
    orientation="h",
    title="State-wise Per Capita CO₂ Emissions in India",
    labels={"per capita CO2 (kg per person)": "CO₂ Emissions (kg per person)"},
    color="per capita CO2 (kg per person)",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig1, use_container_width=True)

# India's CO₂ emissions over time
st.subheader("India's CO₂ Emissions Over Time")
india_trend = country_emissions[country_emissions["country_name"] == "India"]
fig2 = px.line(
    india_trend,
    x="year",
    y="value",
    title="India's CO₂ Emissions Trend (kt)",
    labels={"value": "CO₂ Emissions (kt)", "year": "Year"},
    markers=True
)
st.plotly_chart(fig2, use_container_width=True)

# Sector-wise emissions in India
st.subheader("Sector-wise CO₂ Emissions in India")
india_sectors = sector_emissions[sector_emissions["country"] == "India"]
fig3 = px.bar(
    india_sectors,
    x="sector",
    y="value",
    title="Sector-wise CO₂ Emissions in India",
    labels={"value": "CO₂ Emissions"},
    color="sector",
)
st.plotly_chart(fig3, use_container_width=True)

# User selection for India vs Global Leaders
st.subheader("India vs Global Leaders in Per Capita CO₂ Emissions")
available_years = sorted(country_emissions["year"].unique(), reverse=True)
selected_year = st.selectbox("Select Year", available_years, index=0)
available_countries = sorted(country_emissions["country_name"].unique())
selected_countries = st.multiselect("Select Countries", available_countries, default=["India", "China", "United States", "Germany", "Brazil"])

global_comparison = country_emissions[(country_emissions["year"] == selected_year) & (country_emissions["country_name"].isin(selected_countries))]

if not global_comparison.empty:
    fig4 = px.bar(
        global_comparison.sort_values(by="value", ascending=False),
        x="value",
        y="country_name",
        orientation="h",
        title=f"Per Capita CO₂ Emissions Comparison ({selected_year})",
        labels={"value": "CO₂ Emissions (kt)", "country_name": "Country"},
        color="value",
        color_continuous_scale="Reds",
        text_auto=True
    )
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.warning("No data available for selected countries and year. Please adjust your selections.")

st.markdown("\n\n**Insights:**\n")
st.markdown("- Some states in India have significantly higher per capita emissions than others.")
st.markdown("- India's overall CO₂ emissions have been rising steadily over the years.")
st.markdown("- Power and transportation sectors contribute majorly to emissions.")
st.markdown("- India’s per capita emissions are still lower than major global economies.")
