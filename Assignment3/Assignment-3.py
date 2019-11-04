from flask import Flask, render_template, url_for
import pandas as pd

global energy_columns, card_columns

energy_columns = {'A':'date','B':'Appliances', 'C':'lights', 'D':'T1', 'E':'RH_1', 'F':'T2', 'G':'RH_2', 'H':'T3', 'I':'RH_3', 'J':'T4', 'K':'RH_4', 'L':'T5', 'M':'RH_5', 'N':'T6', 'O':'RH_6', 'P':'T7', 'Q':'RH_7', 'R':'T8', 'S':'RH_8', 'T':'T9', 'U':'RH_9', 'V':'T_out', 'W':'Press_mm_hg', 'X':'RH_out', 'Y':'Windspeed', 'Z':'Visibility', 'AA':'Tdewpoint', 'AB':'rv1', 'AC':'rv2'}
card_columns = {'A':'ID', 'B':'LIMIT_BAL', 'C':'SEX', 'D':'EDUCATION', 'E':'MARRIAGE', 'F':'AGE', 'G':'PAY_0', 'H':'PAY_2', 'I':'PAY_3', 'J':'PAY_4', 'K':'PAY_5', 'L':'PAY_6', 'M':'BILL_AMT1', 'N':'BILL_AMT2', 'O':'BILL_AMT3', 'P':'BILL_AMT4', 'Q':'BILL_AMT5', 'R':'BILL_AMT6', 'S':'PAY_AMT1', 'T':'PAY_AMT2', 'U':'PAY_AMT3', 'V':'PAY_AMT4', 'W':'PAY_AMT5', 'X':'PAY_AMT6', 'Y':'default payment next month'}

app = Flask(__name__)

@app.route('/IMT2015042_Assignment-3')
def AssignmentMainPage():
    return render_template("index.html")

@app.route('/PCVisualization/<filenum>/<columns>/<color>')
def PCVisualize(filenum, columns, color):
    global energy_columns, card_columns
    if(filenum == '1'):
        datadf = pd.read_csv("energydata_complete.csv")
        columndata = columns.split(',')
        columndata = [energy_columns[c] for c in columndata]
        resultdf = datadf[columndata]
        columns += color + '1.csv'
        resultdf.to_csv('static/' + columns , encoding='utf-8', index=False)
    elif(filenum == '2'):
        datadf = pd.read_csv("card-data.csv")
        columndata = columns.split(',')
        columndata = [card_columns[c] for c in columndata]
        resultdf = datadf[columndata]
        columns += color + '2.csv'
        resultdf.to_csv('static/' + columns , encoding='utf-8', index=False)
    return render_template("ParallelCoordinates.html", filnam = columns, colors = card_columns[color])

@app.route('/TMVisualization/<filenum>/<value>/<level1>/<level2>/<filterc>')
def TMVisualize(filenum, value, level1, level2, filterc):
    global energy_columns, card_columns
    filename = 'static/' + level1 + '-' + level2 + '-' + filterc + '-' + filenum + '.json'
    if(filenum == '1'):
        datadf = pd.read_csv("energydata_complete.csv")
        df = datadf[ datadf[filterc.split('-')[0]] == int(filterc.split('-')[1]) ]
        with open(filename, 'w') as outfile:
            c = len(df.index) - 1
            outfile.write('[\n')
            i = 0
            for index, row in df.iterrows():
                row = list(row)
                outfile.write('{\n')
                outfile.write('"key" : "' + str(row[0]) + '",\n')
                outfile.write('"region" : "' + str(row[1]) + '",\n')
                outfile.write('"subregion" : "' + str(row[2]) + '",\n')
                outfile.write('"value" : ' + str(row[3]) + '\n')
                if i == c:
                    outfile.write('}\n')
                else:
                    outfile.write('},\n')
                i = i + 1
            outfile.write(']')
    if(filenum == '2'):
        datadf = pd.read_csv("card-data.csv")
        df = datadf[ datadf[filterc.split('-')[0]] == int(filterc.split('-')[1]) ]
        with open(filename, 'w') as outfile:
            c = len(df.index) - 1
            outfile.write('[\n')
            i = 0
            for index, row in df.iterrows():
                row = list(row)
                outfile.write('{\n')
                outfile.write('"key" : "' + str(row[0]) + '",\n')
                outfile.write('"region" : "' + str(row[1]) + '",\n')
                outfile.write('"subregion" : "' + str(row[2]) + '",\n')
                outfile.write('"value" : ' + str(row[3]) + '\n')
                if i == c:
                    outfile.write('}\n')
                else:
                    outfile.write('},\n')
                i = i + 1
            outfile.write(']')

if __name__ == '__main__':
    app.run( host = '0.0.0.0', port = 5000, debug = True )


df = pd.read_csv("census-income.csv")
for index, row in df.iterrows():
    if row[0] <= 35:
        df.iloc[index,0] = '17-35'
    elif row[0] <= 53 and row[0] > 35:
        df.iloc[index,0] = '36-53'
    elif row[0] <= 72 and row[0] > 53:
        df.iloc[index,0] = '54-72'
    elif row[0] <= 90 and row[0] > 72:
        df.iloc[index,0] = '73-90'


data = {'age':[], ' education':[], ' race':[], ' sex':[], ' workclass':[], 'count':[], 'hours-per-week':[], 'income':[]}
grouped = df.groupby(['age', ' education', ' race', ' sex', ' workclass', ' income']).groups
groups = list(grouped.keys())
for key in groups:
    indexes = list(grouped[key])
    hpw = [df.iloc[ind,12] for ind in indexes]
    data['age'].append(key[0])
    data[' education'].append(key[1])
    data[' race'].append(key[2])
    data[' sex'].append(key[3])
    data[' workclass'].append(key[4])
    data['count'].append(len(indexes))
    data['hours-per-week'].append(sum(hpw))
    data['income'].append(key[5])


df = pd.DataFrame(data)
filename = 'income.json'
with open(filename, 'w') as outfile:
    c = len(df.index) - 1
    outfile.write('[\n')
    i = 0
    for index, row in df.iterrows():
        row = list(row)
        outfile.write('{\n')
        outfile.write('"key" : "' + row[1] + row[2] + ' - ' + str(row[5]) + '",\n')
        outfile.write('"region" : "' + row[0] + row[3] + '",\n')
        outfile.write('"subregion" : "Age : ' + row[4] + ', income :' + row[7] + '",\n')
        outfile.write('"value" : ' + str(row[6]) + '\n')
        if i == c:
            outfile.write('}\n')
        else:
            outfile.write('},\n')
        i = i + 1
    outfile.write(']')
