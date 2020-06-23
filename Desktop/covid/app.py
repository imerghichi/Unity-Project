import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# run Flask app
if __name__ == "__main__":
    app.run(debug=True)

import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml.html as lh

page = requests.get("https://www.worldometers.info/coronavirus/")
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find("table", {"id": "main_table_countries_today"})

url='https://www.worldometers.info/coronavirus/'
page = requests.get(url)
doc = lh.fromstring(page.content)

tr_elements = doc.xpath('//tr')
col=[]

i=0 #For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    col.append((name,[]))


for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]
    
    #If row is not of size 10, the //tr data is not from our table 
    if len(T)!=19:
        break
    
    #i is the index of our column
    i=0
    
    #Iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content() 
        #Check if row is empty
        if i>0:
        #Convert any numerical value to integers
            try:
                data=int(data)
            except:
                pass
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1


Dict={title:column for (title,column) in col}
df=pd.DataFrame(Dict)

df=df.dropna(axis=1,how='all')

df = df.drop(['Tot\xa0Cases/1M pop',
 'Deaths/1M pop',
 'TotalTests',
 'Tests/\n1M pop\n',
 'Population',
 'Continent',
 '1 Caseevery X ppl',
 '1 Deathevery X ppl',
 '1 Testevery X ppl'], axis=1)

df['Country,Other'] = df['Country,Other'].str.replace('\n', '')
df['NewCases'] = df['NewCases'].str.replace('+', '')
df['NewDeaths'] = df['NewDeaths'].str.replace('+', '')
df[['TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths']] = df[['TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths']].replace('', 0)
df[['TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths']] = df[['TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths']].replace(' ', '')

df = df.drop(index=range(0,8))
df = df.drop(index=range(208,df.index[-1]+1))

df['NewDeaths'].fillna(0, inplace = True)
df['TotalCases'].fillna(0, inplace = True)
df['NewCases'].fillna(0, inplace = True)
df['TotalDeaths'].fillna(0, inplace = True)
df['NewDeaths'].fillna(0, inplace = True)

@app.route("/show_stats", methods=['GET'])
def show_stats(x):
    country = request.args.get("country")
    tc = df.loc[df['Country,Other'] == country, 'TotalCases'].values[0]
    nc = df.loc[df['Country,Other'] == country, 'NewCases'].values[0]
    td = df.loc[df['Country,Other'] == country, 'TotalDeaths'].values[0]
    nd = df.loc[df['Country,Other'] == country, 'NewDeaths'].values[0]
    
    reply = "{country}: \\nTotal Cases: {tc} \\nNew Cases: +{nc} \\nTotal Deaths: {td} \\nNew Deaths: +{nd}".format(country=x,tc=tc,nc=nc,td=td,nd=nd)
    return jsonify({"data": reply})