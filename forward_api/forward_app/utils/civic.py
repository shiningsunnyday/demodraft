import requests
KEY = "AIzaSyAGtU8i3hOlQXIuWL2t3eIBua9YXbC8x78"
URL = "https://www.googleapis.com/civicinfo/v2/representatives"
LEVELS = ["administrativeArea1", "administrativeArea2", "country", "international", "locality", "regional", "special",
          "subLocality1", "subLocality2"]

"""
Returns 
"""
def fetch(address):
    r = requests.get('%s?key=%s&address=%s' % (URL, KEY, address))
    offices = r.json()['offices']
    names = {lev: [] for lev in LEVELS}
    for o in offices:
        names[o['levels'][0]].append({'name': o['name'], 'division_id': o['divisionId']})
    return names

def fetchAddress(address):
    r = requests.get('%s?key=%s&address=%s' % (URL, KEY, address))
    normalizedInput = r.json()['normalizedInput']
    return normalizedInput