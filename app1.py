from flask import Flask,render_template,flash,session,redirect,url_for
from models import *
from datetime import datetime,timedelta

app=Flask(__name__,template_folder="template",static_folder="public")
app.secret_key=''
POSTGRES={
    'user'='antho',
    'pw'='flask',
    'host'='localhost',
    'port'='8080',
    'db'='alice'
}
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s %POSTGRES'
db.init_app(app)
app.config.update({
    'DEBUG'=True,
    'MAIL_USE_TLS'=False,
    'MAIL_USE_SSL'=True,
    'MAIL_USER'='',
    'MAIL_PASSWORD'='',
    'MAIL_USERNAME'='',
}
@app.route("/")
def home()
return render_template("home.html")

@app.route("/usignup",methods=["POST","GET"])
def usignup():
    if 'user' in session:
        if request.method=="POST":
            if not request.form["username"] or not request.form["password"] or not request.form["repeat_password"] or not request.form["email"]:
                flash("all fields are requierd to be filled")
                return redirect(url_for('usignup'))
            elif not request.form["password"] == request.form["repeat_password"]:
                flash('passwords don\'t match')
                return redirect(url_for('usignup'))
                newUser=users(request.form['username'].capitalize(),request.form['password'],request.form['repeat_password'],request.form['email'])
                newUser.save()
                session['user']==newUser.username
                return render_template("login.html")
        return render_template(usign.html)

@app.route("/ulogin",,methods=["POST","GET"])
def ulogin():
    if 'user' in session:
        if method=="POST":
            if not request.form['username'] or request.form['password']:
                flash('please enter your details')
            elif not user:
                flash('user does not exist')
                return redirect(url_for('ulogin'))
            elif not sha256_crypt.verify(request.form['password']):
                flash('enter correct password')
                return redirect(url_for('ulogin'))
                user=users.query.filter(request.form['username'])
                session['user']=newUser.username
                return render_template("uwel.html")
        return render_template("ulogin.html")


@app.route("/asignup",methods=["POST","GET"])
def asignup():
    if 'admin' in session:
        if request.method=="POST":
            if not request.form["username"] or not request.form["password"] or not request.form["repeat_password"] or not request.form["email"]:
                flash("all fields are requierd to be filled")
                return redirect(url_for('asignup'))
            elif not request.form["password"] == request.form["repeat_password"]:
                flash('passwords don\'t match')
                return redirect(url_for('asignup'))
                newAdmin=admins(request.form['username'].capitalize(),request.form['password'],request.form['repeat_password'],request.form['email'])
                newAdmin.save()
                session['admin']==newAdmin.username
                return render_template("alogin.html")
        return render_template(asign.html)

@app.route("/alogin",methods=["POST","GET"])
def alogin():
    if 'admin' in session:
        if method=="POST":
            if not request.form['username'] or request.form['password']:
                flash('please enter your details')
            elif not admin:
                flash('admin does not exist')
                return redirect(url_for('alogin'))
            elif not sha256_crypt.verify(request.form['password']):
                flash('enter correct password')
                return redirect(url_for('alogin'))
                user=users.query.filter(request.form['username'])
                session['user']=newUser.username
                return render_template("awel.html")
        return render_template("alogin.html")

@app.route("/books")
def books():
    if request.method=="POST":  
        if not request.form["title"] or  request.form["author"] or request.form["isbn"] or  request.form["quantity"]:
            flash('enter correct credentials') 
            return redirect(url_for('books'))

@app.route("/")
def view():



                   


if __name__=="__main__":
    app.config['DEBUG']=True
    app.run()













































