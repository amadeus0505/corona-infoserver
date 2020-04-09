from covidsession import Covid
import sqlite3
from sqlite3 import Error
import time


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_country_tables(session, conn):
    print("start creating tables")
    countries = session.get_country_names()
    start = time.time()
    for country in countries:
        country = replace_all(country, {" ": "_", ",": "", "*": "", "(": "", ")": "", "'": "", "-": "_"}).lower()
        create_table_cmd = f"""CREATE TABLE IF NOT EXISTS "{country}" (
        "date"	INTEGER NOT NULL,
        "confirmed"	INTEGER NOT NULL,
        "deaths"	INTEGER NOT NULL,
        "recovered"	INTEGER NOT NULL
    );"""
        create_table(conn, create_table_cmd)
    print("Table creation complete\nDuration: " + str(time.time() - start) + " seconds\n")


def replace_all(text, dic: dict):
    for key in dic.keys():
        text = text.replace(key, dic[key])
    return text


def timestamp_exists(cursor, country, timestamp):
    cursor.execute(f"SELECT date FROM {country} WHERE date={timestamp}   ")
    rows = cursor.fetchall()
    return False if len(rows) == 0 else True


def write_data(session: Covid, conn):
    start = time.time()
    all_info = session.get_all_cases_mod()
    print(f"fetched infos in {time.time()-start} seconds")
    cursor = conn.cursor()
    start = time.time()
    for country_info in all_info:
        country = country_info["Country_Region"]
        update_timestamp = int(country_info["Last_Update"]/1000)
        confirmed = country_info["Confirmed"]
        deaths = country_info["Deaths"]
        reco = country_info["Recovered"]
        country = replace_all(country, {" ": "_", ",": "", "*": "", "(": "", ")": "", "'": "", "-": "_"}).lower()
        if timestamp_exists(cursor, country, update_timestamp):
            print(f"data for country {country} at timestamp {update_timestamp} already exists. Continue")
            continue
        else:
            # print("write data for country " + str(country))
            cursor.execute(f"INSERT INTO {country} (date, confirmed, deaths, recovered) VALUES (?,?,?,?)",
                           (update_timestamp, confirmed, deaths, reco))
    conn.commit()
    print(f"wrote info in {time.time() - start} seconds")


def update():
    import os
    try:
        covid_session = Covid()
        connection = create_connection(os.path.join("database", "corona_info.db"))
        create_country_tables(covid_session, connection)
        write_data(covid_session, connection)
    except Exception as e:
        print(e)
    finally:
        connection.close()
