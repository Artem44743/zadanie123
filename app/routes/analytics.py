import streamlit as st
import plotly.express as px
from app.services.data_manager import DataProcessor
def render_page():
    st.title("📈 Аналитика")
    if "dataset" not in st.session_state: return
    df = st.session_state["dataset"]
    cats = ["Все категории"] + list(df["Категория"].unique())
    sc = st.selectbox("Категория:", cats)
    f_df = DataProcessor.filter_by_category(df, sc)
    s = DataProcessor.calculate_summary(f_df)
    st.metric("Выручка", f"${s["total_revenue"]:.2f}")
    st.plotly_chart(px.line(f_df, x="Дата", y="Выручка_USD"))