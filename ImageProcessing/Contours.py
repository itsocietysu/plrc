import cv2
import numpy as np

from ImageProcessing.Stage import Stage


"""Binarize image and remove basical noize"""
class Contours(Stage):
    _name = 'contours'

    def __init__(self):
        Stage().__init__()
        self.w = 0
        self.h = 0

    def process(self, parent):
        """smooth the data"""
        self.w, self.h = parent.width, parent.height
        res = []
        for img in self.img:
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cnt = cv2.findContours(gray_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
            res.append(cnt[0][0])

        self.img = res
        self.desc = self.desc
        self.update_status(Stage.STATUS_SUCCEEDED)

    def visualize_stage(self):
        img = np.zeros((self.h, self.w, 3), np.uint8)
        cv2.drawContours(img, self.img, -1, (0, 0, 255), 3)
        return img

