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


def body_picker(button, choice):
    """Function for directly changing the text in body_container"""
    if choice == "Todo":
        body_container.body = urwid.Text("Todo", 'left', 'clip')
    elif choice == "Companies":
        body_container.body = companies()
    elif choice == "Contacts":
        body_container.body = contacts()
    elif choice == "Jobs":
        body_container.body = jobs()
    else:
        body_container.body = urwid.Text("There must have been a mistake.", 'left', 'clip')


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
    body_container = urwid.Filler(urwid.Text("default", 'left', 'clip'), "top")

    # Arrange primary items into a Pile
    main_pile = urwid.Pile([('pack', tab_menu), body_container])

    mainloop = urwid.MainLoop(main_pile,
                              palette=[('reversed', 'standout', '')],
                              unhandled_input=q_for_exit)

    mainloop.run()
