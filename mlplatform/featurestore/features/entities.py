from snowflake.ml.feature_store import Entity

airport_entity = Entity(name="AIRPORT_ZIP_CODE", join_keys=["AIRPORT_ZIP_CODE"])
plane_entity = Entity(name="PLANE_MODEL", join_keys=["PLANE_MODEL"])
