import os
import csv
import pandas as pd


class Log_file:
    """
    Log_file class for managing a CSV log file.

    Parameters:
        filename (str, optional): The name of the log file. Default is 'log.csv'.
        overwrite (bool, optional): If True, overwrite the file if it already exists. If False,
                                    raise a warning and set filename to None if the file exists.
                                    Default is False.

    Attributes:
        filename (str): The name of the log file.
        file_exists (bool): True if the file exists, False otherwise.
        column_names (list): The list of column names for the log file.

    Methods:
        check_last_batch(): Check and return the last batch number from the log file.
        check_if_batch_exists(batch_number): Check if a batch with a given number exists in the log file.
        write_entry(batch_number, batch_dic): Write an entry to the log file for a new batch.
        length(): Get the number of entries in the log file.
        delete_file(): Delete the log file (if it exists).

    Note:
        This class assumes the CSV file uses the following format:
        - The first row contains the column names specified in the 'column_names' attribute.
        - Each subsequent row represents an entry for a batch with the format: batch_number, start_CP, end_CP.
    """

    def __init__(self, filename="log.csv", overwrite=False):
        """
        Initialize the Log_file object.

        Args:
            filename (str, optional): The name of the log file. Default is 'log.csv'.
            overwrite (bool, optional): If True, overwrite the file if it already exists. If False,
                                        raise a warning and set filename to None if the file exists.
                                        Default is False.
        """
        self.filename = filename
        self.file_route = "classes/"+self.filename
        self.file_exists = os.path.exists(self.file_route)
        self.column_names = ["batch_number", "start_CP", "end_CP"]
        if self.file_exists and not overwrite:
            print("That log file already exists. Please turn on the overwrite option ")
            print("when you use the Log_file class if you want a new object. Else dismiss.")
            #self.filename = None
            #self.file_route = None
            #self.file_exists = False
            return None
        else:
            self.file_exists = True
            with open(self.file_route, "w", newline="") as csv_file:
                log_writer = csv.writer(csv_file)
                log_writer.writerow(self.column_names)

    def check_last_batch(self):
        """
        Check and return the last batch number from the log file.

        Returns:
            int or None: The last batch number if it exists, or None if the log file is empty.
        """
        df = pd.read_csv(self.file_route)
        try:
            last_batch_number = df.iloc[-1][self.column_names[0]]
        except IndexError:
            return None
        return last_batch_number

    def check_if_batch_exists(self, batch_number):
        """
        Check if a batch with a given number exists in the log file.

        Args:
            batch_number (int): The batch number to check.

        Returns:
            bool: True if the batch number exists, False otherwise.
        """
        df = pd.read_csv(self.file_route)
        return batch_number in df[self.column_names[0]].to_list()

    def write_entry(self, batch_number, batch_dic):
        """
        Write an entry to the log file for a new batch.

        Args:
            batch_number (int): The batch number for the new entry.
            batch_dic (dict): A dictionary representing the start and end control points of the batch.

        Note:
            - The batch_dic dictionary should have the following format: {start_CP: value, end_CP: value}
            - The function writes the batch_number, start_CP, and end_CP to the log file.
        """
        if self.check_if_batch_exists(batch_number):
            print(f"Entry {batch_number} already exists.")
        else:
            with open(self.file_route, "a", newline="") as csv_file:
                log_writer = csv.writer(csv_file)
                log_writer.writerow([batch_number, list(batch_dic.keys())[0], list(batch_dic.keys())[-1]])

    def length(self):
        """
        Get the number of entries in the log file.

        Returns:
            int: The number of entries in the log file.
        """
        df = pd.read_csv(self.file_route)
        return len(df)

    def delete_file(self):
        """
        Delete the log file (if it exists).
        """
        if self.file_exists:
            os.remove(self.file_route)
            self.file_exists = False
        self.filename = None
        self.file_route = None