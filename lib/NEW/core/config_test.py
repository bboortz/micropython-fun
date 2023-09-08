
import pytest
import asyncio

from core.core import Core
from core.config import Config, ConfigException


def test_get_config():
    attr = Config.get("STAGE")
    assert attr == "dev"


def test_set_config():
    Config.set("BOOT_BUTTON", 0)
    attr = Config.get("BOOT_BUTTON")
    assert attr == 0


def test_load_config():
    Config.load('./config_test.json')
    attr = Config.get("STAGE")
    Config.print()
    assert attr == "test"
    attr = Config.get("WDT_TIMEOUT_MS")
    assert attr == 5000


def test_attr_not_found():
    c = Core()
    with pytest.raises(ConfigException):
        attr = Config.get("UNKNOWN_ATTR")
