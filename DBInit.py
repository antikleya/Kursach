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

    with open('routers', 'r') as f:
        routers = f.readlines()
        for router in routers:
            if router:
                params = router.split(';')
                cur.execute(f"""INSERT INTO routers (price, model, frequencies, wifi_standard, ports)
                        VALUES ({params[0]}, '{params[1]}', '{params[2]}', '{params[3]}', '{params[4]}');""")

    print('Routers generated')


if __name__ == '__main__':
    conn = connect()
    cur = conn.cursor()

    generate_clients(cur)
    generate_accounts(cur)
    generate_routers(cur)

    conn.commit()
    conn.close()
