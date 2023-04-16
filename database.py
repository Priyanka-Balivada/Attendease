# streamlit_app.py

import streamlit as st
import mysql.connector
import pandas as pd

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

# number = conn.cursor().execute("SELECT count(*) FROM information_schema.columns WHERE table_name ='eventdata';")
# st.write(number)
# rows = pd.read_sql('SELECT * from eventdata;',conn)

rows = run_query("SELECT * from student;")

# query_df = pd.DataFrame(query_results)
					# st.dataframe(query_df)

# Print results.
col1, col2, col3 = st.columns(3)
with col1:
        st.header("PRN")
with col2:
        st.header("Name")
with col3:
        st.header("Division")

for row in rows:
    with col1:
        st.write(f"{row[0]}")
    with col2:
        st.write(f"{row[1]}")
    with col3:
        st.write(f"{row[6]}")
        # st.write(f"{row}")