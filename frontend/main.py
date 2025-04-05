import streamlit as st
import requests


# Set FastAPI URL
API_BASE_URL = "http://127.0.0.1:8000"


st.title("Mini Manus")

st.subheader("An AI Research Assistant")

st.divider()

years_quarters_list = ['2024 Q4', '2024 Q3', '2024 Q2', '2024 Q1', 
                '2023 Q4', '2023 Q3', '2023 Q2', '2023 Q1',
                '2022 Q4', '2022 Q3', '2022 Q2', '2022 Q1',
                '2021 Q4', '2021 Q3', '2021 Q2', '2021 Q1',
                '2020 Q4', '2020 Q3', '2020 Q2', '2020 Q1']

years_quarters = st.multiselect("Select the years and quarters", years_quarters_list)

agents_list = ['RAG Agent', 'Snowflake Agent', 'Web Search Agent']
agents_names = st.multiselect("Select the agents", agents_list)

question = st.text_input("Enter a query to get report")

if st.button("Get the Reasearch Report") and question:

    params = {"question": question, "agents_names": agents_names, "years_quarters": years_quarters}
    response = requests.get(f"{API_BASE_URL}/ask_question", params=params)

    st.write(response.json())
