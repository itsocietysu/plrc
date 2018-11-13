import cv2
from ImageProcessing.Stage import Stage

class Pipeline:
    def __init__(self, _pipeline=[], _img=None, _desc=None, parameters=None, _graph=None,_label_map=None, _verbose=False):
        self.pipeline = _pipeline
        self.img = _img
        self.desc = _desc
        self.verbose = _verbose
        self.width = None
        self.height = None
        self.out_dir = None
        self.parameters_file = parameters
        self.graph = _graph
        self.label_map = _label_map

    def process(self):
        for stage in self.pipeline:
            _ = stage()
            _.pass_data(self.img, self.desc, self.parameters_file)
            _.process(self)

            if _.status == Stage.STATUS_SUCCEEDED:
                self.img, self.desc = _.retrieve_data()

                if self.verbose:
                    _.visualize_stage()

            if _.status == Stage.STATUS_FAILED:
                raise Exception('Stage %s, failed' % _._name)

        if self.verbose:
            cv2.waitKey(0)
