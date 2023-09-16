
import pytest

from core.config import Config
from adapter.wifi_mock import WifiMock



def test_create_wifi():
    w = WifiMock()


def test_wifi_connect():
    w = WifiMock()
    w.connect()


def test_wifi_connect_disconnect():
    w = WifiMock()
    w.connect()
    w.disconnect()

