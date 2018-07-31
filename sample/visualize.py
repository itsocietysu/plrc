import cv2 
import sys
import json

img = cv2.imread(sys.argv[1])

with open(sys.argv[2]) as fp:
	input_tags = json.load(fp)

color_mapping = {
    'door': (0, 0, 255),
    'balcony_door': (0, 255, 0),
    'balcony_wall': (100, 50, 200),
    'window': (255, 0, 0),
    'vent_channel': (255, 255, 0)
}


for _ in input_tags['objects']:
    c = _['coords']
    s = (c[0], c[1])
    e = (c[2], c[3])
    cv2.rectangle(img, s, e, color_mapping[_['tag']], 2)
    print(_)

cv2.imshow('res', img)
cv2.waitKey(0)