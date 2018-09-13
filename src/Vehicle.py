from src.Common import Lane
from src.Config import Config


class Vehicle:
    def __init__(self, x, y, lane, image, surface):
        self.x = x
        self.y = y
        self.lane = lane
        self.image = image
        self.surface = surface

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

        if self.lane == Lane.left_to_right:
            self.x += speed
            self.y += 0
            if front_vehicle:
                self.x = min(self.x, front_vehicle.x - safe_distance)
        elif self.lane == Lane.right_to_left:
            self.x -= speed
            self.y += 0
            if front_vehicle:
                self.x = max(self.x, front_vehicle.x + front_vehicle.width + safe_distance)
        elif self.lane == Lane.bottom_to_top:
            self.x += 0
            self.y -= speed
            if front_vehicle:
                self.y = max(self.y, front_vehicle.y + front_vehicle.height + safe_distance)
        elif self.lane == Lane.top_to_bottom:
            self.x += 0
            self.y += speed
            if front_vehicle:
                self.y = min(self.y, front_vehicle.y - safe_distance)

    def is_behind_traffic_light(self, traffic_light):
        pass
