import PySimpleGUI as sg


def auth_window():
    layout = [[sg.Text('Login: ', size=(10, 1)), sg.InputText(key='-LOGIN-')],
              [sg.Text('Password: ', size=(10, 1)), sg.InputText(key='-PASS-', password_char='*')],
              [sg.Button('Registration'), sg.Button('Log in', key='-AUTH-'), sg.Button('Exit')]]
    return sg.Window('Authentication window', layout, location=(800, 600), finalize=True)


def admin_reg_window():
    layout = [[sg.Text('Login: ', size=(20, 1)), sg.InputText(key='-A-REG-LOGIN-')],
              [sg.Text('Password: ', size=(20, 1)), sg.InputText(key='-A-REG-PASS-', password_char='*')],
              [sg.Text('Password confirmation: ', size=(20, 1)), sg.InputText(key='-A-REG-PASS-CONFIRM-', password_char='*')],
              [sg.Text('Employee registration requires an admin token')],
              [sg.Text('Admin token: ', size=(20, 1)), sg.InputText(key='-A-REG-TOKEN-', password_char='*')],
              [sg.Button('Register', key='-A-REGISTER-'), sg.Button('Back')]]
    return sg.Window('Employee registration window', layout, location=(800, 600), finalize=True)


def reg_choice_window():
    layout = [[sg.Text('Choose type of registration')],
              [sg.Button('Client'), sg.Button('Employee'), sg.Button('Back')]]
    return sg.Window('Registration choice window', layout, location=(800, 600), finalize=True)


def reg_window():
    layout = [[sg.Text('Login: ', size=(20, 1)), sg.InputText(key='-REG-LOGIN-')],
              [sg.Text('Password: ', size=(20, 1)), sg.InputText(key='-REG-PASS-', password_char='*')],
              [sg.Text('Password confirmation: ', size=(20, 1)), sg.InputText(key='-REG-PASS-CONFIRM-', password_char='*')],
              [sg.Text('Phone Number: ', size=(20, 1)), sg.InputText(key='-REG-PHONE-')],
              [sg.Text('First name: ', size=(20, 1)), sg.InputText(key='-REG-NAME-')],
              [sg.Text('Last name: ', size=(20, 1)), sg.InputText(key='-REG-LAST-NAME-')],
              [sg.Text('Address: ', size=(20, 1)), sg.InputText(key='-REG-ADDRESS-')],
              [sg.Text('Passport data: ', size=(20, 1)), sg.InputText(key='-REG-PASSPORT-')],
              [sg.Button('Register', key='-REGISTER-', size=(20, 1)), sg.Button('Back')]]
    return sg.Window('Client registration window', layout, location=(800, 600), finalize=True)


def menu_window():
    layout = [[sg.Text('Main menu')],
              [sg.Button('New contract', size=(15, 1))],
              [sg.Button('My contracts', size=(15, 1))],
              [sg.Button('Exit', size=(15, 1))]]
    return sg.Window('Menu Window', layout, location=(800, 600), finalize=True)


def admin_menu_window():
    layout = [[sg.Text('Main menu')],
              [sg.Button('Add server', size=(15, 1))],
              [sg.Button('Database', size=(15, 1))],
              [sg.Button('Exit', size=(15, 1))]]
    return sg.Window('Menu Window', layout, location=(800, 600), finalize=True)


def int_tariffs_window():
    layout = [[sg.Text("Choose an internet tariff(don't select anything to skip)")],
              [sg.Table([], headings=['tariff_id', 'name', 'speed', 'price'],
                        key='-INT-TARIFFS-', visible_column_map=[False, True, True, True],
                        select_mode=sg.TABLE_SELECT_MODE_BROWSE, enable_events=True)],
              [sg.Button('Back'), sg.Button('Next')]]
    return sg.Window('Menu Window', layout, location=(800, 600), finalize=True)


def routers_window():
    layout = [[sg.Text("Choose a router(don't select anything to skip)")],
              [sg.Table([], headings=['router_id', 'model', 'wifi_standard', 'frequencies', 'ports'], key='-ROUTERS-',
                        visible_column_map=[False, True, True, True, True], select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                        enable_events=True)],
              [sg.Button('Back'), sg.Button('Next')]]
    return sg.Window('Menu Window', layout, location=(800, 600), finalize=True)


def tv_tariffs_window():
    layout = [[sg.Text("Choose a tv tariff(don't select anything to skip)")],
              [sg.Table([], headings=['tariff_id', 'name', 'channels', 'hd_channels', 'price'],
                        key='-TV-TARIFFS-', visible_column_map=[False, True, True, True, True],
                        select_mode=sg.TABLE_SELECT_MODE_BROWSE, enable_events=True)],
              [sg.Button('Back'), sg.Button('Next')]]
    return sg.Window('Menu Window', layout, location=(800, 600), finalize=True)


def order_window():
    layout = [[sg.Text('Your order:')],
              [sg.Text('Internet tariff:', size=(20, 1)), sg.Text('', key='-INT-TARIFF-', size=(30, 1)),
               sg.Text('', key='-INT-TARIFF-PRICE-', size=(5, 1))],
              [sg.Text('Router:', size=(20, 1)), sg.Text('', key='-ROUTER-', size=(30, 1)),
               sg.Text('', key='-ROUTER-PRICE-', size=(5, 1))],
              [sg.Text('TV tariff:', size=(20, 1)), sg.Text('', key='-TV-TARIFF-', size=(30, 1)),
               sg.Text('', key='-TV-TARIFF-PRICE-', size=(5, 1))],
              [sg.Text('Order price', size=(52, 1)), sg.Text('', key='-PRICE-', size=(5, 1))],
              [sg.Button('Back'), sg.Button('Confirm')]]
    return sg.Window('Menu Window', layout, location=(800, 600), finalize=True)


def my_contracts_window():
    layout = [[sg.Text('My contracts')],
              [sg.Table([], headings=['Date', 'Router model', 'Internet tariff', 'TV tariff'],
                        key='-CONTRACTS-', select_mode=sg.TABLE_SELECT_MODE_BROWSE, enable_events=True)],
              [sg.Button('Back')]]
    return sg.Window('Menu Window', layout, location=(800, 600), finalize=True)


def database_window():
    layout = [[sg.Text('Table contents')],
              [sg.Combo(['accounts', 'clients', 'contracts', 'internet tariffs', 'routers', 'tv_tariffs', 'servers',
                         'owned servers'], default_value='clients', key='-TABLES-', enable_events=True, size=(30, 1))],
              [sg.Text('Complex queries')],
              [sg.Combo(['Client with the most contracts', 'Amount of contracts per internet tariff',
                         'Summary price of owned servers',
                         'Amount of clients that joined in the last 2 years and got a tv tariff'],
                        default_value='Client with the most contracts', key='-COMPLEX-',
                        enable_events=True, size=(50, 1))],
              [sg.Button('Back')]]
    return sg.Window('Menu Window', layout, location=(800, 600), finalize=True)


def servers_window():
    layout = [[sg.Text("Choose a server")],
              [sg.Table([], headings=['server_id', 'CPU', 'RAM', 'price'], key='-SERVERS-',
                        visible_column_map=[False, True, True, True], select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                        enable_events=True, col_widths=[10, 20, 20, 10], auto_size_columns=False)],
              [sg.Text('Enter server location')],
              [sg.InputText(size=(20, 1), key='-LOCATION-')],
              [sg.Button('Back'), sg.Button('Confirm')]]
    return sg.Window('Menu Window', layout, location=(800, 600), finalize=True)
