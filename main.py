import os
import sys

# Принудительно исправляем пути для Windows, чтобы не было ошибки Not Found
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
from app.routes import home, analytics
from app.utils.helpers import ensure_demo_data

# Конфигурация страницы веб-интерфейса Streamlit
st.set_page_config(
    page_title="Сервис бизнес-аналитики",
    page_icon="📊",
    layout="wide"
)

def main():
    # Проверяем и генерируем демо-данные (30 строк) при первом запуске
    ensure_demo_data()
    
    # Создаем удобную навигацию на русском языке в боковой панели
    st.sidebar.title("📌 Навигация")
    page = st.sidebar.radio("Перейти на страницу:", ["Главная & Загрузка", "Аналитика & Графики"])
    
    st.sidebar.markdown("---")
    st.sidebar.info("Экзаменационный проект по дисциплине «Разработка программных модулей»")

    # Маршрутизация страниц приложения
    if page == "Главная & Загрузка":
        home.render_page()
    elif page == "Аналитика & Графики":
        analytics.render_page()

if __name__ == "__main__":
    import streamlit.web.cli as stcli
    if not os.environ.get("STREAMLIT_RUN_AS_MODULE"):
        os.environ["STREAMLIT_RUN_AS_MODULE"] = "1"
        
        # Конфигурируем запуск: отключаем developmentMode и открываем доступ для всей сети (0.0.0.0)
        sys.argv = [
            "streamlit", "run", __file__, 
            "--global.developmentMode", "false",
            "--server.port", "9999", 
            "--server.address", "0.0.0.0"
        ]
        sys.exit(stcli.main())
    main()
