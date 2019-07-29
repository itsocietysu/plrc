import sys
import os

from ImageProcessing.FindZones import FindZones
from ImageProcessing.FurniturePlacement import FurniturePlacement
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

import easygui

from Utils.label_map_reader import load_label_map_file, label_map_to_dict
from Utils.load_graph import load_graph

graph = None
label_map = None
parameters = "./Assets/parameters.txt"
pipeline_steps = [Load, ObjectDetection, Preprocessing, Components, Contours, RoomConstructor, OpeningPlacement, Save]
#                  RoomTypeDetection, FindZones, FurniturePlacement]


def load():
    global graph, label_map
    graph = load_graph('./Assets/frozen_inference_graph.pb')
    label_map = label_map_to_dict(load_label_map_file('./Assets/label_map.pbtxt'))


def process_image(path):
    pipeline = Pipeline(pipeline_steps, path, os.path.join('.', 'out', os.path.splitext(os.path.basename(path))[0]),
                        parameters, _verbose=False, _graph=graph, _label_map=label_map)
    pipeline.process()


if __name__ == '__main__':
    title = "Application functions"
    msg = "You can choose new picture for processing or exit application."
    ch_chp = 'Choose the picture'
    ch_exit = 'Exit'

    print("Upload graph of the neural network. Please wait.\n")
    load()

    while True:
        reply = easygui.buttonbox(msg=msg, title=title, choices=[ch_chp, ch_exit], cancel_choice=ch_exit)

        if reply == ch_exit:
            break

        img = easygui.fileopenbox(msg=ch_chp, default="*.png", filetypes=["*.png"])

        if img is None:
            continue

        process_image(img)
