import sqlite3
from os import path, mkdir
import pathlib

DB_PATH = pathlib.Path("data/")
DB_FILEPATH = pathlib.Path("data/data.db")

def create_new_db(conn):
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
    conn.execute('''CREATE TABLE IF NOT EXISTS company
             (company_id       INTEGER     PRIMARY KEY     NOT NULL,
              company_name      TEXT    NOT NULL
             );
             ''')

    # Create Jobs table with
    # id,id_company,job_title,date_added,date_posted,description,status
    #              FOREIGN KEY (job_company) REFERENCES company (company_id) NOT NULL,
    conn.execute('''CREATE TABLE IF NOT EXISTS job
             (job_id INTEGER PRIMARY KEY NOT NULL,
              job_company INTEGER NOT NULL,
              job_title TEXT,
              job_date_added TEXT DEFAULT CURRENT_DATE,
              job_date_posted TEXT,
              job_description TEXT,
              job_status TEXT DEFAULT "Interested",
              FOREIGN KEY (job_company) REFERENCES company (company_id)
             );''')

    # Create Person table with
    # id,id_company,name,email, phone
    conn.execute('''CREATE TABLE IF NOT EXISTS person
             (person_id         INTEGER     PRIMARY KEY     NOT NULL,
              person_company    INTEGER     NOT NULL,
              person_name       TEXT,
              person_email      TEXT,
              person_phone      INTEGER,
              FOREIGN KEY(person_company) REFERENCES company(company_id)
             );''')

    # Create Notes table with
    # id,id_company,id_job,id_person,date,note
    conn.execute('''CREATE TABLE IF NOT EXISTS note
             (note_id           INTEGER     PRIMARY KEY     NOT NULL,
              note_company      INTEGER,
              note_person       INTEGER,
              note_job          INTEGER,
              note_title        TEXT,
              note_date_edited  TEXT DEFAULT CURRENT_DATE,
              note_details      TEXT,
              FOREIGN KEY(note_company) REFERENCES company(company_id),
              FOREIGN KEY(note_job) REFERENCES job(job_id),
              FOREIGN KEY(note_person) REFERENCES person(person_id)
             );''')

    # Create Todos table with
    # id,title,details
    conn.execute('''CREATE TABLE IF NOT EXISTS todo
             (todo_id               INTEGER     PRIMARY KEY NOT NULL,
              todo_title            TEXT,
              todo_date_modified    TEXT    DEFAULT CURRENT_DATE,
              todo_details          TEXT
             );''')
    print("from creator", conn)
    return conn


def insert_many_table_data(conn, table, list_of_data_to_insert):
    """Given a connection, a table, and a dict of items, insert data into the table
        assumes keys in

        This may benefit from a validation method and a more global approach to table column names"""
    if table == "job":
        """(job_id INTEGER PRIMARY KEY NOT NULL,
        job_company INTEGER NOT NULL,
        job_title TEXT,
        job_date_added TEXT DEFAULT CURRENT_DATE,
        job_date_posted TEXT,
        job_description TEXT,
        job_status TEXT DEFAULT "Interested","""
        db_data_names = """job_title, job_date_added, job_date_posted, job_description, job_status"""
        table_data_names = db_data_names.split(", ")
        cursor = conn.executemany('''INSERT INTO job
                                  VALUES (?, ?, ?, ?, ?, ?, ?)''', list_of_data_to_insert)

    if table == "company":
        db_data_names = "company_name"
        table_data_names = db_data_names.split(", ")
        cursor = conn.executemany('''INSERT INTO company
                                  VALUES (?, ?)''', list_of_data_to_insert)

    if table == "note":
        db_data_names = """note_id, note_company, note_person, note_job, note_title, note_date_edited, note_details"""
        table_data_names = db_data_names.split(", ")
        cursor = conn.executemany('''INSERT INTO note
                               VALUES (?, ?, ?, ?, ?, ?, ?)''', list_of_data_to_insert)

    if table == "person":
        db_data_names = """person_id, person_company, person_name, person_email, person_phone"""
        table_data_names = db_data_names.split(", ")
        cursor = conn.executemany('''INSERT INTO person
                                  VALUES (?, ?, ?, ?, ?)''', list_of_data_to_insert)

    if table == "todo":
        db_data_names = """todo_title, todo_date_modified, todo_details"""
        table_data_names = db_data_names.split(", ")
        cursor = conn.executemany('''INSERT INTO todo
                                  VALUES (?, ?, ?, ?)''', list_of_data_to_insert)
    return conn


