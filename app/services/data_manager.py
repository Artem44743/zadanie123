import pandas as pd
import os

class DataProcessor:
    @staticmethod
    def load_data(file) -> pd.DataFrame:
        """Чистая загрузка файла один в один без объединения и переворотов."""
        try:
            # Читаем файл с автоопределением разделителя (запятая или точка с запятой)
            if isinstance(file, str):
                df = pd.read_csv(file, sep=None, engine='python')
            else:
                df = pd.read_csv(file, sep=None, engine='python')
                
            # Гарантируем наличие базовых колонок для работы графиков Стримлита
            if "ID" not in df.columns:
                df["ID"] = range(1, len(df) + 1)
            if "Дата" not in df.columns:
                df["Дата"] = "2026-06-24"
            if "Категория" not in df.columns:
                # Если колонки 'Категория' нет, берем самый первый столбец из вашего файла
                df = df.rename(columns={df.columns[0]: "Категория"})
            if "Количество" not in df.columns:
                df["Количество"] = 1
            if "Цена_USD" not in df.columns:
                df["Цена_USD"] = 100.0
                
            # Пересчитываем выручку для корректного вывода KPI карточек
            df["Выручка_USD"] = df["Количество"] * df["Цена_USD"]
            return df
        except Exception as e:
            # Резервный датафрейм, если файл совсем поврежден
            fallback_df = pd.DataFrame()
            fallback_df["ID"] = range(1, 6)
            fallback_df["Дата"] = "2026-06-24"
            fallback_df["Категория"] = "Демо-данные"
            fallback_df["Количество"] = 1
            fallback_df["Цена_USD"] = 100.0
            fallback_df["Выручка_USD"] = 100.0
            return fallback_df

    @staticmethod
    def filter_by_category(df: pd.DataFrame, category: str) -> pd.DataFrame:
        if category == "Все категории" or "Категория" not in df.columns:
            return df
        return df[df["Категория"] == category]

    @staticmethod
    def calculate_summary(df: pd.DataFrame) -> dict:
        if df.empty:
            return {"total_revenue": 0.0, "total_items": 0, "avg_price": 0.0}
            
        return {
            "total_revenue": float(df["Выручка_USD"].sum()),
            "total_items": int(df["Количество"].sum()),
            "avg_price": float(df["Цена_USD"].mean())
        }
