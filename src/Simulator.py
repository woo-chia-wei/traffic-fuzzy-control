import pygame
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
        self.colors = Config['colors']

    def spawn(self):
        self.spawn_single_vehicle(Lane.left_to_right)
        self.spawn_single_vehicle(Lane.right_to_left)
        self.spawn_single_vehicle(Lane.bottom_to_top)
        self.spawn_single_vehicle(Lane.top_to_bottom)

    def spawn_single_vehicle(self, lane: Lane):
        self.vehicle_ctrl.create_vehicle(lane, self.traffic_ctrl.traffic_lights[lane])

    def loop(self):
        game_over = False
        SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(SPAWN_EVENT, Config['simulator']['spawn_gap'])

        while not game_over:
            for event in pygame.event.get():
                if event.type == SPAWN_EVENT:
                    self.spawn()
                if event.type == pygame.QUIT:
                    game_over = True

            self.background_ctrl.refresh_screen()
            self.background_ctrl.draw_road_markings()
            self.background_ctrl.draw_vechile_count(self.vehicle_ctrl.counter)

            self.traffic_ctrl.update_and_draw_traffic_lights()
            self.vehicle_ctrl.update_and_draw_vehicles()

            pygame.display.update()
            self.clock.tick(Config['simulator']['frame_rate'])

    def start(self):
        pygame.init()
        pygame.display.set_caption(self.caption)
        self.spawn()
        self.loop()
        pygame.quit()
        quit()
