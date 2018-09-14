import time
from src.Common import TrafficStatus, Lane
from src.Config import Config


class TrafficLight:
    def __init__(self, x:float, y:float, lane:Lane, images, surface, status=TrafficStatus.green):
        self.x = x
        self.y = y
        self.lane = lane
        self.images = images  # expected to be dictionary with TrafficStatus as keys
        self.surface = surface
        self.duration = {
            TrafficStatus.green: Config['traffic_light']['green_light_duration'],
            TrafficStatus.red: Config['traffic_light']['red_light_duration'],
            TrafficStatus.yellow: Config['traffic_light']['yellow_light_duration']
        }
        self.start_time = {
            TrafficStatus.green: time.time(),
            TrafficStatus.red: time.time(),
            TrafficStatus.yellow: time.time()
        }
        self.status = status

    @property
    def center_x(self):
        return self.x + self.width / 2

    @property
    def center_y(self):
        return self.x + self.height / 2

    @property
    def width(self):
        return Config['traffic_light']['body_width']

    @property
    def height(self):
        return Config['traffic_light']['body_height']

    def draw(self):
        self.surface.blit(self.images[self.status], (self.x, self.y))

    def change_status(self, next_status=None):
        if not next_status:
            if self.status == TrafficStatus.green:
                new_status = TrafficStatus.yellow
            elif self.status == TrafficStatus.yellow:
                new_status = TrafficStatus.red
            elif self.status == TrafficStatus.red:
                new_status = TrafficStatus.green
        self.status = new_status
        self.start_time[self.status] = time.time()

    def auto_update(self):
        to_change_status = (time.time() - self.start_time[self.status]) > self.duration[self.status]
        if to_change_status:
            self.change_status()


