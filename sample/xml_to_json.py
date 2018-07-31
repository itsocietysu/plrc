import sys
import xml.etree.ElementTree
from os.path import basename
import json

e = xml.etree.ElementTree.parse(sys.argv[1]).getroot()

def createLine(c):
    print(c)
    _str = '''{"type": "line",
                "point_1": {
                    "type": "point",
                    "x": %d,
                    "y": %d
                },
                "point_2": {
                    "type": "point",
                    "x": %d,
                    "y": %d
                }}''' % (c[0], c[1], c[2], c[3])
    print(_str)
    return json.loads(_str)

result = []
for _ in e.findall('object'):
    new_item = {'type': '', 'placement': {}}
    for v in _:
        if v.tag == 'name':
            new_item['type'] = v.text
        if v.tag == 'bndbox':
            coords = []
            for sv in v:
                coords.append(int(sv.text))
            new_item['placement'] = createLine(coords)

    result.append(new_item)


res_json = json.dumps({'openings': result}, indent=2)

with open(basename(sys.argv[1]).split('.')[0] + '.json', 'wt') as fp:
    fp.write(res_json)