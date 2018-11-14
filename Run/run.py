
from ImageProcessing.NewLoad import Load
from ImageProcessing.Preprocessing import Preprocessing
from ImageProcessing.Components import Components
from ImageProcessing.Contours import Contours
from ImageProcessing.RoomConstructor import RoomConstructor
from ImageProcessing.OpeningPlacement import OpeningPlacement
from ImageProcessing.ObjectDetection import ObjectDetection
from ImageProcessing.NewSave import Save


from ImageProcessing.Pipeline import Pipeline


def run(image, graph, label_map):
    pipeline_steps = [Load, ObjectDetection, Preprocessing, Components, Contours, RoomConstructor, OpeningPlacement, Save]

    pipeline = Pipeline(pipeline_steps, _img=image, _graph=graph, _label_map=label_map, _verbose=False)
    pipeline.process()
    return pipeline.desc
