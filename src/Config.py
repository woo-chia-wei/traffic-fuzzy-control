Config = {
    'vehicle': {
        'speed': 4,
        'safe_distance': 20,
        'body_length': 70,
        'body_width': 40
    },
    'simulator': {
        'screen_width': 800,
        'screen_height': 800,
        'bumper_distance': 10,
        'spawn_gap': 1000,  # millisecond
        'frame_rate': 30,
        'gap_between_traffic_switch': 1  # second
    },
    'colors': {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'dark_gray': (169, 169, 169),
        'dark_yellow': (204, 204, 0)
    },
    'traffic_light': {
        'red_light_duration': 3,  # second
        'yellow_light_duration': 1,  # second
        'green_light_duration': 5,  # second
        'distance_from_center': (60, 60),
        'body_height': 60,
        'body_width': 25
    }
}
