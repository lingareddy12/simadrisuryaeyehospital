import psycopg2

DB_URL = "postgresql://mydatabase_8cun_user:xUw8BZ8swteQRj6HK1XycFfEhqZFbUw5@dpg-cq578p5ds78s73ct5dk0-a.oregon-postgres.render.com/mydatabase_8cun"

def get_db_connection():
    conn = psycopg2.connect(DB_URL)
    return conn

def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS feedbacks (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            rating INTEGER,
            review TEXT
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

def delete_all_rows():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM feedbacks;')
    conn.commit()
    cur.close()
    conn.close()
    
def delete_stat_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
       Drop table hospital_statistics''')
    conn.commit()
    cur.close()
    conn.close()

# Example usage
if __name__ == "__main__":
    delete_stat_table()
