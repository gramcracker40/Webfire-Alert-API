from db import db

class AlertModel(db.Model):
    __tablename__ = "Alert"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    device_name = db.Column(db.String(80), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String)

