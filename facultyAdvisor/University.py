#UNIVERSITY DATABASE
#Define SCHEMA of the DATABASE
from app import db
from datetime import datetime

class Student(db.Model):
	usn = db.Column(db.String(12), primary_key = True)
	name = db.Column(db.String(25))
	sem = db.Column(db.Integer)
	dept = db.Column(db.String(3))
	email = db.Column(db.String(50), unique = True)
	mob = db.Column(db.BigInteger, unique = True)

	#foreign key relationship
	#backref: creates a virtual column called 'student' in 'Student_feedback' class that references the 'Student' class.
	feedback_by_student = db.relationship('Student_feedback' , backref = 'student', lazy = 'dynamic')
	feedback_by_faculty = db.relationship('Faculty_feedback', backref = 'student', lazy = 'dynamic')
	student_n_advisor = db.relationship('Student_and_advisor', backref = 'student', lazy = 'dynamic')
	
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
	mob = db.Column(db.BigInteger, unique = True)

	feedback_by_faculty = db.relationship('Faculty_feedback', backref = 'faculty', lazy = 'dynamic')
	faculty_advisor = db.relationship('Student_and_advisor', backref = 'faculty', lazy = 'dynamic' )

	def __init__(self, fid, name, dept, email, mob):
		self.fid = fid
		self.name = name
		self.dept = dept
		self.email = email
		self.mob = mob

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
	password = db.Column(db.String(50))

	def __init__(self, fid, password):
		self.fid = fid
		self.password = password

class Student_feedback(db.Model):
	id = db.Column(db.Integer , primary_key = True)
	usn = db.Column(db.String(12) , db.ForeignKey('student.usn'))
	#Record the current date and time when the row is inserted
	date = db.Column(db.DateTime() , default = datetime.now())
	feedback = db.Column(db.String(200))

	def __init__(self, feedback, student):
		self.feedback = feedback
		self.student = student

class Faculty_feedback(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	fid = db.Column(db.String(12), db.ForeignKey('faculty.fid'))
	student_usn = db.Column(db.String(12), db.ForeignKey('student.usn'))
	#Record the current date and time when the row is inserted
	date = db.Column(db.DateTime() , default = datetime.now())
	feedback = db.Column(db.String(200))

	def __init__(self, feedback, faculty, student):
		self.feedback = feedback
		self.faculty = faculty
		self.student = student


class Student_and_advisor(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	usn = db.Column(db.String(12), db.ForeignKey('student.usn'), unique = True)
	fid = db.Column(db.String(12), db.ForeignKey('faculty.fid'))

	def __init__(self, usn, fid, student, faculty):
		self.usn = usn
		self.fid = fid
		self.student = student
		self.faculty = faculty


db.create_all()
