import cv2
import numpy as np

from ImageProcessing.Stage import Stage


"""Binarize image and remove basical noize"""
class Components(Stage):
    _name = 'components'

    MIN_SIZE = 1500
    MIN_FILL_RATE = 0.6
    ASPECT_RATIO = 5.0
    CONNECTIVITY = 4
    ERODE_KERNEL = np.ones((25, 25), np.uint8)

    def __init__(self):
        Stage().__init__()

    def process(self, parent):
        """smooth the data"""
        self.update_status(Stage.STATUS_RUNNING)

        output = cv2.connectedComponentsWithStats(self.img, Components.CONNECTIVITY, cv2.CV_32S)

        valuable_components = []
        for i in range(output[0]):
            if output[2][i][0] <= 5:
                continue

            if output[2][i][0] >= self.img.shape[1] - 1:
                continue

            if output[2][i][4] <= Components.MIN_SIZE:
                continue

            factor = float(output[2][i][4]) / (float(output[2][i][2] * output[2][i][3]))
            if factor <= Components.MIN_FILL_RATE:
                continue

            ratio = float(output[2][i][2]) / float(output[2][i][3])
            if ratio <= 0.0 or Components.ASPECT_RATIO <= ratio or Components.ASPECT_RATIO <= (1.0 / ratio):
               continue

            valuable_components.append(i)


        w, h = self.img.shape[0], self.img.shape[1]
        images = []
        for _ in valuable_components:
            new_img = np.zeros((w, h, 3), np.uint8)
            new_img[output[1] == _] = (0, 0, 255)
            images.append(new_img)

        self.img = []
        for _ in images:
            interm = cv2.dilate(_, Components.ERODE_KERNEL, iterations=1)
            self.img.append(cv2.erode(interm, Components.ERODE_KERNEL, iterations=1))


        #res = cv2.bitwise_or(self.img[0], self.img[0])

        #for _ in self.img:
        #    res = cv2.bitwise_or(res, _)

        #self.img = res
        self.desc = self.desc
        self.update_status(Stage.STATUS_SUCCEEDED)
