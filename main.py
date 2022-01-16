# main.py


"""
This program is an attempt to make a TUI for a few processes I find myself doing frequently
while looking for a job. The general layout is expected to be as follows:

One of the simpler screens will look something like this:
 ┌──────────────────┐
 │┌────────────────┐│
 │├────────────────┤│
 ││ ┌─┐ ┌─────────┐││
 ││ │ │ │         │││
 ││ └─┘ └─────────┘││
 │└────────────────┘│
 └──────────────────┘


Outer/Top-most layer:
 ┌──────────────────┐
 │                  │
 │  main_pile       │
 │                  │
 │                  │
 │                  │
 │                  │
 └──────────────────┘

Inside main_pile is:
 ┌────────────────┐
 │ tab_menu       │
 ├────────────────┤
 │                │
 │ body_container │
 │                │
 │                │
 └────────────────┘

Next steps will involve adding more containers into body_container
Inside body_container will be some kind of subdivision
 ┌───────────┐  ┌─────────────────────────────┐
 │  body_    │  │  body_main_window           │
 │  side_    │  │                             │
 │  bar      │  │                             │
 │           │  │                             │
 │           │  │                             │
 │           │  │                             │
 │           │  │                             │
 │           │  │                             │
 └───────────┘  └─────────────────────────────┘
"""


import urwid
import string
import database

"""
TODO

- Create button handler that is called when todo side bar item is clicked
- In todo main body, add retreival of data from database when todo sidebar button pressed
- In todo layout, add "new todo" to side bar
- In todo main body, add "complete todo" as a button at the top


"""

