
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Air Tracker Dashboard",
    page_icon="✈️",
    layout="wide"
)

conn = sqlite3.connect("airtracker.db")
cursor = conn.cursor()

st.title("✈️ Air Tracker Dashboard")

# Dashboard Metrics
col1, col2, col3, col4 = st.columns(4)

cursor.execute("SELECT COUNT(*) FROM airport")
airports = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM aircraft")
aircraft = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM flights")
flights = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM airport_delays")
delays = cursor.fetchone()[0]

col1.metric("Airports", airports)
col2.metric("Aircraft", aircraft)
col3.metric("Flights", flights)
col4.metric("Delay Records", delays)

st.divider()


st.subheader("🔍 Flight Search")

flight_no = st.text_input("Enter Flight Number")

if flight_no:
    query = """
    SELECT flight_number,
           airline_code,
           origin_iata,
           destination_iata,
           status
    FROM flights
    WHERE flight_number = ?
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(flight_no,)
    )

    st.dataframe(df)

st.divider()

st.subheader("🛫 Airport Information")

airport_df = pd.read_sql_query(
    "SELECT * FROM airport",
    conn
)

st.dataframe(airport_df)

st.divider()

st.subheader("📊 Flight Status Analysis")

status_df = pd.read_sql_query("""
SELECT status,
       COUNT(*) as total
FROM flights
GROUP BY status
""", conn)

st.bar_chart(
    status_df.set_index("status")
)



st.divider()

st.subheader("🏆 Top Routes")

routes_df = pd.read_sql_query("""
SELECT origin_iata || ' → ' || destination_iata AS route,
       COUNT(*) AS total
FROM flights
GROUP BY route
ORDER BY total DESC
LIMIT 10
""", conn)

st.dataframe(routes_df)

st.divider()

st.subheader("⏱ Airport Delay Analysis")

delay_df = pd.read_sql_query("""
SELECT airport_iata,
       average_delay,
       arrival_delay,
       departure_delay
FROM airport_delays
""", conn)

st.dataframe(delay_df)

st.bar_chart(
    delay_df.set_index("airport_iata")[["average_delay"]]
)

conn.close()
