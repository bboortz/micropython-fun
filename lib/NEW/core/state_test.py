
import pytest

from core.state import State, StateException


def test_create_state():
    s = State()
    assert s.is_init() == True
    assert s.is_running() == True
    assert s.is_stopped() == False
    assert s.is_healthy() == False
    assert s.is_in_setup() == False
    assert s.is_setup_done() == False


def test_to_init():
    s = State()
    s.to_stopped()
    s.to_init()
    assert s.is_init() == True
    assert s.is_running() == True
    assert s.is_stopped() == False
    assert s.is_healthy() == False
    assert s.is_unhealthy() == False
    assert s.is_in_setup() == False
    assert s.is_setup_done() == False


def test_to_stopped():
    s = State()
    s.to_stopped()
    assert s.is_init() == False
    assert s.is_running() == False
    assert s.is_stopped() == True
    assert s.is_healthy() == False
    assert s.is_unhealthy() == False
    assert s.is_in_setup() == False
    assert s.is_setup_done() == False


def test_to_in_setup():
    s = State()
    s.to_in_setup()
    assert s.is_init() == False
    assert s.is_running() == True
    assert s.is_stopped() == False
    assert s.is_healthy() == False
    assert s.is_unhealthy() == False
    assert s.is_in_setup() == True
    assert s.is_setup_done() == False


def test_to_setup_done():
    s = State()
    s.to_in_setup()
    s.to_setup_done()
    assert s.is_init() == False
    assert s.is_running() == True
    assert s.is_stopped() == False
    assert s.is_healthy() == False
    assert s.is_unhealthy() == False
    assert s.is_in_setup() == False
    assert s.is_setup_done() == True


def test_to_healthy():
    s = State()
    s.to_in_setup()
    s.to_setup_done()
    s.to_healthy()
    assert s.is_init() == False
    assert s.is_running() == True
    assert s.is_stopped() == False
    assert s.is_healthy() == True
    assert s.is_unhealthy() == False
    assert s.is_in_setup() == False
    assert s.is_setup_done() == True


def test_to_unhealthy():
    s = State()
    s.to_in_setup()
    s.to_setup_done()
    s.to_healthy()
    s.to_unhealthy()
    assert s.is_init() == False
    assert s.is_running() == True
    assert s.is_stopped() == False
    assert s.is_healthy() == False
    assert s.is_unhealthy() == True
    assert s.is_in_setup() == False
    assert s.is_setup_done() == True


def test_set_states():
    s = State()
    assert s.is_init() == True
    assert s.is_running() == True
    assert s.is_stopped() == False
    assert s.is_healthy() == False
    assert s.is_unhealthy() == False
    assert s.is_in_setup() == False
    assert s.is_setup_done() == False

    s.to_in_setup()
    assert s.is_init() == False
    assert s.is_running() == True
    assert s.is_stopped() == False
    assert s.is_healthy() == False
    assert s.is_unhealthy() == False
    assert s.is_in_setup() == True
    assert s.is_setup_done() == False

    s.to_setup_done()
    assert s.is_init() == False
    assert s.is_running() == True
    assert s.is_stopped() == False
    assert s.is_healthy() == False
    assert s.is_unhealthy() == False
    assert s.is_in_setup() == False
    assert s.is_setup_done() == True

    s.to_healthy()
    assert s.is_init() == False
    assert s.is_running() == True
    assert s.is_stopped() == False
    assert s.is_healthy() == True
    assert s.is_unhealthy() == False
    assert s.is_in_setup() == False
    assert s.is_setup_done() == True

    s.to_unhealthy()
    assert s.is_init() == False
    assert s.is_running() == True
    assert s.is_stopped() == False
    assert s.is_healthy() == False
    assert s.is_unhealthy() == True
    assert s.is_in_setup() == False
    assert s.is_setup_done() == True

    s.to_healthy()
    assert s.is_init() == False
    assert s.is_running() == True
    assert s.is_stopped() == False
    assert s.is_healthy() == True
    assert s.is_unhealthy() == False
    assert s.is_in_setup() == False
    assert s.is_setup_done() == True

    s.to_unhealthy()
    assert s.is_init() == False
    assert s.is_running() == True
    assert s.is_stopped() == False
    assert s.is_healthy() == False
    assert s.is_unhealthy() == True
    assert s.is_in_setup() == False
    assert s.is_setup_done() == True

    s.to_in_setup()
    assert s.is_init() == False
    assert s.is_running() == True
    assert s.is_stopped() == False
    assert s.is_healthy() == False
    assert s.is_unhealthy() == False
    assert s.is_in_setup() == True
    assert s.is_setup_done() == False

    s.to_stopped()
    assert s.is_init() == False
    assert s.is_running() == False
    assert s.is_stopped() == True
    assert s.is_healthy() == False
    assert s.is_unhealthy() == False
    assert s.is_in_setup() == False
    assert s.is_setup_done() == False
