from project import db
from datetime import datetime


class Weather(db.Model):
    __tablename__ = 'weathers'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    max_temp = db.Column(db.Float)
    min_temp = db.Column(db.Float)
    wind = db.Column(db.Float)
    rain = db.Column(db.Float)
    daylight = db.Column(db.Float)

    __table_args__ = (db.UniqueConstraint('date', 'city'),)

    def __init__(self, **kwargs):
        super(Weather, self).__init__(**kwargs)

    def to_json(self):
        return {
            'date': self.date.strftime("%Y/%m/%d"),
            'city': self.city,
            'max_temp': self.max_temp,
            'min_temp': self.min_temp,
            'wind': self.wind,
            'rain': self.rain,
            'daylight': self.daylight
        }
