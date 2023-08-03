import requests
import json
import pandas as pd
import time
import math 
import os
import csv
from collections import OrderedDict

from classes.log_file import Log_file as Log_file
from classes.CPs_file import CPs_file as CPs_file

def request_coordinates(CP):
    URL = "https://nominatim.openstreetmap.org/search?postalcode="+str(CP)+"&country=Argentina&format=geojson"
    my_request = requests.get(URL)
    json_full_answer = json.loads(my_request.text)
    try:
        answer = json_full_answer['features'][0]['geometry']['coordinates']
        answer.reverse()
    except IndexError:
        answer = [float("nan")]*2
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

def process_batch(batch):
    return_dic = OrderedDict()
    for CP in batch:
        coordinates = request_coordinates(CP)
        return_dic[CP] = coordinates
    return return_dic

def scrap_step(batched_CPs, the_log_file, the_CPs_file):
    last_batch_number = the_log_file.check_last_batch()
    if last_batch_number is None:
        last_batch_number = -1
    batch = batched_CPs[last_batch_number+1]
    return_dic = process_batch(batch)

    if not the_log_file.check_if_batch_exists(last_batch_number+1):
        the_CPs_file.write_entry(return_dic)
    the_log_file.write_entry(last_batch_number+1,return_dic)

    print(f"batch {last_batch_number+1} computed")
    return return_dic

























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




