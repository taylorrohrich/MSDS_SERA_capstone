import pandas as pd
x = pd.read_csv('colnames.txt')
y = list(map(lambda x: x[0],x.values))
print(y)
