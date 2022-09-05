from flask import Flask,redirect, render_template_string,url_for,render_template,request,jsonify
from flask_mysqldb import MySQL
import yaml
import json
import time
app = Flask(__name__)

db2 = yaml.full_load(open('s_db.yaml'))
app.config['MYSQL_HOST'] = db2['mysql_host']
app.config['MYSQL_USER'] = db2['mysql_user']
app.config['MYSQL_PASSWORD'] = db2['mysql_password']
app.config['MYSQL_DB'] = db2['mysql_db']

mysql = MySQL(app)

@app.route("/", methods=["POST","GET"])
def home():
    if request.method =="POST":
        name=request.form["pid"]
        return redirect(url_for("name",nid=name))
    else:
        return render_template('apiform.html')

@app.route('/salarylist')
def salarylist():
    cur = mysql.connection.cursor()
    cur.execute("Use SalaryController")
    cur.execute("SELECT * FROM Salary ")
    
    posts=cur.fetchall()
    
    
    return render_template('salarytable.html',posts=posts)

@app.route('/salarylist/<nid>')
def name(nid):
    cur = mysql.connection.cursor()
  
    cur.execute("SELECT * FROM Salary where EmpCode='"+nid+"'")
    
    posts=cur.fetchall()
    
    return render_template('salarytable.html',posts=posts)

@app.route('/insert' ,methods=['GET','POST'])
def salary():
    if request.method =="POST":
        cur = mysql.connection.cursor()
        # eid = request.form['eid']
        # cur.execute("Use PersonController")
        # cur.execute("SELECT EmpCode FROM Persons where ID='"+eid+"'")
        ecode=request.form['eid']
        basic = request.form['basic']
        da = request.form['da']
        gross = float(basic) +float(da)
        cur = mysql.connection.cursor()
        cur.execute("Use SalaryController")
        cur.execute("insert into Salary(EmpCode,Basic,DA,Gross) values (%s,%s,%s,%s)",(ecode,basic,da,gross))
        
        mysql.connection.commit()
        cur.close()
        return redirect('/salarylist')
        
    return render_template('salaryform.html')

@app.route('/api/salarylist')
def api_salarylist():
    cur = mysql.connection.cursor()
    cur.execute("Use SalaryController")
    cur.execute("SELECT * FROM Salary ")
    row_headers=[x[0] for x in cur.description]
    salary=cur.fetchall()
    json_data=[]
    for result in salary:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)

    #return render_template('salarytable.html',salary=salary)

@app.route('/api/salarylist/<nid>')
def api_salary(nid):
    time.sleep(4)
    cur = mysql.connection.cursor()
  
    cur.execute("SELECT * FROM Salary where EmpCode='"+nid+"'")
    row_headers=[x[0] for x in cur.description]
    posts=cur.fetchall()
    json_data=[]
    for result in posts:
        json_data.append(dict(zip(row_headers,result)))
    r=(jsonify(json_data))
    return (r)  

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001,debug=True)