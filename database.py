import sqlite3
from os import path, mkdir
import pathlib

DB_PATH = pathlib.Path("data/")
DB_FILEPATH = pathlib.Path("data/data.db")


def initialize_new_db(conn):
    """
    Jobs
    id,id_company,job_title,date_added,date_posted,description,status

    Companies
    id,name

    People
    id,id_company,name,email

    Notes
    id,id_company,id_job,id_person,date,note

    Todos
    id,title,details


    """
    # Create Company table with
    # id, name
    conn.execute('''CREATE TABLE COMPANY
             (COMPANY_ID        INT     PRIMARY KEY     NOT NULL,
              COMPANY_NAME      TEXT    NOT NULL
             );
             ''')

    # Create Jobs table with
    # id,id_company,job_title,date_added,date_posted,description,status
    conn.execute('''CREATE TABLE JOB
             (JOB_ID            INT     PRIMARY KEY     NOT NULL,
              FOREIGN KEY(jobcompany) REFERENCES company(company_id) NOT NULL,
              JOB_TITLE         TEXT,
              JOB_DATE_ADDED    TEXT    DEFAULT CURRENT_DATE,
              JOB_DATE_POSTED   TEXT,
              JOB_DESCRIPTION   TEXT,
              JOB_STATUS        TEXT    DEFAULT "Interested",
             );''')

    # Create Person table with
    # id,id_company,name,email, phone
    conn.execute('''CREATE TABLE PERSON
             (PERSON_ID         INT     PRIMARY KEY     NOT NULL,
              FOREIGN KEY(personcompany) REFERENCES company(company_id) NOT NULL,
              PERSON_NAME       TEXT,
              PERSON_EMAIL      TEXT,
              PERSON_PHONE      INT,
             );''')

    # Create Notes table with
    # id,id_company,id_job,id_person,date,note
    conn.execute('''CREATE TABLE NOTE
             (NOTE_ID           INT     PRIMARY KEY     NOT NULL,
              FOREIGN KEY(notecompany) REFERENCES company(company_id) NOT NULL,
              FOREIGN KEY(notejob) REFERENCES job(job_id) NOT NULL,
              FOREIGN KEY(noteperson) REFERENCES person(person_id) NOT NULL,
              NOTE_DATE_EDITED  TEXT DEFAULT CURRENT_DATE,
              NOTE_DETAILS      TEXT
             );''')

    # Create Todos table with
    # id,title,details
    conn.execute('''CREATE TABLE TODO
             (TODO_ID               INT     PRIMARY KEY     NOT NULL,
              TODO_TITLE            TEXT,
              TODO_DATE_MODIFIED    TEXT    DEFAULT CURRENT_DATE,
              TODO_DETAILS          TEXT,
             );''')

    return conn


def open_db():
    if not path.exists(DB_PATH):
        mkdir(DB_PATH)
    if not path.exists(DB_FILEPATH):
        conn = sqlite3.connect(DB_FILEPATH)
        conn = initialize_new_db(conn)
    else:
        conn = sqlite3.connect(DB_FILEPATH)
    return conn


def get_job_data(conn, job_id):
    """Returns all data for a job as dict of objects
        JOB_ID            INT     PRIMARY KEY     NOT NULL,
        FOREIGN KEY(jobcompany) REFERENCES company(company_id) NOT NULL,
        JOB_TITLE         TEXT,
        JOB_DATE_ADDED    TEXT    DEFAULT CURRENT_DATE,
        JOB_DATE_POSTED   TEXT,
        JOB_DESCRIPTION   TEXT,
        JOB_STATUS        TEXT    DEFAULT "Interested",
    """
    cursor = conn.execute("""SELECT 
                                job_id, 
                                job_title, 
                                job_date_added, 
                                job_date_posted, 
                                job_description, 
                                job_status 
                             FROM job
                             WHERE job_id == (?)
                          """, job_id)
    job_data = {}
    job_data_names = ['job_id',
                      'job_title',
                      'job_date_added',
                      'job_date_posted',
                      'job_description',
                      'job_status']

    for i, cursor_row in enumerate(cursor):
        job_data[job_data_names[i]] = cursor_row[i]

    return job_data


def get_company_data(conn, company_id):
    """Returns all data for a job as dict of objects
        COMPANY_ID        INT     PRIMARY KEY     NOT NULL,
        COMPANY_NAME      TEXT    NOT NULL
    """
    cursor = conn.execute("""SELECT 
                                company_id, 
                                company_name, 
                             FROM company
                             WHERE company_id == (?)
                          """, company_id)
    company_data = {}
    company_data_names = ['company_id',
                          'company_name'
                          ]

    for i, cursor_row in enumerate(cursor):
        company_data[company_data_names[i]] = cursor_row[i]

    return company_data


