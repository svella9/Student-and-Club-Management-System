from app import db

class Event_Volenteers(db.Model):
	#id = db.Column(db.Integer,primary_key=True)
	usn = db.Column(db.String(10),db.ForeignKey('member.usn'), primary_key = True)
	eventId= db.Column(db.String(10),db.ForeignKey('event.eventId'), primary_key = True)	
	def __init__(self,usn,eventId):
		self.usn = usn
		self.eventId = eventId				

class Attendance(db.Model):
	#id = db.Column(db.Integer,primary_key = True)
	eventId= db.Column(db.String(10),db.ForeignKey('event.eventId'),primary_key = True)	
	usn = db.Column(db.String(10),db.ForeignKey('member.usn'),primary_key = True)
	date = db.Column(db.DateTime(),primary_key = True)
	print(date)
	def __init__(self,eventId,usn,date):
		self.usn = usn
		print(date)
		self.eventId = eventId
		self.date = date		


class Club(db.Model):
	name = db.Column(db.String(50))
	id = db.Column(db.String(10), primary_key = True)
	member_constraint = db.relationship('Member', backref='member',lazy='dynamic')
	event_constraint = db.relationship('Event', backref='event',lazy='dynamic')
	def __init__(self,name,id):
		self.name = name
		self.id = id

class Member(db.Model):
	usn = db.Column(db.String(10),primary_key=True)
	name = db.Column(db.String(20))
	clubId = db.Column(db.String(10), db.ForeignKey('club.id'))
	email = db.Column(db.String(25))
	eventVolenteer_constraint = db.relationship('Event_Volenteers', backref='eventVolenteers2',lazy='dynamic')
	attendance_constraint = db.relationship('Attendance', backref='attendance2',lazy='dynamic')
	def __init__(self,cId,name,usn,email):
		self.usn = usn
		self.name = name
		self.clubId = cId
		self.email = email

class Event(db.Model):
	eventId = db.Column(db.String(10), primary_key = True)
	name = db.Column(db.String(25))	
	clubId = db.Column(db.String(10), db.ForeignKey('club.id'))
	eventVolenteer_constraint = db.relationship('Event_Volenteers', backref='eventVolenteers1',lazy='dynamic')	
	attendance_constraint = db.relationship('Attendance', backref='attendance1',lazy='dynamic')	
	def __init__(self,eventId,name,cId):
		self.name = name
		self.clubId= cId
		self.eventId= eventId

db.create_all()		