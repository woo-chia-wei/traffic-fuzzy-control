import time

from src.Common import TrafficStatus
from src.Config import Config


class TrafficController:
    def __init__(self, traffic_lights, opposite_traffic_lights):
        if len(traffic_lights) == 0 or len(opposite_traffic_lights) == 0:
            raise Exception('There must be at least one traffic lights!')

        self.traffic_lights = traffic_lights
        self.opposite_traffic_lights = opposite_traffic_lights
        self.toggle_state = False

    def go(self, traffic_lights):
        for traffic_light in traffic_lights:
            if traffic_light.status != TrafficStatus.green:
                traffic_light.change_status(TrafficStatus.green)

    def stop(self, traffic_lights):
        for traffic_light in traffic_lights:
            if traffic_light.status == TrafficStatus.green:
                traffic_light.change_status(TrafficStatus.yellow)

    def toggle(self):
        gap = Config['simulator']['gap_between_traffic_switch']
        if self.toggle_state:
            self.stop(self.opposite_traffic_lights)
            time.sleep(gap)
            self.go(self.traffic_lights)
        else:
            self.stop(self.traffic_lights)
            time.sleep(gap)
            self.go(self.opposite_traffic_lights)
        self.toggle_state = not self.toggle_state

    def has_conflicts(self):
        all_traffic_lights = self.traffic_lights + self.opposite_traffic_lights
        return all([t.status == TrafficStatus.green for t in all_traffic_lights])
