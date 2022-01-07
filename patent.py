from flask import Flask, render_template, flash, redirect, url_for, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
import urllib.request
from werkzeug.utils import secure_filename
import os

patent= Blueprint("patent",__name__,static_folder="static",template_folder="templates")

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

class patent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True)
    rollno = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(150), index=True)
    year = db.Column(db.Integer, index=True)
    department = db.Column(db.String(50), index=True)
    idea = db.Column(db.String(150), index=True)
    title = db.Column(db.String(150), index=True)
    app_number = db.Column(db.String(150), index=True)
    level = db.Column(db.String(50), index=True)
    students = db.Column(db.Integer, index=True)
    reg_date =db.Column(db.Date, index=True)
    approved_date = db.Column(db.Date, index=True)
    status = db.Column(db.String(50), index=True)
    drive = db.Column(db.String(300), index=True)
    proof = db.Column(db.String(150))



@app.route('/')
def patents():
    return render_template('patent.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['proof']
    st_name = request.form['name']
    st_rollno = request.form['rollno']
    st_email = request.form['email']
    st_year = request.form['year']
    st_department = request.form['department']
    st_idea = request.form['idea']
    st_title = request.form['title']
    st_app_number = request.form['app_number']
    st_level = request.form['level']
    st_students = request.form['students']
    st_reg_date = request.form['reg_date']
    st_approved_date = request.form['approved_date']
    st_status = request.form['status']
    st_drive = request.form['drive']
    filename = secure_filename(file.filename)

    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        newFile = patent(proof=file.filename, name=st_name, rollno=st_rollno, email=st_email ,year=st_year,department=st_department,  idea=st_idea , title=st_title, app_number=st_app_number, level=st_level, students=st_students,reg_date=st_reg_date,approved_date=st_approved_date,  status= st_status, drive=st_drive)
        db.session.add(newFile)
        db.session.commit()
        flash('File successfully uploaded ' + file.filename )
        return redirect('/')
    else:
        flash('Invalid Upload only txt, pdf, png, jpg, jpeg, gif')
    return redirect('/')




