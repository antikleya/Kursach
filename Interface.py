import PySimpleGUI as sg
from misc import connect, new_order, check_order
from hashlib import md5
import re
import layouts
from datetime import date, timedelta


conn = connect()
cur = conn.cursor()
current_user = {'login': None, 'id': None}
current_order = new_order()
auth_win, menu_win, admin_reg_win, choice_win, reg_win, order_win = layouts.auth_window(), None, None, None, None, None
int_tariffs_win, tv_tariffs_win, routers_win, my_contracts_win, admin_menu_win = None, None, None, None, None
db_win, servers_win = None, None
admin_token = open('admin_token', 'r').read()


def get_max_contracts():
    cur.execute("""SELECT first_name, last_name, MAX(contract_num) 
                   FROM (select clients.first_name, clients.last_name, COUNT(contracts.contract_id) AS contract_num
                   FROM contracts JOIN accounts ON contracts.account_id = accounts.account_id
                   JOIN clients ON accounts.client_id = clients.client_id
                   GROUP BY first_name, last_name) AS sub_table GROUP BY first_name, last_name;""")
    return ['First name', 'Last name', 'Number of contracts'], cur.fetchall()


def get_tariff_popularity():
    cur.execute("""SELECT internet_tariffs.name as name, COUNT(contracts.tariff_id) as count
                   FROM contracts JOIN internet_tariffs ON contracts.tariff_id = internet_tariffs.tariff_id 
                   GROUP BY name 
                   ORDER BY count DESC;""")
    return ['Tariff Name', 'Amount of contracts'], cur.fetchall()


def get_servers_price():
    cur.execute("""SELECT SUM(servers.price) 
                   FROM servers JOIN owned_servers ON servers.server_id = owned_servers.server_id;""")
    return cur.fetchone()


def get_new_tv_clients():
    _date = (date.today() - timedelta(days=730)).strftime('%Y-%m-%d')
    cur.execute(f"""SELECT COUNT(account_id) 
                   FROM (SELECT DISTINCT accounts.account_id as account_id 
                         FROM accounts JOIN contracts ON contracts.account_id = accounts.account_id 
                         JOIN tv_tariffs ON contracts.tv_tariff_id = tv_tariffs.tariff_id 
                         WHERE accounts.creation_date > '{_date}') as sub_table;""")
    return cur.fetchone()


def get_column_names(table_name):
    cur.execute(f"""SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table_name}';""")
    return [x[0] for x in cur.fetchall()]


def fill_servers():
    cur.execute("""SELECT server_id, cpu, ram, price FROM servers;""")
    servers_win.find_element('-SERVERS-').update(values=cur.fetchall())


def fill_order():
    router = current_order['router'][1] if current_order['router'] else 'Not Selected'
    router_price = current_order['router'][5] if current_order['router'] else '-----'
    order_win.find_element('-ROUTER-').update(value=router)
    order_win.find_element('-ROUTER-PRICE-').update(value=router_price)

    int_tariff = current_order['int_tariff'][1] if current_order['int_tariff'] else 'Not Selected'
    int_tariff_price = current_order['int_tariff'][3] if current_order['int_tariff'] else '-----'
    order_win.find_element('-INT-TARIFF-').update(value=int_tariff)
    order_win.find_element('-INT-TARIFF-PRICE-').update(value=int_tariff_price)

    tv_tariff = current_order['tv_tariff'][1] if current_order['tv_tariff'] else 'Not Selected'
    tv_tariff_price = current_order['tv_tariff'][4] if current_order['tv_tariff'] else '-----'
    order_win.find_element('-TV-TARIFF-').update(value=tv_tariff)
    order_win.find_element('-TV-TARIFF-PRICE-').update(value=tv_tariff_price)

    price = router_price if router_price != '-----' else 0
    price += int_tariff_price if int_tariff_price != '-----' else 0
    price += tv_tariff_price if tv_tariff_price != '-----' else 0
    order_win.find_element('-PRICE-').update(value=price)


def fill_routers():
    cur.execute("""SELECT router_id, model, wifi_standard, frequencies, ports, price FROM routers;""")
    routers_win.find_element('-ROUTERS-').update(values=cur.fetchall())


