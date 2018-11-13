import sys

from ImageProcessing.NewLoad import Load
from ImageProcessing.Preprocessing import Preprocessing
from ImageProcessing.Components import Components
from ImageProcessing.Contours import Contours
from ImageProcessing.RoomConstructor import RoomConstructor
from ImageProcessing.OpeningPlacement import OpeningPlacement
from ImageProcessing.ObjectDetection import ObjectDetection
from ImageProcessing.NewSave import Save


from ImageProcessing.Pipeline import Pipeline


def run():
    pipeline_steps = [Load, ObjectDetection, Preprocessing, Components, Contours, RoomConstructor, OpeningPlacement, Save]

    pipeline = Pipeline(pipeline_steps, sys.argv[1], sys.argv[2], sys.argv[3], _verbose=False)
    pipeline.process()
    return desc_to_json(pipeline.desc)


def desc_to_json(desc):
    #аналогичная функция в Save
    return None
