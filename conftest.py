import pytest
from accounts.models import User
from rest_framework.test import APIClient
from test_data import test_data


@pytest.fixture(autouse=True)
def populate_db_with_test_data():
    """Adds test data to the database."""

    for model, values in test_data.items():
        for data in values:
            model(**data).save()


@pytest.fixture
def worker_1():
    """
    Provides logged user with worker status
    """
    user = User.objects.get(username="tom_hagen")
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.fixture
def worker_2():
    """
    Provides logged user with worker status
    """
    user = User.objects.get(username="luca_brasi")
    client = APIClient()
    client.force_authenticate(user)
    return client
