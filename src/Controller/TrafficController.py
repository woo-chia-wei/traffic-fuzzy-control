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

        y = self.screen_width / 2 - self.traffic_light_distance_from_center[0] - self.traffic_light_body_width
        x = self.screen_height / 2 + self.traffic_light_distance_from_center[1]
        self.create_traffic_light(x, y, Lane.top_to_bottom)

        y = self.screen_width / 2 + self.traffic_light_distance_from_center[0]
        x = self.screen_height / 2 - self.traffic_light_distance_from_center[1] - self.traffic_light_body_height
        self.create_traffic_light(x, y, Lane.bottom_to_top)

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

    def design_traffic_image(self, file_dir, filename, rotation):
        image = pygame.image.load(os.path.join(file_dir, filename))
        return pygame.transform.rotate(pygame.transform.scale(image,
                    (self.traffic_light_body_width, self.traffic_light_body_height)), rotation)

    def create_traffic_light(self, x, y, lane: Lane):
        traffic_light_images_dir = os.path.join(os.getcwd(), 'images', 'traffic_light')
        rotation = 0
        if lane == Lane.bottom_to_top:
            rotation = 90
        elif lane == Lane.right_to_left:
            rotation = 180
        elif lane == Lane.top_to_bottom:
            rotation = 270
        traffic_light_images = {
            TrafficStatus.red: self.design_traffic_image(traffic_light_images_dir, 'traffic_light_red.png', rotation),
            TrafficStatus.green: self.design_traffic_image(traffic_light_images_dir, 'traffic_light_green.png', rotation),
            TrafficStatus.yellow: self.design_traffic_image(traffic_light_images_dir, 'traffic_light_yellow.png', rotation)
        }
        self.traffic_lights[lane] = TrafficLight(x, y, lane, traffic_light_images, self.surface)

    def update_and_draw_traffic_lights(self):
        for lane, traffic_light in self.traffic_lights.items():
            opposite_status = self.get_opposite_status(lane)
            traffic_light.auto_update(opposite_status)
            traffic_light.draw()
            traffic_light.update_traffic_countdown()

    def change_status(self, double_lane: DoubleLane, status: TrafficStatus):
        for traffic_light in self.get_traffic_lights(double_lane):
            traffic_light.change_status(status)

    def go(self, double_lane: DoubleLane):
        self.change_status(double_lane, TrafficStatus.green)

    def stop(self, double_lane: DoubleLane):
        self.change_status(double_lane, TrafficStatus.yellow)

    def get_opposite_status(self, lane: Lane):
        if lane == Lane.right_to_left or \
           lane == Lane.left_to_right:
            return self.traffic_lights[Lane.bottom_to_top].status
        else:
            return self.traffic_lights[Lane.left_to_right].status
