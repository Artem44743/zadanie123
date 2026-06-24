import streamlit as st
import os
from app.services.data_manager import DataProcessor
from app.utils.helpers import ensure_demo_data

def render_page():
    st.title("📊 Импорт данных из таблицы-реестра")
    st.markdown("Модуль импорта: загрузите вашу общую таблицу, и данные из неё автоматически запишутся на сайт.")

    source = st.radio("Выберите источник данных:", ["Актуальная база сайта", "Импортировать новую таблицу CSV"])
    filepath = "data/mock_data.csv"
    
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        ensure_demo_data()
        
    try:
        df = DataProcessor.load_data(filepath)
    except Exception:
        ensure_demo_data()
        df = DataProcessor.load_data(filepath)

    if source == "Актуальная база сайта":
        st.success(f"Отображаются актуальные записанные данные ({len(df)} записей).")
    else:
        # Компонент принимает одну главную таблицу-реестр
        uploaded_file = st.file_uploader(
            "Выберите файл таблицы CSV для записи на сайт", 
            type=["csv"], 
            accept_multiple_files=False
        )
        
        if uploaded_file is not None:
            try:
                # Читаем и обрабатываем строки из загруженной таблицы
                new_df = DataProcessor.load_data(uploaded_file)
                
                # Физически записываем и сохраняем эти данные в систему сайта
                os.makedirs("data", exist_ok=True)
                new_df.to_csv(filepath, index=False, encoding="utf-8")
                
                st.success(f"🚀 Данные из таблицы успешно записаны на сайт! Всего импортировано строк: {len(new_df)}")
                st.rerun()
            except Exception as e:
                st.error(f"Ошибка при записи таблицы на сайт: {e}")

    if df is not None:
        st.session_state["dataset"] = df
        st.subheader("📋 Текущая таблица исходных данных на сайте")
        st.dataframe(df, use_container_width=True)
