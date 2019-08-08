import json
import numpy as np
import os
import sdxf

from bottle import template

from Entities.Line import Line
from Entities.Point import Point
from ImageProcessing.Stage import Stage
from Renderer.Render import render_room


class Save(Stage):
    """Save results"""
    _name = 'save'

    def __init__(self):
        Stage.__init__(self)
        self.shape = ()

    def process(self, parent):
        self.update_status(Stage.STATUS_RUNNING)
        self.shape = (parent.height, parent.width, 3)

        way = 'initial'

        self.save(parent.out_dir, way, self.desc)

        self.update_status(Stage.STATUS_SUCCEEDED)

    def save(self, out_dir, way, desc):

        if not os.path.exists(out_dir + '/' + way + '/'):
            os.makedirs(out_dir + '/' + way + '/')

        self.save_in_dxf(out_dir + '/' + way + '/' + '%s.dxf' % way, desc)

        for i, _ in enumerate(desc):
            with open('%s/%s/%d.json' % (out_dir, way, i), 'wt') as fp:
                json.dump(_.to_dict(), fp, indent=2)

        # with open('./Assets/templates/viewer_json.tpl', 'rt') as f:
        #    with open('%s/all_in_one.json' % parent.out_dir, 'wt') as fw:
        #        fw.write(template(f.read(), rooms=self.desc))

    def save_in_dxf(self, name, desc):
        z = 0
        d = sdxf.Drawing()
        for room in desc:
            if room.type == 'kitchen':
                wall = room.walls[0]
                p1 = wall.inner_part.point_1
                p2 = wall.inner_part.point_2
                point = (int(p1.x + (p2.x - p1.x) / 2) - 30, int(p1.y + (p2.x - p1.y) / 2))
                d.append(sdxf.Text(text='k', point=[point[0], -point[1], z], height=20))

            for wall in room.walls:
                line = wall.inner_part
                d.append(sdxf.Line(points=[(line.point_1.x, -line.point_1.y, z), (line.point_2.x, -line.point_2.y, z)]))

            for opening in room.openings:
                if opening._type == 'door':
                    for line in opening.placement:
                        d.append(sdxf.Line(points=[(line.point_1.x, -line.point_1.y, z),
                                                   (line.point_2.x, -line.point_2.y, z)],
                                           color=3))
                    continue

                if opening._type == 'window':
                    for line in opening.placement:
                        d.append(sdxf.Line(points=[(line.point_1.x, -line.point_1.y, z),
                                                   (line.point_2.x, -line.point_2.y, z)],
                                           color=4))
                    continue

                if opening._type == 'arch':
                    for line in opening.placement:
                        d.append(sdxf.Line(points=[(line.point_1.x, -int(line.point_1.y), z),
                                                   (line.point_2.x, -int(line.point_2.y), z)],
                                           color=2))
                    continue

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
                    continue
                if room.furniture:
                    for furniture in room.furniture:
                        rect = furniture.placement
                        p1 = rect.point_1
                        p3 = rect.point_2
                        p2 = Point(p1.x, p3.y)
                        p4 = Point(p3.x, p1.y)
                        lines = [Line(p1, p2), Line(p2, p3), Line(p3, p4), Line(p1, p4)]
                        for line in lines:
                            d.append(sdxf.Line(points=[(line.point_1.x, -line.point_1.y, z),
                                                       (line.point_2.x, -line.point_2.y, z)],
                                               color=6))

        d.saveas(name)

    def visualize_stage(self):
        img = np.zeros(self.shape, np.uint8)
        for r in self.desc:
            img = render_room(img, r, line_w=3)
        return img

