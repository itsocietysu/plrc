import cv2

from ImageProcessing.Stage import Stage


"""Upload processing data"""
class Load(Stage):
    _name = 'load'

    def __init__(self):
        Stage.__init__(self)

    def process(self, parent):
        """load the data"""

        def on_alpha_change(val):
            parent.on_alpha_change(val)

        def on_stage_change(val):
            parent.on_stage_change(val)

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

        if parent.verbose:
            cv2.namedWindow(parent.window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(parent.window_name, 1000, 800)
            cv2.createTrackbar(parent.tr_alpha, parent.window_name, parent.max_alpha, parent.max_alpha, on_alpha_change)
            cv2.createTrackbar(parent.tr_stage, parent.window_name, 0, parent.cnt_stages - 2, on_stage_change)

        self.update_status(Stage.STATUS_SUCCEEDED)

    def visualize_stage(self):
        return self.img
