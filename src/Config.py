Config = {
    'vehicle': {
        'speed': 5,
        'safe_distance': 5,
        'body_length': 35,
        'body_width': 25,
        'safe_spawn_factor': 1.1
    },
    'simulator': {
        'screen_width': 800,
        'screen_height': 800,
        'bumper_distance': 5,
        'spawn_rate': {
            'fast': 500,  # millisecond
            'medium': 900,  # millisecond
            'slow': 1200,  # millisecond
        },
        'frame_rate': 30,
        'gap_between_traffic_switch': 2  # second
    },
    'colors': {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'dark_gray': (169, 169, 169),
        'traffic_yellow': (250, 210, 1),
        'red': (255, 0, 0)
    },
    'traffic_light': {
        'red_light_duration': 9999999,  # second
        'yellow_light_duration': 1,  # second
        'green_light_duration': 9999999,  # second
        'distance_from_center': (60, 60),
        'body_height': 60,
        'body_width': 25
    },
    'background': {
        'road_marking_width': 3,
        'road_marking_alternate_lengths': (30, 20),
        'road_marking_gap_from_yellow_box': 10,
        'yellow_box_junction': (50, 50, 50, 50),  # top, right, bottom, left
    }
}
