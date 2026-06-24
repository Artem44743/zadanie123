import streamlit as st
import os
from app.services.data_manager import DataProcessor
from app.utils.helpers import ensure_demo_data

def render_page():
    st.title("📊 Загрузка и обзор данных")
    st.markdown("Синхронный модуль: любые изменения базы данных мгновенно видны всем пользователям сети.")

    source = st.radio("Выберите источник данных:", ["Актуальная общая база", "Загрузить новую общую таблицу CSV"])
    filepath = "data/mock_data.csv"
    
    # Если файла нет или он сломался на хостинге, принудительно пересоздаем демо-версию
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        ensure_demo_data()
        
    try:
        df = DataProcessor.load_data(filepath)
    except Exception:
        ensure_demo_data()
        df = DataProcessor.load_data(filepath)

    if source == "Актуальная общая база":
        st.success(f"Отображаются актуальные общие данные ({len(df)} записей).")
    else:
        uploaded_file = st.file_uploader("Выберите новый CSV-файл (он обновит данные для всех)", type=["csv"])
        if uploaded_file is not None:
            try:
                temp_df = DataProcessor.load_data(uploaded_file)
                
                os.makedirs("data", exist_ok=True)
                uploaded_file.seek(0)
                with open(filepath, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.success("🚀 База данных успешно обновлена на сервере для всех пользователей!")
                st.rerun()
            except Exception as e:
                st.error(f"Ошибка при обработке файла: {e}")

    if df is not None:
        st.session_state["dataset"] = df
        st.subheader("📋 Таблица исходных данных (Общий просмотр)")
        st.dataframe(df, use_container_width=True)
