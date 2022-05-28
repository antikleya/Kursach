import PySimpleGUI as sg


def auth_window():
    layout = [[sg.Text('Login:     '), sg.InputText(key='-LOGIN-')],
              [sg.Text('Password:  '), sg.InputText(key='-PASS-', password_char='*')],
              [sg.Button('Registration'), sg.Button('Log in', key='-AUTH-'), sg.Button('Exit')]]
    return sg.Window('Authentication window', layout, location=(800, 600), finalize=True)


def admin_reg_window():
    layout = [[sg.Text('Login:                 '), sg.InputText(key='-A-REG-LOGIN-')],
              [sg.Text('Password:              '), sg.InputText(key='-A-REG-PASS-', password_char='*')],
              [sg.Text('Password confirmation: '), sg.InputText(key='-A-REG-PASS-CONFIRM-', password_char='*')],
              [sg.Text('Employee registration requires an admin token')],
              [sg.Text('Admin token:           '), sg.InputText(key='-A-REG-TOKEN-', password_char='*')],
              [sg.Button('Register', key='-A-REGISTER-'), sg.Button('Back')]]
    return sg.Window('Employee registration window', layout, location=(800, 600), finalize=True)


def reg_choice_window():
    layout = [[sg.Text('Choose type of registration')],
              [sg.Button('Client'), sg.Button('Employee'), sg.Button('Back')]]
    return sg.Window('Registration choice window', layout, location=(800, 600), finalize=True)


def reg_window():
    layout = [[sg.Text('Login:                 '), sg.InputText(key='-REG-LOGIN-')],
              [sg.Text('Password:              '), sg.InputText(key='-REG-PASS-', password_char='*')],
              [sg.Text('Password confirmation: '), sg.InputText(key='-REG-PASS-CONFIRM-', password_char='*')],
              [sg.Text('Phone Number:          '), sg.InputText(key='-REG-PHONE-')],
              [sg.Text('First name:            '), sg.InputText(key='-REG-NAME-')],
              [sg.Text('Last name:             '), sg.InputText(key='-REG-LAST-NAME-')],
              [sg.Text('Address:               '), sg.InputText(key='-REG-ADDRESS-')],
              [sg.Text('Passport data:         '), sg.InputText(key='-REG-PASSPORT-')],
              [sg.Button('Register', key='-REGISTER-'), sg.Button('Back')]]
    return sg.Window('Client registration window', layout, location=(800, 600), finalize=True)


def menu_window():
    layout = [[sg.Text('The second window')],
              [sg.Input(key='-IN-', enable_events=True)],
              [sg.Text(size=(25, 1), k='-OUTPUT-')],
              [sg.Button('Erase'), sg.Button('Exit')]]
    return sg.Window('Menu Window', layout, finalize=True)
