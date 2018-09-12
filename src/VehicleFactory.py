import glob
import pygame
import random
from src.Common import Lane
from src.Config import Config
from src.Vehicle import Vehicle


class VehicleFactory:
    def __init__(self, surface):
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
            Lane.bottom_to_top: [pygame.image.load(f) for f in glob.glob('images/vehicles_bottom_to_top/*.png')],
        }

    @property
    def last_vehicle(self, lane):
        return self.get_vehicles(lane)[-1]

    def get_vehicles(self, lane):
        return self.vehicles[lane]

    def random_vehicle_image(self, lane):
        return random.choice(self.vehicle_images[lane])

    def create_vehicle(self, lane):
        image = self.random_vehicle_image(lane)
        surface = self.surface
        screen_height = Config['simulator']['screen_height']
        screen_width = Config['simulator']['screen_width']
        vehicle_body_width = Config['vehicle']['body_width']
        bumper_distance = Config['simulator']['bumper_distance']

        if lane == Lane.left_to_right:
            x = 0
            y = screen_height / 2 - vehicle_body_width - bumper_distance
        elif lane == Lane.right_to_left:
            x = screen_width
            y = screen_height / 2 + bumper_distance
        elif lane == Lane.top_to_bottom:
            x = screen_width / 2 + bumper_distance
            y = 0
        elif lane == Lane.bottom_to_top:
            x = screen_width / 2 - vehicle_body_width - bumper_distance
            y = screen_height

        new_vehicle = Vehicle(x, y, lane, image, surface)
        self.vehicles[lane].append(new_vehicle)

    def update_and_draw_vehicles(self):
        all_vehicles = [
            self.vehicles[Lane.left_to_right],
            self.vehicles[Lane.right_to_left],
            self.vehicles[Lane.top_to_bottom],
            self.vehicles[Lane.bottom_to_top]
        ]

        for vehicles_lane in all_vehicles:
            for vehicle in vehicles_lane:
                vehicle.move()
                vehicle.draw()
