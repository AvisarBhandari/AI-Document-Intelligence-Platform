import importlib

import pytest

from app.core import config as config_module


@pytest.fixture(autouse=True)
def reload_settings_module_after_test():
    yield
    importlib.reload(config_module)


def test_database_url_prefers_database_url(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///preferred.db")
    monkeypatch.setenv("URL_DATABASE", "sqlite:///legacy.db")

    reloaded_config = importlib.reload(config_module)

    assert reloaded_config.settings.DATABASE_URL == "sqlite:///preferred.db"


def test_database_url_falls_back_to_legacy_name(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("URL_DATABASE", "sqlite:///legacy.db")

    reloaded_config = importlib.reload(config_module)

    assert reloaded_config.settings.DATABASE_URL == "sqlite:///legacy.db"
