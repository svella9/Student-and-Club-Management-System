from flask import Flask, flash, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:rakshith@localhost/clubmanagement' 
POSTGRES = {
	'user' : 'uuvxsrrlsehajv',
	'pw' : '3439a19f192e6e6060c7f81f60130cbf452ef8cca871b09057934cab5064d9be',
	'db' : 'dar7l22v5sck20',
	'host' : 'ec2-107-22-173-160.compute-1.amazonaws.com',
	'port' : '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uuvxsrrlsehajv:3439a19f192e6e6060c7f81f60130cbf452ef8cca871b09057934cab5064d9be@ec2-107-22-173-160.compute-1.amazonaws.com:5432/dar7l22v5sck20' % POSTGRES #'postgresql://postgres:mypassword@localhost/University' #URI format: 'postgres://username:password@localhost/database_name'
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True
db = SQLAlchemy(app)
mail_credentials = open('text.txt').read().split('\n')
#print(mail_credentials)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = mail_credentials[0]
app.config['MAIL_PASSWORD'] = mail_credentials[1]
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/') #default page
def index():
	return render_template('index.html')

@app.route('/addNewClub') #Addin new club to database
def addNewClub():
	return render_template('clubInformation.html')

@app.route('/addClubToDatabase',methods = ['POST']) #storing
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

@app.route('/addNewMember') #adding new member to database
def addNewMember():
	return render_template('memberInformation.html')
		

@app.route('/addMemberToDatabase',methods = ['POST']) #storing
def addMemberToDatabase():   #member,event,event_Volenteers,Attendance
	from database import Member,Club
	if request.method == 'POST':
		name = request.form['name']
		USN = request.form['USN']
		clubId = request.form['clubId']
		email = request.form['email']
		member=Member(clubId,name,USN,email)
		db.session.add(member)
		db.session.commit()
		club = Club.query.filter_by(id = clubId).first()
		msg = Message('Registration successful',
			sender = 'ClubNotification@gmail.com',
			recipients = [email])
		msg.body = "Dear Student\n You have been successfully registered for the club" + club.name+"."
		mail.send(msg)
		return 'Member added successfully!!'

	else:
		#Bad Request
		abort(400)

@app.route('/listAllMembers') #to view all members of the club
def list():
	from database import Member
	return render_template("listAllMembers.html",rows=Member.query.all())

@app.route('/addNewEvent') #add new event under a club
def addNewEvent():
	return render_template('eventInformation.html')

@app.route('/addEventToDatabase',methods = ['POST'])
def addEventToDatabase():   #member,event,event_Volenteers,Attendance
	from database import Event, Club, Member
	if request.method == 'POST':
		name = request.form['name']
		eventId = request.form['eventId']
		clubId = request.form['clubId']
		event=Event(eventId,name,clubId)
		db.session.add(event)
		db.session.commit()
		event = Event.query.filter_by(eventId = eventId).first()
		club = Club.query.filter_by(id = clubId).first()
		students = Member.query.filter_by(clubId = club.id).all()
		students = [x.email for x in students]#list(map(lambda x : x.email, students))
	    #print('sending Message', students)
		msg = Message('Event coming up notification.',
			sender = 'ClubNotification@gmail.com',
			recipients = students)
		#print('Object created!')
		msg.body = "Dear Student\n We have a event coming up from the club" + club.name + "and the event is"+event.name+".\n We request you to attend it."
		mail.send(msg)
		return 'Event added successfully!!'

	else:
		#Bad Request
		abort(400)

@app.route('/listAllEvents') #To view all events
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
 
 