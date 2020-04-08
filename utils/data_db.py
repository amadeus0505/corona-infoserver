import sqlite3
from datetime import datetime


db_path = ""


def setup(path):
    global db_path
    db_path = path


def get_cursor():
    with sqlite3.connect(db_path) as db_conn:
        db_cursor = db_conn.cursor()
    return db_cursor


def get_countries():
    db_cursor = get_cursor()
    db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = db_cursor.fetchall()
    country_names = [row[0] for row in rows]
    country_names.sort()
    return country_names


def get_available_timestamps(country):
    db_cursor = get_cursor()
    db_cursor.execute(f"SELECT date FROM {country} ORDER BY date DESC;")
    rows = db_cursor.fetchall()
    timestamps = [timestamp[0] for timestamp in rows]
    return timestamps


def get_db_info(country, timestamp=None):
    db_cursor = get_cursor()
    if timestamp is None:
        db_cursor.execute(f"SELECT * FROM {country};")
    else:
        db_cursor.execute(f"SELECT * FROM {country} WHERE date = {timestamp}")
    rows = db_cursor.fetchall()
    return rows[len(rows)-1]


def beatify_country_list(countries: list):
    for index, country in enumerate(countries):
        countries[index] = country.replace("_", " ").capitalize()
    return countries


def get_daily_info(country):
    timestamps = get_available_timestamps(country)
    dates = {}
    for timestamp in reversed(timestamps):
        date = str(datetime.fromtimestamp(timestamp)).split(" ")
        dates[date[0]] = timestamp

    return dates


if __name__ == "__main__":
    setup(r"D:\Gabriel\Development\python\corona_info\database\corona_info.db")
    get_available_timestamps("austria")

