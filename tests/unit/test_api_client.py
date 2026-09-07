from unittest.mock import MagicMock

from api_tests.api_client import ApiClient, API_BASE_URL


def test_default_base_url_and_auth_header():
    client = ApiClient()
    assert client.base_url == API_BASE_URL
    assert client.session.headers["x-api-key"] == "reqres-free-v1"


def test_custom_base_url_is_respected():
    client = ApiClient(base_url="https://example.test/api")
    assert client.base_url == "https://example.test/api"


def test_get_builds_full_url_against_base():
    client = ApiClient()
    client.session.get = MagicMock()

    client.get("/users/2", params={"page": 1})

    client.session.get.assert_called_once_with("https://reqres.in/api/users/2", params={"page": 1})


def test_post_sends_json_payload_to_full_url():
    client = ApiClient()
    client.session.post = MagicMock()
    payload = {"name": "Funmilola Olorode", "job": "QA Engineer"}

    client.post("/users", json=payload)

    client.session.post.assert_called_once_with("https://reqres.in/api/users", json=payload)
