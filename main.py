import pandas as pd
import csv
import json

preset ='''
    {
  "type": "FeatureCollection",
  "features": [
    {
      "geometry": {
        "type": "Point",
        "coordinates": [
          0,
          0
        ]
      },
      "type": "Feature",
      "properties": {
        "category": "patisserie",
        "name": "Josie's Patisserie Mayfair",
        "phone": "+44 20 1234 5678",
        "storeid": "0"
      }
    }
  ]
}
'''


# preset vai ser a base, entao read only o que vai ser static: geometry type, type feature, category fixed,
# vou tirar: "hours": "10am - 6pm",  description tb: "description": "Modern twists on classic pastries. We're part of
# a larger chain of patisseries and cafes.", storeid vai ter que ser numerado incremnetalmente

# temp vai ser a copia do preset, dai vou editar o temp e dps add no json filé

#pd.set_option('display.max_columns', None)
#se quiser printar all

excel=pd.DataFrame(pd.read_excel("original.xlsx"))
#exemplo de printar um cliente
#print(excel.loc[1])



print('---')

data = json.loads(preset)

# print(df.info())
print(type(data['features']))
print(data)

for features in data['features']:
    print(features['geometry'])