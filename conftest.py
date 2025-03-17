""" This file serves as a means of providing fixtures for the entire framework directory structure """
import pytest
from framework.input_data import InputData
from framework.output_data import OutputData


@pytest.fixture(scope="session", autouse=False)
def input_data():
    """ Pytest fixture to provide InputData instance
    """
    return InputData("in.json")


@pytest.fixture(scope="session", autouse=False)
def output_data():
    """ Pytest fixture to provide OutputData instance
    """
    return OutputData("out.json")
