import pygame

from src.Config import Config


class BackgroundController:
    def __init__(self, surface, traffic_lights):
        self.surface = surface
        self.traffic_lights = traffic_lights

        self.screen_height = Config['simulator']['screen_height']
        self.screen_width = Config['simulator']['screen_width']

        self.black = Config['colors']['black']

    def refresh_screen(self):
        self.surface.fill(Config['colors']['white'])

    def draw_vechile_count(self, total):
        font = pygame.font.SysFont('Comic Sans MS', Config['background']['total_vehicles_font_size'])
        text_surface = font.render('Total Vehicles: {}'.format(total), False, self.black)
        self.surface.blit(text_surface, Config['background']['total_vehicles_position'])

    def draw_road_markings(self):
        bumper_distance = Config['simulator']['bumper_distance']
        vehicle_body_width = Config['vehicle']['body_width']
        road_marking_width = Config['background']['road_marking_width']
        road_marking_length, road_marking_distance = Config['background']['road_marking_alternate_lengths']
        traffic_yellow = Config['colors']['traffic_yellow']
        white = Config['colors']['white']
        junction_cover = Config['background']['junction_cover']

        # lane from bottom to top
        x = self.screen_width / 2 - bumper_distance - vehicle_body_width / 2 - road_marking_width / 2
        y = 0
        while self.within_boundary(x, y):
            pygame.draw.rect(self.surface, traffic_yellow, (x, y, road_marking_width, road_marking_length))
            y += road_marking_length + road_marking_distance

        # lane from top to bottom
        x = self.screen_width / 2 + bumper_distance + vehicle_body_width / 2 - road_marking_width / 2
        y = 0
        while self.within_boundary(x, y):
            pygame.draw.rect(self.surface, traffic_yellow, (x, y, road_marking_width, road_marking_length))
            y += road_marking_length + road_marking_distance

        # lane from left to right
        x = 0
        y = self.screen_height / 2 - bumper_distance - vehicle_body_width / 2 - road_marking_width / 2
        while self.within_boundary(x, y):
            pygame.draw.rect(self.surface, traffic_yellow, (x, y, road_marking_length, road_marking_width))
            x += road_marking_length + road_marking_distance

        # lane from left to right
        x = 0
        y = self.screen_height / 2 + bumper_distance + vehicle_body_width / 2 - road_marking_width / 2
        while self.within_boundary(x, y):
            pygame.draw.rect(self.surface, traffic_yellow, (x, y, road_marking_length, road_marking_width))
            x += road_marking_length + road_marking_distance

        top, left, bottom, right = junction_cover
        x = self.screen_width / 2 - left
        y = self.screen_height / 2 - top
        pygame.draw.rect(self.surface, white, (x, y, left + right, top + bottom))

    def within_boundary(self, x, y):
        return 0 <= x <= self.screen_width and 0 <= y <= self.screen_height
