from snowflake.ml.feature_store import FeatureStore, CreationMode
from snowflake.snowpark import DataFrame, Session
from snowflake.ml.registry import Registry

from snowflake.ml.version import VERSION



def predict(session: Session, spine_table_name: str):
    """"
    fs = FeatureStore(
        session=session,
        database="AIRLINE_FEATURE_STORE",
        name="FEATURE_STORE",
        default_warehouse=session.get_current_warehouse(),
    )

    mr = Registry(
        session=session,
        database_name="AIRLINE_FEATURE_STORE",
        schema_name="FEATURE_STORE",
    )

    model = mr.get_model("WEATHER_DELAY").version("V2")
    dataset = model.lineage(domain_filter=["dataset"], direction="upstream")[0]

    feature_df = fs.retrieve_feature_values(
        spine_df=session.table(spine_table_name),
        features=fs.load_feature_views_from_dataset(dataset),
        spine_timestamp_col=dataset.selected_version._get_metadata().properties.spine_timestamp_col,
    )

    prediction_df = model.run(feature_df, function_name='predict_proba')

    return prediction_df
    """
    return VERSION #prediction_df
