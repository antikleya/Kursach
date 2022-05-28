import PySimpleGUI as sg
from misc import connect
from hashlib import md5
import re
import layouts
from datetime import date


conn = connect()
cur = conn.cursor()
current_user = {'login': None, 'admin': False}
auth_win, menu_win, admin_reg_win, choice_win, reg_win = layouts.auth_window(), None, None, None, None        # start off with 1 window open
admin_token = open('admin_token', 'r').read()

while True:
    window, event, values = sg.read_all_windows()

    if event == sg.WIN_CLOSED or event == 'Exit':
        window.close()
        break

    elif event == '-AUTH-':
        login = re.sub(r'[^\w]', '', values['-LOGIN-'])
        hashed_pass = md5(values['-PASS-'].encode('utf-8')).hexdigest()
        print(login + ':' + hashed_pass)
        cur.execute(f"""SELECT * FROM accounts WHERE login='{login}' AND pass_hash='{hashed_pass}'""")
        user = cur.fetchone()
        if user:
            current_user['login'] = user[1]
            current_user['admin'] = user[4]
            window.close()
            menu_win = layouts.menu_window()
            auth_win = None
        else:
            sg.popup('Incorrect user data')

    elif event == 'Registration':
        choice_win = layouts.reg_choice_window()

    elif event == 'Employee':
        window.close()
        choice_win = None
        admin_reg_win = layouts.admin_reg_window()
        auth_win.close()
        auth_win = None

    elif event == 'Client':
        window.close()
        choice_win = None
        reg_win = layouts.reg_window()
        auth_win.close()
        auth_win = None

    elif event == 'Back':
        if window == choice_win:
            window.close()
            choice_win = None
            if not auth_win:
                auth_win = layouts.auth_window()

        if window == reg_win:
            window.close()
            reg_win = None
            choice_win = layouts.reg_choice_window()

        if window == admin_reg_win:
            window.close()
            admin_reg_win = None
            choice_win = layouts.reg_choice_window()

    elif event == '-A-REGISTER-':
        login = re.sub(r'[^\w]', '', values['-A-REG-LOGIN-'])
        password = values['-A-REG-PASS-']
        conf_pass = values['-A-REG-PASS-CONFIRM-']
        token = values['-A-REG-TOKEN-']
        if not login:
            sg.popup('Login is empty')
            continue

        if not password:
            sg.popup('Password is empty')
            continue

        if password != conf_pass:
            sg.popup("Passwords do not match")

        if not token:
            sg.popup('Admin token is empty')
            continue

        if token != admin_token:
            sg.popup('Incorrect admin token')
            continue

        pass_hash = md5(password.encode('utf-8')).hexdigest()
        curr_date = date.today().strftime('%Y-%m-%d')

        cur.execute(f"""INSERT INTO accounts (login, pass_hash, creation_date, is_admin)
                        VALUES ('{login}', '{pass_hash}', '{curr_date}', {True});""")
        conn.commit()

        window.close()
        admin_reg_win = None
        current_user['login'] = login
        current_user['admin'] = True
        menu_win = layouts.menu_window()

    elif event == '-REGISTER-':
        login = re.sub(r'[^\w]', '', values['-REG-LOGIN-'])
        password = values['-REG-PASS-']
        conf_pass = values['-REG-PASS-CONFIRM-']
        phone = values['-REG-PHONE-']
        address = values['-REG-ADDRESS-']
        first_name = values['-REG-NAME-']
        last_name = values['-REG-LAST-NAME-']
        passport = values['-REG-PASSPORT-']
        if not login:
            sg.popup('Login is empty')
            continue

        if not password:
            sg.popup('Password is empty')
            continue

        if not phone or not address or not first_name or not last_name or not passport:
            sg.popup('Please fill in all the fields')
            continue

        if password != conf_pass:
            sg.popup("Passwords do not match")

        pass_hash = md5(password.encode('utf-8')).hexdigest()
        curr_date = date.today().strftime('%Y-%m-%d')

        cur.execute(f"""INSERT INTO clients (phone_number, first_name, last_name, address, passport_data)
                                VALUES ('{phone}', '{first_name}', '{last_name}', '{address}', '{passport}')
                                RETURNING client_id;""")
        client_id = cur.fetchone()[0]

        cur.execute(f"""INSERT INTO accounts (login, pass_hash, creation_date, is_admin, client_id)
                        VALUES ('{login}', '{pass_hash}', '{curr_date}', {False}, {client_id});""")

        conn.commit()

        window.close()
        reg_win = None
        current_user['login'] = login
        current_user['admin'] = False
        menu_win = layouts.menu_window()


window.close()
conn.close()
