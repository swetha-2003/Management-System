from flask import Flask, render_template, flash, redirect, url_for, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
import urllib.request
from werkzeug.utils import secure_filename
import os

publication= Blueprint("paper_publication",__name__,static_folder="static",template_folder="templates")

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

class publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True)
    rollno = db.Column(db.String(20), index=True)
    email = db.Column(db.String(150), index=True)
    year = db.Column(db.Integer, index=True)
    department = db.Column(db.String(50), index=True)
    title = db.Column(db.String(150), index=True)
    journal = db.Column(db.String(150), index=True)
    publisher = db.Column(db.String(150), index=True)
    students = db.Column(db.Integer, index=True)
    submission_date = db.Column(db.Date, index=True)
    publication_date = db.Column(db.Date, index=True)
    index = db.Column(db.String(50), index=True)
    details = db.Column(db.String(300), index=True)
    drive = db.Column(db.String(300), index=True)
    proof = db.Column(db.String(150))

@app.route('/')
def paper_publication():
    return render_template('paper_publication.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['proof']
    st_name = request.form['name']
    st_rollno = request.form['rollno']
    st_email = request.form['email']
    st_year = request.form['year']
    st_department = request.form['department']
    st_title = request.form['title']
    st_journal = request.form['journal']
    st_publisher = request.form['publisher']
    st_students = request.form['students']
    st_submission_date = request.form['submission_date']
    st_publication_date = request.form['publication_date']
    st_index = request.form['index']
    st_details = request.form['details']
    st_drive = request.form['drive']
    filename = secure_filename(file.filename)

    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        newFile = publication(proof=file.filename, name=st_name, rollno=st_rollno, email=st_email,year=st_year, department=st_department,
                        title=st_title, journal=st_journal, publisher=st_publisher, students=st_students,
                         submission_date=st_submission_date, publication_date=st_publication_date, index=st_index,details=st_details,drive=st_drive)
        db.session.add(newFile)
        db.session.commit()
        flash('File successfully uploaded ' + file.filename)
        return redirect('/')
    else:
        flash('Invalid Upload only txt, pdf, png, jpg, jpeg, gif')
    return redirect('/')