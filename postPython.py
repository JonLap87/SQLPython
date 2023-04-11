import psycopg2

def create_db(conn):
	with conn.cursor() as cur:
		cur.execute("""
			DROP TABLE Phone;
			DROP TABLE Client;
			""")

		cur.execute("""
			CREATE TABLE IF NOT EXISTS Client(
			id SERIAL PRIMARY KEY,
			name VARCHAR(60) NOT NULL,
			lastname VARCHAR(60) NOT NULL,
			email VARCHAR(60) NOT NULL UNIQUE;
			""")
		conn.commit()

		cur.execute("""
			CREATE TABLE IF NOT EXISTS Phone(
			number DECIMAL UNIQUE CHECK (number <= 99999999999),
			id INTEGER REFERENCES Client(id));
			""")
		conn.commit()


def add_client (conn, name, lastname, email, phones=None):
	with conn.cursor() as cur:
		cur.execute("""
			INSERT INTO Client (name, lastname, email)
			VALUES (name, lastname, email)
			RETURNING id, name, lastname, email;
			""")
	print (cur.fetchone())


def add_phone (conn, id, number):
	with conn.cursor() as cur:
		cur.execute("""
			INSERT INTO Phone (number, id)
			VALUES (number, id)
			RETURNING id, name, lastname, email;
			""")
	print (cur.fetchone())

def change_client(conn, id, name=None, lastname=None, email=None, number=None):
	with conn.cursor() as cur:
		cur.execute("""
			UPDATE Client
			SET name=%s, lastname=%s, email=%s;
			WHERE id=%s
			RETURNING id, name, lastname, email;
			""", (name, lastname, email,))
    
	

def change_phone(conn, id, name=None, lastname=None, email=None, number=None):
    with conn.cursor() as cur:
	    cur.execute("""
			UPDATE Phone
			SET number=%s;
			WHERE id=%s
			RETURNING id, number;
			""", (number,))
    

def delete_phone (conn, id, number):
	with conn.cursor() as cur:
		cur.execute("""
			DELETE FROM Phone
			WHERE id=%s;
			""", (id,))
	print (cur.fetchall())

def delete_client (conn, id):
	with conn.cursor() as cur:
		cur.execute("""
			DELETE FROM Client
			WHERE id=%s;
			""", (id,))
	print (cur.fetchall())

def find_client (conn, name=None, lastname=None, email=None, number=None):
	with conn.cursor() as cur:
		cur.execute("""
			SELECT c.name, c.lastname, c.email, p.number From Client c
			LEFT JOIN Phone p ON c.id = p.id
			WHERE c.name=%s OR c.lastname=%s OR c.email=%s OR p.number=%s;
			""", (name, lastname, email, number,))
	return cur.fetchone()[0]

conn = psycopg2.connect(database="netol_db", user= "postgres", password= "220261") 


print (add_client(conn,'Tom', 'Adoms', 'adom@mail.ru'))
print (add_phone(conn, '1', '89109467816'))
print (change_client (conn, '1', 'Jon', 'Varon', 'samual@mail.com'))
print (delete_phone (conn, '1', '89109467816'))
print (delete_client(conn, '1'))
print (find_client(conn, 'Tom'))

conn.close()