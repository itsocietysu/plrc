import cv2

from ImageProcessing.Stage import Stage


class Preprocessing(Stage):
    """Binarize image and remove basical noize"""
    _name = 'preprocessing'

    GAUSS_CORE = (5, 5)
    
    def __init__(self):
        Stage().__init__()

    def process(self, parent):
        """smooth the data"""
        self.update_status(Stage.STATUS_RUNNING)

        smooth = cv2.GaussianBlur(self.img, Preprocessing.GAUSS_CORE, 0)

        gray = cv2.cvtColor(smooth, cv2.COLOR_BGR2GRAY)

        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        self.img = binary
        self.desc = self.desc
        self.update_status(Stage.STATUS_SUCCEEDED)

    def visualize_stage(self):
        return cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
