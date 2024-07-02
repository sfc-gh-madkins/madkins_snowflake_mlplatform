from mlplatform.featurestore.features.entities import airport_entity

from snowflake.ml.feature_store import FeatureView

from snowflake.snowpark import DataFrame, Window
from snowflake.snowpark.functions import avg


def airport_weather_transform(airport_weather_station_df: DataFrame):
    '''
    Calculate the average rain in the last 30 and 60 minutes for each airport
    '''

    window = Window.partition_by("AIRPORT_ZIP_CODE").order_by("DATETIME_UTC").rows_between(-29, Window.CURRENT_ROW)
    window2 = Window.partition_by("AIRPORT_ZIP_CODE").order_by("DATETIME_UTC").rows_between(-59, Window.CURRENT_ROW)
    transformed_airport_weather_station_df = airport_weather_station_df.select(
        "DATETIME_UTC",
        "AIRPORT_ZIP_CODE",
        avg("RAIN_MM_H").over(window).alias("AVG30MIN_RAIN_MM_H"),
        avg("RAIN_MM_H").over(window2).alias("AVG60MIN_RAIN_MM_H")
    )

    return transformed_airport_weather_station_df

def create_airport_weather_feature_view(session):

    airport_weather_station_df = session.table("AIRLINE_FEATURE_STORE.FEATURE_STORE.AIRPORT_WEATHER_STATION")

    airport_weather_fv = FeatureView(
        name="AIRPORT_WEATHER",
        feature_df=airport_weather_transform(airport_weather_station_df),
        timestamp_col = 'DATETIME_UTC',
        entities = [airport_entity],
        refresh_freq="30 minutes"
    )
    return airport_weather_fv
