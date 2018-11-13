import cv2

from ImageProcessing.Stage import Stage


"""Upload processing data"""
class Load(Stage):
    _name = 'load'

    def __init__(self):
        Stage.__init__(self)

    def process(self, parent):
        """load the data"""
        self.update_status(Stage.STATUS_RUNNING)

        parent.img = self.img
        parent.width = self.img.shape[1]
        parent.height = self.img.shape[0]

        self.update_status(Stage.STATUS_SUCCEEDED)
