import json

from ImageProcessing.Stage import Stage

"""Upload processing data"""
class Save(Stage):
    _name = 'save'

    def __init__(self):
        Stage.__init__(self)

    def process(self, parent):
        """load the data"""
        self.update_status(Stage.STATUS_RUNNING)

        for i, _ in enumerate(self.desc):
            with open('%s/%d.json' % (parent.out_dir, i), 'wt') as fp:
                json.dump(_.to_dict(), fp, indent=2)

        self.update_status(Stage.STATUS_SUCCEEDED)