def get_table_data(conn, table, row_id):
    table_data_names = []
    if table == "job":
        db_data_names = """job_id, job_title, job_date_added, 
                              job_date_posted, job_description, job_status"""
        table_data_names = db_data_names.split(", ")
        cursor = conn.execute("""SELECT (?)
                                 FROM job
                                 WHERE job_id == (?)
                              """, db_data_names, row_id)

    if table == "company":
        db_data_names = """company_id, company_name"""
        table_data_names = db_data_names.split(", ")
        cursor = conn.execute("""SELECT (?)
                                 FROM company
                                 WHERE company_id == (?)
                              """, db_data_names, row_id)

    if table == "note":
        db_data_names = """note_id, note_date_added, note_details"""
        table_data_names = db_data_names.split(", ")
        cursor = conn.execute("""SELECT (?)
                                 FROM note
                                 WHERE note_id == (?)
                              """, db_data_names, row_id)

    if table == "people":
        db_data_names = """person_id, person_name, person_email, person_phone"""
        table_data_names = db_data_names.split(", ")
        cursor = conn.execute("""SELECT (?)
                                 FROM person
                                 WHERE person_id == (?)
                              """, db_data_names, row_id)

    if table == "todo":
        db_data_names = """todo_id, todo_title, todo_date_modified, todo_description"""
        table_data_names = db_data_names.split(", ")
        cursor = conn.execute("""SELECT (?)
                                 FROM todo
                                 WHERE todo_id == (?)
                              """, db_data_names, row_id)
    data = {}

    # Extract data from query cursor
    for i, cursor_row in enumerate(cursor):
        data[table_data_names[i]] = cursor_row[i]

    return data

def insert_table_data(conn, table, dict_of_data_to_insert):
    """Given a connection, a table, and a dict of items, insert data into the table
        assumes keys in

        This may benefit from a validation method and a more global approach to table column names"""
    if table == "job":
        db_data_names = """job_title, job_date_added, 
                              job_date_posted, job_description, job_status"""
        table_data_names = db_data_names.split(", ")
        data_to_insert = (dict_of_data_to_insert[table_data_names[0]],
                          dict_of_data_to_insert[table_data_names[1]],
                          dict_of_data_to_insert[table_data_names[2]],
                          dict_of_data_to_insert[table_data_names[3]],
                          dict_of_data_to_insert[table_data_names[4]])
        cursor = conn.execute("""INSERT INTO job (?)
                                 VALUES (?)
                              """, db_data_names, data_to_insert)

    if table == "company":
        db_data_names = """company_name"""
        table_data_names = db_data_names.split(", ")
        data_to_insert = dict_of_data_to_insert[table_data_names[0]]
        cursor = conn.execute("""INSERT INTO company (?)
                                 VALUES (?)
                              """, db_data_names, data_to_insert)

    if table == "note":
        db_data_names = """note_date_added, note_details"""
        table_data_names = db_data_names.split(", ")
        data_to_insert = (dict_of_data_to_insert[table_data_names[0]],
                          dict_of_data_to_insert[table_data_names[1]])
        cursor = conn.execute("""INSERT INTO note (?)
                                 VALUES (?)
                              """, db_data_names, data_to_insert)

    if table == "person":
        db_data_names = """person_name, person_email, person_phone"""
        table_data_names = db_data_names.split(", ")
        data_to_insert = (dict_of_data_to_insert[table_data_names[0]],
                          dict_of_data_to_insert[table_data_names[1]],
                          dict_of_data_to_insert[table_data_names[2]])
        cursor = conn.execute("""INSERT INTO person (?)
                                 VALUES (?)
                              """, db_data_names, data_to_insert)


    if table == "todo":
        db_data_names = """todo_title, todo_date_modified, todo_description, todo_details"""
        table_data_names = db_data_names.split(", ")
        data_to_insert = (dict_of_data_to_insert[table_data_names[0]],
                          dict_of_data_to_insert[table_data_names[1]],
                          dict_of_data_to_insert[table_data_names[2]],
                          dict_of_data_to_insert[table_data_names[3]])
        cursor = conn.execute("""INSERT INTO person (?)
                                 VALUES (?)
                              """, db_data_names, data_to_insert)

    # Catch errors
    # Commit and return True if successful, return False otherwise

    return conn


def close_db(conn):
    conn.close()
    return True
