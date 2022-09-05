
from flask import Flask,redirect, render_template_string,url_for,render_template,request,jsonify
from flask_mysqldb import MySQL
import yaml
import json
import time
app = Flask(__name__)


db = yaml.full_load(open('p_db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']


mysql = MySQL(app)

@app.route("/", methods=["POST","GET"])
def home():
    if request.method =="POST":
        id=request.form["pid"]
        return redirect(url_for("single_user",pid=id))
    else:
        return render_template('apiform.html')

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    cur.execute("Use PersonController")
    cur.execute("SELECT * FROM Persons ")
    
    posts=cur.fetchall()
    
    return render_template('usertable.html',posts=posts)
    
@app.route('/users/<pid>')
def single_user(pid):
    cur = mysql.connection.cursor()
    cur.execute("Use PersonController")
    cur.execute("SELECT * FROM Persons where EmpCode='"+pid+"'")
    posts=cur.fetchall()
    
    return(render_template('usertable.html',posts=posts))

@app.route('/insert', methods=['GET','POST'])
def insert():
    
    if request.method =="POST":
        ecode = request.form['ecode']
        ename = request.form['ename']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("Use PersonController")
        cur.execute("insert into Persons(EmpCode,EmpName,Address,Phone_No,Email_ID) values (%s,%s,%s,%s,%s)",(ecode,ename,address,phone,email))
        #cur.execute("insert into Persons values (ecode,ename,address,phone,email)",(ecode,ename,address,phone,email))
        mysql.connection.commit()
        cur.close()
        return redirect('/users')
        
    return render_template('empform.html')
   


@app.route('/api/users')
def api_users():
    cur = mysql.connection.cursor()
    cur.execute("Use PersonController")
    cur.execute("SELECT * FROM Persons ")
    row_headers=[x[0] for x in cur.description]
    posts=cur.fetchall()
    json_data=[]
    for result in posts:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)
    #return render_template('usertable.html',posts=posts)

@app.route('/api/users/<pid>')
def name_name(pid):
    time.sleep(4)
    cur = mysql.connection.cursor()
    cur.execute("Use PersonController")
    cur.execute("SELECT * FROM Persons where EmpCode='"+pid+"'")
    row_headers=[x[0] for x in cur.description]
    posts=cur.fetchall()
    json_data=[]
    for result in posts:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)
    #return(render_template('usertable.html',posts=posts))

"""
@app.route('/salary' ,methods=['GET','POST'])
def salary():
    if request.method =="POST":
        cur = mysql.connection.cursor()
        eid = request.form['eid']
        cur.execute("Use PersonController")
        cur.execute("SELECT EmpCode FROM Persons where ID='"+eid+"'")
        ecode=cur.fetchall()
        basic = request.form['basic']
        da = request.form['da']
        gross = float(basic) +float(da)
        cur = mysql.connection.cursor()
        cur.execute("Use SalaryController")
        cur.execute("insert into Salary(P_ID,EmpCode,Basic,DA,Gross) values (%s,%s,%s,%s,%s)",(eid,ecode,basic,da,gross))
        
        mysql.connection.commit()
        cur.close()
        return redirect('/salarylist')
        
    return render_template('salaryform.html')

@app.route('/salarylist')
def salarylist():
    cur = mysql.connection.cursor()
    cur.execute("Use SalaryController")
    cur.execute("SELECT * FROM Salary ")
    salary=cur.fetchall()
    return render_template('salarytable.html',salary=salary)


"""



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)


