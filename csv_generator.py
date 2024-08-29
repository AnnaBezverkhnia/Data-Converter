import csv 
from datetime import datetime

from constants import OutputData


def csv_generator(data):
    '''
    Method saves received data into .csv file.
    '''
    filename =  datetime.now().strftime('%Y-%m-%d') + '.csv'

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[attr.value for attr in OutputData])
        writer.writeheader()
        for item in data:
            writer.writerow(item)


