import psycopg2
from misc import connect


if __name__ == '__main__':
    conn = connect()

    commands = (
        """DROP TABLE IF EXISTS clients CASCADE""",
        """DROP TABLE IF EXISTS accounts CASCADE""",
        """DROP TABLE IF EXISTS routers CASCADE""",
        """DROP TABLE IF EXISTS internet_tariffs CASCADE""",
        """DROP TABLE IF EXISTS tv_tariffs CASCADE""",
        """DROP TABLE IF EXISTS servers CASCADE""",
        """DROP TABLE IF EXISTS owned_servers CASCADE""",
        """DROP TABLE IF EXISTS contracts CASCADE""",
        """
        CREATE TABLE clients (
            client_id SERIAL PRIMARY KEY,
            phone_number TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            passport_data CHAR(10) NOT NULL,
            address TEXT NOT NULL
        )
        """,
        """ CREATE TABLE accounts (
                account_id SERIAL PRIMARY KEY,
                login TEXT NOT NULL,
                pass_hash TEXT NOT NULL,
                creation_date DATE NOT NULL,
                is_admin BOOL NOT NULL,
                client_id INTEGER,
                FOREIGN KEY (client_id)
                    REFERENCES clients (client_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE routers (
                router_id SERIAL PRIMARY KEY,
                price INTEGER NOT NULL,
                wifi_standard TEXT NOT NULL,
                model TEXT NOT NULL,
                frequencies TEXT NOT NULL,
                ports TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE internet_tariffs (
                tariff_id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                speed INTEGER NOT NULL,
                price INTEGER NOT NULL
        )
        """,
        """
        CREATE TABLE tv_tariffs (
                tariff_id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                channels INTEGER NOT NULL,
                price INTEGER NOT NULL,
                hd_channels INTEGER NOT NULL
        )
        """,
        """
        CREATE TABLE servers (
                server_id SERIAL PRIMARY KEY,
                price INTEGER NOT NULL,
                cpu TEXT NOT NULL,
                ram TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE owned_servers (
                o_server_id SERIAL PRIMARY KEY,
                cpu TEXT NOT NULL,
                ram TEXT NOT NULL,
                location TEXT NOT NULL,
                server_id INTEGER NOT NULL,
                FOREIGN KEY (server_id)
                    REFERENCES servers (server_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE contracts (
                contract_id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                account_id INTEGER NOT NULL,
                router_id INTEGER,
                tariff_id INTEGER,
                tv_tariff_id INTEGER,
                server_id INTEGER,
                FOREIGN KEY (account_id)
                    REFERENCES accounts (account_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (router_id)
                    REFERENCES routers (router_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (tariff_id)
                    REFERENCES internet_tariffs (tariff_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (tv_tariff_id)
                    REFERENCES tv_tariffs (tariff_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (server_id)
                    REFERENCES servers (server_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
    )
    try:
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        print('Created tables: Clients, Accounts, Routers, '
              'Internet_tariffs, TV_Tariffs, Servers, Owned_servers, Contracts')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

