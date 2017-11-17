from flask import Flask, flash, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
#from database import *
#from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:rakshith@localhost/clubmanagement' 
db = SQLAlchemy(app)

@app.route('/addNewClub')
def addNewClub():
	return render_template('clubInformation.html')

@app.route('/addClubToDatabase',methods = ['POST'])
def addClubToDatabase():
	from database import Club
	if request.method == 'POST':
		name = request.form['name']
		id = request.form['id']
		club = Club(name,id)
		db.session.add(club)
		db.session.commit()

		return 'Club Registered successfully!!'

	else:
		#Bad Request
		print(request.form['name'])
		abort(400)

@app.route('/addNewMember')
def addNewMember():
	return render_template('memberInformation.html')
		

@app.route('/addMemberToDatabase',methods = ['POST'])
def addMemberToDatabase():   #member,event,event_Volenteers,Attendance
	from database import Member
	if request.method == 'POST':
		name = request.form['name']
		USN = request.form['USN']
		clubId = request.form['clubId']
		email = request.form['email']
		member=Member(clubId,name,USN,email)
		db.session.add(member)
		db.session.commit()

		return 'Member added successfully!!'

	else:
		#Bad Request
		abort(400)

@app.route('/listAllMembers')
def list():
	from database import Member
	return render_template("listAllMembers.html",rows=Member.query.all())

@app.route('/addNewEvent')
def addNewEvent():
	return render_template('eventInformation.html')

@app.route('/addEventToDatabase',methods = ['POST'])
def addEventToDatabase():   #member,event,event_Volenteers,Attendance
	from database import Event
	if request.method == 'POST':
		name = request.form['name']
		eventId = request.form['eventId']
		clubId = request.form['clubId']
		event=Event(eventId,name,clubId)
		db.session.add(event)
		db.session.commit()

		return 'Event added successfully!!'

	else:
		#Bad Request
		abort(400)

@app.route('/listAllEvents')
def listEvents():
	from database import Event
	return render_template("listAllEvents.html",rows=Event.query.all())

@app.route('/addVolunterForAnEvent')
def addVolunterForAnEvent():
	return render_template('VolunterInformation.html')

@app.route('/addVolunterToDatabase',methods = ['POST'])
def addVolunterToDatabase():   #member,event,event_Volenteers,Attendance
	from database import Event_Volenteers
	if request.method == 'POST':
		usn = request.form['usn']
		eventId = request.form['eventId']
		event_volenteers=Event_Volenteers(usn,eventId)
		db.session.add(event_volenteers)
		db.session.commit()

		return 'Event Volunteer added successfully!!'

	else:
		#Bad Request
		abort(400)

@app.route('/listAllVolunteers')
def listAllVolunteers():	
	from database import Event_Volenteers
	return render_template("listAllVolunteers.html",rows = Event_Volenteers.query.all())

@app.route('/markAttendanceOfAnEvent')
def markAttendanceOfAnEvent():
	return render_template('attendanceInformation.html')

@app.route('/markAttendanceToDatabase',methods = ['POST'])
def markAttendanceToDatabase():		
	from database import Attendance
	
	if request.method == 'POST':
		eventId = request.form['eventId']
		usn = request.form['usn']
		date = request.form['date']
		attendance=Attendance(eventId,usn,date)
		db.session.add(attendance)
		db.session.commit()

		return 'attendance marked'
	else:
		#Bad Request
		abort(400)		

@app.route('/listAllAttendance')
def listAllAttendance():
	from database import Attendance
	return render_template("listAllAttendance.html",rows=Attendance.query.all())  

if __name__ == '__main__':
	app.run(debug=True)		
 
 