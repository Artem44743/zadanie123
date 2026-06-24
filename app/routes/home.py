import streamlit as st
import os
from app.services.data_manager import DataProcessor

def render_page():
    st.title("📊 Загрузка и обзор данных")
    st.markdown("Добро пожаловать в модуль аналитики. Изменения, внесенные сюда, увидят все пользователи сети!")

    source = st.radio("Выберите источник данных:", ["Текущая общая база данных", "Загрузить новую общую таблицу CSV"])
    
    filepath = "data/mock_data.csv"
    df = None

    if source == "Текущая общая база данных":
        if os.path.exists(filepath):
            df = DataProcessor.load_data(filepath)
            st.success(f"Отображаются актуальные общие данные ({len(df)} записей).")
        else:
            st.warning("Общая база данных еще не создана. Переключитесь на пункт загрузки ниже.")
    else:
        uploaded_file = st.file_uploader("Выберите новый CSV-файл (он обновит данные для всех пользователей)", type=["csv"])
        if uploaded_file is not None:
            try:
                # Безопасно проверяем структуру загруженного файла
                temp_df = DataProcessor.load_data(uploaded_file)
                
                # ЖЕСТКО СОХРАНЯЕМ ФАЙЛ НА ДИСК (Перезаписываем базу для всех)
                os.makedirs("data", exist_ok=True)
                uploaded_file.seek(0)  # Сбрасываем указатель файла
                with open(filepath, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.success(f"🚀 База данных успешно обновлена на сервере для всех пользователей! Найдено {len(temp_df)} строк.")
                df = temp_df
                
                # Кнопка для принудительного сброса кэша сайта
                st.button("🔄 Обновить интерфейс сайта")
            except Exception as e:
                st.error(f"Ошибка при обработке файла: {e}")
        else:
            st.info("Пожалуйста, выберите файл, чтобы обновить общую базу.")

    # Сохраняем результат в сессию и выводим на экран
    if df is not None:
        st.session_state["dataset"] = df
        st.subheader("📋 Таблица исходных данных (Общий просмотр)")
        st.dataframe(df, use_container_width=True)
