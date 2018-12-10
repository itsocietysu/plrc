from Entities.Furniture import Furniture
from Entities.Line import Line
from ImageProcessing.Stage import Stage
import copy
import math
from Entities.Point import Point
SIZE = 20

FURNITURE_TYPE_MAP = {
    'kitchen_sink': Line(Point(0, 0), Point(SIZE, SIZE)),
    'dishwasher': Line(Point(0, 0), Point(SIZE, SIZE)),
    'washer': Line(Point(0, 0), Point(SIZE, SIZE)),
    'refrigerator': Line(Point(0, 0), Point(SIZE, SIZE)),
    'stove': Line(Point(0, 0), Point(SIZE, SIZE)),
}
# 9 направлений
FURNITURE_ORIENTATION_MAP = {
    'north': Point(0, -1),
    'south': Point(0, 1),
    'west': Point(-1, 0),
    'east': Point(1, 0),
    'north-west': Point(-1, -1),
    'south-west': Point(-1, 1),
    'north-east': Point(1, -1),
    'south-east': Point(1, 1),
}


# TODO
def check_bad_zones():
    return


'''
start_point - точка от которой начинается расстановка

'''


def simple_placement(furniture, start_point, placement_orientation, len_x, len_y, delta=0):
    if len_x > len_y:
        start_point.x += placement_orientation.x * delta
    else:
        start_point.y += placement_orientation.y * delta
    p = copy.deepcopy(start_point)
    # update start point
    if len_x > len_y:
        start_point.x += placement_orientation.x * furniture.placement.point_2.x
        start_point.y += placement_orientation.y * furniture.placement.point_1.y
    else:
        start_point.x += placement_orientation.x * furniture.placement.point_1.x
        start_point.y += placement_orientation.y * furniture.placement.point_2.y
    # point 1
    p.x += placement_orientation.x * furniture.placement.point_1.x
    p.y += placement_orientation.x * furniture.placement.point_1.y
    furniture.placement.point_1.x = p.x
    furniture.placement.point_1.y = p.y
    # point 2
    p.x += placement_orientation.x * furniture.placement.point_2.x
    p.y += placement_orientation.x * furniture.placement.point_2.y
    furniture.placement.point_2.x = p.x
    furniture.placement.point_2.y = p.y


'''
Необходимо добавить в качестве параметра start_point - точку, от которой начинается расстановка.
Она определяется вводом пользователя или по стояку.
    ] по умолчанию NW угол - start point
'''


