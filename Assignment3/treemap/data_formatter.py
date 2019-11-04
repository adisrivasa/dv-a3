import pandas as pd
import json

df = pd.read_csv('Pokemon.csv')

# subregion = education, region = sex, value = bill_amt1
# key = id

with open('pokedex.json', 'w') as outfile:
    c = len(df.index) - 1
    outfile.write('[\n')
    i = 0
    for index, row in df.iterrows():
        row = list(row)
        outfile.write('{\n')
        outfile.write('"key" : "' + str(row[1]) + '",\n')
        outfile.write('"region" : "' + str(row[2]) + '",\n')
        if(str(row[3]) == "nan"):
            outfile.write('"subregion" : "only ' + str(row[2]) + '",\n')
        else:
            outfile.write('"subregion" : "' + str(row[3]) + '",\n')
        outfile.write('"value" : ' + str(1) + '\n')
        if i == c:
            outfile.write('}\n')
        else:
            outfile.write('},\n')
        i = i + 1
    outfile.write(']')