class App():
    def __init__(self):
        # Establish database connection
        self.conn = database.open_db()
        # database.initialize_db(self.conn)

        # Build primary two subdivisions: tab_menu and body_container
        tab_menu = self.build_tab_menu(['Todos', 'Jobs', 'Companies', 'People'])
        self.tab_name_table_name_map = {
            'Todos': "todo",
            'Jobs': "job",
            'Companies': "company",
            'People': "person",
        }
        # body_container = urwid.Filler(urwid.Text("default", 'left', 'clip'), "top")
        self.body_container = urwid.Columns(self.get_body_container_columns())

        # Arrange primary items into a Pile
        # main_pile = urwid.Pile([('pack', tab_menu), body_container])
        self.main_pile = urwid.Pile([('pack', tab_menu), self.body_container])

        self.view = self.main_pile
        self.item_selected_for_popup = None
        self.mainloop = urwid.MainLoop(self.view,
                                  palette=[('reversed', 'standout', ''),
                                           ('bold', 'bold', '')],
                                  unhandled_input=self.q_for_exit)

        self.mainloop.run()


    def close_pop_up_window(self, button):
        """Closes the pop up window"""
        self.mainloop.widget = self.main_pile
        self.body_container[1].focus_position = self.item_selected_for_popup
        # raise ValueError(f"{self.item_selected_for_popup}")

    def commit_pop_up_changes(self, button, list_of_name_data_id_table):
        """Updates the data in the field"""
        # raise ValueError(f"{list_of_name_data_id_table=}")
        database.update_value_by_id_fieldname(self.conn,
                                              list_of_name_data_id_table[3],
                                              list_of_name_data_id_table[2],
                                              list_of_name_data_id_table[0],
                                              list_of_name_data_id_table[1].edit_text,
                                              )
        self.modify_side_body(button, list_of_name_data_id_table[3])
        self.modify_main_body(button, list_of_name_data_id_table[3], identifier=list_of_name_data_id_table[2])
        self.close_pop_up_window(button)

    def make_pop_up_window(self, button, list_of_things):
        """Returns a simple box window, to be rendered on top of the layout"""
        field_name, edit_field, id, table = list_of_things[0], list_of_things[1], list_of_things[2], list_of_things[3]
        self.item_selected_for_popup = self.body_container[1].focus_position

        body = [urwid.Text("item " + id + ": " + field_name)]
        body.append(urwid.Divider())
        edited_text = urwid.Edit(caption='', edit_text=edit_field, multiline=True)
        body.append(edited_text)
        body.append(urwid.Divider())

        save_button = urwid.Button('Save')
        urwid.connect_signal(save_button, 'click', self.commit_pop_up_changes, [field_name, edited_text, id, table])

        cancel_button = urwid.Button('Cancel')
        urwid.connect_signal(cancel_button, 'click', self.close_pop_up_window)

        buttons = urwid.Columns([urwid.AttrMap(save_button, None, focus_map='reversed'),
                                urwid.AttrMap(cancel_button, None, focus_map='reversed')])
        body.append(buttons)

        popup = urwid.LineBox(urwid.ListBox(urwid.SimpleFocusListWalker(body)))

        self.mainloop.widget = urwid.Overlay(popup, self.main_pile, "center", ("relative", 50), "middle", ("relative", 50))


    def build_tab_menu(self, choices):
        """Defines and builds tab_menu using provided choices
        Probably doesn't need to be this convoluted.
        """
        cells = []
        for item in choices:
            button = urwid.Button(item)
            urwid.connect_signal(button, 'click', self.on_tab_click, item)
            cells.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.GridFlow(cells, 20, 2, 1, "left")

    def build_job_status_button_gridflow(self):
        """Defines and builds tab_menu using provided choices
        Probably doesn't need to be this convoluted.
        """
        choices = ["Interested", "Applied", "Interviewing", 'Accepted', "Interviewed", "Rejected"]
        cells = []
        for item in choices:
            button = urwid.Button(item)
            # urwid.connect_signal(button, 'click', self.on_tab_click, item)
            cells.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.GridFlow(cells, 16, 1, 0, "left")

    def build_related_jobs_for_company_walkable(self, company_identifier):
        """Builds a table of job_title, date_added, and job_status for a given selected company"""
        # Retrieve job data
        data = database.get_related_jobs(self.conn, 'company', company_identifier)

        rows = [urwid.Columns([(10, urwid.Text(('bold', "Job ID"))),
                               (14, urwid.Text(('bold', "Status"))),
                               urwid.Text(('bold', "Job Title")),
                               ('pack', urwid.Text(('bold', "Date Added"))),
                               ], dividechars=3, min_width=10)]

        for item in data:
            if item:
                button = urwid.Button(str(item["job_id"]))
                urwid.connect_signal(button, 'click', self.on_related_company_job_click, item["job_id"])

                one_row = urwid.Columns([(10, button),
                                         (14, urwid.Text(item["job_status"])),
                                         urwid.Text(item["job_title"]),
                                         ('pack', urwid.Text(item["job_date_added"])),
                                        ], dividechars=3, min_width=10)
                rows.append(urwid.AttrMap(one_row, None, focus_map='reversed'))

        return urwid.ListBox(urwid.SimpleFocusListWalker(rows))

    def build_related_people_for_company_walkable(self, company_identifier):
        """Builds a table of job_title, date_added, and job_status for a given selected company"""
        # Retrieve job data
        data = database.get_related_people(self.conn, 'company', company_identifier)

        rows = [urwid.Columns([(10, urwid.Text(('bold', "Person ID"))),
                               (18, urwid.Text(('bold', "Phone"))),
                               ('weight', 1, urwid.Text(('bold', "Name"))),
                               ('weight', 1, urwid.Text(('bold', "Email")))
                               ], dividechars=3, min_width=10)]

        for item in data:
            if item:
                button = urwid.Button(str(item["person_id"]))
                urwid.connect_signal(button, 'click', self.on_related_company_person_click, item["person_id"])

                one_row = urwid.Columns([(10, button),
                                         (18, urwid.Text(item["person_phone"])),
                                         ('weight', 1, urwid.Text(item["person_name"])),
                                         ('weight', 1, urwid.Text(item["person_email"]))
                                        ], dividechars=3, min_width=10)
                rows.append(urwid.AttrMap(one_row, None, focus_map='reversed'))

        return urwid.ListBox(urwid.SimpleFocusListWalker(rows))


    def build_list_of_jobs_for_sidebar(self):
        """Defines and builds sidebar used on Jobs view with list of jobs
        CLicking on one should show that job's information.

        job_list: a list of dicts of jobs with all of their data
        """
        job_data = database.get_all_rows_from_table(self.conn, "job")
        rows = [urwid.Columns([(10, urwid.Text(('bold', "Job ID"))), urwid.Text(('bold', "Job Title"))], dividechars=1)]

        for item in job_data:
            if item:
                button = urwid.Button(str(item["job_id"]))
                urwid.connect_signal(button, 'click', self.on_job_item_click, item["job_id"])
                one_row = urwid.Columns([(10, button), urwid.Text(item["job_title"]),
                                          ], dividechars=1)

                rows.append(urwid.AttrMap(one_row, None, focus_map='reversed'))

        return urwid.ListBox(urwid.SimpleFocusListWalker(rows))

    def build_list_of_companies_for_sidebar(self):
        """Defines and builds sidebar used on Companies view with list of jobs
        CLicking on one should show that company's information.
        """

        company_data = database.get_all_rows_from_table(self.conn, "company")
        rows = [urwid.Columns([(10, urwid.Text(('bold', "Company ID"))), urwid.Text(('bold', "Company Name"))], dividechars=1)]

        for item in company_data:
            if item:
                button = urwid.Button(str(item["company_id"]))
                urwid.connect_signal(button, 'click', self.on_company_item_click, item["company_id"])
                one_row = urwid.Columns([(10, button), urwid.Text(item["company_name"]),
                                          ], dividechars=1)

                rows.append(urwid.AttrMap(one_row, None, focus_map='reversed'))

        return urwid.ListBox(urwid.SimpleFocusListWalker(rows))

    def build_list_of_people_for_sidebar(self):
        """Defines and builds sidebar used on Companies view with list of jobs
        CLicking on one should show that company's information.
        """
        person_data = database.get_all_rows_from_table(self.conn, "person")
        rows = [
            urwid.Columns([(10, urwid.Text(('bold', "Person ID"))), urwid.Text(('bold', "Person Name"))], dividechars=1)]

        for item in person_data:
            if item:
                button = urwid.Button(str(item["person_id"]))
                urwid.connect_signal(button, 'click', self.on_person_item_click, item["person_id"])
                one_row = urwid.Columns([(10, button), urwid.Text(item["person_name"]),
                                         ], dividechars=1)

                rows.append(urwid.AttrMap(one_row, None, focus_map='reversed'))

        return urwid.ListBox(urwid.SimpleFocusListWalker(rows))


    def build_list_of_todos_for_sidebar(self):
        """Defines and builds sidebar used on Todos view with list of todos
        Clicking on one should show that company's information.
        """
        todo_data = database.get_all_rows_from_table(self.conn, "todo")
        rows = [
            urwid.Columns([(10, urwid.Text(('bold', "Todo ID"))), urwid.Text(('bold', "Todo Title"))], dividechars=1)]

        for item in todo_data:
            if item:
                button = urwid.Button(str(item["todo_id"]))
                urwid.connect_signal(button, 'click', self.on_todo_item_click, item["todo_id"])
                one_row = urwid.Columns([(10, button), urwid.Text(item["todo_title"]),
                                         ], dividechars=1)

                rows.append(urwid.AttrMap(one_row, None, focus_map='reversed'))

        return urwid.ListBox(urwid.SimpleFocusListWalker(rows))

    def build_related_note_linebox(self, table, identifier):
        # Turn list of note data into walkable list of strings
        list_of_notes_data_dicts = database.get_related_notes_by_id(self.conn, table, identifier)
        # raise ValueError(f"{list_of_notes_data_dicts=}")
        editables = ['note_company', 'note_person', 'note_job', 'note_title', 'note_details']
        rows = []
        for note in list_of_notes_data_dicts:
            for item in note:
                if str(item) in editables:
                    button = urwid.Button(str(note[item]))
                    item_name = str(item)
                    item_value = str(note[item])
                    item_id = str(note["note_id"])
                    urwid.connect_signal(button, 'click', self.make_pop_up_window, [item_name, item_value, item_id, 'note'])
                    one_row = urwid.Columns([('pack', urwid.Text(str(item) + ": ")), button], dividechars=1)
                else:
                    one_row = urwid.Text(str(item) + ": " + str(note[item]))

                rows.append(urwid.AttrMap(one_row, None, focus_map='reversed'))
            rows.append(urwid.Divider("-"))

        related_note_linebox = urwid.LineBox(urwid.ListBox(urwid.SimpleFocusListWalker(rows)),
                                         title="Notes", title_align="left")

        return related_note_linebox



    def build_todo_main_body(self, table, identifier=None):
        """Defines and builds main_body used on Todos view based on selected sidebar item Identifier

        todo_id, todo_title, todo_date_modified, todo_description
        """
        editables = ["todo_title", "todo_details"]
        # This addition makes all items that show up editable by clicking them as buttons
        data = database.get_one_row_from_table_by_id(self.conn, table, identifier)
        rows = []
        for item in data:
            if str(item) in editables:
                button = urwid.Button(str(data[item]))
                item_name = str(item)
                item_value = str(data[item])
                item_id = str(data["todo_id"])
                urwid.connect_signal(button, 'click', self.make_pop_up_window, [item_name, item_value, item_id, table])
                one_row = urwid.Columns([('pack', urwid.Text(str(item) + ": ")), button], dividechars=1)
            else:
                one_row = urwid.Text(str(item) + ": " + str(data[item]))
            rows.append(urwid.AttrMap(one_row, None, focus_map='reversed'))

        return urwid.ListBox(urwid.SimpleFocusListWalker(rows))

    def build_company_main_body(self, table, identifier=None):
        # Top Box - Open Jobs
        main_body_top = urwid.LineBox(self.build_related_jobs_for_company_walkable(identifier),
                                      title="Open Jobs", title_align="left")

        main_body_mid = urwid.LineBox(self.build_related_people_for_company_walkable(identifier),
                                       title="People", title_align="left")

        main_body_bottom = self.build_related_note_linebox(table, identifier)

        list_of_main_body_widgets = [main_body_top, main_body_mid, main_body_bottom]

        return list_of_main_body_widgets

    def build_person_main_body(self, table, identifier):
        # Top Box - Person Details
        editables = ["person_company", "person_name", "person_email", "person_phone"]
        data = database.get_one_row_from_table_by_id(self.conn, table, identifier)
        rows = []
        for item in data:
            if str(item) in editables:
                button = urwid.Button(str(data[item]))
                item_name = str(item)
                item_value = str(data[item])
                item_id = str(data["person_id"])
                urwid.connect_signal(button, 'click', self.make_pop_up_window, [item_name, item_value, item_id, table])
                one_row = urwid.Columns([('pack', urwid.Text(str(item) + ": ")), button], dividechars=1)
            else:
                one_row = urwid.Text(str(item) + ": " + str(data[item]))
            rows.append(urwid.AttrMap(one_row, None, focus_map='reversed'))

        main_body_top = urwid.LineBox(urwid.ListBox(urwid.SimpleFocusListWalker(rows)), title="Details", title_align="left")

        main_body_bottom = self.build_related_note_linebox("person", identifier)
        list_of_main_body_widgets = [main_body_top, main_body_bottom]

        return list_of_main_body_widgets

    def build_job_main_body(self, table, identifier=None):
        """Defines and builds main_body used on Jobs view based on selected sidebar item Identifier
        Main body has three parts:
        top: Job Status as buttons
        middle: Posting Details
        bottom: Notes related to job
        job_id, job_title, job_date_added, job_date_posted, job_description, job_status
        """
        data = database.get_one_row_from_table_by_id(self.conn, table, identifier)

        text_items = []
        for item in data:
            text_items.append(str(item) + ": " + str(data[item]))

        # Top Box - Job Status
        status_content = urwid.Pile([urwid.Text(f"Status: {data['job_status']}"), self.build_job_status_button_gridflow()])
        main_body_top = urwid.LineBox(urwid.Filler(status_content, "top"),
                                      title="Status", title_align="left")

        # Mid Box - Details about the posting
        editables = ["job_company", "job_date_added", "job_title", "job_date_posted", "job_description", "job_status"]
        # This addition makes all items that show up editable by clicking them as buttons
        data = database.get_one_row_from_table_by_id(self.conn, table, identifier)
        rows = []
        for item in data:
            if str(item) == "job_status":
                continue
            if str(item) in editables:
                button = urwid.Button(str(data[item]))
                item_name = str(item)
                item_value = str(data[item])
                item_id = str(data["job_id"])
                urwid.connect_signal(button, 'click', self.make_pop_up_window, [item_name, item_value, item_id, table])
                one_row = urwid.Columns([('pack', urwid.Text(str(item) + ": ")), button], dividechars=1)
            else:
                one_row = urwid.Text(str(item) + ": " + str(data[item]))
            rows.append(urwid.AttrMap(one_row, None, focus_map='reversed'))

        main_body_mid = urwid.LineBox(urwid.ListBox(urwid.SimpleFocusListWalker(rows)),
                      title="Posting Details", title_align="left")

        # Bottom Box - Notes about the posting
        main_body_bottom = self.build_related_note_linebox(table, identifier)

        return [main_body_top, ("weight", 3, main_body_mid), ("weight", 3, main_body_bottom)]

    def build_body_main_window(self):
        """Builds the main window of the body depending on which tab is currently active
        The calling method is a Filler, and this will return different Text objects to it
        :return: Lineboxed urwid object
        """
        main_window_text = urwid.Text(f"Choose a tab to get started", 'center', 'clip')
        return urwid.LineBox(urwid.Filler(main_window_text, "top"))

    # Main screen on first load
    def get_body_container_columns(self, choice="todo"):
        column_1 = urwid.LineBox(urwid.Filler(urwid.Text("", 'center', 'clip'), "middle"))
        column_2 = self.build_body_main_window()
        return [("weight", 1, column_1), ("weight", 3, column_2)]

    def build_body_container(self, choice="todo"):
        """Builds the body container"""
        return urwid.Columns(self.get_body_container_columns())


    def modify_main_body(self, button, choice, identifier = None):
        if choice == "todo":
            if not identifier:
                main_body = urwid.LineBox(urwid.Filler(urwid.Text("Todo items", 'center', 'clip'), "top"),
                                          title="Todos", title_align="left")
            else:
                main_body = urwid.LineBox(self.build_todo_main_body(choice, identifier),
                                          title="Todos", title_align="left")

            self.body_container.contents[1] = (main_body, ("weight", 3, False))

        elif choice == "company":
            list_of_main_body_widgets = None

            # Layout for if no company is selected
            if not identifier:
                # Top Box - Open Jobs
                # Show a grid of Job title, Date added, and Status
                main_body_top = urwid.LineBox(urwid.Filler(urwid.Text(""), "top"),
                                              title="Status", title_align="left")

                # Mid Box - Related Notes
                main_body_mid = urwid.LineBox(urwid.Filler(urwid.Edit(), "top"),
                                              title="People", title_align="left")

                # Bottom Box - Related People
                main_body_bottom = urwid.LineBox(urwid.Filler(urwid.Edit(), "top"),
                                                 title="Notes", title_align="left")

                list_of_main_body_widgets = [main_body_top, main_body_mid, main_body_bottom]


            # Modify existing layout when a job is selected
            if identifier:
                list_of_main_body_widgets = self.build_company_main_body(choice, identifier)

            main_body = urwid.Pile(list_of_main_body_widgets)

            self.body_container.contents[1] = (main_body, ("weight", 3, False))

        elif choice == "job":

            list_of_main_body_widgets = None
            # Layout for if no job is selected
            if not identifier:
                # Top Box - Job Status
                main_body_top = urwid.LineBox(urwid.Filler(self.build_job_status_button_gridflow(), "top"),
                                              title="Status", title_align="left")

                # Mid Box - Details about the posting
                main_body_mid = urwid.LineBox(urwid.Filler(urwid.Edit(), "top"),
                                              title="Posting Details", title_align="left")

                # Bottom Box - Notes about the posting
                main_body_bottom = urwid.LineBox(urwid.Filler(urwid.Edit(), "top"),
                                                 title="Notes", title_align="left")

                list_of_main_body_widgets = [main_body_top, ("weight", 3, main_body_mid), ("weight", 3, main_body_bottom)]

            # Modify existing layout when a job is selected
            if identifier:
                list_of_main_body_widgets = self.build_job_main_body(choice, identifier)

            main_body = urwid.Pile(list_of_main_body_widgets)

            self.body_container.contents[1] = (main_body, ("weight", 3, False))

        elif choice == "person":
            list_of_main_body_widgets = None

            # Layout for if no company is selected
            if not identifier:
                # Main body top - Details about the person (probably contact info)
                main_body_top = urwid.LineBox(urwid.Filler(urwid.Edit(), "top"),
                                              title="Details", title_align="left")

                # Main body bottom - Notes connected to this person (list sorted by dates)
                main_body_bottom = urwid.LineBox(urwid.Filler(urwid.Edit(), "top"),
                                                 title="Notes", title_align="left")
                main_body = urwid.Pile([main_body_top, main_body_bottom])

                list_of_widgets_to_return = [main_body_top, main_body_bottom]

            # Modify existing layout when a job is selected
            if identifier:
                list_of_main_body_widgets = self.build_person_main_body(choice, identifier)

            main_body = urwid.Pile(list_of_main_body_widgets)

            self.body_container.contents[1] = (main_body, ("weight", 3, False))

    def modify_side_body(self, button, table_name):
        """Reruns side-bar code to update list"""
        side_body_item_list = None
        if table_name == "todo":
            side_body_item_list = self.build_list_of_todos_for_sidebar()

        elif table_name == "company":
            side_body_item_list = self.build_list_of_companies_for_sidebar()

        elif table_name == "job":
            side_body_item_list = self.build_list_of_jobs_for_sidebar()

        elif table_name == "person":
            side_body_item_list = self.build_list_of_people_for_sidebar()

        # Assings rebuilt item list to the correct part of the body
        # body_container[0] is the main window
        # body_container[0][0] is the LineBox of the side bar
        # body_container[0][0].contents[0] in the new botton in side bar
        # body_container[0][0][1] is the divider in the side bar
        # raise ValueError(f"{side_body_item_list=}\n{self.body_container.contents[0][0].original_widget.contents[2]}")
        self.body_container.contents[0][0].original_widget.contents[2] = (side_body_item_list, ("weight", 1))

    def default_body_builder(self, button, choice):
        """Function for directly changing the text in body_container"""

        if choice == "todo":
            # Default view
            # side_bar = urwid.LineBox(urwid.Filler(urwid.Text("todo items", 'center', 'clip'), "top"))
            # side_bar = urwid.LineBox(self.build_list_of_todos_for_sidebar(self.todos()))

            # main_body = self.build_body_main_window()
            # list_of_widgets_to_return = [(side_bar, ("weight", 1, False)), (main_body, ("weight", 3, False))]

          # Side Bar - Selectable list of companies
            # Note, buttons need connecting
            new_button = urwid.Button("New Todo")
            # on_create_new_item_click [requires table_name, related_company_id=None, related_person_id=None, related_job_id=None]
            urwid.connect_signal(new_button, 'click', self.on_create_new_item_click, ["todo"])
            new_button = urwid.AttrMap(new_button, None, focus_map='reversed')
            linebox_of_todos = self.build_list_of_todos_for_sidebar()
            side_bar = urwid.LineBox(urwid.Pile([("pack",new_button), ('pack', urwid.Divider(" ")), linebox_of_todos]))

            # Main body - Displays selected Todos
            main_body = urwid.LineBox(urwid.Filler(urwid.Text("Todo items", 'center', 'clip'), "top"),
                                              title="Todos", title_align="left")

            list_of_widgets_to_return = [(side_bar, ("weight", 1, False)), (main_body, ("weight", 3, False))]

        elif choice == "company":
            # Side Bar - Selectable list of companies
            # Note, buttons need connecting
            new_button = urwid.Button("New Company")
            # on_create_new_item_click [requires table_name, related_company_id=None, related_person_id=None, related_job_id=None]
            urwid.connect_signal(new_button, 'click', self.on_create_new_item_click, ["company"])
            new_button = urwid.AttrMap(new_button, None, focus_map='reversed')
            linebox_of_companies = self.build_list_of_companies_for_sidebar()
            side_bar = urwid.LineBox(urwid.Pile([("pack",new_button), ('pack', urwid.Divider(" ")), linebox_of_companies]))

            # side_bar = urwid.LineBox(self.build_list_of_companies_for_sidebar())

            # Main body top - Open Jobs at selected company
            main_body_top = urwid.LineBox(urwid.Filler(urwid.Text("Open Jobs", 'center', 'clip'), "top"),
                                          title="Open Jobs", title_align="left")

            # Main body middle - People known at selected company
            main_body_mid = urwid.LineBox(urwid.Filler(urwid.Text("People", 'center', 'clip'), "top"),
                                          title="People", title_align="left")

            # Main body bottom - Notes about selected company
            main_body_bottom = urwid.LineBox(urwid.Filler(urwid.Edit(), "top"),
                                          title="Notes", title_align="left")

            main_body = urwid.Pile([main_body_top, main_body_mid, main_body_bottom])

            list_of_widgets_to_return = [(side_bar, ("weight", 1, False)), (main_body, ("weight", 3, False))]

        elif choice == "person":
            # Side Bar - Selectable list of companies
            # Note, buttons need connecting
            side_bar = urwid.LineBox(self.build_list_of_people_for_sidebar())

            # Main body top - Details about the person (probably contact info)
            main_body_top = urwid.LineBox(urwid.Filler(urwid.Edit(), "top"),
                                          title="Details", title_align="left")

            # Main body bottom - Notes connected to this person (list sorted by dates)
            main_body_bottom = urwid.LineBox(urwid.Filler(urwid.Edit(), "top"),
                                          title="Notes", title_align="left")
            main_body = urwid.Pile([main_body_top, main_body_bottom])

            list_of_widgets_to_return = [(side_bar, ("weight", 1, False)), (main_body, ("weight", 3, False))]

        elif choice == "job":
            # Side Bar - Selectable list of jobs
            # Note, buttons need connecting
            side_bar = urwid.LineBox(self.build_list_of_jobs_for_sidebar())
            # raise ValueError(f"{side_bar=}")
            # Top Box - Job Status
            main_body_top = urwid.LineBox(urwid.Filler(self.build_job_status_button_gridflow(), "top"),
                                          title="Status", title_align="left")

            # Mid Box - Details about the posting
            main_body_mid = urwid.LineBox(urwid.Filler(urwid.Edit(), "top"),
                                          title="Posting Details", title_align="left")

            # Bottom Box - Notes about the posting
            main_body_bottom = urwid.LineBox(urwid.Filler(urwid.Edit(), "top"),
                                             title="Notes", title_align="left")

            main_body = urwid.Pile([main_body_top, ("weight", 3, main_body_mid), ("weight", 3, main_body_bottom)])

            list_of_widgets_to_return = [(side_bar, ("weight", 1, False)), (main_body, ("weight", 3, False))]

        else:
            list_of_widgets_to_return = [("pack", urwid.Text("There must have been a mistake.", 'left', 'clip'))]

        self.body_container.contents = urwid.MonitoredFocusList(list_of_widgets_to_return)

    def on_tab_click(self, button, choice):
        """Callback function for changing main_body
        :param button: not sure what this is for, but some first variable is expected
        :param choice: user variable used for switch
        :return: None. For now, this just calls the body_picker function which directly changes
        """
        self.default_body_builder(button, self.tab_name_table_name_map[choice])

    def on_todo_item_click(self, button, identifier):
        """Callback function for changing main_body
        :param button: not sure what this is for, but some first variable is expected
        :param choice: user variable used for switch
        :return: None. For now, this just calls the body_picker function which directly changes
        """
        self.modify_main_body(button, "todo", identifier)

    def on_job_item_click(self, button, identifier):
        """Callback function for changing main_body
        :param button: not sure what this is for, but some first variable is expected
        :param choice: user variable used for switch
        :return: None. For now, this just calls the body_picker function which directly changes
        """
        self.modify_main_body(button, "job", identifier)

    def on_company_item_click(self, button, identifier):
        """Callback function for changing main_body
        :param button: not sure what this is for, but some first variable is expected
        :param choice: user variable used for switch
        :return: None. For now, this just calls the body_picker function which directly changes
        """
        self.modify_main_body(button, "company", identifier)

    def on_person_item_click(self, button, identifier):
        """Callback function for changing main_body
        :param button: not sure what this is for, but some first variable is expected
        :param choice: user variable used for switch
        :return: None. For now, this just calls the body_picker function which directly changes
        """
        self.modify_main_body(button, "person", identifier)

    def on_related_company_job_click(self, button, identifier):
        """Callback function for when clicking on a job on the companies tab

        When looking at a company and clicking on a job, view should change to that
        job so data entry can happen. identifier will be the job ID

        :param button: not sure what this is for, but some first variable is expected
        :param choice: user variable used for switch
        :return: None. For now, this just calls the body_picker function which directly changes
        """
        # raise ValueError(f"the identifier passed was {identifier}")
        self.default_body_builder(button, "job")
        self.modify_main_body(button, "job", identifier)

    def on_related_company_person_click(self, button, identifier):
        """Callback function for when clicking on a person on the companies tab

        When looking at a company and clicking on a person, view should change to that
        person so data entry can happen. Identifier will be the person ID

        :param button: the button object that called this function
        :param choice: user variable used for switch
        :return: None. For now, this just calls the body_picker function which directly changes
        """
        # raise ValueError(f"the identifier passed was {identifier}")
        self.default_body_builder(button, "person")
        self.modify_main_body(button, "person", identifier)

    def on_create_new_item_click(self, button, table_name_and_related_ids):
        """ Creates a new item, refreshes the sidebar, and triggers a selection of that item
        :param button: button that was clicked to create the new item
        :param table_name_and_related_ids: [table_name, related_company_id, related_person_id, related_job_id]
        :return: None
        """

        identifier = database.insert_one_default_item(self.conn, table_name_and_related_ids[0], table_name_and_related_ids[1:])
        table_name = table_name_and_related_ids[0]

        #related_company_id=None, related_person_id=None, related_job_id=None
        if table_name == "todo":
            self.modify_side_body(button, table_name)
            self.on_todo_item_click(button, identifier)
        if table_name == "person":
            self.modify_side_body(button, table_name)
            self.on_person_item_click(button, identifier)
        if table_name == "company":
            self.modify_side_body(button, table_name)
            self.on_company_item_click(button, identifier)
        if table_name == "job":
            self.modify_side_body(button, table_name)
            self.on_job_item_click(button, identifier)


    def exit_program(self):
        raise urwid.ExitMainLoop()

    def q_for_exit(self, key):
        if key == "1":
            self.make_pop_up_window()
        if key == "2":
            self.close_pop_up_window()
        if key in ('q', 'Q'):
            self.exit_program()


if __name__ == "__main__":
    app = App()

