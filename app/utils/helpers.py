import os
import pandas as pd
import numpy as np
def ensure_demo_data():
    os.makedirs("data", exist_ok=True)
    file_path = "data/mock_data.csv"
    if not os.path.exists(file_path):
        np.random.seed(42)
        df = pd.DataFrame({"ID": range(1, 31), "Дата": pd.date_range("2026-01-01", periods=30).strftime("%Y-%m-%d"), "Категория": np.random.choice(["Смартфоны", "Ноутбуки"], size=30), "Количество": np.random.randint(1, 10, size=30), "Цена_USD": np.random.randint(50, 1200, size=30).astype(float)})
        df["Выручка_USD"] = df["Количество"] * df["Цена_USD"]
        df.to_csv(file_path, index=False, encoding="utf-8")