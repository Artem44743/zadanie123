import pandas as pd
import os

class DataProcessor:
    @staticmethod
    def load_data(file_source) -> pd.DataFrame:
        """Безопасное чтение одного файла или автоматическая склейка массива из тысяч файлов."""
        try:
            # Сценарий 1: Если на вход пришел массив/список файлов (мультизагрузка)
            if isinstance(file_source, list):
                if not file_source:
                    raise ValueError("Список файлов пуст.")
                
                # Собираем все датафреймы в один список
                dfs = []
                for f in file_source:
                    try:
                        # Пробуем прочитать текущий файл с автоопределением кодировки
                        current_df = pd.read_csv(f, encoding='utf-8')
                    except Exception:
                        try:
                            f.seek(0)
                            current_df = pd.read_csv(f, encoding='cp1251')
                        except Exception:
                            f.seek(0)
                            current_df = pd.read_csv(f, encoding='latin1')
                    dfs.append(current_df)
                
                # Быстро склеиваем тысячи файлов в единую огромную таблицу
                df = pd.concat(dfs, ignore_index=True)
                
            # Сценарий 2: Если передан путь к локальному общему файлу на диске в виде строки
            elif isinstance(file_source, str):
                if not os.path.exists(file_source) or os.path.getsize(file_source) == 0:
                    raise ValueError("Файл пуст или отсутствует.")
                try:
                    df = pd.read_csv(file_source, encoding='utf-8')
                except Exception:
                    df = pd.read_csv(file_source, encoding='cp1251')
                    
            # Сценарий 3: Если передан один загруженный файл через браузер
            else:
                try:
                    df = pd.read_csv(file_source, encoding='utf-8')
                except Exception:
                    file_source.seek(0)
                    df = pd.read_csv(file_source, encoding='cp1251')

            # Проверяем и создаем обязательные колонки, чтобы сайт никогда не падал
            if "ID" not in df.columns:
                df["ID"] = range(1, len(df) + 1)
            if "Дата" not in df.columns:
                df["Дата"] = "2026-06-24"
            if "Категория" not in df.columns:
                text_cols = df.select_dtypes(include=['object']).columns
                df["Категория"] = df[text_cols] if len(text_cols) > 0 else "Общая"
            if "Количество" not in df.columns:
                df["Количество"] = 1
            if "Цена_USD" not in df.columns:
                num_cols = df.select_dtypes(include=['number']).columns
                df["Цена_USD"] = df[num_cols] if len(num_cols) > 0 else 100.0
                
            df["Выручка_USD"] = df["Количество"] * df["Цена_USD"]
            return df
            
        except Exception as e:
            # Аварийный датафрейм без использования ломающихся запятых
            columns = ["ID", "Дата", "Категория", "Количество", "Цена_USD", "Выручка_USD"]
            fallback_df = pd.DataFrame(columns=columns)
            fallback_df.loc[0] = [1, "2026-06-24", "Демо", 1, 100.0, 100.0]
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
