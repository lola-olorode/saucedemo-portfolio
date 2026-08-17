"""Minimal API client wrapper around requests.

Keeps HTTP calls and base-URL/header setup in one place, same rationale
as the Page Object Model on the UI side — tests describe *what* they're
checking, not how the request is built.
"""

import requests

API_BASE_URL = "https://reqres.in/api"


class ApiClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"x-api-key": "reqres-free-v1"})

    def get(self, path: str, **kwargs):
        return self.session.get(f"{self.base_url}{path}", **kwargs)

    def post(self, path: str, json=None, **kwargs):
        return self.session.post(f"{self.base_url}{path}", json=json, **kwargs)

    def put(self, path: str, json=None, **kwargs):
        return self.session.put(f"{self.base_url}{path}", json=json, **kwargs)

    def delete(self, path: str, **kwargs):
        return self.session.delete(f"{self.base_url}{path}", **kwargs)
