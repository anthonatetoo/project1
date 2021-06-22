from flask import Flask,url_for,render_template,redirect,session,flash,request
import psycopg2
from flask_migrate import Migrate
from models import *
from flask_mail import Message,Mail
import os
import uuid
from datetime import datetime as Date,timedelta
from werkzeug.utils import secure_filename
from PIL import Image

UPLOAD_FOLDER=os.path.dirname(os.path.abspath(__file__)) + "/public/img"
app=Flask(__name__,template_folder="templates",static_folder="public")
app.secret_key= 'godwill8764'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
POSTGRES = {
    'user':'godwill',
    'pw' : 'godwill63',
    'port' :'5432',
    'host' : 'localhost',
    'db' : 'jerop',
}
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db.init_app(app)
app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USE_TLS=False,
    MAIL_USERNAME='gtreksolution@gmail.com',
    MAIL_PASSWORD='godwill8764'

)
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(minutes=10)

connection=psycopg2.connect(user="godwill",password="godwill63",host="127.0.0.1",port="5432",database="jerop")
cursor=connection.cursor()
migrate=Migrate(app,db)
mail=Mail(app)
@app.route("/")
def home():
    print(uuid.uuid4())
    return render_template("homepage.html")

@app.route("/signup",methods=["POST","GET"]) 
def signup():
    if request.method == "POST":
        if not(request.form['first_name'] or not request.form['last_name'] or not request.form['username'] or not request.form['password'] or not request.form['repeat_password'] or not request.form['email'] or not request.form['gender']):            
            flash('please fill all fields')
            return redirect(url_for('signup'))
        elif request.form['password'] != request.form['repeat_password']:            
            flash('passwords don\'t match')
            return redirect(url_for('signup'))

        newUser=users(username=request.form['username'].capitalize(),password=request.form['password'],email=request.form['email'],first_name=request.form['first_name'].capitalize(),last_name=request.form['last_name'].capitalize(),gender=request.form["gender"])
        newUser.save()
        session['user']=newUser.username
        session.permanent=False
        activitis=activities.query.filter(activities.username==session['user']).all()
        return render_template("user/udashboard.html",activities=activitis,profile=newuser,user=session['user'])
    return render_template("user/signup.html")
@app.route("/ulogins",methods=["POST","GET"])
def ulogins():
    if 'user' in session:
        user=users.query.filter(users.username==session['user'].capitalize()).first()
        activitis=activities.query.filter(activities.username==session['user']).all()
        return render_template("user/udashboard.html",activities=activitis,profile=user,user=session['user'])
    elif request.method == "POST":
        if not(request.form['username'] or not request.form['password']):
            flash('enter your detail in all fields')

            return redirect(url_for('ulogins'))
        user=users.query.filter(users.username==request.form['username'].capitalize()).first()
        #print(user)
        if not user:
            flash("user does not exist")
            return redirect(url_for('ulogins'))
        
        elif not sha256_crypt.verify(request.form['password'],user.password):
            flash( "enter correct credentials")
            return redirect(url_for('ulogins'))
        else:
            session['user']=user.username
            session.permanent=False
            activitis=activities.query.filter(activities.username==session['user']).all()
            return render_template("user/udashboard.html",activities=activitis,profile=user,user=session['user'])
    elif request.method=="GET":
        return render_template("user/ulogin.html")

@app.route('/upload_folder',methods=["POST","GET"])
def upload_folder():
    if 'user' in session:
        if request.method=='POST':
            user=users.query.filter(users.username==session['user']).first()
            if user.image != '':
                path= os.path.join(UPLOAD_FOLDER, user.image)
                os.remove(path)
            file=request.files['file']
            image=Image.open(file)
            newImage=image.resize((200,200))
            filename=secure_filename(file.filename)
            newImage.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            user.image=filename
            activity=activities(activity_id=uuid.uuid4(),username=session['user'],date=Date.now(),category='Upload Photo')
            activity.save()
            user.save()
            return redirect(url_for('profile'))
    return render_template("user/ulogin.html")    

