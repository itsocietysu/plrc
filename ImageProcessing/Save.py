import json
import os

from bottle import template

from ImageProcessing.Stage import Stage

"""Upload processing data"""
class Save(Stage):
    _name = 'save'

    def __init__(self):
        Stage.__init__(self)

    def process(self, parent):
        """load the data"""
        self.update_status(Stage.STATUS_RUNNING)

        if not os.path.exists(parent.out_dir):
            os.makedirs(parent.out_dir)

        for i, _ in enumerate(self.desc):
            with open('%s/%d.json' % (parent.out_dir, i), 'wt') as fp:
                json.dump(_.to_dict(), fp, indent=2)

        with open('./Assets/templates/viewer_json.tpl', 'rt') as f:
            with open('%s/all_in_one.json' % parent.out_dir, 'wt') as fw:
                fw.write(template(f.read(), rooms=self.desc))

        self.update_status(Stage.STATUS_SUCCEEDED)
