import cv2
import numpy as np
import sys
import json

H = 1000
W = 1000
SCALER = 1
SHIFT = 100

img = np.zeros((H, W, 3), np.uint8)

input_tags = None
for i in range(7):
    with open('%d.json' % i) as fp:
        nl = json.load(fp)
        if input_tags == None:
            input_tags = nl
        else:
            input_tags['walls'].extend(nl['walls'])
            input_tags['openings'].extend(nl['openings'])


color_mapping = {
    'door': (0, 255, 0),
    'balcony_door': (0, 255, 0),
    'balcony_wall': (100, 50, 200),
    'window': (255, 0, 0),
    'vent_channel': (255, 255, 0),
    'wall': (0, 0, 255)
}

def process_line(line_obj):
    if 'type' in line_obj and line_obj['type'] == 'line':
        return [(int(line_obj['point_1']['x']) / SCALER + SHIFT, int(line_obj['point_1']['y']) / SCALER + SHIFT),
                (int(line_obj['point_2']['x']) / SCALER + SHIFT, int(line_obj['point_2']['y']) / SCALER + SHIFT)]

    return None

def wall_lambda(obj):
    if 'type' in obj and obj['type'] == 'wall' and 'inner_part' in obj:
        wall = obj['inner_part']
        return process_line(wall)

    return None

def door_lambda(obj):
    if 'type' in obj and obj['type'] == 'door' and 'placement' in obj:
        plc = obj['placement']
        return process_line(plc)

    return None

def window_lambda(obj):
    if 'type' in obj and obj['type'] == 'window' and 'placement' in obj:
        wnd = obj['placement']
        return process_line(wnd)

    return None

processing_mapper = {
    'wall': wall_lambda,
    'door': door_lambda,
    'window': window_lambda,
}


for _ in input_tags['walls']:
    wall = processing_mapper[_['type']](_)
    cv2.rectangle(img, wall[0], wall[1], color_mapping[_['type']], 2)

for _ in input_tags['openings']:
    obj = processing_mapper[_['type']](_)
    cv2.rectangle(img, obj[0], obj[1], color_mapping[_['type']], 2)


cv2.imshow('res', img)
cv2.waitKey(0)