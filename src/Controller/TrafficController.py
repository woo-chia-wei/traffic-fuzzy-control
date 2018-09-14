import os
import pygame

from src.Common import TrafficStatus, DoubleLane, Lane
from src.Config import Config
from src.Entity.TrafficLight import TrafficLight


class TrafficController:
    def __init__(self, surface):
        self.surface = surface
        self.screen_height = Config['simulator']['screen_height']
        self.screen_width = Config['simulator']['screen_width']
        self.traffic_light_body_height = Config['traffic_light']['body_height']
        self.traffic_light_body_width = Config['traffic_light']['body_width']
        self.traffic_light_distance_from_center = Config['traffic_light']['distance_from_center']

        self.traffic_lights = {}

        x = self.screen_width / 2 - self.traffic_light_distance_from_center[0] - self.traffic_light_body_width
        y = self.screen_height / 2 - self.traffic_light_distance_from_center[1] - self.traffic_light_body_height
        self.create_traffic_light(x, y, Lane.left_to_right)

        x = self.screen_width / 2 + self.traffic_light_distance_from_center[0]
        y = self.screen_height / 2 + self.traffic_light_distance_from_center[1]
        self.create_traffic_light(x, y, Lane.right_to_left)

        x = self.screen_width / 2 - self.traffic_light_distance_from_center[0] - self.traffic_light_body_width
        y = self.screen_height / 2 + self.traffic_light_distance_from_center[1]
        self.create_traffic_light(x, y, Lane.bottom_to_top)

        x = self.screen_width / 2 + self.traffic_light_distance_from_center[0]
        y = self.screen_height / 2 - self.traffic_light_distance_from_center[1] - self.traffic_light_body_height
        self.create_traffic_light(x, y, Lane.top_to_bottom)

    def get_traffic_lights(self, double_lane: DoubleLane):
        if double_lane == DoubleLane.Horizontal:
            return [
                self.traffic_lights[Lane.left_to_right],
                self.traffic_lights[Lane.right_to_left]
            ]
        elif double_lane == DoubleLane.Vertical:
            return [
                self.traffic_lights[Lane.bottom_to_top],
                self.traffic_lights[Lane.top_to_bottom]
            ]
        return None

    def change_status(self, double_lane: DoubleLane, status: TrafficStatus):
        for traffic_light in self.get_traffic_lights(double_lane):
            traffic_light.change_status(status)

    def create_traffic_light(self, x, y, lane: Lane):
        traffic_light_images_dir = os.path.join(os.getcwd(), 'images', 'traffic_light')
        traffic_light_images = {
            TrafficStatus.red: pygame.image.load(os.path.join(traffic_light_images_dir, 'traffic_light_red.png')),
            TrafficStatus.green: pygame.image.load(os.path.join(traffic_light_images_dir, 'traffic_light_green.png')),
            TrafficStatus.yellow: pygame.image.load(os.path.join(traffic_light_images_dir, 'traffic_light_yellow.png'))
        }
        self.traffic_lights[lane] = TrafficLight(x, y, lane, traffic_light_images, self.surface)

    def update_and_draw_traffic_lights(self):
        for lane, traffic_light in self.traffic_lights.items():
            traffic_light.auto_update()
            traffic_light.draw()

    def go(self, double_lane: DoubleLane):
        for traffic_light in self.get_traffic_lights(double_lane):
            if traffic_light.status != TrafficStatus.green:
                traffic_light.change_status(TrafficStatus.green)

    def stop(self, double_lane: DoubleLane):
        for traffic_light in self.get_traffic_lights(double_lane):
            if traffic_light.status == TrafficStatus.green:
                traffic_light.change_status(TrafficStatus.yellow)

    # def toggle(self):
    #     gap = Config['simulator']['gap_between_traffic_switch']
    #     if self.toggle_state:
    #         self.stop(self.opposite_traffic_lights)
    #         time.sleep(gap)
    #         self.go(self.traffic_lights)
    #     else:
    #         self.stop(self.traffic_lights)
    #         time.sleep(gap)
    #         self.go(self.opposite_traffic_lights)
    #     self.toggle_state = not self.toggle_state
    #
    # def has_conflicts(self):
    #     all_traffic_lights = self.traffic_lights + self.opposite_traffic_lights
    #     return all([t.status == TrafficStatus.green for t in all_traffic_lights])
