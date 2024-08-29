import json

from data_converter import DataConverter
from csv_generator import csv_generator


def generate_output_data():
    ### collect input data ###
    with open('input_data_example.json', 'r') as file:
        data = json.load(file)['data']

    ### Process the data and perform nesessary calculations ###
    data_converter = DataConverter(data=data)
    output_data = data_converter.create_output_data()

    ### Dave output dat ato .csv
    csv_generator(output_data)

if __name__ == '__main__':
    generate_output_data()
