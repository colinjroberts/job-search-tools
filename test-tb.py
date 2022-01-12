import sqlite3
from os import path, mkdir
import pathlib
import database

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

    return


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
    db_data_names = """note_id, note_company, note_person, note_job, note_date_edited, note_details"""
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


def get_all_todo_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM todo")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print()

def get_all_company_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM company")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print()


def get_all_person_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM person")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print()


def get_all_person_data_with_company_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM person INNER JOIN company ON company.company_id = person.person_company")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print()


def get_all_job_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM job")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print()


def get_all_job_data_with_company_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM job INNER JOIN company ON company.company_id = job.job_company")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print()


def get_all_note_data_etc(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM note")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print()

    cur = conn.cursor()
    cur.execute("SELECT * FROM note INNER JOIN company ON company.company_id = note.note_company WHERE note.note_company > 0 ")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print()

    cur = conn.cursor()
    cur.execute("SELECT * FROM note  INNER JOIN job ON job.job_id = note.note_job WHERE note.note_job > 0")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print()

    cur = conn.cursor()
    cur.execute("SELECT * FROM note  INNER JOIN person ON person.person_id = note.note_person WHERE note.note_person > 0")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print()

def get_note_data_via_others(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM company INNER JOIN note ON company.company_id = note.note_company")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print()

    cur = conn.cursor()
    cur.execute("SELECT * FROM job INNER JOIN note ON job.job_id = note.note_job")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print()

    cur = conn.cursor()
    cur.execute("SELECT * FROM person INNER JOIN note ON person.person_id = note.note_person")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    print()


    data = {}
    # Extract data from query cursor
    list_of_column_names = [x[0] for x in cur.description]
    for i, item in enumerate(rows[0]):
        data[list_of_column_names[i]] = item

    print(data)


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

def open_db():
    if not path.exists(DB_PATH):
        mkdir(DB_PATH)
    if not path.exists(DB_FILEPATH):
        conn = sqlite3.connect(DB_FILEPATH)
        conn.execute("PRAGMA foreign_keys = ON")
        conn = create_new_db(conn)

    else:
        conn = sqlite3.connect(DB_FILEPATH)
        conn.execute("PRAGMA foreign_keys = ON")
        insert_test_data_via_objects(conn)
        get_all_todo_data(conn)
        get_all_company_data(conn)
        get_all_person_data(conn)
        get_all_person_data_with_company_data(conn)
        get_all_job_data(conn)
        get_all_job_data_with_company_data(conn)
        get_all_note_data_etc(conn)
        get_note_data_via_others(conn)

        get_all_names_from_table(conn, "person")
        get_all_names_from_table(conn, "todo")
        get_all_names_from_table(conn, "note")
        get_all_names_from_table(conn, "job")
        get_all_names_from_table(conn, "company")

    return conn


if __name__ == "__main__":
    conn = None
    try:
        conn = database.open_db()
        database.initialize_db(conn)

    finally:
        if conn:
            # data = database.get_all_names_from_table(conn, "todo")
            # print(data)
            data = database.get_one_row_from_table_by_id(conn, "todo", 1)
            print(data)
            update = database.update_value_by_id_fieldname(conn, "todo", 1, "todo_details", "Something")
            data = database.get_one_row_from_table_by_id(conn, "todo", 1)
            print(data)
            conn.close()
