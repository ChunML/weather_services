from flask import Blueprint
from flask_restful import Resource, Api
from .models import Weather
from datetime import datetime


weather_blueprint = Blueprint('weather', __name__)
api = Api(weather_blueprint)


class WeatherOneDay(Resource):
    def get(self, year, month, day):
        weather_data = Weather.query.filter_by(date=datetime(year, month, day)).all()
        response_object = {
            'data': [data.to_json() for data in weather_data],
            'message': 'success'
        }

        return response_object, 200


class WeatherList(Resource):
    def get(self):
        weather_data = Weather.query.all()
        response_object = {
            'data': [data.to_json() for data in weather_data],
            'message': 'success'
        }

        return response_object, 200


class WeatherCity(Resource):
    def get(self, city):
        weather_data = Weather.query.filter_by(city=city).all()
        response_object = {
            'data': [data.to_json() for data in weather_data],
            'message': 'success'
        }

        return response_object, 200


class WeatherCityOneYear(Resource):
    def get(self, city, year):
        weather_data = Weather.query.filter(
            Weather.date >= datetime(year, 1, 1),
            Weather.date < datetime(year + 1, 1, 1)).filter_by(city=city).all()
        response_object = {
            'data': [data.to_json() for data in weather_data],
            'message': 'success'
        }

        return response_object, 200


class WeatherCityOneMonth(Resource):
    def get(self, city, year, month):
        weather_data = Weather.query.filter(
            Weather.date >= datetime(year, month, 1),
            Weather.date < datetime(year, month + 1, 1)).filter_by(city=city).all()
        response_object = {
            'data': [data.to_json() for data in weather_data],
            'message': 'success'
        }

        return response_object, 200


class WeatherCityOneDay(Resource):
    def get(self, city, year, month, day):
        weather_data = Weather.query.filter_by(
            date=datetime(year, month, day), city=city).all()
        response_object = {
            'data': [data.to_json() for data in weather_data],
            'message': 'success'
        }

        return response_object, 200


api.add_resource(WeatherOneDay, '/weathers/<int:year>/<int:month>/<int:day>')
api.add_resource(WeatherList, '/weathers')
api.add_resource(WeatherCity, '/weathers/<city>')
api.add_resource(WeatherCityOneYear, '/weathers/<city>/<int:year>')
api.add_resource(WeatherCityOneMonth, '/weathers/<city>/<int:year>/<int:month>')
api.add_resource(WeatherCityOneDay, '/weathers/<city>/<int:year>/<int:month>/<int:day>')
