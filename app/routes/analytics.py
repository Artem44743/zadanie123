import streamlit as st
import plotly.express as px
from app.services.data_manager import DataProcessor

def render_page():
    st.title("📈 Аналитический дашборд")

    if "dataset" not in st.session_state:
        st.warning("⚠️ Данные не найдены! Сначала загрузите их на вкладке 'Главная & Загрузка'.")
        return

    df = st.session_state["dataset"]

    st.subheader("🎛️ Настройка фильтров")
    categories = ["Все категории"] + list(df["Категория"].unique())
    selected_category = st.selectbox("Выберите категорию для анализа:", categories)
    
    filtered_df = DataProcessor.filter_by_category(df, selected_category)

    summary = DataProcessor.calculate_summary(filtered_df)
    
    # Русский перевод карточек показателей
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Общая выручка", value=f"${summary.get('total_revenue', 0.0):.2f}")
    with col2:
        st.metric(label="Продано товаров", value=f"{summary.get('total_items', 0):,} шт.")
    with col3:
        st.metric(label="Средняя цена товара", value=f"${summary.get('avg_price', 0.0):.2f}")

    if filtered_df.empty:
        st.error("Нет данных для отображения графиков по выбранным фильтрам.")
        return

    st.markdown("---")
    st.subheader("📊 Визуализация показателей")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("**График 1: Динамика выручки во времени**")
        fig1 = px.line(
            filtered_df.sort_values("Дата"), 
            x="Дата", 
            y="Выручка_USD", 
            labels={"Дата": "Дата продажи", "Выручка_USD": "Выручка ($)"},
            markers=True
        )
        st.plotly_chart(fig1, use_container_width=True)

    with chart_col2:
        st.markdown("**График 2: Доля категорий в общих продажах**")
        fig2 = px.pie(
            filtered_df, 
            names="Категория", 
            values="Выручка_USD", 
            labels={"Категория": "Категория товара", "Выручка_USD": "Выручка ($)"},
            hole=0.3
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("💾 Сохранение отчетов")
    csv_to_download = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Скачать текущий отфильтрованный отчет в CSV",
        data=csv_to_download,
        file_name="analiticheskiy_otchet.csv",
        mime="text/csv"
    )
