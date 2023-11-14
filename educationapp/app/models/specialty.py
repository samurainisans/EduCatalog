from educationapp.app.database import db
class Specialty(db.Model):
    __tablename__ = 'specialties'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    cut_off_score = db.Column(db.Float, nullable=False)  # Проходной балл для специальности

    # Представление объекта в виде строки
    def __repr__(self):
        return f'<Specialty {self.name}>'