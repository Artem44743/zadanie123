import streamlit as st
from app.services.data_manager import DataProcessor
def render_page():
    st.title("📊 Загрузка данных")
    df = DataProcessor.load_data("data/mock_data.csv")
    st.session_state["dataset"] = df
    st.dataframe(df)