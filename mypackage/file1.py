import csv
import pandas as pd
import glob
import os


titles1 = [' ID ', ' hash_ID ', ' phone number ']
data1 =   [[' 6rtuk ', 12678,   ' 0903707636 '],
        [' 56tyu ', 23487 , ' 0903719527 '],
        [' 7890hjk ', 12346 , ' 09835618 '], 
        [' 7895ryusth ', 90873 , ' 097186789 ']]

with open ('file1.csv', 'w') as f1:

    csvwriter = csv.writer(f1)
    csvwriter.writerow(titles1)
    csvwriter.writerows(data1)

with open('file1.csv', 'r') as f1: 
        reader1 = csv.reader(f1, dialect=csv.excel_tab) 
        header1 = next(reader1) 


