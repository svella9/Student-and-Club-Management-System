from ExaminationAllot import db

class student_subject_code(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    usn = db.Column(db.String(12))
    scode = db.Column(db.String(12))
    def __init__(self, usn, scode):
        self.usn = usn
        self.scode = scode


class exam_hall(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    hallno = db.Column(db.String(5))
    no_of_benches = db.Column(db.Integer)

    def __init__(self, hallno, no_of_benches):
        self.hallno = hallno
        self.no_of_benches = no_of_benches


class faculty_subject_code(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fid = db.Column(db.String(12))
    scode = db.Column(db.String(12))

    def __init__(self, fid, scode):
        self.fid = fid
        self.scode = scode

db.create_all()