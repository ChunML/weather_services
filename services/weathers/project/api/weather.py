from flask import Blueprint
from flask_restful import Resource, Api
from .models import Weather
from datetime import datetime


weather_blueprint = Blueprint('weather', __name__)
api = Api(weather_blueprint)


class WeatherList(Resource):
    def get(self):
        weather_data = Weather.query.all()
        response_object = {
            'data': [data.to_json() for data in weather_data],
            'status': 'success'
        }

        return response_object, 200


class WeatherDate(Resource):
    def get(self, date):
        date = date.split('-')
        date = [int(d) for d in date]
        if len(date) == 1:
            # Get weather for the whole year
            weather_data = Weather.query.filter(
                Weather.date >= datetime(date[0], 1, 1),
                Weather.date < datetime(date[0] + 1, 1, 1)).all()
        elif len(date) == 2:
            # Get weather for the whole month
            weather_data = Weather.query.filter(
                Weather.date >= datetime(date[0], date[1], 1),
                Weather.date < datetime(date[0], date[1] + 1, 1)).all()
        elif len(date) == 3:
            # Get weather for the specified date
            weather_data = Weather.query.filter_by(date=datetime(*date)).all()

        response_object = {
            'data': [data.to_json() for data in weather_data],
            'status': 'success'
        }

        return response_object, 200


class WeatherDateCity(Resource):
    def get(self, date, city):
        date = date.split('-')
        date = [int(d) for d in date]
        if len(date) == 1:
            # Get weather for the whole year
            query = Weather.query.filter(
                Weather.date >= datetime(date[0], 1, 1),
                Weather.date < datetime(date[0] + 1, 1, 1))
        elif len(date) == 2:
            # Get weather for the whole month
            query = Weather.query.filter(
                Weather.date >= datetime(date[0], date[1], 1),
                Weather.date < datetime(date[0], date[1] + 1, 1))
        elif len(date) == 3:
            # Get weather for the whole month
            query = Weather.query.filter_by(date=datetime(*date))
        weather_data = query.filter_by(city=city).all()
        response_object = {
            'data': [data.to_json() for data in weather_data],
            'status': 'success'
        }

        return response_object, 200


class WeatherCity(Resource):
    def get(self, city):
        weather_data = Weather.query.filter_by(city=city).all()
        response_object = {
            'data': [data.to_json() for data in weather_data],
            'status': 'success'
        }

        return response_object, 200

api.add_resource(WeatherList, '/weathers/')
api.add_resource(WeatherDate, '/weathers/date/<date>/')
api.add_resource(WeatherDateCity, '/weathers/date/<date>/<city>/')
api.add_resource(WeatherCity, '/weathers/city/<city>/')
