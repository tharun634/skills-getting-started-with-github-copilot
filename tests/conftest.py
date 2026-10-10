from copy import deepcopy
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def client():
    with TestClient(app_module.app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def restore_activities():
    original_activities = deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original_activities)


@pytest.fixture
def activity_url():
    def build_url(activity_name):
        return f"/activities/{quote(activity_name, safe='')}/signup"

    return build_url
