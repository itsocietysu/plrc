import cv2

from ImageProcessing.Stage import Stage


"""Binarize image and remove basical noize"""
class Contours(Stage):
    _name = 'contours'

    def __init__(self):
        Stage().__init__()

    def process(self, parent):
        """smooth the data"""
        res = []
        for img in self.img:
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cnt = cv2.findContours(gray_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
            res.append(cnt[0][0])

        self.img = res
        self.desc = self.desc
        self.update_status(Stage.STATUS_SUCCEEDED)
