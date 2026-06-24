import streamlit as st
import os
from app.services.data_manager import DataProcessor
from app.utils.helpers import ensure_demo_data

def render_page():
    st.title("📊 Загрузка и обзор данных")
    st.markdown("Модуль загрузки: выберите ваш CSV-файл, чтобы полностью обновить данные на сайте.")

    source = st.radio("Выберите источник данных:", ["Текущая база данных", "Загрузить новый файл CSV"])
    filepath = "data/mock_data.csv"
    df = None
    
    if source == "Текущая база данных":
        ensure_demo_data()
        df = DataProcessor.load_data(filepath)
        st.success("Отображаются актуальные текущие данные.")
    else:
        # Строго одиночная загрузка одного файла (accept_multiple_files=False)
        uploaded_file = st.file_uploader("Выберите один CSV-файл для полной замены данных", type=["csv"], accept_multiple_files=False)
        if uploaded_file is not None:
            try:
                # Читаем загруженный файл напрямую
                temp_df = DataProcessor.load_data(uploaded_file)
                
                # Полностью перезаписываем файл на сервере (старые данные стираются)
                os.makedirs("data", exist_ok=True)
                uploaded_file.seek(0)
                with open(filepath, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.success("🚀 Данные на сайте успешно заменены на ваш новый файл!")
                df = temp_df
                st.rerun()
            except Exception as e:
                st.error(f"Ошибка при обработке файла: {e}")
        else:
            st.info("Пожалуйста, выберите файл CSV.")

    if df is not None:
        st.session_state["dataset"] = df
        st.subheader("📋 Таблица данных на сайте")
        st.dataframe(df, use_container_width=True)
