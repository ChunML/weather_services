from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import Weather
from project.utils.download_and_prepare import get_weather_from_date, clean_data
from sqlalchemy.exc import IntegrityError


app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('seed_db')
def seed_db():
    df = get_weather_from_date(2019, 9, 1)
    df = clean_data(df)
    dict_df = df.to_dict('index')
    try:
        db.session.add_all([Weather(**rec) for rec in dict_df.values()])
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print('Something just went wrong when populating past data!')


if __name__ == '__main__':
    cli()
