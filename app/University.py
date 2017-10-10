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

	def __init__(self, usn, name, sem, dept, email, mob):
		self.usn = usn
		self.name = name
		self.sem = sem
		self.dept = dept
		self.email = email
		self.mob = mob

	def __repr__(self):
		return '<Student %r>' % self.name

class Faculty(db.Model):
	fid = db.Column(db.String(12), primary_key = True)
	name = db.Column(db.String(25))
	dept = db.Column(db.String(3))
	email = db.Column(db.String(50), unique = True)
	mob = db.Column(db.Integer, unique = True)

	def __init__(self, fid, name, dept, email, mob):
		self.fid = fid
		self.name = name
		self.dept = dept
		self.email = email
		self.mob = mob

	def __repr__(self):
		return '<Faculty %r>' %self.name

db.create_all()