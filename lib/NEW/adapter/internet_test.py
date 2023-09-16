
import pytest

from core.config import Config
from adapter.internet import Internet
from adapter.wifi_mock import WifiMock



def test_create_internet():
    i = Internet()


def test_wifi_connect():
    wifi = WifiMock()
    i = Internet(connection = wifi)
    i.connect()
    assert True == i.is_connected()


def test_wifi_connect_disconnect():
    wifi = WifiMock()
    i = Internet(connection = wifi)
    i.connect()
    assert True == i.is_connected()
    i.disconnect()
