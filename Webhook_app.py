#!/usr/bin/env python
# coding: utf-8

# In[13]:


import json
import os
import requests
from datetime import datetime
from flask import Flask,request,make_response

# Flask app should start in global layout
app=Flask(__name__)

@app.route('/webhook',method=['POST'])

def webhook():
    req=request.get_json(silent=True,force=True)
    print(json.dumps(req,indent=4))
    
    res=makeResponse(req)
    
    res=json.dump(res,indent=4)
    r=make_response(res)
    r.headers['Content-Type']='application json'
    return r

def makeResponse(req):
    result=req.get('queryResult')
    parameters=result.get('parameters')
    city=parameters.get('geo-city')
    date=parameters.get('date')
    date=date[:11]+' 5:30:00'
    date=datetime.fromisoformat(date).timestamp()
    
    r=requests.get('https://pro.openweathermap.org/data/2.5/climate/month?q='+city+'&appid=b1b15e88fa797225412429c1c50c122a1')
    json_obj=r.jsonson()
    weather=json_obj['list']
    for i in range(0,30):
        if date in weather[i]['dt']:
            condition=weather[i]['weather'][0]['description']
    
    
    speech="the forecast for "+city+" for date "+date+"is"
    return {
        "speech":speech,
        "displayText": speech,
        "source":"apiai-weather-webhook"
    }

if __name__ == '__main__':
    port=int(os.getenv('POST',5000))
    print('starting app on port %d'%port)
    app.run(debug=False,port=port,host='0.0.0.0')
    


# In[20]:


from datetime import datetime
x='2020-01-26 05:30:00'
   
datetime.fromisoformat(x).timestamp()

