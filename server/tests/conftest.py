"""Pytest fixtures for the site-wide search integration tests.

These tests run against the real Docker Postgres (spec A11): tsvector / pg_trgm /
GIN are the feature under test, so SQLite is intentionally NOT used. The
``search_index`` table is assumed to be already populated.

The ``TestClient`` is created WITHOUT a ``with`` block on purpose so the app
lifespan does not run (the lifespan calls ``update_content()`` which would
re-import all content). Starlette's ``TestClient`` still drives the async event
loop and the app's async engine connects to the container Postgres.
"""

import pytest
from fastapi.testclient import TestClient

from sni.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)
