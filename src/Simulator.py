import pygame
import time

from src.Common import Lane, DoubleLane
from src.Config import Config
from src.Controller.VehicleController import VehicleController
from src.Controller.TrafficController import TrafficController
from src.Controller.BackgroundController import BackgroundController


class Simulator:
    def __init__(self, caption):
        self.caption = caption
        self.surface = pygame.display.set_mode((Config['simulator']['screen_width'],
                                                Config['simulator']['screen_height']))
        self.vehicle_ctrl = VehicleController(self.surface)
        self.traffic_ctrl = TrafficController(self.surface)
        self.background_ctrl = BackgroundController(self.surface,
                                                    self.traffic_ctrl.get_traffic_lights(DoubleLane.Horizontal) +
                                                    self.traffic_ctrl.get_traffic_lights(DoubleLane.Vertical))
        self.clock = pygame.time.Clock()
        self.gap_between_switch = Config['simulator']['gap_between_traffic_switch']

        self.HORIZONTAL_SPAWN_EVENT = pygame.USEREVENT + 1
        self.VERTICAL_SPAWN_EVENT = pygame.USEREVENT + 2

        self.switching_traffic = False
        self.switching_traffic_start_time = None

    def spawn(self, double_lane: DoubleLane):
        if double_lane == DoubleLane.Horizontal:
            self.spawn_single_vehicle(Lane.left_to_right)
            self.spawn_single_vehicle(Lane.right_to_left)
        elif double_lane == DoubleLane.Vertical:
            self.spawn_single_vehicle(Lane.bottom_to_top)
            self.spawn_single_vehicle(Lane.top_to_bottom)

    def spawn_single_vehicle(self, lane: Lane):
        self.vehicle_ctrl.create_vehicle(lane, self.traffic_ctrl.traffic_lights[lane])

    def main_loop(self):
        game_over = False

        pygame.time.set_timer(self.HORIZONTAL_SPAWN_EVENT, Config['simulator']['spawn_rate']['slow'])
        pygame.time.set_timer(self.VERTICAL_SPAWN_EVENT, Config['simulator']['spawn_rate']['slow'])

        while not game_over:

            for event in pygame.event.get():
                if event.type == self.HORIZONTAL_SPAWN_EVENT:
                    rate = self.background_ctrl.get_spawn_rate(DoubleLane.Horizontal)
                    pygame.time.set_timer(self.HORIZONTAL_SPAWN_EVENT, Config['simulator']['spawn_rate'][rate])
                    self.spawn(DoubleLane.Horizontal)

                if event.type == self.VERTICAL_SPAWN_EVENT:
                    rate = self.background_ctrl.get_spawn_rate(DoubleLane.Vertical)
                    pygame.time.set_timer(self.VERTICAL_SPAWN_EVENT, Config['simulator']['spawn_rate'][rate])
                    self.spawn(DoubleLane.Vertical)

                if event.type == pygame.QUIT:
                    game_over = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for double_lane in [DoubleLane.Horizontal, DoubleLane.Vertical]:
                        for rate in ['slow', 'medium', 'fast']:
                            if self.background_ctrl.spawn_rate_buttons[double_lane][rate].collidepoint(event.pos):
                                self.background_ctrl.set_spawn_rate(double_lane, rate)
                    # if self.background_ctrl.fuzzy_button.collidepoint(event.pos):
                    #     moving_averages = self.vehicle_ctrl.get_moving_averages_num_vehicles_behind_traffic()
                    #     print(self.calculate_fuzzy_score(moving_averages))

            self.background_ctrl.refresh_screen()
            self.background_ctrl.draw_road_markings()
            self.background_ctrl.draw_vehicle_count(self.vehicle_ctrl.counter)
            self.background_ctrl.draw_spawn_rate_buttons()
            self.background_ctrl.draw_light_durations()
            # self.background_ctrl.draw_fuzzy_button()

            self.traffic_ctrl.update_and_draw_traffic_lights()
            self.vehicle_ctrl.destroy_vehicles_outside_canvas()
            self.vehicle_ctrl.update_and_draw_vehicles()

            self.vehicle_ctrl.update_num_vehicles_behind_traffic()
            moving_averages = self.vehicle_ctrl.get_moving_averages_num_vehicles_behind_traffic()
            self.background_ctrl.draw_moving_averages(moving_averages)
            self.background_ctrl.draw_fuzzy_score(self.calculate_fuzzy_score(moving_averages),
                                                  self.traffic_ctrl.get_current_active_lane())

            pygame.display.update()
            self.clock.tick(Config['simulator']['frame_rate'])

    def calculate_fuzzy_score(self, moving_averages):
        traffic_state = self.traffic_ctrl.get_current_active_lane()
        if traffic_state == DoubleLane.Vertical:
            return self.traffic_ctrl.calculate_fuzzy_score(moving_averages[Lane.top_to_bottom], moving_averages[Lane.left_to_right], 0)
        elif traffic_state == DoubleLane.Horizontal:
            return self.traffic_ctrl.calculate_fuzzy_score(moving_averages[Lane.left_to_right], moving_averages[Lane.top_to_bottom], 0)

    def initialize(self):
        self.spawn(DoubleLane.Horizontal)
        self.spawn(DoubleLane.Vertical)
        # self.toggle_traffic()

    def start(self):
        pygame.init()
        pygame.display.set_caption(self.caption)

        self.initialize()
        self.main_loop()

        pygame.quit()
        quit()
