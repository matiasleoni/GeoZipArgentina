import os
import csv
import pandas as pd


class CPs_file:

    def __init__(self, filename="CPs_coordinates.csv", overwrite=False):
        self.filename = filename
        self.file_route = "classes/"+self.filename
        self.file_exists = os.path.exists(self.file_route)
        self.column_names = ["CP", "Latitude", "Longitude"]
        if self.file_exists and not overwrite:
            print("The File already exists. Please turn on the overwrite option ")
            print("when you use the Log_file class if you want a new object. Else dismiss.")
            return None
        else:
            self.file_exists = True
            with open(self.file_route, "w", newline="") as csv_file:
                log_writer = csv.writer(csv_file)
                log_writer.writerow(self.column_names)


    def write_entry(self, batch_dic):
        with open(self.file_route, "a", newline="") as csv_file:
            log_writer = csv.writer(csv_file)
            for key, value in batch_dic.items():
                log_writer.writerow([key, value[0], value[1]])
