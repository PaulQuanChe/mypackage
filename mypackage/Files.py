import pandas as pd
import glob
import os


df = pd.concat(
    map(pd.read_csv, ['file1.csv', 'file2.csv']), ignore_index=True)
print(df)

