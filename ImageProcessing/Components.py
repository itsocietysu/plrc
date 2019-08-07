import cv2
import numpy as np

from ImageProcessing.Stage import Stage


class Components(Stage):
    """Find rooms"""
    _name = 'components'

    def __init__(self):
        Stage().__init__()
        self.shape = ()

    def process(self, parent):
        self.update_status(Stage.STATUS_RUNNING)

        min_fill_rate = parent.config[self._name]['MIN_FILL_RATE']
        aspect_ratio = parent.config[self._name]['ASPECT_RATIO']
        connectivity = parent.config[self._name]['CONNECTIVITY']
        min_size = int(parent.config[self._name]['MIN_SIZE'] * parent.width * parent.height)
        erode_kernel = np.ones(tuple(parent.config[self._name]['ERODE_KERNEL']), np.uint8)
        self.shape = (parent.height, parent.width, 3)

        output = cv2.connectedComponentsWithStats(self.img, connectivity, cv2.CV_32S)

        h, w = self.img.shape[0], self.img.shape[1]
        valuable_components = []
        for i in range(output[0]):
            if output[2][i][0] <= 5:
                continue

            if output[2][i][0] >= w - 1:
                continue

            if output[2][i][4] <= min_size:
                continue

            factor = float(output[2][i][4]) / (float(output[2][i][2] * output[2][i][3]))
            if factor <= min_fill_rate:
                continue

            ratio = float(output[2][i][2]) / float(output[2][i][3])
            if ratio <= 0.0 or aspect_ratio <= ratio or aspect_ratio <= (1.0 / ratio):
                continue

            valuable_components.append(i)

        images = []
        for _ in valuable_components:
            new_img = np.zeros((h, w, 3), np.uint8)
            new_img[output[1] == _] = (0, 0, 255)
            images.append(new_img)

        self.img = []
        for _ in images:
            interm = cv2.dilate(_, erode_kernel, iterations=1)
            self.img.append(cv2.erode(interm, erode_kernel, iterations=1))

        self.desc = self.desc
        self.update_status(Stage.STATUS_SUCCEEDED)

    def visualize_stage(self):
        img = np.zeros(self.shape, np.uint8)
        for i in self.img:
            img += i
        return img
