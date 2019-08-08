import json
import easygui
import os

from ImageProcessing.Components import Components
from ImageProcessing.Contours import Contours
from ImageProcessing.Load import Load
from ImageProcessing.ObjectDetection import ObjectDetection
from ImageProcessing.OpeningPlacement import OpeningPlacement
from ImageProcessing.Pipeline import Pipeline
from ImageProcessing.Preprocessing import Preprocessing
from ImageProcessing.RoomConstructor import RoomConstructor
from ImageProcessing.Save import Save
from Utils.label_map_reader import *
from Utils.load_graph import load_graph

graph = None
label_map = None
config = "./Assets/config.json"
pipeline_steps = [Load, ObjectDetection, Preprocessing, Components, Contours, RoomConstructor, OpeningPlacement, Save]


def open_config():
    global config
    with open(config, 'r') as f:
        c = json.load(f)
    config_path = os.path.split(config)[0]
    c['PARAMETERS_FILE'] = os.path.join(config_path, c['PARAMETERS_FILE'])
    c[ObjectDetection._name]['GRAPH_LOCATION'] = os.path.join(config_path, c[ObjectDetection._name]['GRAPH_LOCATION'])
    c[ObjectDetection._name]['LABEL_MAP_LOCATION'] = os.path.join(config_path,
                                                                  c[ObjectDetection._name]['LABEL_MAP_LOCATION'])
    config = c


def load():
    global graph, label_map
    graph = load_graph(config[ObjectDetection._name]['GRAPH_LOCATION'])
    label_map = label_map_to_dict(load_label_map_file(config[ObjectDetection._name]['LABEL_MAP_LOCATION']))


def process_image(path):
    pipeline = Pipeline(pipeline_steps, path, os.path.join('.', 'out', os.path.splitext(os.path.basename(path))[0]),
                        config['PARAMETERS_FILE'], _verbose=True, _graph=graph, _label_map=label_map, _config=config)
    pipeline.process()


if __name__ == '__main__':
    title = "Application functions"
    msg = "You can choose new picture for processing or exit application."
    ch_chp = 'Choose the picture'
    ch_exit = 'Exit'

    open_config()

    print("Upload graph of the neural network. Please wait.\n")
    load()

    while True:
        reply = easygui.buttonbox(msg=msg, title=title, choices=[ch_chp, ch_exit], cancel_choice=ch_exit)

        if reply != ch_chp:
            break

        img = easygui.fileopenbox(msg=ch_chp, default="*.png", filetypes=["*.png"])

        if img is None:
            continue

        process_image(img)
