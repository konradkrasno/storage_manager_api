import pytest
from test_data import test_data


@pytest.fixture(autouse=True)
def populate_db_with_test_data():
    """Adds test data to the database."""

    for model, values in test_data.items():
        for data in values:
            model(**data).save()
