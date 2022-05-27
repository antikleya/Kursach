import PySimpleGUI as sg

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [ [sg.Text('Some text on Row 1')],
           [sg.Text('Enter something on Row 2'), sg.InputText()],
           [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Window Title', layout)


def bruh():
    print(values[0])


# Event Loop to process "events" and get the "values" of the inputs
event_dict = {sg.WIN_CLOSED: exit, 'Cancel': exit, 'Ok': bruh}
while True:
    event, values = window.read()
    event_dict[event]()

window.close()