def fill_int_tariffs():
    cur.execute("""SELECT tariff_id, name, speed, price FROM internet_tariffs;""")
    int_tariffs_win.find_element('-INT-TARIFFS-').update(values=cur.fetchall())


def fill_tv_tariffs():
    cur.execute("""SELECT tariff_id, name, channels, hd_channels, price FROM tv_tariffs;""")
    tv_tariffs_win.find_element('-TV-TARIFFS-').update(values=cur.fetchall())


def fill_contracts():
    cur.execute("""SELECT contracts.date, routers.model, internet_tariffs.name, tv_tariffs.name 
                FROM contracts LEFT OUTER JOIN routers ON contracts.router_id = routers.router_id
                LEFT OUTER JOIN internet_tariffs ON contracts.tariff_id = internet_tariffs.tariff_id
                LEFT OUTER JOIN tv_tariffs ON contracts.tv_tariff_id = tv_tariffs.tariff_id
                ORDER BY contracts.date;""")
    my_contracts_win.find_element('-CONTRACTS-').update(values=cur.fetchall())


def get_table_values(table_name):
    cur.execute(f"""SELECT * FROM {table_name};""")
    return cur.fetchall()


queries = {'Client with the most contracts': get_max_contracts,
           'Amount of contracts per internet tariff': get_tariff_popularity,
           'Summary price of owned servers': get_servers_price,
           'Amount of clients that joined in the last 2 years and got a tv tariff': get_new_tv_clients}

