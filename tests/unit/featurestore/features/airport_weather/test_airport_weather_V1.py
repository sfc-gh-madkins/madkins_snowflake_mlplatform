from decimal import Decimal
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pytest

from snowflake.snowpark import Row

from mlplatform.featurestore.features.airport_weather.airport_weather_V1 import airport_weather_transform


@pytest.mark.unit
def test_airport_weather_transform(session):

    np.random.seed(42)
    df = pd.DataFrame({
        'DATETIME_UTC': np.repeat([datetime(2023, 1, 1, 0, 0, 0) + timedelta(minutes=i) for i in range(100)], 2),
        'AIRPORT_ZIP_CODE': np.tile(['12345', '67890'], 100),
        'RAIN_MM_H': np.random.randint(1, 11, 200)
    })

    actual_spdf = airport_weather_transform(session.create_dataframe(df))

    expected_spdf = session.create_dataframe([
        Row(DATETIME_UTC=datetime(2023, 1, 1, 1, 35), AIRPORT_ZIP_CODE='12345', AVG30MIN_RAIN_MM_H=Decimal('5.333'), AVG60MIN_RAIN_MM_H=Decimal('5.433')),
        Row(DATETIME_UTC=datetime(2023, 1, 1, 1, 36), AIRPORT_ZIP_CODE='12345', AVG30MIN_RAIN_MM_H=Decimal('5.500'), AVG60MIN_RAIN_MM_H=Decimal('5.533')),
        Row(DATETIME_UTC=datetime(2023, 1, 1, 1, 37), AIRPORT_ZIP_CODE='12345', AVG30MIN_RAIN_MM_H=Decimal('5.633'), AVG60MIN_RAIN_MM_H=Decimal('5.500')),
        Row(DATETIME_UTC=datetime(2023, 1, 1, 1, 38), AIRPORT_ZIP_CODE='12345', AVG30MIN_RAIN_MM_H=Decimal('5.500'), AVG60MIN_RAIN_MM_H=Decimal('5.433')),
        Row(DATETIME_UTC=datetime(2023, 1, 1, 1, 39), AIRPORT_ZIP_CODE='12345', AVG30MIN_RAIN_MM_H=Decimal('5.366'), AVG60MIN_RAIN_MM_H=Decimal('5.450'))
    ])

    assert actual_spdf.collect()[-5:] == expected_spdf.collect()
