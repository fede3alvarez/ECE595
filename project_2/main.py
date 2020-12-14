import numpy as np
import pandas as pd

data = pd.read_csv('owid-covid-data.csv')

raw_size = data.size
raw_shape = data.shape

data = data["date"] == "2020-10-04"

size_1 = data.size
shape_1 = data.shape

print(data)