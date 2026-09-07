import pytest
from shared.environments import get_environment


def test_defaults_to_prod_when_env_unset(monkeypatch):
    monkeypatch.delenv("ENV", raising=False)
    env = get_environment()
    assert env.name == "prod"
    assert env.base_url == "https://www.saucedemo.com/"


def test_env_variable_selects_staging(monkeypatch):
    monkeypatch.setenv("ENV", "staging")
    env = get_environment()
    assert env.name == "staging"
    assert env.default_timeout == 15


def test_env_lookup_is_case_insensitive(monkeypatch):
    monkeypatch.setenv("ENV", "STAGING")
    assert get_environment().name == "staging"


def test_unknown_environment_raises_value_error(monkeypatch):
    monkeypatch.setenv("ENV", "not_a_real_env")
    with pytest.raises(ValueError, match="Unknown ENV"):
        get_environment()
