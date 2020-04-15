#!/usr/bin/env python
# coding: utf-8

# In[4]:


# import flask dependencies
#!/usr/bin/env python
# coding: utf-8

# In[4]:


# import flask dependencies
from flask import Flask,json,request,make_response,render_template
from firebase import firebase
import requests


# initialize the flask app
app = Flask(__name__)

# default route
@app.route('/')

def home():
    return render_template('index.html')
    #return 'Hello World index!'

# create a route for webhook
@app.route('/webhook',methods=["POST"])
def webhook():
    req = request.get_json(silent=True,force=True)
    saveConversation(req)
    print("Request:")
    print(json.dumps(req,indent=4))
    res = corona_api_calling(req)
    res = json.dumps(res,indent=4)
    print(res)
    r=make_response(res)
    r.headers['Content-Type'] = "application/json"
    return r

def saveConversation(req):
     resultval = req.get("queryResult")
     requestconversation = resultval.get("queryText")
     responseconversation = resultval.get("fulfillmentText")     
     firebaseval = firebase.FirebaseApplication('https://covchatbotdata.firebaseio.com/', None)
     print(firebaseval)
     data =  { 'RequestedText': requestconversation,
               'ResponseText': responseconversation
             }
     result = firebase.post('/python-example-f6d0b/Students/',data)
     print(result)
     r=make_response(result)
     return r
    

def corona_api_calling(req):
    resultval = req.get("queryResult")
    parameters = resultval.get("parameters")
    countrycode = parameters.get("countryname")
    countryname = countrycode.get("name")
    r = requests.get('https://api.covid19api.com/live/country/'+countryname)
    k= r.json()
    Confirmed_Cases = str(k[0]['Confirmed'])
    Recovered_Cases = str(k[0]['Recovered'])
    Death_Count = str(k[0]['Deaths'])
    displayText = "Confirmed Cases :"+Confirmed_Cases+",Recovered Cases :"+Recovered_Cases+",Death Count:"+Death_Count
    print("Response:")
    print(displayText)
    return{ "source":"userinfodetails",
            "speech":displayText,
            "displayText":displayText,
            "fulfillmentText":displayText
          }
    #res = make_response('Corona Results'+Confirmed_Cases,200)
    #return res


# run the app
if __name__ == '__main__':
   app.run(debug=True)

 