@app.route("/asignup",methods=["POST","GET"])
def asignup():
    if request.method=="POST":
        if not request.form['username'] or not request.form['password'] or not request.form['email']:
            flash('please fill all fields') 
            return redirect(url_for('asignup'))
        elif not request.form['password']  == request.form['repeat_password']:
            flash('passwords don\'t match')
            return redirect(url_for('asignup'))
        newAdmin=admins(username=request.form['username'].capitalize(),password=request.form['password'],email=request.form['email'])
        newAdmin.save()
        session['user']=newAdmin.username
        session.permanent=True
        return render_template("admin/adminwel.html",admin=session['user'])
    return render_template("admin/adminsignup.html")
    

# @app.route("/alogin",methods=["POST","GET"])
# def alogin():
#     return render_template("admin/alogin.html")


@app.route("/login",methods=["POST","GET"])
def login():     
    if request.method == "POST":
        if not request.form['username'] or not request.form['password']:
            flash('please fill all fields')
            return redirect(url_for('login'))
        username=admins.query.filter(admins.username==request.form['username'].capitalize()).first()
        if not username:
            flash("admins does not exist")
            return redirect(url_for('login'))
            
        elif not sha256_crypt.verify(request.form['password'],username.password):
            
            flash( "enter correct credentials")
            return redirect(url_for('login'))
        session['admin']=username.username
        session.permanent=True
        return render_template("admin/adminwel.html",admin=session['admin'])
    elif request.method == "GET":        
        return render_template("admin/alogin.html")
@app.route("/abooks",methods=["POST","GET"])
def abooks():
    if 'admin' in session:
        print(session['admin'])
        if request.method =="POST":
            if not request.form['title'] or not request.form['author'] or not request.form['quantity'] or not request.form['ISBN']:
                flash('enter your details in all fields')
                return redirect(url_for('abooks'))              
            newBooks=books(title=request.form['title'].capitalize(),author=request.form['author'].capitalize(),quantity=request.form["quantity"],book_id=uuid.uuid4(),isbn=request.form['ISBN'])
            newBooks.save()
            flash('success')
            return redirect(url_for('abooks'))
        return render_template("books/books.html")
    flash('you are not allowed to access this route')
    return redirect(url_for('login'))
@app.route("/viewbooks")
def viewbooks():
    nbook=books.query.all()
    borrowers=borrow.query.all()
    user=None
    if 'admin' in session:
        user=session['admin']
    else:
        user=session['user']
    return render_template("books/search.html",books=nbook,user=user,borrower=borrowers)

@app.route("/searchedbook",methods=["GET", "POST"])
def searchedbook():
    if request.form['search']=='title':
        book=books.query.filter(books.title==request.form['searchbook'].capitalize()).all()
        return render_template("books/search.html",books=book)
    

    
   
    elif request.form['search']=='isbn':
        book=books.query.filter(books.isbn==request.form['searchbook']).all()
        return render_template("books/search.html",books=book)
    

    elif request.form['search']=='author':
        book=books.query.filter(books.author== request.form['searchbook'].capitalize()).all()
        return render_template("books/search.html",books=book)
           

@app.route("/borrows", methods=['GET', 'POST'])
def borrows():  
    if 'user' in session: 
        ibooks=borrow.query.filter(borrow.username==request.args.get("username")).all()
        if len(ibooks)>=5:
            flash('you can\'t exceed maximum threshold of 5 books')
            return redirect(url_for('viewbooks'))
        for book in ibooks:
            print(book.book_id)
            if(book.book_id==request.args.get('book_id')):
                flash('you can\'t borrow a book twice')
                return redirect(url_for('viewbooks'))
        newBorrow=borrow(book_id=request.args.get("book_id"), username=request.args.get("username"),borrowdate=Date.now(), returndate=(Date.now() + timedelta(days=5)))
        newBorrow.save()
        book=books.query.filter(books.book_id==request.args.get('book_id')).first()
        book.quantity -=1
        book.save()
        activity=activities(activity_id=uuid.uuid4(),username=session['user'],date=Date.now(),category='Borrow Book')
        activity.save()
        flash('success')
        return redirect(url_for('viewbooks'))
    elif 'admin' in session:
        flash('you are an admin and can\'t borrow books')
        return redirect(url_for('viewbooks'))
    flash('you are not authorized to access this route')
    return redirect(url_for('ulogins'))
