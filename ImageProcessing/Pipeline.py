import cv2
import numpy as np

from ImageProcessing.Stage import Stage

window_name = 'process'
tr_alpha = 'alpha'
tr_stage = 'stage'
max_alpha = 100


def show_image(img):
    if img is None:
        return
    height, width, channels = img.shape
    rect = cv2.getWindowImageRect(window_name)
    h = rect[3]
    w = int(h * width / height)
    if w > rect[2]:
        w = rect[2]
        h = int(height / width * w)
    new_img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
    s = np.zeros((rect[3], rect[2], 3), np.uint8)
    s.fill(255)
    sy = int((rect[3] - h) / 2)
    sx = int((rect[2] - w) / 2)
    s[sy:sy + h, sx:sx + w] = new_img
    cv2.imshow(window_name, s)


def on_track_change(images, alpha, stage):
    if len(images) < stage or len(images) == 0 or images[stage] is None or images[0] is None:
        return

    alpha = alpha / max_alpha
    beta = (1.0 - alpha)
    dst = cv2.addWeighted(images[stage], alpha, images[0], beta, 0.0)
    show_image(dst)


def on_alpha_change(images, val):
    stage = cv2.getTrackbarPos(tr_stage, window_name)
    on_track_change(images, val, stage)


def on_stage_change(images, val):
    alpha = cv2.getTrackbarPos(tr_alpha, window_name)
    on_track_change(images, alpha, val)


class Pipeline:
    def __init__(self, _pipeline=[], _img=None, _desc=None, _graph=None, _label_map=None,
                 _verbose=False, _save_dxf=None, _config=None):
        self.pipeline = _pipeline
        self.img = _img
        self.desc = _desc
        self.verbose = _verbose
        self.width = None
        self.height = None
        self.out_dir = None
        self.config = _config
        self.graph = _graph
        self.label_map = _label_map
        self.dxf = _save_dxf

        self.cnt_stages = len(_pipeline)
        self.images = []
        self.window_name = window_name
        self.tr_alpha = tr_alpha
        self.tr_stage = tr_stage
        self.max_alpha = max_alpha

    def on_alpha_change(self, val):
        on_alpha_change(self.images, val)

    def on_stage_change(self, val):
        on_stage_change(self.images, val)

    def process(self):
        if not self.config:
            print("No configuration file\n")
            return
        for i, stage in enumerate(self.pipeline):
            _ = stage()
            _.pass_data(self.img, self.desc, self.graph, self.label_map, self.dxf)
            _.process(self)

            if _.status == Stage.STATUS_SUCCEEDED:
                self.img, self.desc = _.retrieve_data()

                if self.verbose:
                    try:
                        self.images.append(_.visualize_stage())
                        show_image(self.images[i])
                        cv2.setTrackbarPos(tr_stage, window_name, i)
                        cv2.waitKey(7)
                    except:
                        print("Cannot visualize stage %s" % _._name)

            if _.status == Stage.STATUS_FAILED:
                print('Stage %s, failed' % _._name)
                break

        if self.verbose:
            cv2.waitKey(0)
            cv2.destroyWindow(window_name)
