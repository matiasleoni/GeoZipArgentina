import requests
import json
import pandas as pd
import time

def request_coordinates(CP):
    URL = "https://nominatim.openstreetmap.org/search?postalcode="+str(CP)+"&country=Argentina&format=geojson"
    my_request = requests.get(URL)
    #print("Request answer: ")
    #print(my_request.text)

    adic = json.loads(my_request.text)
    answer = adic['features'][0]['geometry']['coordinates']
    answer.reverse()
    return answer



#print(request_coordinates(1414))

localidades = pd.read_csv("data/localities.csv")
CPs = localidades['CP'].drop_duplicates()

n = 0



for CP in CPs:
    initial = time.time()
    print(CP, ": ", request_coordinates(CP))
    final = time.time()
    print(final-initial, " segundos")
    n += 1
    if n > 10:
        break




