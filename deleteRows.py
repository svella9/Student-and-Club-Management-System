from app import app , db
from University import Student, Student_credential, Faculty, Faculty_credential, Student_feedback, Faculty_feedback, Student_and_advisor

for obj in Student.query.all():
	db.session.delete(obj)

for obj in Student_credential.query.all():
	db.session.delete(obj)

for obj in Faculty.query.all():
	db.session.delete(obj)

for obj in Faculty_credential.query.all():
		db.session.delete(obj)

for obj in Student_feedback.query.all():
	db.session.delete(obj)

for obj in Faculty_feedback.query.all():
	db.session.delete(obj)

for obj in Student_and_advisor.query.all():
	db.session.delete(obj)


db.session.commit()
print('Done')