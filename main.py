import pandas as pd
import requests
import json
import re
import os

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

preset2 = '''
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
'''

def writetojsonfile(path, filename, data):
    filepathnamewext='./'+ path + '/' + filename + '.json'
    with open(filepathnamewext,'w') as fp:
        json.dump(data,fp,indent=4)

final={}

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

# requisitar api da google para fazer endereco para coordenada

#for i in tamanho_coluna:

tamanho_row_excel=excel.shape[0]-1
for i in range(tamanho_row_excel):

    API = 'AIzaSyBs39VoT375Fz31ONR4liU1Vn06hDV95PE'
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + lista_uf[i] + lista_cep[i] + lista_cidade[i] + lista_bairro[i] + lista_logradouro[i] + "&key=" + API
    r = requests.get(url)
    resultado_api = json.loads(r.content)

    # TODO fazer loop para todos os clientes
    coord_lat = resultado_api['results'][0]['geometry']['location']['lat']
    coord_lng = resultado_api['results'][0]['geometry']['location']['lng']
    # print(coord_lat)
    # print(coord_lng)

    #carrega um novo para data
    data = json.loads(preset)

    # print(df.info())
    #print(type(data['features']))
    #print(data)

    if not os.path.isfile('output.json'):
    # se o output esta vazio criar a base com dados
        #cord
        for features in data['features']:
            features['geometry']['coordinates'][0] = coord_lat
            features['geometry']['coordinates'][1] = coord_lng
            # print(features['geometry']['coordinates'])

            #razao
            tmp_razao = lista_razao[i]
            tmp_razao_regex = re.sub(r'[0-9]', "", tmp_razao)
            features['properties']['name'] = tmp_razao_regex

            #telefone por phone
            #TODO UF no ddd se precisar
            features['properties']['phone']=str(lista_telefone[i])

            #storeID incremnetado
            features['properties']['storeid']=str(i)
            writetojsonfile('./', 'output', data)
        print('if')
    else:
        tmp_razao = lista_razao[i]
        tmp_razao_regex = re.sub(r'[0-9]', "", tmp_razao)
        with open('output.json') as jsonfile:
            output=json.load(jsonfile)
            tmp=output['features']
            new={'geometry':
                     {"type": "Point",
                "coordinates": [
                    coord_lat,
                    coord_lng
                ]},
                 "type": "Feature",
                 "properties": {
                     "category": "patisserie",
                     "name": tmp_razao_regex,
                     "phone": str(lista_telefone[i]),
                     "storeid":str(i)
                 }
                 }
            tmp.append(new)

        writetojsonfile('./','output',output)
        print('else')

#print(data)

#jsondump=json.dumps(data)
#print(jsondump)
#writetojsonfile('./','output',data)