def propagate_val(val):
    val = val.strip()
    if val.startswith('\''):
        return val[1:-1]

    return int(val)


def load_label_map_file(file_name):
    with open(file_name, 'rt') as fp:
        res = []
        in_object = False

        current_obj = {}
        for line in fp:
            if not in_object:
                if line.strip().startswith('item {'):
                    in_object = True
                    continue
            else:
                ln = line.strip()

                if ln == '}':
                    in_object = False
                    res.append(current_obj)
                    current_obj = {}
                    continue

                if ln != '':
                    [key, val] = ln.split(':')
                    current_obj[key] = propagate_val(val)

        return res


def label_map_to_dict(lm):
    res = {}

    for _ in lm:
        res[_['id']] = _['name']

    return res


