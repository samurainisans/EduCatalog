from educationapp.app import db


class Direction(db.Model):
    __tablename__ = 'directions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialties.id'))
    specialty = db.relationship('Specialty', backref='directions')
