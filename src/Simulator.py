import pygame
from src.Common import Lane
from src.Config import Config
from src.Controller.VehicleController import VehicleController
from src.Controller.BackgroundController import BackgroundController


class Simulator:
    def __init__(self, caption):
        self.caption = caption
        self.surface = pygame.display.set_mode((Config['simulator']['screen_width'],
                                                Config['simulator']['screen_height']))
        self.vehicle_ctrl = VehicleController(self.surface)
        self.traffics = self.vehicle_ctrl.traffic_lights
        self.background_ctrl = BackgroundController(self.surface, self.traffics)
        self.clock = pygame.time.Clock()
        self.colors = Config['colors']

    def spawn(self):
        self.vehicle_ctrl.create_vehicle(Lane.left_to_right)
        self.vehicle_ctrl.create_vehicle(Lane.right_to_left)
        self.vehicle_ctrl.create_vehicle(Lane.bottom_to_top)
        self.vehicle_ctrl.create_vehicle(Lane.top_to_bottom)

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

            self.background_ctrl.draw_all()

            self.vehicle_ctrl.update_and_draw_traffic_lights()
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
