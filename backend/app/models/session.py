import datetime
from backend.app.database import db
class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('sessions', lazy=True))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)

    # Представление объекта в виде строки
    def __repr__(self):
        return f'<Session {self.id}>'