import cv2
import numpy as np

from Entities.Room import Room
from Entities.Wall import Wall
from Entities.Line import Line
from Entities.Point import Point
from Entities.Arch import Arch
from ImageProcessing.Stage import Stage
from Renderer.Render import render_room


WALL_MAP = {
            'space':        0,
            'wall':         1,
            'bearing_wall': 2,
            'outer_wall':   3
}

WALL_COLOR_MAP = {
            'wall':         (0, 255, 0),     # green
            'bearing_wall': (255, 0, 0),     # blue
            'outer_wall':   (0, 0, 255)      # red
}


class RoomConstructor(Stage):
    """Construct rooms by it contours and define type of walls"""
    _name = 'room_constructor'

    def __init__(self):
        Stage().__init__()
        self.shape = ()

    def process(self, parent):
        self.update_status(Stage.STATUS_RUNNING)

        self.TH = 0.1
        if parent.height < 1000 and parent.width < 1000:
            self.TH = 0.25
        self.WALL_DIFF = 0.000001 * max(parent.height, parent.width)
        self.R_OUTER_WALL = int(0.2 * min(parent.width, parent.height))
        self.R_BEARING_WALL = int(self.R_OUTER_WALL / 8)
        self.R_WALL = int(self.R_OUTER_WALL / 8) * 3
        self.R_MAP = {
            'wall': self.R_WALL,
            'bearing_wall': self.R_BEARING_WALL,
            'outer_wall': self.R_OUTER_WALL
        }
        self.shape = (parent.height, parent.width, 3)

        res = []
        for i, cnt in enumerate(self.img):
            room = Room([], [])
            l = len(cnt) - 1
            prev = cnt[l]
            room.walls = []

            for curr in cnt:
                wall = Wall(Line(Point(prev[0][0], prev[0][1]), Point(curr[0][0], curr[0][1])))
                room.walls.append(wall)
                prev = curr

            res.append(room)

        self.align_walls(res)
        self.define_walls_type(res)
        # self.choose_scale(res)
        # self.add_arches(res)

        self.img = res
        self.desc = self.desc
        self.update_status(Stage.STATUS_SUCCEEDED)

    @staticmethod
    def choose_wall(res, point):
        for _ in res:
            for wall in _.walls:
                if wall.inner_part.is_point_of_line(point):
                    return wall
        return None

    @staticmethod
    def align_walls(res):

        def align_wall(room_index, walls_index):
            prev_wall = room.walls[room_index].inner_part
            curr_wall = new_walls[walls_index].inner_part

            angle = prev_wall.angle_between(curr_wall)
            if angle < max_angle:
                pos = Line(new_walls[walls_index].inner_part.point_1, room.walls[room_index].inner_part.point_2)
                wall = Wall(pos)
                new_walls[walls_index] = wall
            else:
                new_walls.append(room.walls[room_index])

        max_angle = 5
        for room in res:
            num_of_walls = len(room.walls)
            new_walls = [room.walls[-1]]
            for i in range(num_of_walls - 1):
                align_wall(i, -1)
            align_wall(num_of_walls - 1, 0)
            room.walls = new_walls

    def choose_scale(self, res):
        if self.parameters_file:
            f = self.parameters_file
            point = Point(int(f[1]), int(f[2]))
            size = int(f[3])
            wall = self.choose_wall(res, point)

            if wall:
                w = wall.inner_part
                wall_len = pow(pow((w.point_2.x - w.point_1.x), 2) + pow((w.point_2.y - w.point_1.y), 2), 1 / 2)
                pix_to_m = size / wall_len
                for room in res:
                    for wall in room.walls:
                        p1 = wall.inner_part.point_1
                        p2 = wall.inner_part.point_2
                        wall_len = pow(pow((p2.x - p1.x), 2) + pow((p2.y - p1.y), 2), 1 / 2)
                        wall.size = pix_to_m * wall_len

    def add_arches(self, res):
        if self.parameters_file:
            f = self.parameters_file
            if len(f) > 5:
                i = 5
                line = Line(Point(f[i], f[i + 1]), Point(f[i + 2], f[i + 3]))
                arch = Arch(line)
                res[0].openings.append(arch)
            else:
                return None
        else:
            return None

    """For detecting wall types"""
    def define_walls_type(self, res):

        def define_type():
            not_bearing = 0
            bearing = 0
            outer = 0
            for x in range(sx - 1, ex + 1, 1):
                for y in range(sy - 1, ey + 1, 1):
                    wall_type = wall_map_img[y][x]

                    if np.array_equal(wall_type, np.asarray(WALL_COLOR_MAP['wall'])):
                        not_bearing += 1

                    if np.array_equal(wall_type, np.asarray(WALL_COLOR_MAP['bearing_wall'])):
                        bearing += 1

                    if np.array_equal(wall_type, np.asarray(WALL_COLOR_MAP['outer_wall'])):
                        outer += 1

            w_max = max(not_bearing, bearing, outer)
            if w_max != 0:
                if w_max == outer:
                    return Wall.WALL_TYPE_MAP['outer_wall']
                if w_max == bearing:
                    return Wall.WALL_TYPE_MAP['bearing_wall']
                if w_max == not_bearing:
                    return Wall.WALL_TYPE_MAP['wall']

            return Wall.WALL_TYPE_MAP['wall']

        img = self.fill_rooms(res)

        dt = cv2.distanceTransform(img, cv2.DIST_L2, 3)
        mask = cv2.normalize(dt, dt, 0, 1., cv2.NORM_MINMAX)

        outer_walls_mask = np.copy(mask)
        r, outer_walls = cv2.threshold(outer_walls_mask, self.TH, 1, cv2.THRESH_BINARY)
        outer_walls_mask[outer_walls == 1] = 0

        wall_map = self.create_wall_map(outer_walls_mask)
        wall_map_img = self.wall_map_color(wall_map)

        for room in res:
            for wall in room.walls:
                sx = int(min(wall.inner_part.point_1.x, wall.inner_part.point_2.x))
                ex = int(max(wall.inner_part.point_1.x, wall.inner_part.point_2.x))
                sy = int(min(wall.inner_part.point_1.y, wall.inner_part.point_2.y))
                ey = int(max(wall.inner_part.point_1.y, wall.inner_part.point_2.y))
                wall.wall_type = define_type()

        return wall_map_img

    @staticmethod
    def fill_rooms(res):
        shift = 100
        x0, y0, x1, y1 = 10000, 10000, 0, 0
        for _ in res:
            _x0, _y0, _x1, _y1 = _.get_bounding_rect()
            x0,  y0,  x1,  y1 = min(x0, _x0), min(y0, _y0), max(x1, _x1), max(y1, _y1)

        img = np.full((int(y1 + shift), int(x1 + shift)), np.uint8(255))
        contours = []
        for _ in res:
            cnt = []
            for wall in _.walls:
                p1 = wall.inner_part.point_1.int_tuple()
                cnt.append(np.array([np.array(p1)]))
            contours.append(np.array(cnt))

        contours = np.array(contours)
        cv2.drawContours(img, contours, -1, 0, -1)
        return img

    @staticmethod
    def find_local_maxima(str):
        maxima = []
        maxima_ids = []
        i = 0
        while i < len(str):
            if str[i] > 0:
                maximum = 0
                idx = i
                while str[i] > 0 and i < len(str) - 1:
                    if str[i] > maximum:
                        maximum = str[i]
                        idx = i
                    i += 1
                maxima.append(maximum)
                maxima_ids.append(idx)
            i += 1
        return maxima_ids, maxima

    def classificate_walls(self, local_maxima):

        def classificate(local_max):
            max_difference = 0
            ind_max_difference = len(local_max) - 1
            for i in range(len(local_max) - 1):
                difference = local_max[i + 1] - local_max[i]
                if difference > max_difference and difference > self.WALL_DIFF:
                    max_difference = difference
                    ind_max_difference = i + 1
            return ind_max_difference

        start_idx_outer = classificate(local_maxima)
        start_idx_bearing = classificate(local_maxima[:start_idx_outer])
        return start_idx_outer, start_idx_bearing

    @staticmethod
    def wall_type(wall, min_outer_wall, min_bearing_wall):
        if wall == 0:
            return WALL_MAP['space']
        if wall > min_outer_wall:
            return WALL_MAP['outer_wall']
        if wall > min_bearing_wall:
            return WALL_MAP['bearing_wall']
        return WALL_MAP['wall']

    def create_maxima_map(self, mask):
        local_maxima = []
        maxima_map = []
        for str in mask:
            ids, str_local_maxima = self.find_local_maxima(str)

            maxima_map_str = np.zeros(np.shape(mask)[1])
            maxima_map_str[ids] = str_local_maxima

            maxima_map.append(maxima_map_str)

            for max in str_local_maxima:
                local_maxima.append(max)

        return local_maxima, maxima_map

    def wall_map_color(self, wall_map):

        def draw_walls(type):
            i = 0
            for str in wall_map:
                j = 0
                for point in str:
                    if point != WALL_MAP['space']:
                        if point == WALL_MAP[type]:
                            cv2.circle(wall_map_img, (j, i), self.R_MAP[type], WALL_COLOR_MAP[type], thickness=-1)
                    j += 1
                i += 1

        wall_map_img = np.zeros((np.shape(wall_map)[0], np.shape(wall_map)[1], 3), np.uint8)
        draw_walls('wall')
        draw_walls('bearing_wall')
        draw_walls('outer_wall')
        return wall_map_img

    def define_type_of_walls(self, maxima_map, min_outer_wall, min_bearing_wall):
        wall_map = []
        for str in maxima_map:
            str_new_map = []
            for wall in str:
                str_new_map.append(self.wall_type(wall, min_outer_wall, min_bearing_wall))
            wall_map.append(str_new_map)
        return wall_map

    def create_wall_map(self, mask):

        transpose_mask = np.transpose(mask)

        hor_local_maxima, hor_maxima_map = self.create_maxima_map(mask)
        vert_local_maxima, vert_maxima_map = self.create_maxima_map(transpose_mask)

        vert_maxima_map = np.transpose(vert_maxima_map)

        local_maxima = []
        local_maxima.extend(hor_local_maxima)
        local_maxima.extend(vert_local_maxima)
        local_maxima.sort()

        start_idx_outer, start_idx_bearing = self.classificate_walls(local_maxima)

        min_outer_wall = local_maxima[start_idx_outer]
        min_bearing_wall = local_maxima[start_idx_bearing]

        hor_wall_map = self.define_type_of_walls(hor_maxima_map,  min_outer_wall, min_bearing_wall)
        vert_wall_map = self.define_type_of_walls(vert_maxima_map, min_outer_wall, min_bearing_wall)

        hor_wall_map = np.asarray(hor_wall_map)
        vert_wall_map = np.asarray(vert_wall_map)

        wall_map = hor_wall_map
        ids = np.where(wall_map == WALL_MAP['space'])
        wall_map[ids] = vert_wall_map[ids]

        return wall_map

    def visualize_stage(self):
        img = np.zeros(self.shape, np.uint8)
        for r in self.img:
            img = render_room(img, Room().from_dict(r.to_dict()), line_w=3)
        return img
