import csv
import os
from datetime import datetime
from dataclasses import dataclass


@dataclass
class CSVData:
    """Class for keeping track of analyzed CSV properties"""

    file_name: str
    column_name: str
    total_rows: int
    longest_value_len: int
    longest_value_row: int


class CSVAnalyzer:
    """Class for analyzing csv"""

    def __init__(self):
        self.data = CSVData("", "", 0, 0, 0)

    def find_longest_value(self, csv_reader: csv.DictReader, column_name: str) -> None:
        longest_value_len = 0
        longest_value_row = 0
        row_idx = 0

        for row_idx, row in enumerate(csv_reader, start=1):
            column_value = row[column_name]
            column_value_len = len(column_value)

            if column_value_len > longest_value_len:
                longest_value_len = column_value_len
                longest_value_row = row_idx

        self.data.total_rows = row_idx
        self.data.longest_value_row = longest_value_row
        self.data.longest_value_len = longest_value_len

    def create_results_file(self) -> str:
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f"{self.data.file_name}_results_{current_time}.txt"

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(f"Results for file '{self.data.file_name}' ({self.data.total_rows} total rows):\n")
            file.write(f"Column name: '{self.data.column_name}'\n")
            file.write(f"Longest value row: '{self.data.longest_value_row}'\n")
            file.write(f"Longest value length: '{self.data.longest_value_len}'\n")

        return file_name

    def analyze_csv_file(self) -> None:
        with open(self.data.file_name, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            self.find_longest_value(csv_reader, self.data.column_name)

    def file_exist(self, file_name: str) -> bool:
        if not os.path.isfile(file_name):
            print(f"File '{file_name}' not found in the script's directory...")
            return False
        print(f"File found...")
        self.data.file_name = file_name
        return True

    def column_exist(self, column_name: str) -> bool:
        with open(self.data.file_name, 'r', encoding='utf-8') as file:
            fieldnames = csv.DictReader(file).fieldnames

        if column_name not in fieldnames:
            print(f"Column '{column_name}' not found in the CSV file...")
            return False
        print(f"Column found...")
        self.data.column_name = column_name
        return True

    def run(self) -> None:
        file_name = input("Enter the CSV file name: ")
        if self.file_exist(file_name):
            column_name = input("Enter the column name to check: ")
            if self.column_exist(column_name):
                self.analyze_csv_file()
                results_file_name = self.create_results_file()
                print(f"Analysis complete. Results saved to '{results_file_name}'.")

        input("Press Enter to exit...")
