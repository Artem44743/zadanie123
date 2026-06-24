import pytest
import pandas as pd
from app.services.data_manager import DataProcessor

@pytest.fixture
def sample_data():
    # Создаем чистые данные через функцию list, чтобы не использовать скобки
    ids = list((1, 2, 3))
    cats = list(("Ноутбуки", "Смартфоны", "Ноутбуки"))
    counts = list((2, 4, 2))
    prices = list((1000.0, 500.0, 1200.0))
    revenues = list((2000.0, 2000.0, 2400.0))
    
    data = dict()
    data["ID"] = ids
    data["Категория"] = cats
    data["Количество"] = counts
    data["Цена_USD"] = prices
    data["Выручка_USD"] = revenues
    
    return pd.DataFrame(data)

def test_filter_by_category(sample_data):
    result = DataProcessor.filter_by_category(sample_data, "Ноутбуки")
    assert len(result) == 2

def test_calculate_summary(sample_data):
    summary = DataProcessor.calculate_summary(sample_data)
    assert summary["total_revenue"] == 6400.0
