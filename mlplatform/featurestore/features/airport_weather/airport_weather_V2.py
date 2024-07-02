from mlplatform.featurestore.features.entities import airport_entity

from snowflake.ml.feature_store import FeatureView


def airport_weather_transform(session):
    '''
    Calculate the average rain in the last 30 and 60 minutes for each airport
    '''

    airport_weather_station_df = session.table("AIRLINE_FEATURE_STORE.FEATURE_STORE.AIRPORT_WEATHER_STATION")

    transformed_airport_weather_station_df = airport_weather_station_df.analytics.moving_agg(
        aggs={"RAIN_MM_H": ["AVG"]},
        window_sizes=[30, 60, 120],
        group_by=["AIRPORT_ZIP_CODE"],
        order_by=["AIRPORT_ZIP_CODE", "DATETIME_UTC"],
    ).select(
        "DATETIME_UTC",
        "AIRPORT_ZIP_CODE",
        "RAIN_MM_H_AVG_30",
        "RAIN_MM_H_AVG_60",
        "RAIN_MM_H_AVG_120"
    )

    return transformed_airport_weather_station_df

def create_airport_weather_feature_view(session):

    airport_weather_fv = FeatureView(
        name="AIRPORT_WEATHER",
        feature_df=airport_weather_transform(session),
        timestamp_col = 'DATETIME_UTC',
        entities = [airport_entity],
        refresh_freq="30 minutes"
    )
    return airport_weather_fv
