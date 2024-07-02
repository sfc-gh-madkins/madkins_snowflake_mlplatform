from mlplatform.featurestore.features.entities import plane_entity

from snowflake.ml.feature_store import FeatureView

from snowflake.snowpark.functions import col


def create_airport_weather_feature_view(session):

    plane_attributes_df = session.table(
        'AIRLINE_FEATURE_STORE.FEATURE_STORE.PLANE_MODEL_ICEBERG'
    ).select(
        col('PLANE_MODEL'),
        col('SEATING_CAPACITY')
    )

    plane_attributes_fv = FeatureView(
        name="PLANE_FEATURES",
        feature_df=plane_attributes_df,
        entities = [plane_entity],
    )
    return plane_attributes_fv
