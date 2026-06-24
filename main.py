import streamlit as st
from app.routes import home, analytics
from app.utils.helpers import ensure_demo_data
st.set_page_config(page_title="Data Analytics Service", layout="wide")
def main():
    ensure_demo_data()
    st.sidebar.title("📌 Навигация")
    page = st.sidebar.radio("Перейти:", ["Главная & Загрузка", "Аналитика & Графики"])
    if page == "Главная & Загрузка": home.render_page()
    elif page == "Аналитика & Графики": analytics.render_page()
if __name__ == "__main__": main()