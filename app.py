from flask import Flask, request, render_template, redirect, url_for,flash
import psycopg2


app = Flask(__name__)
app.secret_key = 'supersecretkey'  

# External PostgreSQL connection URL
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



    

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM feedbacks')
    feedbacks = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('home.html',cards=feedbacks)

@app.route('/aboutus',methods=['GET','POST'])
def aboutus(): 
    return render_template('index.html')

@app.route('/Glaucoma',methods=['GET','POST'])
def glaucoma(): 
    return render_template('glaucoma.html')



@app.route('/Research',methods=['GET','POST'])
def research(): 
    return render_template('research.html')

@app.route('/Cataract',methods=['GET','POST'])
def cataract(): 
    return render_template('cataract.html')

@app.route('/Retina',methods=['GET','POST'])
def retina(): 
    return render_template('retina.html')

@app.route('/Statistics',methods=['GET','POST'])
def statistics(): 
    return render_template('data.html')


@app.route('/Orbit & Oculoplasty',methods=['GET','POST'])
def orbit(): 
    return render_template('orbit.html')



@app.route('/camp',methods=['GET','POST'])
def camp(): 
    return render_template('map.html')

@app.route('/team',methods=['GET','POST'])
def team(): 
    return render_template('team.html')




@app.route('/review', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        rating = request.form['rate']
        review = request.form['review'] 
      
        
        # Insert data into database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO feedbacks (name, email, rating, review) VALUES (%s, %s, %s, %s);
        ''', (name, email, rating, review))
        conn.commit()
        cur.close()
        conn.close()
        flash('Thank you for your feedback!')
        return redirect(url_for('index'))
    
    return render_template('reviewform.html')







if __name__ == '__main__':
    create_table()
    app.run(debug=True)
    



