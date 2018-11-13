

from ImageProcessing.Stage import Stage

"""Upload processing data"""
class Save(Stage):
    _name = 'save'

    def __init__(self):
        Stage.__init__(self)

    def process(self, parent):
        """load the data"""
        self.update_status(Stage.STATUS_RUNNING)


        self.update_status(Stage.STATUS_SUCCEEDED)