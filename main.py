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
For now, the companies(), people(), and jobs() functions read in csvs of text and return them
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


def people():
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
    return urwid.LineBox(urwid.Filler(main_window_text, "top"))


# Main screen on first load
def get_body_container_columns(choice="Todo"):
    column_1 = urwid.LineBox(urwid.Filler(urwid.Text("column1", 'center', 'clip'), "top"))
    column_2 = build_body_main_window(choice)
    return [("weight", 1, column_1), ("weight", 3, column_2)]


def build_body_container(choice="Todo"):
    """Builds the body container"""
    return urwid.Columns(get_body_container_columns())


def body_picker(button, choice):
    """Function for directly changing the text in body_container"""

    if choice == "Todo":
        side_bar = urwid.LineBox(urwid.Filler(urwid.Text("todo items", 'center', 'clip'), "top"))
        main_body = build_body_main_window(choice)
        list_of_widgets_to_return = [(side_bar, ("weight", 1, False)), (main_body, ("weight", 3, False))]

    elif choice == "Companies":
        side_bar = urwid.LineBox(urwid.Filler(companies(), "top"))

        main_body_top = urwid.LineBox(urwid.Filler(urwid.Text("Open Jobs", 'center', 'clip'), "top"),
                                      title="Open Jobs", title_align="left")
        main_body_mid = urwid.LineBox(urwid.Filler(urwid.Text("Notes", 'center', 'clip'), "top"),
                                      title="Notes", title_align="left")
        main_body_bottom = urwid.LineBox(urwid.Filler(urwid.Text("People", 'center', 'clip'), "top"),
                                      title="People", title_align="left")
        main_body = urwid.Pile([main_body_top, main_body_mid, main_body_bottom])

        list_of_widgets_to_return = [(side_bar, ("weight", 1, False)), (main_body, ("weight", 3, False))]

    elif choice == "People":
        side_bar = urwid.LineBox(urwid.Filler(people(), "top"))

        main_body_top = urwid.LineBox(urwid.Filler(urwid.Text("Details", 'center', 'clip'), "top"),
                                      title="Details", title_align="left")
        main_body_bottom = urwid.LineBox(urwid.Filler(urwid.Text("Notes", 'center', 'clip'), "top"),
                                      title="Notes", title_align="left")
        main_body = urwid.Pile([main_body_top, main_body_bottom])

        list_of_widgets_to_return = [(side_bar, ("weight", 1, False)), (main_body, ("weight", 3, False))]

    elif choice == "Jobs":
        side_bar = urwid.LineBox(urwid.Filler(jobs(), "top"))

        main_body_top = urwid.LineBox(urwid.Filler(urwid.Text("Here will be a bunch of options about the job's status",
                                                              'center', 'clip'), "top"),
                                      title="Status", title_align="left")
        main_body_mid = urwid.LineBox(urwid.Filler(urwid.Text("Here will be a bunch of options about the job's posting details",
                                                              'center', 'clip'), "top"),
                                      title="Posting Details", title_align="left")
        main_body_bottom = urwid.LineBox(urwid.Filler(urwid.Text("Here will be a bunch of options about the job's notes", 'center', 'clip'), "top"),
                                      title="Notes", title_align="left")
        main_body = urwid.Pile([main_body_top, main_body_mid, main_body_bottom])

        list_of_widgets_to_return = [(side_bar, ("weight", 1, False)), (main_body, ("weight", 3, False))]


    else:
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
    tab_menu = build_tab_menu(['Todo', 'Jobs', 'Companies', 'People'])
    # body_container = urwid.Filler(urwid.Text("default", 'left', 'clip'), "top")
    body_container = urwid.Columns(get_body_container_columns())

    # Arrange primary items into a Pile
    # main_pile = urwid.Pile([('pack', tab_menu), body_container])
    main_pile = urwid.Pile([('pack', tab_menu), body_container])

    mainloop = urwid.MainLoop(main_pile,
                              palette=[('reversed', 'standout', '')],
                              unhandled_input=q_for_exit)

    mainloop.run()

