"""API-layer test suite.

Demonstrates that the framework isn't UI-only — the same pytest/CI setup
covers API contract checks against a public REST test API (reqres.in).
Assertion style mirrors a typical API test framework: status code,
response schema, response time, and header/auth validation per request —
independent of (and much faster than) driving a browser.
"""

import pytest
from api_tests.api_client import ApiClient

MAX_ACCEPTABLE_RESPONSE_TIME_SECONDS = 2.0


@pytest.fixture
def api():
    return ApiClient()


class TestUsersApi:
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_single_user_returns_expected_shape(self, api):
        response = api.get("/users/2")

        # Status
        assert response.status_code == 200

        # Schema / field validation
        body = response.json()
        assert "data" in body
        user = body["data"]
        for field in ("id", "email", "first_name", "last_name", "avatar"):
            assert field in user, f"Missing expected field: {field}"
        assert user["id"] == 2
        assert "@" in user["email"]

        # Headers
        assert response.headers.get("Content-Type", "").startswith("application/json")

        # Response time
        assert response.elapsed.total_seconds() < MAX_ACCEPTABLE_RESPONSE_TIME_SECONDS

    @pytest.mark.api
    def test_get_user_list_is_paginated(self, api):
        response = api.get("/users", params={"page": 1})

        assert response.status_code == 200
        body = response.json()
        for field in ("page", "per_page", "total", "total_pages", "data"):
            assert field in body
        assert body["page"] == 1
        assert len(body["data"]) == body["per_page"]
        assert response.elapsed.total_seconds() < MAX_ACCEPTABLE_RESPONSE_TIME_SECONDS

    @pytest.mark.api
    def test_get_nonexistent_user_returns_404(self, api):
        response = api.get("/users/999")

        assert response.status_code == 404
        assert response.elapsed.total_seconds() < MAX_ACCEPTABLE_RESPONSE_TIME_SECONDS

    @pytest.mark.api
    @pytest.mark.regression
    def test_create_user_returns_201(self, api):
        payload = {"name": "Funmilola Olorode", "job": "QA Engineer"}
        response = api.post("/users", json=payload)

        assert response.status_code == 201
        body = response.json()
        assert body["name"] == payload["name"]
        assert body["job"] == payload["job"]
        assert "id" in body
        assert "createdAt" in body
        assert response.headers.get("Content-Type", "").startswith("application/json")

    @pytest.mark.api
    @pytest.mark.regression
    def test_update_user_returns_200(self, api):
        response = api.put("/users/2", json={"job": "Senior QA Engineer"})

        assert response.status_code == 200
        body = response.json()
        assert body["job"] == "Senior QA Engineer"
        assert "updatedAt" in body

    @pytest.mark.api
    def test_delete_user_returns_204(self, api):
        response = api.delete("/users/2")

        assert response.status_code == 204
        assert response.text == ""  # 204 No Content should have an empty body

    @pytest.mark.api
    @pytest.mark.regression
    def test_missing_api_key_is_rejected(self, api):
        """Auth/header validation: requests without the required
        x-api-key header should be rejected, not silently succeed."""
        unauthenticated_response = api.session.get(
            f"{api.base_url}/users/2",
            headers={"x-api-key": ""},
        )
        assert unauthenticated_response.status_code in (401, 403)

