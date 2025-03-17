""" This module contains classes for parsing and manipulation with output file data """
from framework.helpers import read_json
from typing import Dict, List, Set


class TransportOrder:
    """ Class representing a single transport order """

    def __init__(self,
                 transport_orders: Dict[str, int]) -> None:
        """ TransportOrder class init method

        :param transport_orders: dictionary with transport order data
        """
        self.time = transport_orders["time"]
        self.agv = transport_orders["agv"]
        self.origin = transport_orders["from"]
        self.destination = transport_orders["to"]


class OutputData:
    """ Class representing output data to be processed """
    def __init__(self,
                 file_name: str) -> None:
        """ OutputData class init method

        :param file_name: path to an 'out.json' data file
        """
        data = read_json(file_name)
        self.idle_time = data["idleTime"]
        self.penalty_time = data["penaltyTime"]
        self.minimum_agv_count = data["minimumAgvCount"]
        self.transport_orders = self.parse_transport_orders(data["transportOrders"])

    @staticmethod
    def parse_transport_orders(transport_orders: List[Dict[str, int]]) -> List[TransportOrder]:
        """ Parse transport order data into a list of separate transport orders

        :param transport_orders: list of transport order data in a dictionary
        :return: list of parsed TransportOrder class instances
        """
        return [TransportOrder(order) for order in transport_orders]

    @property
    def unique_agvs(self) -> Set[int]:
        """ Property representing unique AGV's used in transport orders

        :return: set of unique AGV's used in transport orders
        """
        return set([order.agv for order in self.transport_orders])