while True:
    window, event, values = sg.read_all_windows()

    if event == sg.WIN_CLOSED or event == 'Exit':
        window.close()
        break

    elif event == '-AUTH-':
        login = re.sub(r'[^\w]', '', values['-LOGIN-'])
        hashed_pass = md5(values['-PASS-'].encode('utf-8')).hexdigest()
        cur.execute(f"""SELECT * FROM accounts WHERE login='{login}' AND pass_hash='{hashed_pass}'""")
        user = cur.fetchone()
        if user:
            current_user['login'] = user[1]
            current_user['admin'] = user[4]
            current_user['id'] = user[0]
            window.close()
            auth_win = None
            if user[4]:
                admin_menu_win = layouts.admin_menu_window()
            else:
                menu_win = layouts.menu_window()
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
        window.close()
        if window == choice_win:
            choice_win = None
            if not auth_win:
                auth_win = layouts.auth_window()

        elif window == reg_win:
            reg_win = None
            choice_win = layouts.reg_choice_window()

        elif window == admin_reg_win:
            admin_reg_win = None
            choice_win = layouts.reg_choice_window()

        elif window == routers_win:
            current_order['router'] = None
            routers_win = None
            int_tariffs_win = layouts.int_tariffs_window()
            fill_int_tariffs()

        elif window == tv_tariffs_win:
            current_order['tv_tariff'] = None
            tv_tariffs_win = None
            routers_win = layouts.routers_window()
            fill_routers()

        elif window == int_tariffs_win:
            current_order['int_tariff'] = None
            int_tariffs_win = None
            menu_win = layouts.menu_window()

        elif window == my_contracts_win:
            my_contracts_win = None
            menu_win = layouts.menu_window()

        elif window == order_win:
            order_win = None
            tv_tariffs_win = layouts.tv_tariffs_window()
            fill_tv_tariffs()

        elif window == servers_win:
            servers_win = None
            admin_menu_win = layouts.admin_menu_window()

        elif window == db_win:
            db_win = None
            admin_menu_win = layouts.admin_menu_window()

    elif event == 'Next':
        window.close()
        if window == int_tariffs_win:
            selected_row = values['-INT-TARIFFS-']
            if selected_row:
                current_order['int_tariff'] = int_tariffs_win.find_element('-INT-TARIFFS-').get()[selected_row[0]]
            else:
                current_order['int_tariff'] = None
            int_tariffs_win = None
            routers_win = layouts.routers_window()
            fill_routers()

        elif window == routers_win:
            selected_row = values['-ROUTERS-']
            if selected_row:
                current_order['router'] = routers_win.find_element('-ROUTERS-').get()[selected_row[0]]
            else:
                current_order['router'] = None
            routers_win = None
            tv_tariffs_win = layouts.tv_tariffs_window()
            fill_tv_tariffs()

        elif window == tv_tariffs_win:
            selected_row = values['-TV-TARIFFS-']
            if selected_row:
                current_order['tv_tariff'] = tv_tariffs_win.find_element('-TV-TARIFFS-').get()[selected_row[0]]
            else:
                current_order['tv_tariff'] = None
            tv_tariffs_win = None
            order_win = layouts.order_window()
            fill_order()

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
                        VALUES ('{login}', '{pass_hash}', '{curr_date}', {True})
                        RETURNING account_id;""")
        conn.commit()

        window.close()
        admin_reg_win = None
        current_user['login'] = login
        current_user['id'] = cur.fetchone()[0]
        admin_menu_win = layouts.admin_menu_window()

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
                        VALUES ('{login}', '{pass_hash}', '{curr_date}', {False}, {client_id})
                        RETURNING account_id;""")

        conn.commit()

        window.close()
        reg_win = None
        current_user['login'] = login
        current_user['id'] = cur.fetchone()[0]
        menu_win = layouts.menu_window()

    elif event == 'New contract':
        window.close()
        int_tariffs_win = layouts.int_tariffs_window()
        fill_int_tariffs()
        menu_win = None

    elif event == 'My contracts':
        window.close()
        my_contracts_win = layouts.my_contracts_window()
        fill_contracts()
        menu_win = None

    elif event == 'Confirm':
        if window == order_win:
            if not check_order(current_order):
                sg.popup('Your order is empty')
                continue

            int_tariff_id = current_order['int_tariff'][0] if current_order['int_tariff'] else None
            tv_tariff_id = current_order['tv_tariff'][0] if current_order['tv_tariff'] else None
            router_id = current_order['router'][0] if current_order['router'] else None
            curr_date = date.today().strftime('%Y-%m-%d')

            cur.execute("""INSERT INTO contracts 
                        (account_id, date, tariff_id, tv_tariff_id, router_id) 
                        VALUES (%s, %s, %s, %s, %s)""", (current_user['id'], curr_date, int_tariff_id,
                                                         tv_tariff_id, router_id))
            sg.popup('Your order has been confirmed')
            window.close()
            menu_win = layouts.menu_window()
            order_win = None
            conn.commit()

        elif window == servers_win:
            selected_row = values['-SERVERS-']
            location = values['-LOCATION-']

            if not location:
                sg.popup('Location is empty')
                continue

            if not selected_row:
                sg.popup('No server selected')
                continue

            server_id = servers_win.find_element('-SERVERS-').get()[selected_row[0]][0]
            curr_date = date.today().strftime('%Y-%m-%d')

            cur.execute("""INSERT INTO contracts 
                                    (account_id, date, server_id) 
                                    VALUES (%s, %s, %s)""", (current_user['id'], curr_date, server_id))
            cur.execute("""INSERT INTO owned_servers
                                    (location, server_id)
                                    VALUES (%s, %s)""", (location, server_id))
            sg.popup('Your order has been confirmed')
            window.close()
            admin_menu_win = layouts.admin_menu_window()
            servers_win = None
            conn.commit()

    elif event == 'Database':
        window.close()
        admin_menu_win = None
        db_win = layouts.database_window()

    elif event == '-TABLES-':
        sg.Window('Table contents', [[sg.Table(values=get_table_values(values['-TABLES-']),
                                               headings=get_column_names(values['-TABLES-']))]]).read(close=True)

    elif event == '-COMPLEX-':
        query = queries[values['-COMPLEX-']]()
        if values['-COMPLEX-'] == 'Summary price of owned servers':
            sg.popup(f'Summary price is {query[0]}')
            continue

        elif values['-COMPLEX-'] == 'Amount of clients that joined in the last 2 years and got a tv tariff':
            sg.popup(f'Amounts of new tv clients is {query[0]}')
            continue

        sg.Window('Query result', [[sg.Table(values=query[1], headings=query[0])]]).read(close=True)

    elif event == 'Add server':
        window.close()
        admin_menu_win = None
        servers_win = layouts.servers_window()
        fill_servers()


window.close()
conn.close()
