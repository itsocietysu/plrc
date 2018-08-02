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
    input_tags = None
    for _ in files:
        with open('%s%s' % (path, _)) as fp:
            nl = json.load(fp)
            if input_tags == None:
                input_tags = nl
            else:
                input_tags['walls'].extend(nl['walls'])
                input_tags['openings'].extend(nl['openings'])

    return input_tags



if __name__ == '__main__':
    room = Room().from_dict(read_apartments(sys.argv[1]))
    scale = 1.0
    if len(sys.argv) == 3:
        scale = float(sys.argv[2])

    x0, y0, h, w = room.get_bounding_rect()

    x0 *= scale
    y0 *= scale
    h *= scale
    w *= scale
    SHIFT *= scale

    img = np.zeros((int(w + SHIFT), int(h + SHIFT), 3), np.uint8)


    cv2.imshow('res', render_room(img, room, line_w=2, shift=(Point(SHIFT / 2 - x0 / 2, SHIFT / 2 - y0 / 2)), scale=scale))
    cv2.waitKey(0)