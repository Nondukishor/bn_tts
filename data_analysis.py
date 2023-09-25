import pandas as pd
from variables import DATA_PATH
data = pd.read_csv(DATA_PATH+"/line_index.tsv")

print(data.info())