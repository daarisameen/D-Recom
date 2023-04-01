from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import json
from flask import request
from flask import json, jsonify, after_this_request
from flask import Flask, render_template, url_for, request

app = Flask(__name__,static_folder='static',template_folder='templates')

mlist=[]

@app.route('/')
def index():
    return render_template('index.html',embed=mlist)



@app.route('/test', methods=['POST','GET'])
def test():
    mlist.clear()
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
    
    output = request.get_json()
    # print(output) # This is the output that was stored in the JSON within the browser
    # print(type(output))
    result=json.loads(output)
    ani = result
    print(ani)
    print(result)
    print(type(result))
    resp = requests.get(ani)
    anisoup = BeautifulSoup(resp.text, "html.parser")

    series = anisoup.select('div.col-title')
    ratings = anisoup.select('div.col-imdb-rating')

    kstratings=[]

    for rat in range(0,len(ratings)):
        ksrating=ratings[rat].get_text()
        ksrating = (' '.join(ksrating.split()))
        kstratings.append(ksrating)

    kstmovie=[] 
    kstyear=[]

    for index in range(0, len(series)):
        ksmovie_string = series[index].get_text()
        ksmovie = (' '.join(ksmovie_string.split()).replace('.', ''))
        ksmovie_title = ""
        for i in range(len(str(index))+1,len(ksmovie)):
            if(ord(ksmovie[i+2])>=49 and ord(ksmovie[i+2])<=57):
                break
            else:
                ksmovie_title+=ksmovie[i];
        kstmovie.append(ksmovie_title)
        year = ksmovie[i+2:i+6]
        kstyear.append(year)
        data = {"movie_title": str(ksmovie_title),
			"rating": str(kstratings[index]),
			"year": str(year),
			}
        mlist.append(data)
    print(mlist) 
    # if(request.method == 'GET'):
    # print(mlist)
    # return render_template('index.html',embed=mlist)
    # index()
    return "good"
    # if(request.method == 'POST'):
    # response = app.response_class(
    #     response=json.dumps(mlist),
    #     status=200,
    #     mimetype='application/json'
    # )
    # return response
    
if __name__ == "__main__":
  app.run(debug=True)