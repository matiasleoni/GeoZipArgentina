import requests
import json
import pandas as pd
import time
import math 

def request_coordinates(CP):
    URL = "https://nominatim.openstreetmap.org/search?postalcode="+str(CP)+"&country=Argentina&format=geojson"
    my_request = requests.get(URL)
    #print("Request answer: ")
    #print(my_request.text)

    adic = json.loads(my_request.text)
    answer = adic['features'][0]['geometry']['coordinates']
    answer.reverse()
    return answer

def partition(number_of_CPs = 3448, batch_size = 30):
    number_of_batches = number_of_CPs//batch_size + (number_of_CPs % batch_size != 0)

    intervals = [(n,n+batch_size) for n in range(0,number_of_CPs-batch_size,batch_size)]
    intervals.append((batch_size*(number_of_batches-1),number_of_CPs))
    
    return intervals

def batcher(CPs, batch_size):
    index_partition = partition(number_of_CPs = len(CPs), batch_size =  batch_size)

    batched_CPs = [CPs[slice(*index_partition[batch_index])] for batch_index in range(len(index_partition))]
    return batched_CPs




#print(request_coordinates(1414))

#localidades = pd.read_csv("data/localities.csv")
#CPs = localidades['CP'].drop_duplicates().reset_index(drop= True)

#number_of_batches = 30

#index_partition = partition(number_of_CPs = len(CPs), number_of_batches =  number_of_batches)

#batched_CPs = [CPs[slice(*index_partition[batch_index])] for batch_index in range(number_of_batches)]



# n = 0
# for CP in CPs:
#     initial = time.time()
#     print(CP, ": ", request_coordinates(CP))
#     final = time.time()
#     print(final-initial, " segundos")
#     n += 1
#     if n > 10:
#         break




