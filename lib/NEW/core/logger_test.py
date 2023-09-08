
import pytest

from core.logger import Logger



def test_create_logger():
    l = Logger("test_name", "test_task")


def test_logging():
    l = Logger("test_name", "test_task")
    l.print_info("test_message")
    l.print_error("test_message")
    l.print_cmd("test_message")
    l.print_wait()

