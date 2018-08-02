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
SCALER = 3
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

    w, h = room.get_bounding_rect()
    img = np.zeros((int(w + 2 * SHIFT), int(h + 2 * SHIFT), 3), np.uint8)


    cv2.imshow('res', render_room(img, room, line_w=2))
    cv2.waitKey(0)