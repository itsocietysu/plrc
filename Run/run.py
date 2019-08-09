from ImageProcessing.Components import Components
from ImageProcessing.Contours import Contours
from ImageProcessing.Load import Load
from ImageProcessing.ObjectDetection import ObjectDetection
from ImageProcessing.OpeningPlacement import OpeningPlacement
from ImageProcessing.Pipeline import Pipeline
from ImageProcessing.Preprocessing import Preprocessing
from ImageProcessing.RoomConstructor import RoomConstructor


def run(image, graph, label_map):
    pipeline_steps = [Load, ObjectDetection, Preprocessing, Components, Contours, RoomConstructor, OpeningPlacement]

    pipeline = Pipeline(pipeline_steps, _img=image, _graph=graph, _label_map=label_map, _verbose=False)
    pipeline.process()
    return pipeline.desc
