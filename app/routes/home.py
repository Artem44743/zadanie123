import streamlit as st
import os
from app.services.data_manager import DataProcessor
from app.utils.helpers import ensure_demo_data

def render_page():
    st.title("📊 Загрузка и обзор данных")
    st.markdown("Модуль массовой загрузки: вы можете перетащить до 5000 файлов CSV одновременно, и система объединит их.")

    source = st.radio("Выберите источник данных:", ["Актуальная общая база", "Загрузить пачку новых таблиц CSV"])
    filepath = "data/mock_data.csv"
    
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        ensure_demo_data()
        
    try:
        df = DataProcessor.load_data(filepath)
    except Exception:
        ensure_demo_data()
        df = DataProcessor.load_data(filepath)

    if source == "Актуальная общая база":
        st.success(f"Отображаются актуальные объединенные данные ({len(df)} записей).")
    else:
        # Включаем параметр accept_multiple_files=True для загрузки тысяч файлов одновременно
        uploaded_files = st.file_uploader(
            "Перетащите сюда файлы CSV для массового анализа", 
            type=["csv"], 
            accept_multiple_files=True
        )
        
        if uploaded_files: # Если загружен хотя бы один файл из пачки
            try:
                # Обрабатываем и склеиваем всю пачку файлов через наш сервис
                temp_df = DataProcessor.load_data(uploaded_files)
                
                # Перезаписываем единую общую склеенную базу данных на сервере
                os.makedirs("data", exist_ok=True)
                temp_df.to_csv(filepath, index=False, encoding="utf-8")
                
                st.success(f"🚀 Успешно объединено и сохранено {len(uploaded_files)} файлов! Итого строк: {len(temp_df)}")
                st.rerun()
            except Exception as e:
                st.error(f"Ошибка при объединении пакета файлов: {e}")

    if df is not None:
        st.session_state["dataset"] = df
        st.subheader("📋 Таблица исходных данных (Общий просмотр)")
        st.dataframe(df, use_container_width=True)
