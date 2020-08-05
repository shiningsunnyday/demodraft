import requests
KEY = "AIzaSyAGtU8i3hOlQXIuWL2t3eIBua9YXbC8x78"
URL = "https://www.googleapis.com/civicinfo/v2/representatives"
LEVELS = ["administrativeArea1", "administrativeArea2", "country", "international", "locality", "regional", "special",
          "subLocality1", "subLocality2"]
LEVEL_MAP = {"administrativeArea1": "state", "administrativeArea2": "local", "country": "country", "locality": "local"}


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


def fetchPositions(address):
    r = requests.get('%s?key=%s&address=%s' % (URL, KEY, address))
    offices = r.json()['offices']
    keys = set(LEVEL_MAP.values())
    names = {lev: [] for lev in keys}
    for o in offices:
        names[LEVEL_MAP[o['levels'][0]]].append({'name': o['name']})
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
