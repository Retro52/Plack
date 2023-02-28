import sqlite3

import config


def select_all_user_events(user_id):
    conn = sqlite3.connect(config.db_path)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {config.db_table} WHERE id={user_id}")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def select_all_events():
    conn = sqlite3.connect(config.db_path)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {config.db_table}")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def init_db():
    sqlite_connection = None
    try:
        sqlite_connection = sqlite3.connect(config.db_path)
        cursor = sqlite_connection.cursor()
        sqlite_create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {config.db_table}
         (
                                    id INTEGER,
                                    event text NOT NULL UNIQUE,
                                    day text NOT NULL,
                                    start_time text NOT NULL,
                                    end_time text NOT NULL,
                                    rep INTEGER,
                                    delta INTEGER 
        );
        '''

        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error connecting to sqlite: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Sqlite connection closed")


def write(id_client, even, day, start_time, end_time, re, delta):
    sqlite_connection = None
    cursor = None
    try:
        sqlite_connection = sqlite3.connect(config.db_path)
        cursor = sqlite_connection.cursor()
    except sqlite3.Error as error:
        print("Error connecting to sqlite: ", error)
    # -
    finally:
        sqlite_test_insert = f'''
        INSERT INTO {config.db_table}
        (id, event, day, start_time, end_time, rep, delta)
        VALUES
        ({id_client},"{even}","{str(day)}","{str(start_time)}","{str(end_time)}",{re},{delta})
        '''
        cursor.execute(sqlite_test_insert)
        sqlite_connection.commit()
        cursor.close()
        sqlite_connection.close()
