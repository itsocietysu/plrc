import cv2
import numpy as np
import tensorflow as tf

from Entities.Room import Room
from Entities.Door import Door
from Entities.Window import Window
from Entities.Line import Line
from Entities.Point import Point
from Entities.Item import Item
from ImageProcessing.Stage import Stage
from Renderer.Render import render_room, COLOR_MAP
from Utils.label_map_reader import *
from Utils.load_graph import load_graph


CHOICE = {
    'door':         [Door, None],
    'window':       [Window, None],
    'balcony_door': [Door, None],
    'vent_channel': [Item, 'vent_channel'],
    'water_pipes':  [Item, 'water_pipes'],
    'toilet':       [Item, 'toilet'],
    'bathroom':     [Item, 'bathroom'],
    'shower_cabin': [Item, 'shower_cabin'],
    'sink':         [Item, 'sink'],
    'kitchen_sink': [Item, 'kitchen_sink'],
    'stove':        [Item, 'stove'],
    'washer':       [Item, 'washer'],
    'test':         [Item, 'test'],
    'test2':        [Item, 'test2'],
    'storeroom':    [Item, 'storeroom']
}


class ObjectDetection(Stage):
    """Detect objects by using of neural network"""
    _name = 'object_detection'
    _graph_location = './Assets/frozen_inference_graph.pb'
    _label_map_location = './Assets/label_map.pbtxt'

    def __init__(self):
        Stage.__init__(self)

    def proceed_with_boxes(self, graph):
        with tf.Session(graph=graph) as s:
            image_tensor = graph.get_tensor_by_name('image_tensor:0')
            detection_boxes = graph.get_tensor_by_name('detection_boxes:0')
            detection_scores = graph.get_tensor_by_name('detection_scores:0')
            detection_classes = graph.get_tensor_by_name('detection_classes:0')
            num_detections = graph.get_tensor_by_name('num_detections:0')

            img_np = np.expand_dims(self.img, axis=0)

            return s.run([detection_boxes, detection_scores, detection_classes, num_detections],
                         feed_dict={image_tensor: img_np})

    def process(self, parent):
        self.update_status(Stage.STATUS_RUNNING)

        if self.label_map:
            labels = self.label_map
        else:
            labels = label_map_to_dict(load_label_map_file(self._label_map_location))

        tf.logging.set_verbosity(tf.logging.WARN)

        if self.graph:
            graph = self.graph
        else:
            graph = load_graph(self._graph_location)

        (boxes, scores, classes, num) = self.proceed_with_boxes(graph)

        w, h = parent.width, parent.height
        room = Room(_openings=[])

        for i in range(int(num[0])):
            sy, sx, ey, ex = int(boxes[0][i][0] * h), \
                             int(boxes[0][i][1] * w), \
                             int(boxes[0][i][2] * h), \
                             int(boxes[0][i][3] * w)

            placement = Line(Point(sx, sy), Point(ex, ey))
            ch = CHOICE[labels[int(classes[0][i])]]
            t = ch[1]
            cl = ch[0]
            room.openings.append(cl(placement, t=t))
        self.desc = room

        self.update_status(Stage.STATUS_SUCCEEDED)

    def visualize_stage(self):
        line_w = 3
        img = render_room(self.img.copy(), self.desc, line_w=line_w)

        for o in self.desc.openings:
            p1 = o.placement[0].point_1
            p2 = o.placement[0].point_2
            if o._type == 'item':
                color = COLOR_MAP[o.item_type]
            else:
                color = COLOR_MAP[o._type]
            cv2.rectangle(img, (p1.x, p1.y), (p2.x, p2.y), color, line_w)

        return img
