from flask import Flask, render_template, flash, redirect, url_for, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
import urllib.request
from werkzeug.utils import secure_filename
import os

project= Blueprint("project",__name__,static_folder="static",template_folder="templates")

app = Flask("Student Activity Management")
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/flaskapp"

UPLOAD_FOLDER = 'C:/Users/sweth/PycharmProjects/flaskProject1/static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'swetha'

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


db = SQLAlchemy(app)

class project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True)
    rollno = db.Column(db.String(20), index=True)
    email = db.Column(db.String(120), index=True)
    year = db.Column(db.Integer, index=True)
    department = db.Column(db.String(50), index=True)
    title = db.Column(db.String(150), index=True)
    event= db.Column(db.String(150), index=True)
    organizer = db.Column(db.String(150), index=True)
    level = db.Column(db.String(50), index=True)
    students = db.Column(db.Integer, index=True)
    from_date =db.Column(db.Date, index=True)
    to_date = db.Column(db.Date, index=True)
    status = db.Column(db.String(50), index=True)
    drive = db.Column(db.String(300), index=True)
    proof = db.Column(db.String(150))



@app.route('/')
def projects():
    return render_template('project.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['proof']
    st_name = request.form['name']
    st_rollno = request.form['rollno']
    st_email = request.form['email']
    st_year = request.form['year']
    st_department = request.form['department']
    st_title = request.form['title']
    st_event = request.form['event']
    st_organizer = request.form['organizer']
    st_level = request.form['level']
    st_students = request.form['students']
    st_from_date = request.form['to_date']
    st_to_date = request.form['from_date']
    st_status = request.form['status']
    st_drive = request.form['drive']
    filename = secure_filename(file.filename)

    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        newFile = project(proof=file.filename, name=st_name, rollno=st_rollno,email=st_email, year=st_year, department=st_department,
                         title=st_title, event=st_event, organizer=st_organizer, level=st_level, students=st_students,
                         from_date=st_from_date, to_date=st_to_date, status=st_status,drive=st_drive)
        db.session.add(newFile)
        db.session.commit()
        flash('File successfully uploaded ' + file.filename)
        return redirect('/')
    else:
        flash('Invalid Upload only txt, pdf, png, jpg, jpeg, gif')
    return redirect('/')




