import cv2
import numpy as np
import json
import os
import sys

from Entities.Room import Room
from Entities.Point import Point
from Renderer.Render import render_room

H = 1000
W = 1000
SHIFT = 100

img = np.zeros((H, W, 3), np.uint8)

def read_apartments(path):
    files = os.listdir(path)
    input_tags = []
    for _ in filter(lambda x: x != 'all_in_one.json', files):
        with open('%s%s' % (path, _)) as fp:
            nl = json.load(fp)
            input_tags.append(nl)

    return input_tags



if __name__ == '__main__':
    rooms = [Room().from_dict(_) for _ in read_apartments(sys.argv[1])]
    scale = 1.0
    if len(sys.argv) == 3:
        scale = float(sys.argv[2])

    x0, y0, x1, y1 = 10000, 10000, 0, 0
    for _ in rooms:
        _x0, _y0, _x1, _y1 = _.get_bounding_rect()
        x0, y0, x1, y1 = min(x0, _x0), min(y0, _y0), max(x1, _x1), max(y1, _y1)

    x0 *= scale
    y0 *= scale
    x1 *= scale
    y1 *= scale
    SHIFT *= scale

    img = np.zeros((int(y1 + SHIFT), int(x1 + SHIFT), 3), np.uint8)

    for _ in rooms:
        cv2.imshow('res', render_room(img, _, line_w=2, shift=(Point(SHIFT / 2 - x0 / 2, SHIFT / 2 - y0 / 2)), scale=scale))

    cv2.waitKey(0)