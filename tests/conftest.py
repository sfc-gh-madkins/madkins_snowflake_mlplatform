from datetime import datetime
import pytest
import os
import uuid

from snowflake.snowpark.session import Session


CONNECTION_PARAMETERS = {
    'ACCOUNT': os.environ['SNOWFLAKE_ACCOUNT'],
    'USER': os.environ['SNOWFLAKE_USER'],
    'PASSWORD': os.environ['SNOWFLAKE_PASSWORD'],
}

DATABASE = f"SNOWFLAKE_MLPLATFORM_TEST_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4()}"


def pytest_sessionstart(session):
    print("Pytest session is starting...")
    session = Session.builder.configs(CONNECTION_PARAMETERS).create()
    session.sql(f"CREATE DATABASE {DATABASE}").collect()


def pytest_sessionfinish(session, exitstatus):
    print(f"Pytest session finished with exit status: {exitstatus}")
    session = Session.builder.configs(CONNECTION_PARAMETERS).create()
    session.sql(f"DROP DATABASE {DATABASE}").collect()


@pytest.fixture(scope='module')
def session() -> Session:
    session = Session.builder.configs(CONNECTION_PARAMETERS).create()
    session.sql(f"USE DATABASE {DATABASE}").collect()
    return session
