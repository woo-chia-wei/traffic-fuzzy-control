import glob
import pygame
import random
import numpy as np

from src.Common import Lane
from src.Config import Config
from src.Entity.Vehicle import Vehicle
from src.Entity.TrafficLight import TrafficLight


class VehicleController:
    def __init__(self, surface):
        self.screen_height = Config['simulator']['screen_height']
        self.screen_width = Config['simulator']['screen_width']
        self.vehicle_body_width = Config['vehicle']['body_width']
        self.vehicle_body_length = Config['vehicle']['body_length']
        self.bumper_distance = Config['simulator']['bumper_distance']
        self.safe_distance = Config['vehicle']['safe_distance']

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

        self.num_vehicles_behind_traffic = {
            Lane.right_to_left: [],
            Lane.left_to_right: [],
            Lane.top_to_bottom: [],
            Lane.bottom_to_top: []
        }

        self.counter = 0

    def last_vehicle(self, lane: Lane):
        if len(self.get_vehicles(lane)) > 0:
            return self.get_vehicles(lane)[-1]
        else:
            return None

    def get_vehicles(self, lane: Lane):
        return self.vehicles[lane]

    def random_vehicle_image(self, lane: Lane):
        return random.choice(self.vehicle_images[lane])

    def create_vehicle(self, lane: Lane, traffic_light: TrafficLight):
        if traffic_light.lane != lane:
            raise Exception('Vehicle and traffic light must be in same lane.')

        image = self.random_vehicle_image(lane)
        surface = self.surface
        last_vehicle = self.last_vehicle(lane)
        too_close = False
        safe_spawn_factor = Config['vehicle']['safe_spawn_factor']

        if lane == Lane.left_to_right:
            x = 0
            y = self.screen_height / 2 - self.vehicle_body_width - self.bumper_distance
            if last_vehicle:
                too_close = last_vehicle.x - self.safe_distance * safe_spawn_factor < x + self.vehicle_body_length

        elif lane == Lane.right_to_left:
            x = self.screen_width - self.vehicle_body_length
            y = self.screen_height / 2 + self.bumper_distance
            if last_vehicle:
                too_close = last_vehicle.x + self.vehicle_body_length + self.safe_distance * safe_spawn_factor > x

        elif lane == Lane.top_to_bottom:
            x = self.screen_width / 2 + self.bumper_distance
            y = 0
            if last_vehicle:
                too_close = last_vehicle.y - self.safe_distance * safe_spawn_factor < y + self.vehicle_body_length

        elif lane == Lane.bottom_to_top:
            x = self.screen_width / 2 - self.vehicle_body_width - self.bumper_distance
            y = self.screen_height - self.vehicle_body_length
            if last_vehicle:
                too_close = last_vehicle.y + self.vehicle_body_length + self.safe_distance * safe_spawn_factor > y

        if too_close:
            return

        new_vehicle = Vehicle(x, y, lane, image, surface, traffic_light)
        self.vehicles[lane].append(new_vehicle)
        self.counter += 1

    def update_and_draw_vehicles(self):
        for lane, vehicles_in_single_lane in self.vehicles.items():
            for index, vehicle in enumerate(vehicles_in_single_lane):
                front_vehicle = None
                if index >= 1:
                    front_vehicle = vehicles_in_single_lane[index - 1]
                vehicle.move(front_vehicle)
                vehicle.draw()

    def destroy_vehicles_outside_canvas(self):
        for lane, vehicles_in_single_lane in self.vehicles.items():
            self.vehicles[lane] = [v for v in self.vehicles[lane] if v.inside_canvas()]

    def update_num_vehicles_behind_traffic(self):
        for lane, vehicles_in_single_lane in self.vehicles.items():
            count = len([v for v in self.vehicles[lane] if v.is_behind_traffic_light()])
            self.num_vehicles_behind_traffic[lane].append(count)
            moving_average_max_length = Config['simulator']['frame_rate'] * Config['simulator']['moving_averages_period']
            while len(self.num_vehicles_behind_traffic[lane]) >= moving_average_max_length:
                self.num_vehicles_behind_traffic[lane].pop(0)

    def get_moving_averages_num_vehicles_behind_traffic(self):
        all_lanes = [
            Lane.right_to_left,
            Lane.left_to_right,
            Lane.top_to_bottom,
            Lane.bottom_to_top
        ]
        result = {}
        for lane in all_lanes:
            result[lane] = np.mean(self.num_vehicles_behind_traffic[lane])
        return result
