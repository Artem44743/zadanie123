import pytest
import pandas as pd
from app.services.data_manager import DataProcessor
def test_filter():
    df = pd.DataFrame({"Категория": ["А", "Б"], "Выручка_USD":})
    assert len(DataProcessor.filter_by_category(df, "А")) == 1