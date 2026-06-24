import pandas as pd
import os

class DataProcessor:
    @staticmethod
    def load_data(file) -> pd.DataFrame:
        """Та самая первая логика: берет столбцы из CSV и записывает их на сайт строками."""
        try:
            # Читаем файл в зависимости от того, путь это или объект из браузера
            if isinstance(file, str):
                raw_df = pd.read_csv(file, sep=None, engine='python')
            else:
                raw_df = pd.read_csv(file, sep=None, engine='python')
                
            # Извлекаем все столбцы из загруженного файла
            columns_list = list(raw_df.columns)
            
            # Строим итоговую таблицу, записывая столбцы в виде строк
            df = pd.DataFrame()
            df["ID"] = range(1, len(columns_list) + 1)
            df["Дата"] = "2026-06-24"
            df["Категория"] = columns_list
            df["Количество"] = 1
            df["Цена_USD"] = 100.0
            df["Выручка_USD"] = df["Количество"] * df["Цена_USD"]
            
            return df
        except Exception as e:
            # Если файл пустой, создаем простую чистую заглушку
            fallback_df = pd.DataFrame()
            fallback_df["ID"] = range(1, 6)
            fallback_df["Дата"] = "2026-06-24"
            fallback_df["Категория"] = "Демо-товар"
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
