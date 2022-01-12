from rest_framework.exceptions import ErrorDetail
from pykml import parser
from pykml.parser import Schema
import re


def google_file_to_dict(file):
    schema_gx = Schema("kml22gx.xsd")
    maps_dict = {}
    with open(file, 'rb') as f:
        try:
            root = parser.parse(f).getroot().Document.Folder
            print(root)
            print(type(root))
            if schema_gx.validate(root) is True:
                for folder in root:
                    for pm in folder.Placemark:
                        title = pm.name
                        for i in pm.Polygon.outerBoundaryIs.LinearRing:
                            result = re.sub(r'\s+', '\n',
                                            str(i.coordinates)).strip().split(
                                '\n')
                            maps_dict.setdefault(title, []).append(result)
                return maps_dict
            else:
                raise ErrorDetail({"error": "wrong file schema"})
                #return 'Wrong file...'
        except Exception as e:
            #return 'Export a whole map, not a layout.'
            raise ErrorDetail({"error": "export a whole map, not a layout"})
