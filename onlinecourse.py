from flask import Flask, render_template, flash, redirect, url_for, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
import urllib.request
from werkzeug.utils import secure_filename
import os


onlinecourse = Blueprint("onlinecourse",__name__,static_folder="static",template_folder="templates")

app = Flask("Student Activity Management")
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/flaskapp"
app.config['SECRET_KEY'] = 'swetha'

UPLOAD_FOLDER = 'C:/Users/sweth/PycharmProjects/flaskProject1/static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


db = SQLAlchemy(app)


class onlinecourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    rollno = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True)
    year = db.Column(db.Integer, index=True)
    department = db.Column(db.String(50), index=True)
    coursename = db.Column(db.String(120), index=True)
    organizer = db.Column(db.String(120), index=True)
    duration = db.Column(db.Integer, index=True)
    fromdate = db.Column(db.Date, index=True)
    todate = db.Column(db.Date, index=True)
    score = db.Column(db.Float, index=True)
    drive = db.Column(db.String(300), index=True)
    proof = db.Column(db.String(150))



@app.route('/')
def course():
    return render_template('course.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['proof']
    st_name = request.form['name']
    st_rollno = request.form['rollno']
    st_email = request.form['email']
    st_year = request.form['year']
    st_department = request.form['department']
    st_coursename = request.form['coursename']
    st_organizer = request.form['organizer']
    st_duration = request.form['duration']
    st_fromdate = request.form['fromdate']
    st_todate = request.form['todate']
    st_score = request.form['score']
    st_drive = request.form['drive']
    filename = secure_filename(file.filename)

    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        newFile = onlinecourse(proof=file.filename, name=st_name, rollno=st_rollno,email=st_email,year=st_year,department=st_department, coursename=st_coursename, organizer=st_organizer, duration=st_duration, fromdate= st_fromdate, todate=st_todate, score=st_score, drive=st_drive)
        db.session.add(newFile)
        db.session.commit()
        flash('File successfully uploaded ' + file.filename )
        return redirect('/')
    else:
        flash('Invalid Upload only txt, pdf, png, jpg, jpeg, gif')
    return redirect('/')