def insert_test_data_via_objects(conn):
    # Insert test data into each of the tables

    # Insert test data into todos table
    list_of_data_to_insert = [
        (None, "Add SQLite insertions to DB interface", "2021-12-01", ""),
        (None, "Reply to Abby at Google", "2021-12-02", ""),
        (None, "Review companies of interest to see if they have any new positions", "2021-12-03", ""),
        (None, "Add jobs from LinkedIn recruiters", "2021-12-04", ""),
        (None, "Develop prototype of job scraper", "2021-12-05", ""),
        (None, "Spend 1 hour thinking about tools for learning", "2021-12-06", ""),
    ]
    insert_many_table_data(conn, "todo", list_of_data_to_insert)

    # Insert test data into company table
    list_of_data_to_insert = [
        (None, "Albacore"),
        (None, "BuyNLarge"),
        (None, "Caltech"),
        (None, "Dennys"),
        (None, "Enron"),
        (None, "Facebook"),
        (None, "Google"),
    ]
    insert_many_table_data(conn, "company", list_of_data_to_insert)

    # Insert test data into job table
    list_of_data_to_insert = [
        (None, 1, "Software Engineer", "2021-12-01", "2021-11-01", "Lorem Ipsum", "Interested"),
        (None, 2, "Engineer in Test", "2021-12-01", "2021-11-02", "Lorem Ipsum", "Interested"),
        (None, 3, "Program Manager", "2021-12-01", "2021-11-02", "Lorem Ipsum", "Interested"),
        (None, 1, "Product Designer", "2021-12-01", "2021-11-04", "Lorem Ipsum", "Interested"),
        (None, 5, "Engineering Manager", "2021-12-01", "2021-11-05", "Lorem Ipsum", "Interested"),
        (None, 7, "Junior Software Engineer", "2021-12-06", "2021-12-01", "Lorem Ipsum", "Interested"),
        (None, 1, "SDE I", "2021-12-06", "2021-12-02", "Lorem Ipsum", "Interested"),
        (None, 1, "Software Engineer - Backend, Finance", "2021-12-06", "2021-12-03", "Lorem Ipsum", "Interested"),
        (None, 1, "Manager; Software Engineering", "2021-12-06", "2021-12-04", "Lorem Ipsum", "Interested"),
        (None, 1, "Software Engineering and Product Design Specialist", "2021-12-06", "2021-12-05", "Lorem Ipsum", "Interested"),
    ]
    insert_many_table_data(conn, "job", list_of_data_to_insert)

    # Insert test data into people table
    # person_id, company_id, person_name, person_email, person_phone
    list_of_data_to_insert = [
        (None, 1, "Alice Baker", "abaker@something.com", "123-456-7890"),
        (None, 1, "Cooper Douglas", "cdcdcd@something.com", "123-456-7890"),
        (None, 1, "Eugene Fernando", "eforever@something.com", "123-456-7890"),
        (None, 2, "Gretchen Hyacinth", "hyacinth-g@something.com", "123-456-7890"),
        (None, 3, "Jeannie Kidseth", "jkidseth@something.com", "123-456-7890"),
        (None, 4, "Liz Maroney", "notjennamaroney@something.com", "123-456-7890"),
        (None, 5, "Norbert Ort", "norbort@something.com", "123-456-7890"),
        (None, 6, "Penny Quinn", "pennyforaquinn@something.com", "123-456-7890")
    ]
    insert_many_table_data(conn, "person", list_of_data_to_insert)


    # Insert test data into note table
    db_data_names = """note_id, note_company, note_person, note_job, note_title, note_date_edited, note_details"""
    list_of_data_to_insert = [
        (None, 6,   1, 3, "Test note 1", "2021-12-01", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam quis magna vitae augue ornare luctus et vel sapien. Etiam et neque id nisl volutpat venenatis eget id odio. Etiam lobortis orci nulla, sed varius libero mattis sit amet. Aenean tristique finibus tincidunt. Duis interdum, lectus in volutpat congue, odio libero condimentum enim, cursus vulputate tortor elit et odio."),
        (None, 4,   None, 2, "Test note 2", "2021-12-02", "Phasellus posuere consequat arcu, at convallis erat scelerisque in. Vestibulum id volutpat augue. Curabitur pretium augue diam, a dignissim risus fringilla eu. Phasellus blandit luctus erat eget vulputate. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos."),
        (None, 2,   None, None, "Test note 3", "2021-12-03", "Praesent volutpat justo in ante bibendum, id posuere elit facilisis. Nullam nec dolor id eros blandit porta nec vel ante. Duis ante velit, pretium nec mi non, pharetra tristique neque. Praesent eu rutrum ex, nec faucibus purus. "),
        (None, None, 2, 1, "Test note 4", "2021-12-04", "Nulla tincidunt, nunc semper fringilla tincidunt, ex orci egestas risus, ut eleifend libero ante id massa. Curabitur ut leo non ex dignissim iaculis. Aliquam erat volutpat. Morbi blandit tristique odio, non fringilla turpis scelerisque vel. Vivamus laoreet neque nisl. Ut ac placerat leo. Nulla justo mi, malesuada et ullamcorper in, facilisis viverra lorem. In rutrum, turpis et maximus aliquam, ante sapien feugiat ex, vel pharetra ex est non risus. Phasellus ac enim justo. "),
        (None, None, None, 2, "Test note 5", "2021-12-05", "Suspendisse potenti."),
        (None, None, None, None, "Test note 6", "2021-12-06", "Quisque commodo bibendum mi, vel lobortis nisi tincidunt ac. Sed ultricies ac ipsum mattis blandit."),
        (None, None, 4, 5, "Test note 7", "2021-12-07", "Proin et ullamcorper lorem. Fusce facilisis lectus sed ex faucibus elementum. Morbi justo lacus, ultricies quis efficitur ac, varius a elit. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam ac tortor tincidunt odio auctor porttitor."),
        (None, None, None, None, "Test note 8", "2021-12-08", " Morbi a ligula id lorem egestas posuere quis a neque. Nullam dui dolor, ornare in est eu, dignissim fermentum turpis. Aenean a ligula lectus. Proin sit amet mi sed lorem molestie eleifend vitae vel erat. Phasellus leo dui, sollicitudin nec ex quis, porta sollicitudin arcu. Proin in justo interdum, vestibulum lacus non, interdum nunc. Donec dapibus porta magna elementum posuere. Nam erat massa, imperdiet at dui at, lacinia blandit erat. Nam vestibulum enim sed erat luctus hendrerit.\nMaecenas metus arcu, aliquet at rhoncus eu, commodo at tortor. Pellentesque in lacus eget neque consequat vulputate. Vivamus euismod tincidunt nisl eu elementum. Sed faucibus placerat nulla vel egestas. Curabitur sit amet mi metus. Aenean vitae metus felis. Nullam tellus dolor, eleifend et sollicitudin in, fermentum eu augue. Fusce faucibus id ante vel malesuada. Donec pharetra eleifend justo, viverra interdum tortor scelerisque eget. Cras vel velit tempus, volutpat ipsum id, tristique velit. Vivamus ut turpis nec enim ullamcorper scelerisque. Sed vitae leo non ex euismod faucibus eget vitae lectus. ")
    ]
    insert_many_table_data(conn, "note", list_of_data_to_insert)
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

def get_first_company_id_given_name(conn, company_name):
    cursor = conn.execute("""SELECT company_id
                             FROM company
                             WHERE company_name == (?)
                          """, [company_name])
    return cursor.fetchone()[0]

def get_one_row_from_table(conn, table, row_id):
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
        db_data_names = """note_id, note_title, note_date_added, note_details"""
        table_data_names = db_data_names.split(", ")
        cursor = conn.execute("""SELECT (?)
                                 FROM note
                                 WHERE note_id == (?)
                              """, db_data_names, row_id)

    if table == "person":
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

    # Extract data from query cursor
    data = {}
    list_of_column_names = [x[0] for x in cursor.description]
    for i, cursor_row in enumerate(cursor):
        data[list_of_column_names[i]] = cursor_row[i]

    return data


def get_one_row_from_table_by_name(conn, table, item_name):
    cursor = None
    if table == "job":
        cursor = conn.execute("""SELECT *
                                 FROM job
                                 WHERE job_title == (?)
                              """, [item_name])

    if table == "company":
        cursor = conn.execute("""SELECT *
                                 FROM company
                                 WHERE company_name == (?)
                              """, [item_name])

    if table == "note":
        cursor = conn.execute("""SELECT *
                                 FROM note
                                 WHERE note_title == (?)
                              """, [item_name])

    if table == "person":
        cursor = conn.execute("""SELECT *
                                 FROM person
                                 WHERE person_name == (?)
                              """, [item_name])

    if table == "todo":
        cursor = conn.execute("""SELECT *
                                 FROM todo
                                 WHERE todo_title == (?)
                              """, [item_name])

    # Extract data from query cursor
    data = {}
    if cursor:
        list_of_column_names = [x[0] for x in cursor.description]
        tuple_of_data = ()

        for cursor_row in cursor:
            tuple_of_data = cursor_row

        for i, item in enumerate(list_of_column_names):
            data[item] = tuple_of_data[i]
    else:
        data["SQL Result"] = "None"
    return data


def get_all_names_from_table(conn, table):
    """Returns all values from the name/title column of all items in a table"""
    name_column = ""
    cursor = None

    if table == "job":
        name_column = "job_title"

    if table == "company":
        name_column = "company_name"

    if table == "note":
        name_column = "note_title"

    if table == "person":
        name_column = "person_name"

    if table == "todo":
        name_column = "todo_title"

    cursor = conn.execute(f"SELECT {name_column} FROM {table}")

    # Extract data from query cursor
    list_output = []
    for cursor_row in cursor:
        list_output.append(cursor_row[0])

    return list_output

def get_related_notes(conn, related_table, related_identifier):
    name_column = ""
    cursor = None

    if related_table == "job":
        note_join_column = "note_job"
        id_column = "job_id"
        name_column = "job_title"

    if related_table == "company":
        note_join_column = "note_company"
        id_column = "company_id"
        name_column = "company_name"

    if related_table == "person":
        note_join_column = "note_person"
        id_column = "person_id"
        name_column = "person_name"


    cursor = conn.execute(f"SELECT * FROM note "
                          f"INNER JOIN {related_table} ON {related_table}.{id_column} == note.{note_join_column} "
                          f"WHERE {name_column} == (?)", [related_identifier])

    # Extract data from query cursor
    list_of_notes = []
    list_output = []
    list_of_column_names = [x[0] for x in cursor.description]
    for cursor_row in cursor:
        data = {}
        for i, item in enumerate(list_of_column_names):
            data[item] = cursor_row[i]
        list_output.append(cursor_row)
        list_of_notes.append(data)

    return list_of_notes

def get_related_people(conn, related_table, related_identifier):
    name_column = ""
    cursor = None

    if related_table == "company":
        note_join_column = "person_company"
        id_column = "company_id"
        name_column = "company_name"

    cursor = conn.execute(f"SELECT * FROM person "
                          f"INNER JOIN {related_table} ON {related_table}.{id_column} == person.{note_join_column} "
                          f"WHERE {name_column} == (?)", [related_identifier])

    # Extract data from query cursor
    list_of_notes = []
    list_output = []
    list_of_column_names = [x[0] for x in cursor.description]
    for cursor_row in cursor:
        data = {}
        for i, item in enumerate(list_of_column_names):
            data[item] = cursor_row[i]
        list_output.append(cursor_row)
        list_of_notes.append(data)

    return list_of_notes

def get_related_jobs(conn, related_table, related_identifier):
    name_column = ""
    cursor = None

    company_id = get_first_company_id_given_name(conn, related_identifier)

    if related_table == "company":
        join_column = "job_company"
        id_column = "company_id"

    cursor = conn.execute(f"SELECT * FROM job "
                          f"INNER JOIN {related_table} ON {related_table}.{id_column} = job.{join_column} "
                          f"WHERE {id_column} = (?)", [company_id])

    # Extract data from query cursor
    list_of_jobs = []
    list_output = []
    list_of_column_names = [x[0] for x in cursor.description]
    for cursor_row in cursor:
        data = {}
        for i, item in enumerate(list_of_column_names):
            data[item] = cursor_row[i]
        list_output.append(cursor_row)
        list_of_jobs.append(data)

    return list_of_jobs


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
    return conn

def open_db():
    """Opens DB, initializing if needed, and inserts test data"""
    if not path.exists(DB_PATH):
        mkdir(DB_PATH)

    need_to_create_db = not path.exists(DB_FILEPATH)

    conn = sqlite3.connect(DB_FILEPATH)
    conn.execute("PRAGMA foreign_keys = ON")

    if need_to_create_db:
        create_new_db(conn)
    return conn

def initialize_db(conn):
    # Until I add data input, always initialize with test data

    conn = insert_test_data_via_objects(conn)
    return conn

def close_db(conn):
    conn.close()
    return True
