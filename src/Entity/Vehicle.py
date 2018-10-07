import pygame

from src.Common import Lane, TrafficStatus
from src.Config import Config


class Vehicle:
    def __init__(self, x, y, lane:Lane, image, surface, traffic_light):
        if lane != traffic_light.lane:
            raise Exception('The lane of traffic light and vehicle must be same.')
        self.x = x
        self.y = y
        self.lane = lane
        if lane in [Lane.left_to_right, Lane.right_to_left]:
            self.image = pygame.transform.scale(image, (Config['vehicle']['body_length'], Config['vehicle']['body_width']))
        elif lane in [Lane.top_to_bottom, Lane.bottom_to_top]:
            self.image = pygame.transform.scale(image, (Config['vehicle']['body_width'], Config['vehicle']['body_length']))
        self.surface = surface
        self.traffic_light = traffic_light

    @property
    def center_x(self):
        return self.x + self.width / 2

    @property
    def center_y(self):
        return self.x + self.height / 2

    @property
    def width(self):
        return self.image.get_width()

    @property
    def height(self):
        return self.image.get_height()

    def draw(self):
        self.surface.blit(self.image, (self.x, self.y))

    def move(self, front_vehicle=None):
        safe_distance = Config['vehicle']['safe_distance']
        speed = Config['vehicle']['speed']
        stopping_non_green_light = self.traffic_light.status != TrafficStatus.green and self.is_behind_traffic_light()

        if self.lane == Lane.left_to_right:
            self.x += speed
            self.y += 0
            if front_vehicle:
                self.x = min(self.x, front_vehicle.x - safe_distance - self.width)
            if stopping_non_green_light:
                self.x = min(self.x, self.traffic_light.x - self.traffic_light.width/2 - self.width)

        elif self.lane == Lane.right_to_left:
            self.x -= speed
            self.y += 0
            if front_vehicle:
                self.x = max(self.x, front_vehicle.x + front_vehicle.width + safe_distance)
            if stopping_non_green_light:
                self.x = max(self.x, self.traffic_light.x + self.traffic_light.width*3/2)

        elif self.lane == Lane.bottom_to_top:
            self.x += 0
            self.y -= speed
            if front_vehicle:
                self.y = max(self.y, front_vehicle.y + front_vehicle.height + safe_distance)
            if stopping_non_green_light:
                self.y = max(self.y, self.traffic_light.y + self.traffic_light.height)

        elif self.lane == Lane.top_to_bottom:
            self.x += 0
            self.y += speed
            if front_vehicle:
                self.y = min(self.y, front_vehicle.y - safe_distance - self.height)
            if stopping_non_green_light:
                self.y = min(self.y, self.traffic_light.y - self.traffic_light.height/2 - self.height)

    def is_behind_traffic_light(self):
        if self.lane == Lane.left_to_right:
            return self.x + self.width <= self.traffic_light.x + self.traffic_light.width
        elif self.lane == Lane.right_to_left:
            return self.traffic_light.x + self.traffic_light.width <= self.x
        elif self.lane == Lane.bottom_to_top:
            return self.traffic_light.y + self.traffic_light.height <= self.y
        elif self.lane == Lane.top_to_bottom:
            return self.y + self.height <= self.traffic_light.y
        return False

    def inside_canvas(self) -> bool:
        return self.x >= 0 and \
                self.x + self.width <= Config['simulator']['screen_width'] and \
                self.y >= 0 and \
                self.y + self.height <= Config['simulator']['screen_height']
