from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Thread(db.Model):
    __tablename__ = "thread"
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.Text, nullable=False)
    output = db.Column(db.Text, nullable=True)
    directory = db.Column(db.Text, nullable=True)