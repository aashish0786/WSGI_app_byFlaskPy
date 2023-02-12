from flask import Flask,render_template,request
from flask import redirect,flash,url_for,make_response
#import requests
import sqlite3 as sql
from weather import get_lat_lon,get_temprature

app=Flask(__name__)
app.secret_key='slkdjasfhsdifubsdfiudbaiufhbdkjfashbkjfaskjdasgdaklsudhgaskjd'

def get_query(query):
    dbname='weather.db'
    con=sql.connect(dbname)
    cursor=con.cursor()
    cursor.execute(query)
    result=cursor.fetchall()
    con.commit()
    cursor.close()
    con.close()
    return result

@app.route('/signup')
def signup():
    return render_template("signup.html")
@app.route('/usercontrol',methods=['POST'])
def usercontrol():
    name=request.form.get("name",None)
    email=request.form.get("email",None)
    password=request.form.get("password",None)
    if all([name,email,password]):
        name=name.strip().title()
        email=email.strip().lower()
        try:
            query=f"INSERT INTO user(email_id,password,name) Values('{email}','{password}','{name}')"
            get_query(query)
            flash("Account sucessfully created please signin")
            return redirect(url_for('signin'))
        except sql.IntegrityError:
            flash("Error! account already exsists")
            return redirect(url_for('signup'))   
    else:
        flash('Invalid data please check again!')
    return redirect(url_for('signup'))

@app.route('/logout')
def logout():
    resp=make_response(render_template('signin.html'))
    resp.set_cookie('email','')
    return resp

@app.route("/")
def signin():
    email=request.cookies.get('email',None)
    if email:
        result=get_query(f'SELECT * FROM user WHERE email_id="{email}"')
        cities=get_query(f'SELECT * FROM city WHERE email_id="{email}"')
        cities=[v[1] for v in cities]
        data=[]
        for city in cities:
            lat,lon=get_lat_lon(city)
            temp=get_temprature(lat,lon)
            data.append(temp)
        return render_template('userhome.html',username=result[0][2],city=data)
    return render_template("signin.html")
@app.route("/login",methods=["POST"])
def login():
    email=request.form.get("email",None)
    password=request.form.get("password",None)
    if all([email,password]):
        email=email.strip().lower()
        query=f'SELECT * FROM user WHERE email_id="{email}"'
        result=get_query(query)
        if len(result)==0:
            flash("Error! No such account exsists!")
            flash("Please signup or check your datails again")
        else:
            db_password=result[0][1]
            if db_password== password:
                resp=make_response(redirect(url_for('signin')))
                resp.set_cookie('email',email)
                return resp
            else:
                flash("Error! Invalid password try again!")
                return redirect(url_for('signin'))
    else:
        flash('ERROR! invalid form data please try again!')
    return redirect(url_for('signin'))

@app.route('/get_city',methods=['POST'])
def get_city():
    email=request.cookies.get('email',None)
    if email:
        city=request.form.get('city',None).strip().title()
        query=f"SELECT * FROM city WHERE email_id='{email}' AND city='{city}'"
        result=get_query(query)
        if result:
            flash('City already Exsists')
        else:
            pass
            coords=get_lat_lon(city)
            if coords:
                query=f'INSERT INTO city(email_id,city) VALUES("{email}","{city}")'
                get_query(query)
            else:
                flash('Error ! Invalid City Name')
        return redirect(url_for('signin'))
    flash('Please login first to add city!')

@app.route('/delete/<name>')
def delete_city(name):
    email=request.cookies.get('email',None)
    if email:
        query=f'DELETE FROM city WHERE email_id="{email}" AND city="{name}"'
        get_query(query)
    else:
        flash('! Need to Login First ')
    return redirect(url_for('signin'))




if __name__=="__main__":
    app.run(debug=True)

