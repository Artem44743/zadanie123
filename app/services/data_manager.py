import pandas as pd
import os

class DataProcessor:
    @staticmethod
    def load_data(file) -> pd.DataFrame:
        """Прямое чтение файла с диска без кэширования для синхронизации всех юзеров."""
        try:
            # Если передана строка (путь к файлу), проверяем время изменения
            if isinstance(file, str):
                # Читаем файл напрямую, чтобы всегда видеть свежие данные
                df = pd.read_csv(file)
            else:
                # Если передан загруженный объект file_uploader
                df = pd.read_csv(file)
                
            required_cols = ["ID", "Дата", "Категория", "Количество", "Цена_USD", "Выручка_USD"]
            if not all(col in df.columns for col in required_cols):
                if "Количество" in df.columns and "Цена_USD" in df.columns:
                    df["Выручка_USD"] = df["Количество"] * df["Цена_USD"]
                else:
                    raise ValueError("Неверная структура файла. Отсутствуют обязательные колонки.")
            return df
        except Exception as e:
            raise RuntimeError(f"Ошибка при чтении файла: {str(e)}")

    @staticmethod
    def filter_by_category(df: pd.DataFrame, category: str) -> pd.DataFrame:
        if category == "Все категории":
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
