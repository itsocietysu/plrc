import tensorflow as tf
import numpy as np

from ImageProcessing.Stage import Stage

from Entities.Room import Room
from Entities.Door import Door
from Entities.Window import Window
from Entities.Line import Line
from Entities.Point import Point
from Entities.Item import Item

from Utils.label_map_reader import *


"""Upload processing data"""
class ObjectDetection(Stage):
    _name = 'object_detection'
    _graph_location = './Assets/frozen_inference_graph.pb'
    _label_map_location = './Assets/label_map.pbtxt'

    def __init__(self):
        Stage.__init__(self)

    def load_graph(self):
        with tf.gfile.GFile(self._graph_location, "rb") as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

        with tf.Graph().as_default() as graph:
            tf.import_graph_def(graph_def, name='')
        return graph

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
        """load the data"""
        self.update_status(Stage.STATUS_RUNNING)

        labels = label_map_to_dict(load_label_map_file(self._label_map_location))

        tf.logging.set_verbosity(tf.logging.WARN)
        graph = self.load_graph()

        (boxes, scores, classes, num) = self.proceed_with_boxes(graph)

        w, h = parent.width, parent.height
        room = Room()

        choice = {
            'door': [Door, None],
            'window': [Window, None],
            'balcony_door': [Door, None],
            'vent_channel': [Item, 'vent_channel'],
            'water_pipes': [Item, 'water_pipes'],
            'toilet': [Item, 'toilet'],
            'bathroom': [Item, 'bathroom'],
            'shower_cabin': [Item, 'shower_cabin'],
            'sink': [Item, 'sink'],
            'kitchen_sink': [Item, 'kitchen_sink'],
            'stove': [Item, 'stove'],
            'washer': [Item, 'washer'],
            'test': [Item, 'test'],
            'test2': [Item, 'test2'],
            'storeroom': [Item, 'storeroom']
        }

        for i in range(int(num[0])):
            sy, sx, ey, ex = int(boxes[0][i][0] * h), \
                             int(boxes[0][i][1] * w), \
                             int(boxes[0][i][2] * h), \
                             int(boxes[0][i][3] * w)

            placement = Line(Point(sx, sy), Point(ex, ey))
            cl = choice[labels[int(classes[0][i])]]
            t = cl[1]
            cl = cl[0]
            room.openings.append(cl(placement, t=t))

        self.desc = room

        self.update_status(Stage.STATUS_SUCCEEDED)
