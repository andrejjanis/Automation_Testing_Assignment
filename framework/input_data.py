""" This module contains classes for parsing and manipulation with input file data """
from framework.helpers import read_json
from typing import Dict, List


class Delivery:
    """ Class representing a periodic delivery """
    def __init__(self,
                 delivery: Dict[str, int],
                 total_duration_time: int) -> None:
        """ Delivery class init method

        :param delivery: dictionary with delivery data
        :param total_duration_time: parameter totalDurationTime from input data file
        """
        self.origin = delivery["from"]
        self.destination = delivery["to"]
        self.takt_time = delivery["time"]
        self.deliveries_needed = total_duration_time // self.takt_time


class InputData:
    """ Class representing input data to be processed """
    def __init__(self,
                 file_name: str) -> None:
        """ InputData class init method

        :param file_name: path to an 'in.json' data file
        """
        data = read_json(file_name)
        self.agv_count = data["agvCount"]
        self.total_duration_time = data["totalDurationTime"]
        self.deliveries = self.parse_deliveries(data["taktTimes"])
        self.distances = data["distances"]
        self.agv_speed = data.get("agvSpeed", 1)

    def parse_deliveries(self,
                         takt_times: List[Dict[str, int]]) -> List[Delivery]:
        """ Parse taktTime data into a list of separate deliveries

        :param takt_times: list of taktTime data in a dictionary
        :return: list of parsed Delivery class instances
        """
        return [Delivery(delivery, self.total_duration_time) for delivery in takt_times]

    def get_distance(self,
                     origin: int,
                     destination: int) -> int:
        """ Get distance from origin point to destination point

        :param origin: origin point to calculate distance from
        :param destination: destination point to calculate distance to
        :return: distance from origin to destination
        """
        if origin > destination:
            origin, destination = destination, origin
        for distance in self.distances:
            if distance["from"] == origin and distance["to"] == destination:
                return distance["distance"]

    def get_transit_time(self,
                         origin: int,
                         destination: int) -> int:
        """ Get transit time from origin point to destination point

        :param origin: origin point to calculate transit time from
        :param destination: destination point to calculate transit time to
        :return: transit time from origin to destination
        """
        return self.get_distance(origin, destination) * self.agv_speed

