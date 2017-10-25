#UNIVERSITY DATABASE
#Define SCHEMA of the DATABASE
from app import db

class Student(db.Model):
	usn = db.Column(db.String(12), primary_key = True)
	name = db.Column(db.String(25))
	sem = db.Column(db.Integer)
	dept = db.Column(db.String(3))
	email = db.Column(db.String(50), unique = True)
	mob = db.Column(db.Integer, unique = True)
	advisor = db.Column(db.String(25))
	visited=db.Column(db.Boolean())
	def __init__(self, usn, name, sem, dept, email, mob):
		self.usn = usn
		self.name = name
		self.sem = sem
		self.dept = dept
		self.email = email
		self.mob = mob
		self.advisor= "none"
		self.visited= 'false'
	def __repr__(self):
		return '<Student %r>' % self.name

class Faculty(db.Model):
	fid = db.Column(db.String(12), primary_key = True)
	name = db.Column(db.String(25))
	dept = db.Column(db.String(3))
	email = db.Column(db.String(50), unique = True)
	mob = db.Column(db.Integer, unique = True)
	date=db.Column(db.DateTime)
	sem=db.Column(db.Integer)
	def __init__(self, fid, name, dept, email, mob):
		self.fid = fid
		self.name = name
		self.dept = dept
		self.email = email
		self.mob = mob
		self.sem=-1
	
	def __repr__(self):
		return '<Faculty %r>' %self.name

class Student_credential(db.Model):
	usn = db.Column(db.String(12) , primary_key = True)
	password = db.Column(db.String(50))

	def __init__(self, usn, password):
		self.usn = usn
		self.password = password

class Faculty_credential(db.Model):
	fid = db.Column(db.String(12), primary_key = True)
	password = db.Column(db.String(50), primary_key = True)

	def __init__(self, fid, password):
		self.fid = fid
		self.password = password

db.create_all()