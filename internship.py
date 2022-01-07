from flask import Flask,render_template, redirect, url_for, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ILUVTOFART'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskapp'


mysql = MySQL(app)

@app.route("/user/<int:id>")
def user(id):
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM student_data WHERE id = %s""", (id))
    user = cur.fetchone()
    return render_template('webbrowser.html', user = user)
