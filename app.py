from flask import Flask, jsonify,request, session,render_template, redirect, url_for,flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database connection
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='flask-app-mysql-server.mysql.database.azure.com',
            user='dbadmin',
            password='Linga@12#',
            database='userdata'
        )
        
    except Error as e:
        pass
    return connection 

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred") 
        
create_feedback_table = """
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    rating INT CHECK (rating >= 0 AND rating <= 5),
    review TEXT NOT NULL
);
"""


create_statistics_table="""
CREATE TABLE IF NOT EXISTS statistics (
  
    date DATE NOT NULL,
    outpatients INT NOT NULL,
    medicine_prescribed INT NOT NULL,
    opticals_prescribed INT NOT NULL,
    surgeries_performed INT NOT NULL,
    free_surgeries_performed INT NOT NULL,
    cataract_male INT NOT NULL,
    cataract_female INT NOT NULL,
    cornea_male INT NOT NULL,
    cornea_female INT NOT NULL,
    retina_male INT NOT NULL,
    retina_female INT NOT NULL,
    orbit_male INT NOT NULL,
    orbit_female INT NOT NULL
);
"""







@app.route('/')
def index():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM reviews')
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
    conn = create_connection()
    cur = conn.cursor()
    
    cur.execute(''' SELECT 
        (SELECT MAX(date) FROM statistics) AS last_date,
        SUM(outpatients) AS total_outpatients,
        SUM(medicine_prescribed) AS total_medicine_prescribed,
        SUM(opticals_prescribed) AS total_opticals_prescribed,
        
        SUM(surgeries_performed) AS total_surgeries_performed,
        SUM(free_surgeries_performed) AS total_free_surgeries_performed,
        SUM(cataract_male) AS total_cataract_male,
        SUM(cataract_female) AS total_cataract_female,
       
        SUM(cornea_male) AS total_cornea_male,
        SUM(cornea_female) AS total_cornea_female,
        SUM(retina_male) AS total_retina_male,
        SUM(retina_female) AS total_retina_female,
        SUM(orbit_male) AS total_orbit_male,
        SUM(orbit_female) AS total_orbit_female
    FROM statistics;''')  
  
    results = cur.fetchone()
    results=list(results)
    
    results[0]=results[0].strftime('%d %B %Y')
  
    return render_template('data.html',stats=results)


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
    if request.method=="POST":
        return redirect(url_for('index'))
        
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
            session['isloggedin']=True
            return redirect(url_for('updates'))
        else:
            return render_template('login.html')

    return render_template('login.html')

@app.route('/updates', methods=['GET', 'POST'])
def updates():
    if request.method == 'POST':
        
        date= request.form['date-of-updation']
        outpatients = request.form['outpatients-treated']
        medicine_prescribed = request.form['medicines-prescribed']
        opticals_prescribed = request.form['optical-prescribed']
        surgeries_performed = request.form['surgeries-prescribed']
        free_surgeries_performed=request.form['free-surgeries-prescribed']
        cataract_male = request.form['cataract-male']
        cataract_female = request.form['cataract-female']
        cornea_male = request.form['cornea-male']
        cornea_female = request.form['cornea-female']
        retina_male = request.form['retina-male']
        retina_female = request.form['retina-female']
        orbit_male = request.form['orbit-male']
        orbit_female = request.form['orbit-female']

        conn = create_connection()
        cur = conn.cursor()
        cur.execute('''
    INSERT INTO statistics (
        date, outpatients, medicine_prescribed, opticals_prescribed,
        surgeries_performed, free_surgeries_performed, cataract_male, 
        cataract_female, cornea_male, cornea_female, retina_male, 
        retina_female, orbit_male, orbit_female
    ) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); '''
, (
    date, outpatients, medicine_prescribed, opticals_prescribed,
    surgeries_performed, free_surgeries_performed, cataract_male,
    cataract_female, cornea_male, cornea_female, retina_male,
    retina_female, orbit_male, orbit_female )) 

        conn.commit()
        cur.close()
        conn.close()
        flash('Successfully updated')
        return redirect(url_for('index'))

    return render_template('updates.html')


@app.route('/review', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        rating = request.form['rate']
        review = request.form['review']


        # Insert data into database
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO reviews (name, email, rating, review) VALUES (%s, %s, %s, %s);
        ''', (name, email, rating, review))
        conn.commit()
        cur.close()
        conn.close()
        flash('Thank you for your feedback!')
        return redirect(url_for('index'))

    return render_template('reviewform.html')

@app.route('/Logout')
def logout():
    session.pop('isloggedin', None)
  
    return redirect(url_for('index'))



if __name__ == '__main__':
    connection=create_connection()
    execute_query(connection, create_statistics_table)
    execute_query(connection, create_feedback_table)
    connection.close()
    app.run(debug=True)
