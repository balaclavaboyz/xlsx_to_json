import pandas as pd
import requests
import json
import re

preset = '''
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
        "name": "none",
        "phone": "123456789",
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

# pd.set_option('display.max_columns', None)
# se quiser printar all

excel = pd.DataFrame(pd.read_excel("original.xlsx"))

# exemplo de printar um cliente
# print(excel.loc[1])

tamanho_coluna = len(excel.columns)

# guardar razao em uma lista
for tamanho_coluna in excel['RAZAO']:
    lista_razao = excel['RAZAO']

for tamanho_coluna in excel['BAIRRO']:
    lista_bairro = excel['BAIRRO']

for tamanho_coluna in excel['CIDADE']:
    lista_cidade = excel['CIDADE']

for tamanho_coluna in excel['UF']:
    lista_uf = excel['UF']

for tamanho_coluna in excel['LOGRADOURO']:
    lista_logradouro = excel['LOGRADOURO']

for tamanho_coluna in excel['TELEFONE']:
    lista_telefone = excel['TELEFONE']

for tamanho_coluna in excel['CEP']:
    lista_cep = excel['CEP']

# print(lista_razao)
# print(lista_bairro)
# print(lista_cidade)
# print(lista_uf)
# print(lista_logradouro)
# print(lista_telefone)
# print(lista_cep)

print('---')

# requisitar api da google para fazer endereco para coordenada

API = 'AIzaSyBs39VoT375Fz31ONR4liU1Vn06hDV95PE'
url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + lista_uf[0] + lista_cep[0] + lista_cidade[0] + \
      lista_bairro[0] + lista_logradouro[0] + "&key=" + API
r = requests.get(url)
resultado_api = json.loads(r.content)

# TODO fazer loop para todos os clientes
coord_lat = resultado_api['results'][0]['geometry']['location']['lat']
coord_lng = resultado_api['results'][0]['geometry']['location']['lng']
# print(coord_lat)
# print(coord_lng)

print('-----')

data = json.loads(preset)

# print(df.info())
print(type(data['features']))
print(data)

for features in data['features']:
    #cord
    features['geometry']['coordinates'][0] = coord_lat
    features['geometry']['coordinates'][1] = coord_lng
    # print(features['geometry']['coordinates'])

    #razao
    tmp_razao = lista_razao[0]
    tmp_razao_regex = re.sub(r'[0-9]', "", tmp_razao)
    features['properties']['name'] = tmp_razao_regex

    #telefone por phone
    #TODO UF no ddd se precisar
    features['properties']['phone']=str(lista_telefone[0])

    #storeID incremnetado
    features['properties']['storeid']='0'

print(data)
