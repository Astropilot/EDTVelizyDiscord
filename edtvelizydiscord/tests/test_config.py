import logging

from config import Settings


def test_settings_default() -> None:
    settings = Settings()

    assert settings.check_delay == 900
    assert settings.timeout == 30
    assert settings.log_level == logging.DEBUG
