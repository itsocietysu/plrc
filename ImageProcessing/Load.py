import cv2
import json

from ImageProcessing.Stage import Stage

from Entities.Room import Room


"""Upload processing data"""
class Load(Stage):
    _name = 'load'

    def __init__(self):
        Stage.__init__(self)

    def process(self, parent):
        """load the data"""
        self.update_status(Stage.STATUS_RUNNING)

        self.img = cv2.imread(self.img)
        parent.width = self.img.shape[1]
        parent.height = self.img.shape[0]

        with open(self.desc, 'rt') as fp:
            self.desc = Room().from_dict(json.load(fp))

        self.update_status(Stage.STATUS_SUCCEEDED)