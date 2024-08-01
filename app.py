from flask import Flask, request,session, render_template, redirect, url_for,flash
import psycopg2

from datetime import datetime



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
    
def create_stat_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS hospital_statistics (
    id SERIAL PRIMARY KEY,
    outpatients_treated INTEGER NOT NULL,
    medicines_prescribed INTEGER NOT NULL,
    optical_prescribed INTEGER NOT NULL,
    surgeries_prescribed INTEGER NOT NULL,
    date_of_updation DATE NOT NULL,
    cataract_male INTEGER NOT NULL,
    cataract_female INTEGER NOT NULL,
    cornea_male INTEGER NOT NULL,
    cornea_female INTEGER NOT NULL,
    retina_male INTEGER NOT NULL,
    retina_female INTEGER NOT NULL,
    orbit_male INTEGER NOT NULL,
    orbit_female INTEGER NOT NULL); ''')
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
    return render_template('aboutus.html')

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
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM hospital_statistics ORDER BY id DESC LIMIT 1; ''')
    stats = cur.fetchall()
    stats=stats[0]
    stats = list(stats)  # Convert tuple to list
    stats[5]=stats[5].strftime('%d %B %Y')
   
    
    cur.close()
    conn.close()
    return render_template('data.html',stats=stats)


@app.route('/Orbit & Oculoplasty',methods=['GET','POST'])
def orbit(): 
    return render_template('orbit.html')



@app.route('/camp',methods=['GET','POST'])
def camp(): 
    return render_template('map.html')

@app.route('/team',methods=['GET','POST'])
def team(): 
    return render_template('team.html')

@app.route('/donate',methods=['GET','POST'])
def donate(): 
    return render_template('donations.html')

@app.route('/payment',methods=['GET','POST'])
def payment(): 
    return render_template('payment.html')

@app.route('/Pro Active Measures',methods=['GET','POST'])
def activemeasures(): 
    return render_template('activemeasures.html')

@app.route('/Admin',methods=['GET','POST'])
def login(): 
    if request.method == 'POST':
        name = request.form['name']
        passw = request.form['password']
        if name=="sseh" and passw=="sseh@2024":
            session['isloggedin']=True; 
            return redirect(url_for('updates'))
        else:
            return render_template('login.html')
            
    return render_template('login.html')



@app.route('/updates', methods=['GET', 'POST'])
def updates(): 
    if 'isloggedin' in session and session['isloggedin']:
        if request.method == 'POST':
            outpatients_treated = request.form['outpatients-treated']
            medicines_prescribed = request.form['medicines-prescribed']
            optical_prescribed = request.form['optical-prescribed']
            surgeries_prescribed = request.form['surgeries-prescribed']
            date_of_updation = request.form['date-of-updation']
            cataract_male = request.form['cataract-male']
            cataract_female = request.form['cataract-female']
            cornea_male = request.form['cornea-male']
            cornea_female = request.form['cornea-female']
            retina_male = request.form['retina-male']
            retina_female = request.form['retina-female']
            orbit_male = request.form['orbit-male']
            orbit_female = request.form['orbit-female']
            
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('''
            INSERT INTO hospital_statistics (
                outpatients_treated, medicines_prescribed, optical_prescribed, 
                surgeries_prescribed, date_of_updation, cataract_male, cataract_female, 
                cornea_male, cornea_female, retina_male, retina_female, orbit_male, orbit_female
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                ''', (
                outpatients_treated, medicines_prescribed, optical_prescribed, 
                surgeries_prescribed, date_of_updation, cataract_male, cataract_female, 
                cornea_male, cornea_female, retina_male, retina_female, orbit_male, orbit_female
                        ))
            conn.commit()
            cur.close()
            conn.close()
            flash('Successfully updated')
            return redirect(url_for('index'))
        else:
            return render_template('updates.html')       
    else:
        return redirect(url_for('login'))



@app.route('/Logout')
def logout():
    session.pop('isloggedin', None)
    return redirect(url_for('index'))



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
    create_stat_table()
    app.run(debug=True)
    



