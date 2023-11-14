from educationapp.app import db

class Profession(db.Model):
    __tablename__ = 'professions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)