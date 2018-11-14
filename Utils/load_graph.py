import tensorflow as tf


def load_graph(graph_location):
    with tf.gfile.GFile(graph_location, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def, name='')
    return graph
