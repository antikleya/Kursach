# import psycopg2
from faker import Faker
from misc import connect
import random
from hashlib import md5


def generate_clients(cur):
    fake = Faker('ru_RU')
    print('-----------------------------------------------')
    print('Starting generating clients...')

    for i in range(9900):
        name = fake.name().split()
        n = 1 if len(name) != 3 else 0

        number = fake.phone_number()
        first_name = name[0 + n]
        last_name = name[2 + n]
        passport_data = str(random.randint(1111111111, 9999999999))
        address = fake.address()

        cur.execute(f"""INSERT INTO clients (phone_number, first_name, last_name, passport_data, address) 
                    VALUES ('{number}', '{first_name}', '{last_name}', '{passport_data}', '{address}');""")
    print('Clients generated.')


def generate_accounts(cur):
    fake = Faker('ru_RU')

    print('-----------------------------------------------')
    print('Starting generating accounts...')
    f = open('users', 'w')
    fa = open('admins', 'w')
    for i in range(9900):
        login = ''.join([chr(random.randint(ord('a'), ord('z'))) for i in range(random.randint(8, 15))])
        password = fake.password(length=12)
        pass_hash = md5(password.encode('utf8')).hexdigest()
        date = fake.date()
        is_admin = False
        client_id = i + 1

        f.write(f'{login}:{password}\n')
        cur.execute(f"""INSERT INTO accounts (login, pass_hash, creation_date, is_admin, client_id)
                        VALUES ('{login}', '{pass_hash}', '{date}', {is_admin}, {client_id});""")

    for i in range(9900, 10000):
        login = ''.join([chr(random.randint(ord('a'), ord('z'))) for i in range(random.randint(8, 15))])
        password = fake.password(length=12)
        pass_hash = md5(password.encode('utf8')).hexdigest()
        date = fake.date()
        is_admin = True

        fa.write(f'{login}:{password}\n')
        cur.execute(f"""INSERT INTO accounts (login, pass_hash, creation_date, is_admin)
                                VALUES ('{login}', '{pass_hash}', '{date}', {is_admin});""")

    f.close()
    fa.close()
    print('Accounts generated.')


def generate_routers(cur):
    print('-----------------------------------------------')
    print('Starting generating routers...')

    with open('scraped/routers', 'r') as f:
        routers = f.readlines()
        for router in routers:
            params = router.split(';')
            cur.execute(f"""INSERT INTO routers (price, model, frequencies, wifi_standard, ports)
                    VALUES ({params[0]}, '{params[1]}', '{params[2]}', '{params[3]}', '{params[4]}');""")

    print('Routers generated')


def generate_int_tariffs(cur):
    print('-----------------------------------------------')
    print('Starting generating internet tariffs...')
    commands = ["""INSERT INTO internet_tariffs (name, speed, price) VALUES ('Basic', 500, 500);""",
                """INSERT INTO internet_tariffs (name, speed, price) VALUES ('Advanced', 750, 750);""",
                """INSERT INTO internet_tariffs (name, speed, price) VALUES ('Premium', 1000, 1000);""",
                """INSERT INTO internet_tariffs (name, speed, price) VALUES ('Premium2', 2000, 2000);""",
                """INSERT INTO internet_tariffs (name, speed, price) VALUES ('Premium3', 3000, 3000);""",
                """INSERT INTO internet_tariffs (name, speed, price) VALUES ('Premium4', 4000, 4000);""",
                """INSERT INTO internet_tariffs (name, speed, price) VALUES ('Premium5', 5000, 5000);""",
                """INSERT INTO internet_tariffs (name, speed, price) VALUES ('Premium6', 6000, 6000);""",
                """INSERT INTO internet_tariffs (name, speed, price) VALUES ('Premium7', 7000, 7000);""",
                """INSERT INTO internet_tariffs (name, speed, price) VALUES ('Premium8', 8000, 8000);"""]
    for i in commands:
        cur.execute(i)

    print('Internet tariffs generated.')


