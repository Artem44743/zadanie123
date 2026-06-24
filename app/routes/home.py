import streamlit as st
import os
from app.services.data_manager import DataProcessor
from app.utils.helpers import ensure_demo_data

def render_page():
    st.title("📊 Загрузка и обзор данных")
    st.markdown("Добро пожаловать в модуль аналитики. Вы можете загрузить свой CSV-файл или использовать демонстрационный.")

    source = st.radio("Выберите источник данных:", ["Демонстрационный файл", "Загрузить свой CSV"])
    filepath = "data/mock_data.csv"
    df = None
    
    if source == "Демонстрационный файл":
        ensure_demo_data()
        df = DataProcessor.load_data(filepath)
        st.success(f"Успешно загружены системные демо-данные ({len(df)} записей).")
    else:
        # Обычная, простая кнопка загрузки одного файла, как было в самом начале
        uploaded_file = st.file_uploader("Выберите CSV файл", type=["csv"])
        if uploaded_file is not None:
            try:
                # Читаем загруженный файл
                temp_df = DataProcessor.load_data(uploaded_file)
                
                # Физически сохраняем его на сайт, перезаписывая старую базу
                os.makedirs("data", exist_ok=True)
                uploaded_file.seek(0)
                with open(filepath, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.success(f"Файл успешно записан на сайт! Найдено {len(temp_df)} строк.")
                df = temp_df
            except Exception as e:
                st.error(f"Ошибка: {e}")
        else:
            st.info("Пожалуйста, загрузите ваш CSV-файл для начала анализа.")

    if df is not None:
        st.session_state["dataset"] = df
        st.subheader("📋 Таблица данных")
        st.dataframe(df, use_container_width=True)
