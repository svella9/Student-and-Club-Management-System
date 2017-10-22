CLUBMANAGEMENT DATABASE
#Define SCHEMA of the DATABASE
from app import db

class Member(db.Model):
    name = db.Column(db.String(20), primary_key = True)
	email = db.Column(db.String(25))
	
    def __init__(self,name,email):
		self.usn = usn
		self.name = name	
		
class Event(db.Model):
	name= db.Column(db.String(20), primary_key = True)
	head= db.Column(db.String(25))	

    def __init__(self,name,head):
		self.name = name
		self.head= head	
		
class Event_Volenteers(db.Model):
	name= db.Column(db.String(20), primary_key = True)
	event= db.Column(db.String(25))	

    def __init__(self,name,head):
		self.name = name
		self.event= event		
		
		
class Attendance(db.Model):
	name= db.Column(db.String(20), primary_key = True)
	event= db.Column(db.String(25))	
	date= db.column(db.String(20))

    def __init__(self,event,name,date):
		self.name=name
		self.event= event
        self.date=date		
		
db.create_all()		
			