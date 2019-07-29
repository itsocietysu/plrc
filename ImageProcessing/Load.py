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

        self.img = cv2.imread(self.img)
        parent.img = self.img
        parent.width = self.img.shape[1]
        parent.height = self.img.shape[0]
        parent.out_dir = self.desc
        f = open(self.parameters_file)
        parent.parameters_file = []
        if f:
            for line in f:
                parent.parameters_file.append(line)
            f.close()

        self.update_status(Stage.STATUS_SUCCEEDED)

    def visualize_stage(self):
        return self.img
