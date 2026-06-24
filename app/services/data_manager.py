import pandas as pd
class DataProcessor:
    @staticmethod
    def load_data(file):
        df = pd.read_csv(file)
        if "Количество" in df.columns and "Цена_USD" in df.columns:
            df["Выручка_USD"] = df["Количество"] * df["Цена_USD"]
        return df
    @staticmethod
    def filter_by_category(df, cat):
        return df if cat == "Все категории" else df[df["Категория"] == cat]
    @staticmethod
    def calculate_summary(df):
        if df.empty: return {"total_revenue": 0.0}
        return {"total_revenue": float(df["Выручка_USD"].sum()), "total_items": int(df["Количество"].sum()), "avg_price": float(df["Цена_USD"].mean())}