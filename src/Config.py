import numpy as np

Config = {
    'vehicle': {
        'speed': 5,
        'safe_distance': 5,
        'body_length': 25,
        'body_width': 15,
        'safe_spawn_factor': 1.1
    },
    'simulator': {
        'screen_width': 800,
        'screen_height': 800,
        'bumper_distance': 5,
        'spawn_rate': {
            'fast': 400,  # millisecond
            'medium': 1500,  # millisecond
            'slow': 3500,  # millisecond
        },
        'frame_rate': 30,
        'gap_between_traffic_switch': 2,  # second
        'moving_averages_period': 1,  # second
        'static_duration': 1,  # second
        'seconds_before_extension': 1,  # second
        'fuzzy_notification_duration': 5  #second
    },
    'colors': {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'dark_gray': (169, 169, 169),
        'traffic_yellow': (250, 210, 1),
        'traffic_green': (34, 139, 94),
        'traffic_red': (184, 29, 19),
        'red': (255, 0, 0),
        'yellow': (255, 255, 0),
        'green': (0, 255, 0)
    },
    'traffic_light': {
        'red_light_duration': 10,  # second
        'yellow_light_duration': 1.5,  # second
        'green_light_duration': 10,  # second
        'distance_from_center': (40, 10),
        'body_height': 30,
        'body_width': 20
    },
    'background': {
        'road_marking_width': 2,
        'road_marking_alternate_lengths': (20, 10),
        'road_marking_gap_from_yellow_box': 10,
        'yellow_box_junction': (50, 50, 50, 50),  # top, right, bottom, left
    },
    'fuzzy': {
        'range': {
            'behind_red_light': np.arange(-4, 17, 1),
            'arriving_green_light': np.arange(-4, 17, 1),
            'extension': np.arange(0, 21, 1)
        },
        'membership_function': {
            'behind_red_light': {
                'few': [0, 0, 3],
                'small': [0, 3, 6],
                'medium': [3, 6, 9],
                'many': [6, 9, 12]
            },
            'arriving_green_light': {
                'few': [0, 0, 3],
                'small': [0, 3, 6],
                'medium': [3, 6, 9],
                'many': [6, 9, 12]
            },
            'extension': {
                'zero': [0, 0, 0],
                'short': [0, 2, 4],
                'medium': [2, 4, 6],
                'long': [4, 6, 8]
            }
        }
    }
}
