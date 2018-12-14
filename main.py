import sys

#from ImageProcessing.FindZones import FindZones
#from ImageProcessing.FurniturePlacement import FurniturePlacement
from ImageProcessing.Load import Load
from ImageProcessing.Preprocessing import Preprocessing
from ImageProcessing.Components import Components
from ImageProcessing.Contours import Contours
from ImageProcessing.RoomConstructor import RoomConstructor
from ImageProcessing.OpeningPlacement import OpeningPlacement
from ImageProcessing.ObjectDetection import ObjectDetection
from ImageProcessing.Save import Save
from ImageProcessing.RoomTypeDetection import RoomTypeDetection

from ImageProcessing.Pipeline import Pipeline

if __name__ == '__main__':
    pipeline_steps = [Load, ObjectDetection, Preprocessing, Components, Contours, RoomConstructor, OpeningPlacement,
                      RoomTypeDetection, Save]

    pipeline = Pipeline(pipeline_steps, sys.argv[1], sys.argv[2], sys.argv[3], _verbose=False)
    pipeline.process()
