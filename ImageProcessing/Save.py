import json
import os
import sdxf
from Entities.Point import Point
from Entities.Line import Line

from bottle import template

from ImageProcessing.Stage import Stage

"""Upload pro]
            room.walls = []
cessing data"""
class Save(Stage):
    _name = 'save'

    def __init__(self):
        Stage.__init__(self)

    def process(self, parent):
        """load the data"""
        self.update_status(Stage.STATUS_RUNNING)

        if self.dxf:
            self.save_in_dxf(self.dxf)

        if not os.path.exists(parent.out_dir):
            os.makedirs(parent.out_dir)

        for i, _ in enumerate(self.desc):
            with open('%s/%d.json' % (parent.out_dir, i), 'wt') as fp:
                json.dump(_.to_dict(), fp, indent=2)

        #with open('./Assets/templates/viewer_json.tpl', 'rt') as f:
        #    with open('%s/all_in_one.json' % parent.out_dir, 'wt') as fw:
        #        fw.write(template(f.read(), rooms=self.desc))

        self.update_status(Stage.STATUS_SUCCEEDED)

    def save_in_dxf(self, name):
        z = 0
        d = sdxf.Drawing()
        for room in self.desc:
            for wall in room.walls:
                line = wall.inner_part
                d.append(sdxf.Line(points=[(line.point_1.x, -line.point_1.y, z), (line.point_2.x, -line.point_2.y, z)]))
            for opening in room.openings:
                if opening._type == 'door':
                    for line in opening.placement:
                        d.append(sdxf.Line(points=[(line.point_1.x, -line.point_1.y, z),
                                                   (line.point_2.x, -line.point_2.y, z)],
                                           color=3))
                if opening._type == 'window':
                    for line in opening.placement:
                        d.append(sdxf.Line(points=[(line.point_1.x, -line.point_1.y, z),
                                                   (line.point_2.x, -line.point_2.y, z)],
                                           color=4))
                if opening._type == 'item':
                    rect = opening.placement[0]
                    p1 = rect.point_1
                    p3 = rect.point_2
                    p2 = Point(p1.x, p3.y)
                    p4 = Point(p3.x, p1.y)
                    lines = [Line(p1, p2), Line(p2, p3), Line(p3, p4), Line(p1, p4)]
                    for line in lines:
                        d.append(sdxf.Line(points=[(line.point_1.x, -line.point_1.y, z),
                                                   (line.point_2.x, -line.point_2.y, z)],
                                           color=5))

        d.saveas(name)
