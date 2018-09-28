import pygame
from src.Common import DoubleLane
from src.Config import Config


class BackgroundController:
    def __init__(self, surface, traffic_lights):
        self.surface = surface
        self.traffic_lights = traffic_lights

        self.screen_height = Config['simulator']['screen_height']
        self.screen_width = Config['simulator']['screen_width']

        self.black = Config['colors']['black']
        self.red = Config['colors']['red']

        self.horizontal_frequency_small = None
        self.horizontal_frequency_medium = None
        self.horizontal_frequency_large = None

        self.vertical_frequency_small = None
        self.horizontal_frequency_medium = None
        self.horizontal_frequency_large = None

        self.spawn_rate = {
            DoubleLane.Horizontal: {
                'slow': True,
                'medium': False,
                'fast': False
            },
            DoubleLane.Vertical: {
                'slow': True,
                'medium': False,
                'fast': False
            }
        }

        self.spawn_rate_buttons = {
            DoubleLane.Horizontal: {
                'slow': None,
                'medium': None,
                'fast': None
            },
            DoubleLane.Vertical: {
                'slow': None,
                'medium': None,
                'fast': None
            }
        }

    def set_spawn_rate(self, double_lane: DoubleLane, target_rate):
        for rate in ['slow', 'medium', 'fast']:
            self.spawn_rate[double_lane][rate] = (target_rate == rate)

    def get_spawn_rate(self, double_lane: DoubleLane):
        for rate in ['slow', 'medium', 'fast']:
            if self.spawn_rate[double_lane][rate]:
                return rate
        raise Exception('None of slow, medium, fast is true!!!')

    def refresh_screen(self):
        self.surface.fill(Config['colors']['white'])

    def draw_spawn_rate_buttons(self):
        normal_font = pygame.font.SysFont('Comic Sans MS', 16)
        underline_font = pygame.font.SysFont('Comic Sans MS', 16)
        underline_font.set_underline(True)

        # Horizontal lanes controls
        self.surface.blit(normal_font.render('Spawn Rate (Horizontal):', False, self.black), (5, 25))
        fonts = [normal_font, normal_font, normal_font]
        colors = [self.black, self.black, self.black]
        if self.spawn_rate[DoubleLane.Horizontal]['slow']:
            fonts[0] = underline_font
            colors[0] = self.red
        if self.spawn_rate[DoubleLane.Horizontal]['medium']:
            fonts[1] = underline_font
            colors[1] = self.red
        if self.spawn_rate[DoubleLane.Horizontal]['fast']:
            fonts[2] = underline_font
            colors[2] = self.red
        self.spawn_rate_buttons[DoubleLane.Horizontal]['slow'] = self.surface.blit(fonts[0].render('Slow', False, colors[0]), (200, 25))
        self.spawn_rate_buttons[DoubleLane.Horizontal]['medium'] = self.surface.blit(fonts[1].render('Medium', False, colors[1]), (240, 25))
        self.spawn_rate_buttons[DoubleLane.Horizontal]['fast'] = self.surface.blit(fonts[2].render('Fast', False, colors[2]), (300, 25))

        # Vertical lanes controls
        self.surface.blit(normal_font.render('Spawn Rate (Vertical):', False, self.black), (5, 45))
        fonts = [normal_font, normal_font, normal_font]
        colors = [self.black, self.black, self.black]
        if self.spawn_rate[DoubleLane.Vertical]['slow']:
            fonts[0] = underline_font
            colors[0] = self.red
        if self.spawn_rate[DoubleLane.Vertical]['medium']:
            fonts[1] = underline_font
            colors[1] = self.red
        if self.spawn_rate[DoubleLane.Vertical]['fast']:
            fonts[2] = underline_font
            colors[2] = self.red
        self.spawn_rate_buttons[DoubleLane.Vertical]['slow'] = self.surface.blit(fonts[0].render('Slow', False, colors[0]), (200, 45))
        self.spawn_rate_buttons[DoubleLane.Vertical]['medium'] = self.surface.blit(fonts[1].render('Medium', False, colors[1]), (240, 45))
        self.spawn_rate_buttons[DoubleLane.Vertical]['fast'] = self.surface.blit(fonts[2].render('Fast', False, colors[2]), (300, 45))

    def draw_vehicle_count(self, total):
        font = pygame.font.SysFont('Comic Sans MS', 16)
        text_surface = font.render('Total Vehicles: {}'.format(total), False, self.black)
        self.surface.blit(text_surface, (5, 5))

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
