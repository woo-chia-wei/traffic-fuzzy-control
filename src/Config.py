import numpy as np

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
        'red': (255, 0, 0),
        'yellow': (255, 255, 0),
        'green': (0, 255, 0)
    },
    'traffic_light': {
        'red_light_duration': 5,  # second
        'yellow_light_duration': 1,  # second
        'green_light_duration': 5,  # second
        'distance_from_center': (40, 10),
        'body_height': 30,
        'body_width': 20
    },
    'background': {
        'road_marking_width': 3,
        'road_marking_alternate_lengths': (30, 20),
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
                'few': [-4, 0, 4],
                'small': [0, 4, 8],
                'medium': [4, 8, 12],
                'many': [8, 12, 16]
            },
            'arriving_green_light': {
                'few': [-4, 0, 4],
                'small': [0, 4, 8],
                'medium': [4, 8, 12],
                'many': [8, 12, 16]
            },
            'extension': {
                'zero': [0, 0, 5],
                'short': [0, 5, 10],
                'medium': [5, 10, 15],
                'long': [10, 15, 20]
            }
        }
    }
}