def generate_tv_tariffs(cur):
    print('-----------------------------------------------')
    print('Starting generating TV tariffs...')
    commands = ["""INSERT INTO tv_tariffs (name, channels, price, hd_channels) VALUES ('Basic', 80, 150, 20);""",
                """INSERT INTO tv_tariffs (name, channels, price, hd_channels) VALUES ('Optimal', 150, 200, 40);""",
                """INSERT INTO tv_tariffs (name, channels, price, hd_channels) VALUES ('Super', 250, 250, 70);""",
                """INSERT INTO tv_tariffs (name, channels, price, hd_channels) VALUES ('Super2', 1250, 1250, 170);""",
                """INSERT INTO tv_tariffs (name, channels, price, hd_channels) VALUES ('Super3', 2250, 1250, 270);""",
                """INSERT INTO tv_tariffs (name, channels, price, hd_channels) VALUES ('Super4', 3250, 1250, 370);""",
                """INSERT INTO tv_tariffs (name, channels, price, hd_channels) VALUES ('Super5', 4250, 1250, 470);""",
                """INSERT INTO tv_tariffs (name, channels, price, hd_channels) VALUES ('Super6', 5250, 1250, 570);""",
                """INSERT INTO tv_tariffs (name, channels, price, hd_channels) VALUES ('Super7', 6250, 1250, 670);""",
                """INSERT INTO tv_tariffs (name, channels, price, hd_channels) VALUES ('Super8', 7250, 1250, 770);"""]
    for i in commands:
        cur.execute(i)

    print('TV tariffs generated.')


def generate_servers(cur):
    print('-----------------------------------------------')
    print('Starting generating servers...')

    with open('scraped/cpu', 'r') as cpu_file:
        ram_file = open('scraped/ram', 'r')
        rams = ram_file.readlines()
        cpus = cpu_file.readlines()
        for i in range(100):
            ram_params = random.choice(rams).split(';')
            cpu_params = random.choice(cpus).split(';')
            cur.execute(f"""INSERT INTO servers (price, cpu, ram)
                        VALUES ({int(ram_params[1]) + int(cpu_params[1])}, '{cpu_params[0]}', '{ram_params[0]}');""")

    print('Servers generated')


def generate_contracts(cur):
    fake = Faker('ru_RU')

    print('-----------------------------------------------')
    print('Starting generating contracts...')

    for i in range(99500):

        account_id = random.randint(1, 9900)
        date = fake.date()
        tariff_id = random.randint(0, 10)
        tariff_id = tariff_id if tariff_id else None
        router_id = random.randint(0, 10)
        router_id = router_id if router_id else None
        tv_tariff_id = random.randint(0, 10) if tariff_id or router_id else random.randint(1, 10)
        tv_tariff_id = tv_tariff_id if tv_tariff_id else None

        cur.execute("""INSERT INTO contracts (account_id, date, tariff_id, tv_tariff_id, router_id) 
                       VALUES (%s, %s, %s, %s, %s)""", (account_id, date, tariff_id, tv_tariff_id, router_id))

    for i in range(500):

        account_id = random.randint(9901, 10000)
        date = fake.date()
        server_id = random.randint(1, 100)
        location = fake.address()

        cur.execute("""INSERT INTO contracts (account_id, date, server_id) 
                       VALUES (%s, %s, %s)""", (account_id, date, server_id))

        cur.execute("""INSERT INTO owned_servers (location, server_id) VALUES (%s, %s)""", (location, server_id))

    print('Contracts generated')


if __name__ == '__main__':
    conn = connect()
    cursor = conn.cursor()

    generate_clients(cursor)
    generate_accounts(cursor)
    generate_routers(cursor)
    generate_int_tariffs(cursor)
    generate_tv_tariffs(cursor)
    generate_servers(cursor)
    generate_contracts(cursor)

    conn.commit()
    conn.close()
