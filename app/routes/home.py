import streamlit as st
import os
import subprocess
from app.services.data_manager import DataProcessor

def run_git_push():
    """Автоматически делает коммит и пуш изнутри работающего сайта."""
    try:
        # 1. Добавляем файл данных в индекс Git
        subprocess.run(["git", "add", "data/mock_data.csv"], check=True, capture_output=True, text=True)
        
        # 2. Делаем коммит изменений
        commit_msg = "data: Динамическое обновление общей базы данных через веб-интерфейс"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True, capture_output=True, text=True)
        
        # 3. Отправляем в ваш репозиторий на GitHub
        result = subprocess.run(["git", "push"], check=True, capture_output=True, text=True)
        return True, "Успешно отправлено на GitHub!"
    except subprocess.CalledProcessError as e:
        # Если нечего коммитить или произошла ошибка сети
        error_msg = e.stderr if e.stderr else str(e)
        if "nothing to commit" in error_msg or "up-to-date" in error_msg:
            return True, "Данные на GitHub уже соответствуют локальным!"
        return False, f"Ошибка Git: {error_msg}"
    except Exception as e:
        return False, f"Системная ошибка: {str(e)}"

def render_page():
    st.title("📊 Загрузка и обзор данных")
    st.markdown("Синхронный модуль: вы можете обновить базу локально или отправить её напрямую на удаленный хостинг GitHub.")

    source = st.radio("Выберите источник данных:", ["Актуальная общая база", "Загрузить новую общую таблицу CSV"])
    filepath = "data/mock_data.csv"
    
    df = DataProcessor.load_data(filepath) if os.path.exists(filepath) else None

    if source == "Актуальная общая база":
        if df is not None:
            st.success(f"Отображаются актуальные локальные данные ({len(df)} записей).")
            
            # --- КНОПКА ЗАПИСИ НА ГИТХАБ ---
            st.markdown("---")
            st.subheader("🌐 Синхронизация с хостингом")
            st.info("Нажмите кнопку ниже, чтобы сохранить текущую таблицу на GitHub для всех удаленных пользователей.")
            
            if st.button("💾 Зафиксировать и отправить изменения на GitHub", type="primary"):
                with st.spinner("Отправка данных на сервера GitHub..."):
                    success, message = run_git_push()
                    if success:
                        st.success(f"🎉 {message}")
                    else:
                        st.error(f"❌ {message}")
            st.markdown("---")
            
        else:
            st.warning("Общая база еще не создана. Загрузите файл во второй вкладке.")
    else:
        uploaded_file = st.file_uploader("Выберите новый CSV-файл (он перезапишет локальную базу)", type=["csv"])
        if uploaded_file is not None:
            try:
                temp_df = DataProcessor.load_data(uploaded_file)
                
                os.makedirs("data", exist_ok=True)
                uploaded_file.seek(0)
                with open(filepath, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.success("🚀 Локальная база успешно обновлена! Перейдите на вкладку 'Актуальная общая база', чтобы отправить её на хостинг.")
                df = DataProcessor.load_data(filepath)
                st.session_state["dataset"] = df
                st.rerun()
            except Exception as e:
                st.error(f"Ошибка при обработке файла: {e}")

    if df is not None:
        st.session_state["dataset"] = df
        st.subheader("📋 Таблица исходных данных")
        st.dataframe(df, use_container_width=True)
