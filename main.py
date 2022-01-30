from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import os
import funcs.data as data

app = Flask(__name__,template_folder='static')
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = os.environ['user']
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['password']
app.config['MYSQL_DATABASE_DB'] = os.environ['dbname']
app.config['MYSQL_DATABASE_HOST'] = os.environ['servername']

mysql.init_app(app) 

e_email_ids = []
e_phone_nos = []

@app.route("/") # index page
def index():
    return render_template("index.html")

@app.route("/user", methods=["GET","POST"]) # index page
def user():
    if request.method == "POST":
        req = request.form 
        c_email_id = req['c_email_id'] # storing the input email id
        c_phone_no = req['c_phone_no'] # storing the input phone number
        c_city = req['c_city'] # storing the input city
        c_size = req['c_size'] # storing the input size of members who live collectively
        c_city = c_city.lower()
        try:
            connect = mysql.connect() # for connecting to the database
            cursor = connect.cursor() # cursor to execute mysql queries
            cursor.execute("INSERT INTO client_info(email_id,phone_no,city,size) VALUES (%(email_id)s,%(phone_no)s,%(city)s,%(size)s);",{'email_id':c_email_id,'phone_no': c_phone_no,'city':c_city,'size':c_size}) # mysql query to append data to the dataabase
            connect.commit() # commit changes to database
            output = 'Data Commited Successfully.'
        except Exception as e:
            with open("log.txt","a") as logs: # for logging the errors
                logs.write(f"{str(e)}\n")
            output = 'Unsuccessful'
        return render_template('user.html',msg=output) # rendering the index page with message
    return render_template('user.html')

@app.route("/add_safe_place", methods=["GET","POST"]) # add safe place page
def add_safe_place():
    if request.method == "POST":
        req = request.form 
        s_email_id = req['s_email_id']
        s_phone_no = req['s_phone_no']
        s_city = req['s_city']
        s_address = req['s_address']
        s_strength = req['s_strength']
        s_type = req['s_type']
        s_city = s_city.lower()
        try:
            connect = mysql.connect() # for connecting to the database
            cursor = connect.cursor() # cursor to execute mysql queries
            cursor.execute("INSERT INTO contributors_info(email_id,phone_no,city,strength,type_bunker,details) VALUES (%(email_id)s,%(phone_no)s,%(city)s,%(strength)s,%(type_bunker)s,%(details)s);",{'email_id':s_email_id,'phone_no': s_phone_no,'city':s_city,'strength':s_strength,'type_bunker':s_type,'details':s_address}) # mysql query to append data to the dataabase
            connect.commit() # commit changes to database
            output = 'Data Commited Successfully.'
        except Exception as e:
            with open("log.txt","a") as logs: # for logging the errors
                logs.write(f"{str(e)}\n")
            output = 'Unsuccessful'
        return render_template('add_safe_place.html',msg=output) # rendering the index page with message
    return render_template('add_safe_place.html')

@app.route("/officials", methods=["GET","POST"]) # official page
def officials():
    if request.method == "POST":
        req = request.form 
        o_email_id = req['o_email_id']
        o_password = req['o_password']
        o_city = req['o_city']
        o_type = req['o_type']
        o_city = o_city.lower()
        try:
            connect = mysql.connect() # for connecting to the database
            cursor = connect.cursor() # cursor to execute mysql queries
            cursor.execute("SELECT * FROM official_info;") # mysql query for retriving data from official_info table
            connect.commit() # commit changes to database
            validation = cursor.fetchall() # fetching all the data from the table
            output = ''
            for i in validation: 
                if i[0] == o_email_id and i[1] == o_password: # checking if the input email id and password is present in the table
                    cursor.execute("SELECT c.email_id, c.phone_no, c.size FROM client_info c WHERE c.city = %(city)s;",{'city':o_city}) # mysql query to retrive data to the dataabase
                    connect.commit()
                    people_info = cursor.fetchall()
                    cursor.execute("SELECT * FROM contributors_info s WHERE s.city = %(city)s AND s.type_bunker = %(type)s;",{'city':o_city,'type':o_type}) # mysql query to retrive data to the dataabase
                    connect.commit() # commit changes to database
                    bunker_info = cursor.fetchall() # fetching all the data from the table
                    for l in people_info:
                        e_email_ids.append(l[0]) # appending the email ids of the people who live in the city
                        e_phone_nos.append(l[1]) # appending the phone numbers of the people who live in the city
                    for j in bunker_info:
                        if o_type == j[4]: # checking if the type of bunker is same as the type of bunker sent in alert
                            message_txt = f"{o_type} Alert!\nAll the people are requested to move to a safe place.\nSafe Place Details: {j[5]}.\nSafe Place Phone No: {j[2]}.\nSafe Place Email Id: {j[1]}.\nSafe Place Location: {data.loc_info(j[5])}." # message to be sent to the people who live in the city
                            for k in range(0,len(e_email_ids)):
                                data.send_data(receiver_add=e_email_ids[k],numbers=e_phone_nos[k],text=message_txt) # sending the message in the form of sms and email, to the people who live in the city
                    output = 'Successfully Sent'
                else:
                    output = 'Invalid Credentials'
        except Exception as e:
            with open("log.txt","a") as logs: # for logging the errors
                logs.write(f"{str(e)}\n")
            output = 'Failed to send'
        return render_template('officials.html',msg=output)
    return render_template('officials.html')

if __name__ == '__main__':
    app.run(debug=True)