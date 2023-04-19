from io import BytesIO
from PIL import Image
import requests
import sys
from apteka_near_func_10 import get_spn_two_points, lonlat_distance

#toponym_to_find = "Улица Ярцевская, 27к1"
toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json",

}
response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    pass
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

map_params_biz = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "text": toponym_to_find+' аптека',
    "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
    "type": "biz",
    "lang": "ru_RU",
    "format": "json"
}

map_api_server_biz ="https://search-maps.yandex.ru/v1/"
response_biz = requests.get(map_api_server_biz, params=map_params_biz)
json_response_biz = response_biz.json()
str2 = ""
snippet = {}
snippet1 = {}
delta_curr = [0,0]
delta_max = [0,0]
for j, toponym_byz in enumerate(json_response_biz['features']):
    toponym_coodrinates_byz = [str(i) for i in toponym_byz['geometry']['coordinates']]
    #print(toponym_byz['properties']['CompanyMetaData'])
    if 'Hours' in toponym_byz['properties']['CompanyMetaData']:
        regim = toponym_byz['properties']['CompanyMetaData']['Hours']['text']
    else:
        regim = 'нет данных'

    if regim == 'нет данных':
        if str2 =='':
            str2 =",".join(toponym_coodrinates_byz+["pm2grm"+str(j+1)])
        else:
            str2 =str2+'~'+",".join(toponym_coodrinates_byz+["pm2grm"+str(j+1)])
    elif 'круглосуточно' in regim:
        if str2 =='':
            str2 =",".join(toponym_coodrinates_byz+["pm2gnm"+str(j+1)])
        else:
            str2 =str2+'~'+",".join(toponym_coodrinates_byz+["pm2gnm"+str(j+1)])
    else:
        if str2 == '':
            str2 = ",".join(toponym_coodrinates_byz + ["pm2blm" + str(j + 1)])
        else:
            str2 = str2 + '~' + ",".join(toponym_coodrinates_byz + ["pm2blm" + str(j + 1)])
    if j == 10:
        break

    snippet1 = {
        "Название " + str(j+1): toponym_byz['properties']['CompanyMetaData']['name'],
        "Адрес "+  str(j+1): toponym_byz['properties']['CompanyMetaData']['address'],
        "Режим работы "+  str(j+1): regim,
        "Расстояние до аптеки, м "+  str(j+1): round(lonlat_distance(toponym_coodrinates, toponym_byz['geometry']['coordinates']),                             2)
    }
    snippet = snippet|snippet1
    delta_curr=get_spn_two_points(toponym,toponym_byz['properties'])
    for i in range(2):
        delta_max[i]=max(delta_curr[i],delta_max[i])

delta_max = [str(i+0.005) for i in delta_max]
# print(delta_max)
str1 = ",".join([toponym_longitude, toponym_lattitude, "home"])
map_api_server = "http://static-maps.yandex.ru/1.x/"
map_params = {
"ll": ",".join([toponym_longitude, toponym_lattitude]),
"spn": ",".join(delta_max),
"l": "map",
"pt": str1 + "~" + str2
}
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(response.content)).show()

print('**** Ближайшие аптеки **** ')
i = 0
for key,value in snippet.items():
    print(key, ': ', value)
    i +=1
    if i % 4 == 0:
        print('**************************************************************')