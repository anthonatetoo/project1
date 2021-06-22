from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt

db=SQLAlchemy()
class users(db.Model):
    __tablename__='users'
    first_name=db.Column(db.String)
    last_name=db.Column(db.String)
    username=db.Column((db.String),primary_key=True)
    password=db.Column(db.String)
    email=db.Column(db.String)
    gender=db.Column(db.String)
    image=db.Column((db.String),nullable=True)

    def __init__(self,username,password,email,first_name,last_name,gender,image):
        self.username=username
        self.password=sha256_crypt.encrypt(password)
        self.email=email
        self.first_name=first_name
        self.last_name=last_name
        self.gender=gender
        self.image=image

    def save(self):
        db.session.add(self)
        db.session.commit()

class admins(db.Model):
    __tablename__='admins'
    username=db.Column((db.String),primary_key=True)
    password=db.Column(db.String)
    email=db.Column(db.String)

    def __init__(self,username,password,email):
        self.username=username
        self.password=sha256_crypt.encrypt(password)
        self.email=email

    def save(self):
        db.session.add(self)
        db.session.commit()

class books(db.Model):
    __tablename__='books'
    title=db.Column(db.String)
    author=db.Column(db.String)
    isbn=db.Column(db.String)
    quantity=db.Column(db.Integer)
    book_id=db.Column((db.String),primary_key=True)

    def __init__(self,title,author,isbn,quantity,book_id):
        self.title=title
        self.author=author
        self.isbn=isbn
        self.quantity=quantity
        self.book_id=book_id

    def save(self):
        db.session.add(self)
        db.session.commit()

class borrow(db.Model):
    __tablename__='borrow'
    book_id=db.Column(db.String,db.ForeignKey('books.book_id'),nullable=False)
    username=db.Column(db.String,db.ForeignKey('users.username'),nullable=False)
    borrowdate=db.Column(db.DateTime)
    returndate=db.Column(db.DateTime)
    serial=db.Column(db.Integer,autoincrement=True,primary_key=True)
    books=db.relationship('books',backref=db.backref('borrow',cascade='all,delete'))
    users=db.relationship('users',backref=db.backref('borrow',cascade='all,delete'))

    def __init__(self,book_id,username,borrowdate,returndate):
        self.book_id=book_id
        self.username=username
        self.borrowdate=borrowdate
        self.returndate=returndate
    
    def save(self):
        db.session.add(self)
        db.session.commit()
class activities(db.Model):
    __tablename__='activities'
    activity_id=db.Column((db.String),primary_key=True)
    category=db.Column(db.String)
    date=db.Column(db.DateTime)
    username=db.Column(db.String,db.ForeignKey('users.username'),nullable=False)
    users=db.relationship('users',backref=db.backref('activities',cascade='all,delete'))

    def __init__(self,activity_id,category,date,username):
        self.activity_id=activity_id
        self.category=category
        self.date=date
        self.username=username
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    