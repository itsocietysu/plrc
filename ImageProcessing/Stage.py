import cv2

from Renderer.Render import render_room

class Stage:
    _name = 'base'

    STATUS_FAILED = 666
    STATUS_SUCCEEDED = 7
    STATUS_INIT = 0
    STATUS_RUNNING = 1

    def __init__(self):
        self.img = None
        self.desc = None

    def pass_data(self, img, desc, parameters_file=None, graph=None, label_map=None, dxf=None):
        self.img = img
        self.desc = desc
        self.parameters_file = parameters_file
        self.graph = graph
        self.label_map = label_map
        self.status = 'initial'
        self.dxf = dxf

    def process(self, parent):
        raise NotImplemented('pure virtual call')

    def retrieve_data(self):
        return self.img, self.desc

    def update_status(self, new_status):
        self.status = int(new_status)

    def visualize_stage(self):
        if not (type(self.img) is list):
            self.img = [self.img]

        for i, _ in enumerate(self.img):
            try:
                cv2.imshow('stage_%s_%d' % (self._name, i), _)
                cv2.imshow('mapping_%s_%d' % (self._name, i), render_room(_.copy(), self.desc, line_w=1))
            except:
                continue

        cv2.waitKey(1)
