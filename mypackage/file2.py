import csv
import pandas as pd
import glob
import os


titles2 = [' ID ', ' hash_ID ', ' phone number ']
data2 =   [[' 650rtuk ', 12678, ' 090345678 '], 
        [' 5690tyu ', 23489 , ' 090097890 '], 
        [' 7890hjk ', 12348 , ' 090378678 '], 
        [' 7273ryusth ', 90877 , ' 090763453 ']]

with open ('file2.csv', 'w') as f2:

    csvwriter = csv.writer(f2)
    csvwriter.writerow(titles2)
    csvwriter.writerows(data2)

with open('file2.csv', 'r') as f2: 
        reader2 = csv.reader(f2, dialect=csv.excel_tab) 
        header2 = next(reader2)

    
    