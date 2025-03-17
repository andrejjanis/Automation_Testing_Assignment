""" This module provides functionality to load structured setup data from files with supported file format """
import json
from typing import Any, Dict


def read_json(file_name: str) -> Dict[str, Any]:
    """ Read JSON format files

    :param file_name: full path to a file to read
    :return: loaded data from file
    """
    with open(file_name, "r", encoding="utf-8-sig") as data_file:
        data = json.load(data_file)
    return data
