from pykml import parser
from pykml.parser import Schema
import re


file = 'map.kml'
schema_gx = Schema("kml22gx.xsd")
maps_dict = {}

with open(file, 'rb') as f:
    try:
        root = parser.parse(f).getroot().Document.Folder
        if schema_gx.validate(root) is True:
            for folder in root:
                for pm in folder.Placemark:
                    title = pm.name
                    for i in pm.Polygon.outerBoundaryIs.LinearRing:
                        result = re.sub(r'\s+', '\n', str(i.coordinates)).strip().split('\n')
                        maps_dict.setdefault(title, []).append(result)
        else:
            print('Wrong file...')
    except Exception as e:
        print('Экспортируйте всю карту, а не отдельный слой.')


print(maps_dict)
