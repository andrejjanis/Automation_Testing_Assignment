""" Module containing test cases covering CeitSolver functionality """
import logging


log = logging.getLogger(__name__)


class TestAgv:
    """ Test class containing CeitSolver functionality """

    def test_min_agv_count(self, input_data, output_data):
        """ Test if minimalAgvCount value adheres to restrictions and was calculated properly """
        log.info("Check if minimalAgvCount is less or equal to the initial agvCount")
        assert output_data.minimum_agv_count <= input_data.agv_count, \
            log.error(f"Value of 'minimalAgvCount' {output_data.minimum_agv_count} is larger "
                      f"than the initial 'agvCount' of {input_data.agv_count}")
        agv_count = len(output_data.unique_agvs)
        log.info("Check if a number of AGV's used in transport orders is less or equal to the initial agvCount")
        assert agv_count <= input_data.agv_count, \
            log.error(f"The count of {agv_count} of unique AGV's used in transport orders is larger "
                      f"than the initial 'agvCount' of {input_data.agv_count}")
        log.info("Check if minimalAgvCount is equal to a number of AGV's used in transport orders")
        assert output_data.minimum_agv_count == agv_count, \
            log.error(f"Value of 'minimalAgvCount' of {output_data.minimum_agv_count} does not match "
                      f"the count of {agv_count} of unique AGV's used in transport orders")

    def test_max_agv_index(self, input_data, output_data):
        """ Test if indexes of AGV's used in transport order do not exceed the value of the initial agvCount """
        max_agv_index = max(output_data.unique_agvs)
        incorrect_indexes = [index for index in output_data.unique_agvs if index > input_data.agv_count]
        log.info("Check if indexes of AGV's used in transport order do not exceed the value of the initial agvCount")
        assert max_agv_index <= input_data.agv_count, \
            log.error(f"AGV indexes {incorrect_indexes} are bigger than initial AGV count of {input_data.agv_count}")

    def test_order_times_ascending(self, input_data, output_data):
        """ Test if the orders in output data are ascending according to the order time """
        previous_order_time = 0
        log.info("Check if orders are ascending according to the order time")
        for idx, order in enumerate(output_data.transport_orders):
            assert previous_order_time <= order.time, \
                log.error(f"Order time {order.time} of order at index {idx} "
                          f"is lower than previous order time of {previous_order_time}")
            previous_order_time = order.time

    def test_start_from_depo(self, output_data):
        """ Test if all AGV's start from depo """
        log.info("Check if all AGV's used in transport orders start from depo")
        for agv in output_data.unique_agvs:
            for idx, order in enumerate(output_data.transport_orders):
                if order.agv == agv:
                    assert order.origin == 0, log.error(f"AGV {agv} does not start from depo. \n"
                                                        f"First transport order for AGV {agv} with index {idx} "
                                                        f"and time {order.time} starts from {order.origin}")
                    break

    def test_continuous_rout(self, output_data):
        """ Test if all AGV's take continuous paths """
        log.info("Check if all AGV's take continuous paths")
        for agv in output_data.unique_agvs:
            previous_order_index = 0
            last_position = 0
            agv_orders = [(idx, order) for idx, order in enumerate(output_data.transport_orders) if order.agv == agv]
            for idx, order in agv_orders:
                assert order.origin == last_position, \
                    log.error(f"AGV {agv} in order index {idx} is starting from position {order.origin} "
                              f"when the last known position of agv is {last_position} "
                              f"in order index {previous_order_index}")
                last_position = order.destination
                previous_order_index = idx

    def test_transit_times(self, input_data, output_data):
        """ Test if transit times for AGV's between transport orders are considered correctly """
        log.info("Check if transit times for AGV's between transport orders are equal to or longer than required")
        for agv in output_data.unique_agvs:
            agv_orders = [(idx, order) for idx, order in enumerate(output_data.transport_orders) if order.agv == agv]
            for agv_specific_idx, agv_order in enumerate(agv_orders[1:], 1):
                order_idx, order = agv_order
                previous_order_idx, previous_order = agv_orders[agv_specific_idx - 1]
                transit_time = input_data.get_transit_time(previous_order.origin, previous_order.destination)
                time_from_previous_order = order.time - previous_order.time
                assert time_from_previous_order >= transit_time, \
                    log.error(f"Time of transport order insufficient for transit of AGV {agv}.\n"
                              f"Transport order with index {order_idx}, time {order.time}.\n"
                              f"Previous transport order with index {previous_order_idx}, time {previous_order.time}, "
                              f"from {previous_order.origin}, to {previous_order.destination}, distance "
                              f"{input_data.get_distance(previous_order.origin, previous_order.destination)},"
                              f" AGV speed {input_data.agv_speed}.\n"
                              f"Minimal required transit time is {transit_time}")

    def test_all_deliveries_completed(self, input_data, output_data):
        """ Test if all scheduled deliveries were completed within totalDurationTime """
        log.info("Check if all scheduled deliveries were completed within totalDurationTime")
        for delivery in input_data.deliveries:
            count = 0
            for order in output_data.transport_orders:
                if order.origin == delivery.origin and order.destination == delivery.destination and \
                        (order.time + input_data.get_transit_time(order.origin, order.destination)) <= \
                        input_data.total_duration_time:
                    count += 1
            assert count == delivery.deliveries_needed, \
                log.error(f"Only {count} transport orders from {delivery.deliveries_needed} scheduled for delivery "
                          f"from {delivery.origin} to {delivery.destination} were completed")

    def test_correct_penalty_time(self, input_data, output_data):
        """ Test if penalty time was calculated correctly """
        delivery_times = dict.fromkeys(input_data.deliveries)
        order_times = dict.fromkeys(input_data.deliveries)
        penalty_time = 0
        for delivery in input_data.deliveries:
            delivery_times[delivery] = [i * delivery.takt_time for i in range(1, delivery.deliveries_needed + 1)]
            order_times[delivery] = []
            for order in output_data.transport_orders:
                if order.origin == delivery.origin and order.destination == delivery.destination:
                    order_times[delivery].append(order.time)
        for delivery in input_data.deliveries:
            penalty_time += sum([y - x for x, y in zip(delivery_times[delivery], order_times[delivery])])
            not_delivered = delivery.deliveries_needed - len(order_times[delivery])
            if not_delivered:
                for delivery_time in delivery_times[delivery][-not_delivered:]:
                    penalty_time += input_data.total_duration_time - delivery_time
        log.info("Check if penalty time was calculated correctly")
        assert penalty_time == output_data.penalty_time, \
            log.error(f"Penalty time of {output_data.penalty_time} is not calculated correctly, "
                      f"correct penalty time from transport orders is {penalty_time}")

    def test_ideal_penalty_time(self, output_data):
        """ Test if ideal penalty time of 0 was achieved """
        log.info("Check if ideal penalty time of 0 was achieved")
        assert output_data.penalty_time == 0, log.error("Penalty time is not equal to zero")

    def test_idle_time(self, input_data, output_data):
        """ Test if idle time of AGV's at the depo was calculated correctly """
        idle_time = input_data.total_duration_time * input_data.agv_count
        for agv in range(1, input_data.agv_count + 1):
            agv_orders = [order for order in output_data.transport_orders if order.agv == agv]
            depo_departure = 0
            depo_arrival = 0
            for order in agv_orders:
                if order.origin == 0:
                    depo_departure = order.time
                if order.destination == 0:
                    depo_arrival = order.time
                    idle_time -= (depo_arrival + input_data.get_transit_time(order.origin, 0)) - depo_departure
            if depo_departure > depo_arrival:
                idle_time -= input_data.total_duration_time - depo_departure
        log.info("Check if idle time at the depo was calculated correctly")
        assert idle_time == output_data.idle_time, log.error(f"Idle time of {output_data.idle_time} is not correct. "
                                                             f"Idle time should be {idle_time}")