@app.route("/returnbook",methods=["POST","GET"])
def returnbook():
    borrowed_books=borrow.query.filter(borrow.book_id==request.args.get('book_id')).all()
    for book in borrowed_books:
        if book.username ==request.args.get('username'):
            db.session.delete(book)
            db.session.commit()
            book=books.query.filter(books.book_id==request.args.get('book_id')).first()
            book.quantity +=1
            book.save()
            # user=users.query.filter(users.username==session['user']).first()
            # msg=Message('Acceptance of returned book',
            # sender='godwillkisia@noreply.com',
            # recipients=[user.email])
            # msg.body=('hello ' + session['user'] + ' you have successfuly returned borrowed book by the name ' + books.query.filter(books.book_id==request.args.get('book_id')).first().title)
            # mail.send(msg)
            activity=activities(activity_id=uuid.uuid4(),username=session['user'],date=Date.now(),category='Return Book')
            activity.save()
            flash('books successfuly returned')
            return redirect(url_for('viewbooks'))
    
    flash('you never borrowed such a book')
    return redirect(url_for('viewbooks'))
@app.route("/logout",methods=['GET','POST'])
def logout():
    if 'admin' in session:
        session.pop('admin', None)
        return redirect(url_for('login'))
    elif 'user' in session:
        session.pop('user',None)
        return redirect(url_for('ulogins'))
@app.route("/viewusers")
def viewusers():
    if 'admin' in session:
        user=users.query.all()
        return render_template("admin/allusers.html",users=user)
    flash('you are not allowed to view available users')
    return redirect(url_for('ulogin')) 

#user profile
@app.route("/profile")
def profile():
    if 'user' in session:
        user=users.query.filter(users.username==session['user']).first()
        return render_template("user/userwel.html",profile=user,user=session['user'])
    return render_template("user/ulogin.html")

# route to change profile information
@app.route("/updateprofile",methods=["POST","GET"])
def updateprofile():
    if 'user' in session:
        if request.method=="POST":
            if not request.form["email"] or not request.form["first_name"] or not request.form["last_name"]:
                flash('enter all fields')
                return redirect(url_for('ulogins'))
            user=users.query.filter(users.username==session['user']).first()
            user.first_name=request.form["first_name"].capitalize()
            user.last_name=request.form["last_name"].capitalize()
            user.email=request.form["email"]
            user.save()
            activity=activities(activity_id=uuid.uuid4(),username=session['user'],date=Date.now(),category='Update Profile')
            activity.save()
            return redirect(url_for('ulogins'))
    return redirect(url_for('home'))
@app.route("/changepassword",methods=["POST","GET"])
def changepassword():
    if 'user' in session:
        if request.method=="POST":
            if not request.form["old_password"] or not request.form["new_password"] or not request.form["repeat_password"]:
                flash('please enter all fields')
                return redirect(url_for('ulogins'))
            elif not request.form['new_password'] == request.form["repeat_password"]:
                flash('passwords don\'t match')
                return redirect(url_for('ulogins'))
            user=users.query.filter(users.username==session['user']).first()
            if sha256_crypt.verify(request.form["old_password"],user.password):
                user.password=sha256_crypt.encrypt(request.form["new_password"])
                user.save()
                activity=activities(activity_id=uuid.uuid4(),username=session['user'],date=Date.now(),category='Change Password')
                activity.save()
                session.pop('user',None)
                flash('login again to continue')
                return redirect(url_for('ulogins'))
            flash('enter correct password')
            return redirect(url_for('ulogins'))
    flash('you are not in session')
    return redirect(url_for('home'))

                
        

if __name__=="__main__":
    
    app.config['DEBUG']=True
    app.run()


