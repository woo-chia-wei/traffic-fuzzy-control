import glob
import pygame
import random
import os

from src.Common import Lane, TrafficStatus
from src.Config import Config
from src.Vehicle import Vehicle
from src.TrafficLight import TrafficLight


class VehicleFactory:
    def __init__(self, surface):
        self.screen_height = Config['simulator']['screen_height']
        self.screen_width = Config['simulator']['screen_width']
        self.vehicle_body_width = Config['vehicle']['body_width']
        self.vehicle_body_length = Config['vehicle']['body_length']
        self.bumper_distance = Config['simulator']['bumper_distance']
        self.traffic_light_distance_from_center = Config['traffic_light']['distance_from_center']
        self.traffic_light_body_height = Config['traffic_light']['body_height']
        self.traffic_light_body_width = Config['traffic_light']['body_width']

        self.surface = surface
        self.vehicles = {
            Lane.right_to_left: [],
            Lane.left_to_right: [],
            Lane.top_to_bottom: [],
            Lane.bottom_to_top: []
        }

        self.vehicle_images = {
            Lane.right_to_left: [pygame.image.load(f) for f in glob.glob('images/vehicles_right_to_left/*.png')],
            Lane.left_to_right: [pygame.image.load(f) for f in glob.glob('images/vehicles_left_to_right/*.png')],
            Lane.top_to_bottom: [pygame.image.load(f) for f in glob.glob('images/vehicles_top_to_bottom/*.png')],
            Lane.bottom_to_top: [pygame.image.load(f) for f in glob.glob('images/vehicles_bottom_to_top/*.png')]
        }

        traffic_light_images_dir = os.path.join(os.getcwd(), 'images', 'traffic_light')

        self.traffic_light_images = {
            TrafficStatus.red: pygame.image.load(os.path.join(traffic_light_images_dir, 'traffic_light_red.png')),
            TrafficStatus.green: pygame.image.load(os.path.join(traffic_light_images_dir, 'traffic_light_green.png')),
            TrafficStatus.yellow: pygame.image.load(os.path.join(traffic_light_images_dir, 'traffic_light_yellow.png'))
        }

        self.traffic_lights = {}
        x = self.screen_width / 2 - self.traffic_light_distance_from_center[0] - self.traffic_light_body_width
        y = self.screen_height / 2 - self.traffic_light_distance_from_center[1] - self.traffic_light_body_height
        self.traffic_lights[Lane.left_to_right] = TrafficLight(x, y, Lane.left_to_right,
                                                               self.traffic_light_images,
                                                               self.surface)
        x = self.screen_width / 2 + self.traffic_light_distance_from_center[0]
        y = self.screen_height / 2 - self.traffic_light_distance_from_center[1] - self.traffic_light_body_height
        self.traffic_lights[Lane.right_to_left] = TrafficLight(x, y, Lane.right_to_left,
                                                               self.traffic_light_images,
                                                               self.surface)
        x = self.screen_width / 2 - self.traffic_light_distance_from_center[0] - self.traffic_light_body_width
        y = self.screen_height / 2 + self.traffic_light_distance_from_center[1]
        self.traffic_lights[Lane.bottom_to_top] = TrafficLight(x, y, Lane.bottom_to_top,
                                                               self.traffic_light_images,
                                                               self.surface)
        x = self.screen_width / 2 + self.traffic_light_distance_from_center[0]
        y = self.screen_height / 2 + self.traffic_light_distance_from_center[1]
        self.traffic_lights[Lane.top_to_bottom] = TrafficLight(x, y, Lane.top_to_bottom,
                                                               self.traffic_light_images,
                                                               self.surface)

    def last_vehicle(self, lane):
        return self.get_vehicles(lane)[-1]

    def get_vehicles(self, lane):
        return self.vehicles[lane]

    def random_vehicle_image(self, lane):
        return random.choice(self.vehicle_images[lane])

    def create_vehicle(self, lane):
        image = self.random_vehicle_image(lane)
        surface = self.surface
        last_vehicle = self.last_vehicle(lane)
        too_close = True

        if lane == Lane.left_to_right:
            x = 0
            y = self.screen_height / 2 - self.vehicle_body_width - self.bumper_distance
            too_close = last_vehicle.x - self.safe_distance * 2 < x + self.vehicle_body_length
        elif lane == Lane.right_to_left:
            x = self.screen_width - self.vehicle_body_length
            y = self.screen_height / 2 + self.bumper_distance
            too_close = last_vehicle.x + self.vehicle_body_length + self.safe_distance * 2 > x
        elif lane == Lane.top_to_bottom:
            x = self.screen_width / 2 + self.bumper_distance
            y = 0
            too_close = last_vehicle.y - self.safe_distance * 2 < y + self.vehicle_body_length
        elif lane == Lane.bottom_to_top:
            x = self.screen_width / 2 - self.vehicle_body_width - self.bumper_distance
            y = self.screen_height - self.vehicle_body_length
            too_close = last_vehicle.y + self.vehicle_body_length + self.safe_distance * 2 > y

        if too_close:
            return

        new_vehicle = Vehicle(x, y, lane, image, surface, self.traffic_lights[lane])
        self.vehicles[lane].append(new_vehicle)

    def update_and_draw_traffic_lights(self):
        for lane, traffic_light in self.traffic_lights.items():
            traffic_light.update()
            traffic_light.draw()

    def update_and_draw_vehicles(self):
        for lane, vehicles_in_single_lane in self.vehicles.items():
            for index, vehicle in enumerate(vehicles_in_single_lane):
                front_vehicle = None
                if index >= 1:
                    front_vehicle = vehicles_in_single_lane[index - 1]
                vehicle.move(front_vehicle)
                vehicle.draw()
