# import psycopg2
from faker import Faker
from misc import connect
import random
from hashlib import md5


def generate_clients(cur):
    fake = Faker('ru_RU')
    print('-----------------------------------------------')
    print('Starting generating clients...')

    for i in range(10):
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
    for i in range(10):
        login = ''.join([chr(random.randint(ord('a'), ord('z'))) for i in range(random.randint(8, 15))])
        password = fake.password(length=12)
        pass_hash = md5(password.encode('utf8')).hexdigest()
        date = fake.date()
        is_admin = False
        client_id = i + 1

        f.write(f'{login}:{password}\n')
        cur.execute(f"""INSERT INTO accounts (login, pass_hash, creation_date, is_admin, client_id)
                        VALUES ('{login}', '{pass_hash}', '{date}', {is_admin}, {client_id});""")

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
                """INSERT INTO internet_tariffs (name, speed, price) VALUES ('Premium', 1000, 1000);"""]
    for i in commands:
        cur.execute(i)

    print('Internet tariffs generated.')


def generate_tv_tariffs(cur):
    print('-----------------------------------------------')
    print('Starting generating TV tariffs...')
    commands = ["""INSERT INTO tv_tariffs (name, channels, price, hd_channels) VALUES ('Basic', 80, 150, 20);""",
                """INSERT INTO tv_tariffs (name, channels, price, hd_channels) VALUES ('Optimal', 150, 200, 40);""",
                """INSERT INTO tv_tariffs (name, channels, price, hd_channels) VALUES ('Super', 250, 250, 70);"""]
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
        for i in range(40):
            ram_params = random.choice(rams).split(';')
            cpu_params = random.choice(cpus).split(';')
            cur.execute(f"""INSERT INTO servers (price, cpu, ram)
                        VALUES ({int(ram_params[1]) + int(cpu_params[1])}, '{cpu_params[0]}', '{ram_params[0]}');""")

    print('Servers generated')


if __name__ == '__main__':
    conn = connect()
    cursor = conn.cursor()

    generate_clients(cursor)
    generate_accounts(cursor)
    generate_routers(cursor)
    generate_int_tariffs(cursor)
    generate_tv_tariffs(cursor)
    generate_servers(cursor)

    conn.commit()
    conn.close()
