from educationapp.app.database import db

class Specialty(db.Model):
    __tablename__ = 'specialties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    code = db.Column(db.String(64), unique=True, nullable=False)
    profession_id = db.Column(db.Integer, db.ForeignKey('professions.id'))
    profession = db.relationship('Profession', backref='specialties')
    education_program = db.Column(db.String(120), nullable=False)
    education_level = db.Column(db.String(120), nullable=False)
    form_of_education = db.Column(db.String(120), nullable=False)
    standard_education_duration = db.Column(db.String(120), nullable=False)
    qualification = db.Column(db.String(120), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'profession_id': self.profession_id,
            'education_program': self.education_program,
            'education_level': self.education_level,
            'form_of_education': self.form_of_education,
            'standard_education_duration': self.standard_education_duration,
            'qualification': self.qualification,
        }