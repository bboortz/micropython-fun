
import pytest

from core.generic import GenericClass, GenericException



def test_create_generic_class():
    g = GenericClass("test_task")


def test_raise_generic_exception():
    with pytest.raises(GenericException):
        raise GenericException("test context", "test message", "test cause")

