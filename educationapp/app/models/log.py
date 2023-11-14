import datetime
from educationapp.app.database import db
class LogEntry(db.Model):
    __tablename__ = 'log_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('log_entries', lazy=True))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    action = db.Column(db.String(64), nullable=False)

    # Представление объекта в виде строки
    def __repr__(self):
        return f'<LogEntry {self.action} by {self.user_id} at {self.timestamp}>'