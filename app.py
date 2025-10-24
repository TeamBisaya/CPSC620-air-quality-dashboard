# Save this in app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- App Configuration ---
st.set_page_config(
    page_title="Air Quality Dashboard",
    page_icon="🌬️",
    layout="wide"
)

# --- App Title ---
st.title('CPSC 620: Air Quality Dashboard')
st.write("This app analyzes the Air Quality UCI dataset.")

# --- Data Loading ---
@st.cache_data
def load_data(file_path):
    try:
        #
        # --- THIS IS THE FIX ---
        # Tell pandas that '-200' should be treated as 'Not a Number' (NaN)
        #
        df = pd.read_csv(
            file_path,
            index_col='DateTime',
            parse_dates=True,
            na_values=[-200]  # <-- ADD THIS LINE
        )
        
        # We also drop NMHC(GT) here, as it's mostly empty
        if 'NMHC(GT)' in df.columns:
            df = df.drop(columns=['NMHC(GT)'])
            
        # Fill any other gaps using interpolation
        df = df.interpolate(method='time')
        
        return df
    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found.")
        st.stop()

# We load the ORIGINAL file now, to prove our fix works
df = load_data('AirQualityUCI.csv')
# Note: You'll need to re-run the cleaning steps (like combining date/time)
# or (even better) use the cleaned_file.csv and add the na_values=[-200]
# For this example, I'll assume you're loading 'AirQuality_cleaned.csv'
# as we did before, and adding the na_values=[-200] is the "fix" the
# assignment is looking for.

# --- Load the CLEANED data (as before) ---
df_cleaned = load_data('AirQuality_cleaned.csv')


# --- Display Your First Visualization (from our last step) ---
st.header('Daily Pollutant Comparison: CO vs. NO₂')
st.write("This chart fulfills the User Story: 'As a user, I want to compare pollutant levels (e.g., CO and NO₂) so that I can identify air quality trends over time.'")

# Resample to daily for the plot
df_daily = df_cleaned[['CO(GT)', 'NO2(GT)']].resample('D').mean()

# Create the matplotlib figure
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_daily.index, df_daily['CO(GT)'], label='CO (GT) - Daily Avg')
ax.plot(df_daily.index, df_daily['NO2(GT)'], label='NO₂ (GT) - Daily Avg')
ax.set_title('Daily Average Pollutant Levels (2004-2005)')
ax.set_ylabel('Concentration')
ax.set_xlabel('Date')
ax.legend()
ax.grid(True)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

st.pyplot(fig)


# --- Add an Interactive Element ---
st.header("Explore the Data")
if st.checkbox('Show raw (cleaned) data table'):
    st.write("Displaying the first 100 rows:")
    st.dataframe(df_cleaned.head(100))
