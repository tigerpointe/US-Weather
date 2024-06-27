# Converts a cities JSON data file into a Python dictionary.
# 01.00 2024-Jun-25 Scott S. Initial release.

# cities.json
# https://gist.github.com/Miserlou/c5cd8364bf9b2420bb29

import json

# Read the cities data file
f = open('cities.json', 'r')
cities = json.loads(f.read())
f.close()

# Create a dictionary of locations
#  key   = city and state (string)
#  value = latitude and longitude (tuple of doubles)
#  filter for only the n-topmost cities by rank (maxrank)
#  save the longest key length (maxkeylen)
locations = {}
maxkeylen = 0
maxrank = 9999  # 9999 for all cities
for city in cities:
    if int(city['rank']) > maxrank:
        continue  # 'break' would assume a sort order by rank
    key = '{c}, {s}'.format(c=city['city'], s=city['state'])
    locations[key] = (city['latitude'], city['longitude'])
    keylen = len(key.replace('\'', '\\\''))  # escape any apostrophes
    if keylen > maxkeylen:
        maxkeylen = keylen

# Sort the dictionary of locations by key
locations = dict(sorted(locations.items()))

# Create the Python code string
#  escape any apostrophes in the key (city or state names)
#  add spacing to the longest key length for better readability
#  round and pad the latitude and longitude to 6 decimal places
s = '# Define the coordinate locations (latitude and longitude)\n'
s += '#  (import locations.py into your custom Python script)\n'
s += 'locations = {\n'
for key in locations.keys():
    esc = key.replace('\'', '\\\'')
    pad = ' ' * (maxkeylen - len(esc))
    lat, lon = locations[key]
    lat = round(lat, 6)
    lon = round(lon, 6)
    s += '    \'{esc}\': {pad}({lat:.6f}, {lon:.6f}),\n'.format(
        esc=esc, pad=pad, lat=lat, lon=lon)
s += '}\n'

# Save the Python code string to a module file
f = open('locations.py', 'w')
f.write(s)
f.close()
