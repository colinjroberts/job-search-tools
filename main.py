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
import csv
import database
import time

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
        database.initialize_db(self.conn)

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

        self.mainloop = urwid.MainLoop(self.main_pile,
                                  palette=[('reversed', 'standout', '')],
                                  unhandled_input=self.q_for_exit)

        self.mainloop.run()


    def companies(self):
        return database.get_all_names_from_table(self.conn, "company")

    def people(self):
        return database.get_all_names_from_table(self.conn, "person")

    def jobs(self):
        return database.get_all_names_from_table(self.conn, "job")

    def todo(self):
        return database.get_all_names_from_table(self.conn, "todo")



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
        return urwid.GridFlow(cells, 17, 2, 1, "left")


    def build_list_of_jobs_for_sidebar(self, job_list):
        """Defines and builds sidebar used on Jobs view with list of jobs
        CLicking on one should show that job's information.
        """
        cells = []
        for item in job_list:
            button = urwid.Button(item)
            urwid.connect_signal(button, 'click', self.on_job_item_click, item)
            cells.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(cells))


    def build_list_of_companies_for_sidebar(self, company_list):
        """Defines and builds sidebar used on Companies view with list of jobs
        CLicking on one should show that company's information.
        """
        cells = []
        for item in company_list:
            button = urwid.Button(item)
            # urwid.connect_signal(button, 'click', on_tab_click, item)
            cells.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(cells))

    def build_list_of_people_for_sidebar(self, person_list):
        """Defines and builds sidebar used on Companies view with list of jobs
        CLicking on one should show that company's information.
        """
        cells = []
        for item in person_list:
            button = urwid.Button(item)
            # urwid.connect_signal(button, 'click', on_tab_click, item)
            cells.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(cells))

    def build_list_of_todos_for_sidebar(self, job_list):
        """Defines and builds sidebar used on Todos view with list of todos
        Clicking on one should show that company's information.
        """
        cells = []
        for item in job_list:
            button = urwid.Button(item)
            urwid.connect_signal(button, 'click', self.on_todo_item_click, item)
            cells.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(cells))

    def build_todo_main_body(self, table, identifier=None):
        """Defines and builds main_body used on Todos view based on selected sidebar item Identifier

        todo_id, todo_title, todo_date_modified, todo_description
        """
        data = database.get_one_row_from_table_by_name(self.conn, table, identifier)

        text_items = []
        for item in data:
            text_items.append(str(item) + ": " + str(data[item]))

        return urwid.Text("\n".join(text_items))

    def build_job_main_body(self, table, identifier=None):
        """Defines and builds main_body used on Jobs view based on selected sidebar item Identifier
        Main body has three parts:
        top: Job Status as buttons
        middle: Posting Details
        bottom: Notes related to job
        job_id, job_title, job_date_added, job_date_posted, job_description, job_status
        """
        # data = database.get_one_row_from_table_by_name(self.conn, table, identifier)

        # Top Box - Job Status
        main_body_top = urwid.LineBox(urwid.Filler(self.build_job_status_button_gridflow(), "top"),
                                      title="Status", title_align="left")

        # Mid Box - Details about the posting
        main_body_mid = urwid.LineBox(urwid.Filler(urwid.Edit(), "top"),
                                      title="Posting Details", title_align="left")

        # Bottom Box - Notes about the posting
        list_of_notes_data_dicts = database.get_related_notes(self.conn, "job", identifier)

        # Turn list of note data into walkable list of strings
        list_of_notes_as_strings = []
        for note_dict in list_of_notes_data_dicts:
            note_as_text = "note_id: " + str(note_dict["note_id"]) + "   " + \
                           "note_company: " + str(note_dict["note_company"]) + "   " + \
                           "note_person: " + str(note_dict["note_person"]) + "   " + \
                           "note_job: " + str(note_dict["note_job"]) + "   " + \
                           "note_title: " + note_dict["note_title"] + "   " + \
                           "note_date_edited: " + note_dict["note_date_edited"] + "\n" + \
                           "note_details: " + note_dict["note_details"] + "\n"

            list_of_notes_as_strings.append(urwid.Text(note_as_text))
            # list_of_notes_as_strings.append(urwid.Text("\n".join([f"{x}: {note_dict[x]}" for x in note_dict])))

        main_body_bottom = urwid.LineBox(urwid.ListBox(urwid.SimpleFocusListWalker(list_of_notes_as_strings)),
                                         title="Notes", title_align="left")

        # text_items = []
        # for item in data:
        #     text_items.append(str(item) + ": " + str(data[item]))

        return [main_body_top, ("weight", 3, main_body_mid), ("weight", 3, main_body_bottom)]


    def build_body_side_bar(self, something, choice):
        """Builds the sidebar of the body depending on which tab is currently active
        :return:
        """

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
                main_body = urwid.LineBox(urwid.Filler(self.build_todo_main_body(choice, identifier), "top"),
                                          title="Todos", title_align="left")

            self.body_container.contents[1] = (main_body, ("weight", 3, False))

        elif choice == "company":
            pass
        elif choice == "job":
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

            if identifier:
                list_of_main_body_widgets = self.build_job_main_body(choice, identifier)

            main_body = urwid.Pile(list_of_main_body_widgets)

            self.body_container.contents[1] = (main_body, ("weight", 3, False))


        elif choice == "person":
            pass


    def body_picker(self, button, choice, identifier = None):
        """Function for directly changing the text in body_container"""

        if choice == "todo":
            # Default view
            side_bar = urwid.LineBox(urwid.Filler(urwid.Text("todo items", 'center', 'clip'), "top"))
            main_body = self.build_body_main_window()
            list_of_widgets_to_return = [(side_bar, ("weight", 1, False)), (main_body, ("weight", 3, False))]

          # Side Bar - Selectable list of companies
            # Note, buttons need connecting
            side_bar = urwid.LineBox(self.build_list_of_todos_for_sidebar(self.todo()))

            # Main body - Displays selected Todos
            if not identifier:
                main_body = urwid.LineBox(urwid.Filler(urwid.Text("Todo items", 'center', 'clip'), "top"),
                                              title="Todos", title_align="left")
            else:
                main_body = urwid.LineBox(urwid.Filler(self.build_todo_main_body(choice, identifier), "top"),
                                          title="Todos", title_align="left")

            list_of_widgets_to_return = [(side_bar, ("weight", 1, False)), (main_body, ("weight", 3, False))]

        elif choice == "company":
            # Side Bar - Selectable list of companies
            # Note, buttons need connecting
            side_bar = urwid.LineBox(self.build_list_of_companies_for_sidebar(self.companies()))

            # Main body top - Open Jobs at selected company
            main_body_top = urwid.LineBox(urwid.Filler(urwid.Text("Open Jobs", 'center', 'clip'), "top"),
                                          title="Open Jobs", title_align="left")

            # Main body middle - Notes about selected company
            main_body_mid = urwid.LineBox(urwid.Filler(urwid.Edit(), "top"),
                                          title="Notes", title_align="left")

            # Main body bottom - People known at selected company
            main_body_bottom = urwid.LineBox(urwid.Filler(urwid.Text("People", 'center', 'clip'), "top"),
                                          title="People", title_align="left")
            main_body = urwid.Pile([main_body_top, main_body_mid, main_body_bottom])

            list_of_widgets_to_return = [(side_bar, ("weight", 1, False)), (main_body, ("weight", 3, False))]

        elif choice == "person":
            # Side Bar - Selectable list of companies
            # Note, buttons need connecting
            side_bar = urwid.LineBox(self.build_list_of_people_for_sidebar(self.people()))

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
            side_bar = urwid.LineBox(self.build_list_of_jobs_for_sidebar(self.jobs()))

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
        self.body_picker(button, self.tab_name_table_name_map[choice])

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


    def exit_program(self):
        raise urwid.ExitMainLoop()


    def q_for_exit(self, key):
        if key in ('q', 'Q'):
            self.exit_program()


if __name__ == "__main__":
    app = App()

