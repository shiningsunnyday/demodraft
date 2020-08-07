import requests
KEY = "AIzaSyAGtU8i3hOlQXIuWL2t3eIBua9YXbC8x78"
URL = "https://www.googleapis.com/civicinfo/v2/representatives"
LEVELS = ["administrativeArea1", "administrativeArea2", "country", "international", "locality", "regional", "special",
          "subLocality1", "subLocality2"]
LEVEL_MAP = {"administrativeArea1": "state", "administrativeArea2": "local", "country": "country", "locality": "local"}


def merge(dict1, dict2):
    """dict1 takes precedence"""
    for key, value in dict1.items():
        if isinstance(value, dict):
            node = dict2.setdefault(key, {})
            merge(value, node)
        else:
            dict2[key] = value
    return dict2


def purge_dup(names):
    """temporary way of making sure values are unique"""
    unique_names = {k: [] for k in names}
    for k in names.keys():
        hash = set()
        for v in names[k]:
            if v['name'] not in hash:
                hash.add(v['name'])
                unique_names[k].append(v)
    return unique_names


def fetchPositions(address, indices=False):
    r = requests.get('%s?key=%s&address=%s' % (URL, KEY, address))
    offices = r.json()['offices']
    keys = set(LEVEL_MAP.values())
    names = {lev: [] for lev in keys}
    for i in range(len(offices)):
        o = offices[i]
        to_add = {'name': o['name'], 'id': i} if indices else {'name': o['name']}
        names[LEVEL_MAP[o['levels'][0]]].append(to_add)
    return purge_dup(names)


def normalizeAddress(address):
    r = requests.get('%s?key=%s&address=%s' % (URL, KEY, address))
    normalizedInput = r.json()['normalizedInput']
    return normalizedInput

def toAddress(p):
    return p.line1 + ' ' + p.city + ', ' + p.state + ' ' + str(p.zipcode)

if __name__ == '__main__':
    x = fetchPositions("1263 Pacific Ave. Kansas City, KS")
    print(x)
