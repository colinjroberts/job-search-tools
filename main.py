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

"""
For now, the companies(), contacts(), and jobs() functions read in csvs of text and return them
as urwid Text objects. Later, these will likely become calls to whatever backend is used...SQLite 
probably?
"""


def companies():
    company_names = []
    with open('data/companies.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        fieldnames = next(csvreader)

        reading = True
        while reading:
            try:
                company_names.append(next(csvreader)[1] + "\n")
            except StopIteration:
                reading = False

    return urwid.Text(company_names)


def contacts():
    contact_names = []
    with open('data/contacts.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        fieldnames = next(csvreader)

        reading = True
        while reading:
            try:
                contact_names.append(next(csvreader)[1] + "\n")
            except StopIteration:
                reading = False

    return urwid.Text(contact_names)


def jobs():
    job_names = []
    with open('data/jobs.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        fieldnames = next(csvreader)

        reading = True
        while reading:
            try:
                job_names.append(next(csvreader)[2] + "\n")
            except StopIteration:
                reading = False

    return urwid.Text(job_names)


def build_tab_menu(choices):
    """Defines and builds tab_menu using provided choices
    Probably doesn't need to be this convoluted.
    """
    cells = []
    for item in choices:
        button = urwid.Button(item)
        urwid.connect_signal(button, 'click', on_tab_click, item)
        cells.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.GridFlow(cells, 20, 2, 1, "left")


def build_body_side_bar(self, choice):
    """Builds the sidebar of the body depending on which tab is currently active

    :return:
    """


def build_body_main_window(choice):
    """Builds the main window of the body depending on which tab is currently active
    The calling method is a Filler, and this will return different Text objects to it
    :return: Lineboxed urwid object
    """
    main_window_text = urwid.Text(f"This will be the main window in which {choice} data will appear", 'center', 'clip')
    return main_window_text


def get_body_container_columns(choice="Todo"):
    column_1 = urwid.LineBox(urwid.Filler(urwid.Text("column1", 'center', 'clip'), "top"))
    column_2 = urwid.LineBox(urwid.Filler(build_body_main_window(choice), "top"))
    return [("weight", 1, column_1), ("weight", 3, column_2)]


def build_body_container(choice="Todo"):
    """Builds the body container"""
    return urwid.Columns(get_body_container_columns())


def body_picker(button, choice):
    """Function for directly changing the text in body_container"""
    if choice == "Todo":
        column_1 = urwid.LineBox(urwid.Filler(urwid.Text("todo items", 'center', 'clip'), "top"))
        column_2 = urwid.LineBox(urwid.Filler(build_body_main_window(choice), "top"))
        list_of_widgets_to_return = [(column_1, ("weight", 1, False)), (column_2, ("weight", 3, False))]

    elif choice == "Companies":
        column_1 = urwid.LineBox(urwid.Filler(companies(), "top"))
        column_2 = urwid.LineBox(urwid.Filler(build_body_main_window(choice), "top"))
        # body_container.widget_list = build_body_main_window(choice=choice)
        list_of_widgets_to_return = [(column_1, ("weight", 1, False)), (column_2, ("weight", 3, False))]

    elif choice == "Contacts":
        column_1 = urwid.LineBox(urwid.Filler(contacts(), "top"))
        column_2 = urwid.LineBox(urwid.Filler(build_body_main_window(choice), "top"))
        # body_container.widget_list = build_body_main_window(choice=choice)
        list_of_widgets_to_return = [(column_1, ("weight", 1, False)), (column_2, ("weight", 3, False))]

    elif choice == "Jobs":
        column_1 = urwid.LineBox(urwid.Filler(jobs(), "top"))
        column_2 = urwid.LineBox(urwid.Filler(build_body_main_window(choice), "top"))
        # body_container.widget_list = build_body_main_window(choice=choice)
        list_of_widgets_to_return = [(column_1, ("weight", 1, False)), (column_2, ("weight", 3, False))]

    else:
        # body_container.body = urwid.Text("There must have been a mistake.", 'left', 'clip')
        list_of_widgets_to_return = [("pack", urwid.Text("There must have been a mistake.", 'left', 'clip'))]

    body_container.contents = urwid.MonitoredFocusList(list_of_widgets_to_return)


def on_tab_click(button, choice):
    """Callback function for changing main_body
    :param button: not sure what this is for, but some first variable is expected
    :param choice: user variable used for switch
    :return: None. For now, this just calls the body_picker function which directly changes
    """
    body_picker(button, choice)


def exit_program():
    raise urwid.ExitMainLoop()


def q_for_exit(key):
    if key in ('q', 'Q'):
        exit_program()


if __name__ == "__main__":
    # Build primary two subdivisions: tab_menu and body_container
    tab_menu = build_tab_menu(['Todo', 'Jobs', 'Companies', 'Contacts'])
    # body_container = urwid.Filler(urwid.Text("default", 'left', 'clip'), "top")
    body_container = urwid.Columns(get_body_container_columns())

    # Arrange primary items into a Pile
    # main_pile = urwid.Pile([('pack', tab_menu), body_container])
    main_pile = urwid.Pile([('pack', tab_menu), body_container])

    mainloop = urwid.MainLoop(main_pile,
                              palette=[('reversed', 'standout', '')],
                              unhandled_input=q_for_exit)

    mainloop.run()