def place_furniture(furniture, room, point):
    walls = room.walls
    delta = 3
    min_wall_len = 473
    angles = []

    '''Выделение всех углов комнаты'''
    for idx, wall in enumerate(walls):
        # Definition of first wall
        cur_wall = wall
        # Definition of second wall
        next_wall = walls[(idx + 1) % len(walls)]
        if ((math.fabs(cur_wall.inner_part.point_2.x - next_wall.inner_part.point_2.x) < delta) and
            (math.fabs(cur_wall.inner_part.point_2.y - next_wall.inner_part.point_2.y) > delta)) \
                or \
                ((math.fabs(cur_wall.inner_part.point_2.y - next_wall.inner_part.point_2.y) < delta) and
                 (math.fabs(cur_wall.inner_part.point_2.x - next_wall.inner_part.point_2.x) > delta)):
            angles.append(cur_wall.inner_part.point_2)

    '''Взятие NW угла'''
    nw_angle = point#Point(angles[0].x, angles[0].y)
    for a in angles:
        nw_angle.x = min(nw_angle.x, a.x)
        nw_angle.y = min(nw_angle.y, a.y)
    '''Взятие NE, SW углов'''
    ne_angle = Point()
    sw_angle = Point()
    for idx, a in enumerate(angles):
        if ((a.x - angles[(idx + 1) % len(angles)].x) < delta) and (
                (a.y - angles[(idx + 1) % len(angles)].y) < delta):
            if idx == 0:
                sw_angle = angles[(idx + 1) % len(angles)]
                ne_angle = angles[-1]
            else:
                sw_angle = angles[(idx + 1) % len(angles)]
                ne_angle = angles[(idx - 1) % len(angles)]
            break
    '''Взятие SE угла'''
    se_angle = Point(0.0, 0.0)
    for a in angles:
        if a.x >= se_angle.x and a.y >= se_angle.y:
            se_angle.x = a.x
            se_angle.y = a.y
    '''Вычисление длин сторон'''
    len_x = math.fabs(nw_angle.x - ne_angle.x)  # длина по X
    len_y = math.fabs(nw_angle.y - sw_angle.y)  # длина по Y

    '''Выбор расстановки углом или по прямой'''
    if len_x >= min_wall_len and len_y >= min_wall_len:
        '''Расстановка по прямой от выбранной начальной точки и с заданным направлением'''
        for f in furniture:
            simple_placement(f, nw_angle, FURNITURE_ORIENTATION_MAP['north-west'], len_x, len_y)
    else:
        '''Расстановка углом'''
        furniture_len = 0
        shift = 100
        i = 0
        start_point = copy.deepcopy(nw_angle)
        if len_x >= len_y:
            '''Вставляем сколько влезает по большей стене'''
            while i < len(furniture):
                f = furniture[i]
                furniture_len += f.placement.point_2.x
                if furniture_len >= min_wall_len:
                    furniture_len -= f.placement.point_2.x
                    break
                simple_placement(f, start_point, FURNITURE_ORIENTATION_MAP['south-east'], len_x, len_y)
                i += 1
            '''Добиваем остатки по второй стене в направлении перпендикулярном к заданному'''
            if i < len(furniture):
                ''' Обновляем точку начала расстановки с учётом разметки'''
                start_point.x = furniture[0].placement.point_1.x
                start_point.y = furniture[0].placement.point_2.y + shift
                while i < len(furniture):
                    f = furniture[i]
                    simple_placement(f, start_point, FURNITURE_ORIENTATION_MAP['south-east'], len_x - furniture_len,
                                     len_y)
                    i += 1
        else:
            while i < len(furniture):
                f = furniture[i]
                furniture_len += f.placement.point_2.y
                if furniture_len < min_wall_len:
                    furniture_len -= f.placement.point_2.y
                    break
                simple_placement(f, nw_angle, FURNITURE_ORIENTATION_MAP['south-east'], len_x, len_y)
                i += 1
                '''Добиваем остатки по второй стене в направлении перепендикулярном к заданному'''
                if i <= len(furniture):
                    ''' Обновляем точку начала расстановки с учётом разметки'''
                    ''' Рассматривается частный слай для NW угла'''
                    '''В общем случае необходимо домножать на коэффициент, задающий направление вектора расстановки и 
                    смещения'''
                    start_point.x = furniture[0].placement.point_1.x + shift
                    start_point.y = furniture[0].placement.point_2.y
                    while i < len(furniture):
                        f = furniture[i]
                        simple_placement(f, start_point, FURNITURE_ORIENTATION_MAP['south-east'], len_x,
                                         len_y - furniture_len)
                        i += 1
    return furniture


class FurniturePlacement(Stage):
    _name = 'furniture_placement'

    def __init__(self):
        Stage().__init__()

    def process(self, parent):
        """smooth the data"""

        if parent.parameters_file:
            f = parent.parameters_file
            point = Point(int(f[1]), int(f[2]))

        res = []
        furniture = []
        for i, room in enumerate(self.desc):
            new_room = copy.deepcopy(room)
            if i == 4:
                furniture = [
                    Furniture(FURNITURE_TYPE_MAP['kitchen_sink'], FURNITURE_ORIENTATION_MAP['north'], 'kitchen_sink'),
                    Furniture(FURNITURE_TYPE_MAP['dishwasher'], FURNITURE_ORIENTATION_MAP['north'], 'dishwasher'),
                    Furniture(FURNITURE_TYPE_MAP['washer'], FURNITURE_ORIENTATION_MAP['north'], 'washer'),
                    Furniture(FURNITURE_TYPE_MAP['stove'], FURNITURE_ORIENTATION_MAP['north'], 'stove'),
                    Furniture(FURNITURE_TYPE_MAP['refrigerator'], FURNITURE_ORIENTATION_MAP['north'], 'refrigerator')]

                furniture = place_furniture(furniture, new_room, point)
            if furniture:
                for f in furniture:
                    new_room.furniture.append(f)

            res.append(new_room)
        self.desc = res
        self.update_status(Stage.STATUS_SUCCEEDED)
