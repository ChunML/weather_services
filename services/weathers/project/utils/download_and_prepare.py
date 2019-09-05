import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta


URL_TEMPLATE = 'https://tenki.jp/past/{}/{:02d}/{:02d}/amedas/3/17/'
CITY_MAPPING = {
    '横浜': 'Yokohama',
    '日吉': 'Hiyoshi',
    '海老名': 'Ebina',
    '三浦': 'Miura',
    '辻堂': 'Tsujido',
    '相模原中央': 'Sagamihara-Chuo',
    '平塚': 'Hiratsuka',
    '相模湖': 'Sagamiko',
    '丹沢湖': 'Tanzawako',
    '小田原': 'Odawara',
    '箱根': 'Hakone'
}


def get_weather_for_one_day(year, month, day):
    url = URL_TEMPLATE.format(year, month, day)
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc)
    table = soup.find(lambda tag: tag.name == 'table' and 'amedas-point-detail-entries-table' in tag['class'])

    try:
        df = pd.read_html(str(table), na_values=['---'], header=0)[0]
    except Exception as e:
        print(e)
        raise ValueError('No data is available for {}/{}/{}'.format(
            year, month, day))
    df.drop(df.shape[0] - 1, inplace=True)
    df.columns = ['city', 'max_temp', 'min_temp', 'rain', 'wind', 'daylight']
    df['date'] = pd.to_datetime('{}/{}/{}'.format(year, month, day))

    return df


def get_weather_from_date(year, month, day):
    date = datetime(year, month, day)
    today = datetime.utcnow()
    df = []

    while (today - date).days >= 1:
        try:
            df.append(get_weather_for_one_day(date.year, date.month, date.day))
        except ValueError as e:
            print(e)
        finally:
            date += timedelta(days=1)

    return pd.concat(df)


def clean_data(df):
    df = df.copy()
    df.city = df.city.map(CITY_MAPPING)

    temp = df.max_temp.str.split()
    df.max_temp = pd.to_numeric(temp.str.get(0))

    temp = df.min_temp.str.split()
    df.min_temp = pd.to_numeric(temp.str.get(0))

    temp = df.wind.str.split()
    df.wind = pd.to_numeric(temp.str.get(0))
    df.rain = pd.to_numeric(df.rain)

    df = df.fillna(-1e9)

    df = df.reset_index(drop=True)

    return df
