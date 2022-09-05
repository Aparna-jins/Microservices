from flask import Flask,session,render_template,render_template_string,request,redirect,url_for,jsonify
import asyncio
import httpx
import asgiref
from google.appengine.api import urlfetch
import requests
import json
import time
app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def home():
    if request.method =="POST":
        name=request.form["pid"]
        action=request.form['action']
        if action == 'Asynchronous call':
            return redirect(url_for("get_name_async",nid=name))
        else:
            return redirect(url_for("get_name_sync",nid=name))
    else:
        return render_template('api.html')

@app.route("/sync/<nid>")
def get_name_sync(nid):
    st=time.time()
    
    response1 = requests.get('http://10.162.14.137:5000/api/users/'+nid)
    response2 = requests.request(method="GET", url='http://10.162.14.137:5001/api/salarylist/'+nid)
    r1=(response1.json())
    r2=(response2.json())
    r3 = []
    for i in r1:
        for j in r2:
            r3.append(i | j)
    et=time.time()
    el=et-st
    # print("=======time taken Synchronously======= "+str(el)+ 's')
    return render_template('append.html', r3=r3,el=el)
    
@app.route("/async/<nid>")
async def get_name_async(nid):
    st=time.time()
    async with httpx.AsyncClient() as client:

        response1,response2 = await asyncio.gather(
            client.get('http://10.162.14.137:5000/api/users/'+nid),
            client.get('http://10.162.14.137:5001/api/salarylist/'+nid)

    )
    r1=(response1.json())
    r2=(response2.json())
    r3 = []
    for i in r1:
        for j in r2:
            r3.append(i | j)
    et=time.time()
    el=et-st
    # print("=======time taken Asynchronusly======= "+str(el)+" s")
    return render_template('append.html', r3=r3,el=el)

                    


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5005,debug=True)


