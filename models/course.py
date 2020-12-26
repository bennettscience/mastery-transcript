from app import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    canvas_course_id = db.Column(db.Integer)
    course_name = db.Column(db.String(64), index=True)