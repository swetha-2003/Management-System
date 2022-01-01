import os
import pathlib

import mysql
import requests
from flask import Flask, session, abort, redirect, flash, url_for
from flask_mysqldb import MySQL
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
from flask import request
from flask import render_template
from sqlalchemy import create_engine, Column, Integer, String, Date, exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy


Base = declarative_base()

app = Flask("Student Activity Management")
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/flaskapp"
app.secret_key = "studentactivitymanagement"
UPLOAD_FOLDER = 'C:/Users/sweth/PycharmProjects/flaskProject1/static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


engine = create_engine("mysql://root:@localhost/flaskapp",echo = False)
engine.connect()
con=engine.connect()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    username = Column(String(20))
    password = Column(String(20))



os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "528892848344-q72f3aqpihjdu0j3rdrcktjspf50n06o.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

Session = sessionmaker(bind=engine)
s = Session()

db = SQLAlchemy(app)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()
    return wrapper

@app.route('/register', methods=['POST'])
def register():
    username = str(request.form['username'])
    password = str(request.form['password'])

    query = s.query(Users).filter(Users.username==username, Users.password==password)
    result = query.first()
    if result:
        session['logged_in'] = True
        return render_template("mainpage.html")
    else:
        return render_template("login.html")


@app.route('/login')
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)



@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    if ((id_info.get("email").endswith('@bitsathy.ac.in'))==True):
        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        session["email"] = id_info.get("email")
        return redirect("/protected_area")
    else:
        return redirect("/loginpage")



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/home")


@app.route('/')
def index():
    return redirect("/home")


@app.route('/protected_area')
@login_is_required
def protected_area():
    return render_template("mainpage.html")

@app.route('/back')
def back():
    return render_template("mainpage.html")

@app.route('/projects')
def projects():
    return render_template("project.html")

@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/loginpage')
def loginpage():
    return render_template("login.html")

@app.route('/paper_presentation')
def paper_presentation():
    return render_template("paper_presentation.html")

@app.route('/paper_publication')
def paper_publication():
    return render_template("paper_publication.html")

@app.route('/patents')
def patents():
    return render_template("patent.html")



@app.route('/product')
def product():
    return render_template("product.html")

@app.route('/course')
def course():
    return render_template("course.html")


@app.route('/intern')
def intern():
    return render_template("internship.html")



class Internship(db.Model):

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(30), index=True)
        rollno = db.Column(db.String(20), index=True, unique=True)
        email = db.Column(db.String(150), index=True)
        year = db.Column(db.Integer, index=True)
        department = db.Column(db.String(50), index=True)
        industryname = db.Column(db.String(150), index=True)
        website = db.Column(db.String(200))
        address = db.Column(db.String(200))
        duration = db.Column(db.String(50))
        fromdate = db.Column(db.Date)
        todate = db.Column(db.Date)
        drive = db.Column(db.String(300))
        proof = db.Column(db.String(150))

@app.route('/upload', methods=['POST'])
def upload_internship():

    st_name = request.form['name']
    st_rollno = request.form['rollno']
    st_email = request.form['email']
    st_year = request.form['year']
    st_department = request.form['department']
    st_industryname = request.form['industryname']
    st_website = request.form['website']
    st_address = request.form['address']
    st_duration = request.form['duration']
    st_fromdate = request.form['fromdate']
    st_todate = request.form['todate']
    st_drive = request.form['drive']
    file = request.files['proof']
    filename = secure_filename(file.filename)

    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))



        new_internship = Internship( name=st_name, rollno=st_rollno,email=st_email,year=st_year,department=st_department,industryname=st_industryname,website=st_website,address=st_address,duration=st_duration, fromdate= st_fromdate, todate=st_todate,drive=st_drive,proof=file.filename)
        db.session.add(new_internship)
        db.session.commit()
        flash('File successfully uploaded ' + file.filename)
        return redirect('/intern')
    else:
        flash('Invalid Upload only txt, pdf, png, jpg, jpeg, gif')
        return redirect('/intern')



class paperpresentation(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True)
    rollno = db.Column(db.String(20), index=True)
    email = db.Column(db.String(150), index=True)
    year = db.Column(db.Integer, index=True)
    department = db.Column(db.String(50), index=True)
    title = db.Column(db.String(150))
    event = db.Column(db.String(150))
    organizer = db.Column(db.String(150))
    level = db.Column(db.String(50))
    students = db.Column(db.Integer)
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)
    status = db.Column(db.String(50))
    drive = db.Column(db.String(300))
    proof = db.Column(db.String(150))


@app.route('/upload_pp', methods=['POST'])
def upload_pp():
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

        new_pp = paperpresentation(proof=file.filename, name=st_name, rollno=st_rollno, email=st_email, year=st_year,
                                    department=st_department,
                                    title=st_title, event=st_event, organizer=st_organizer, level=st_level,
                                    students=st_students,
                                    from_date=st_from_date, to_date=st_to_date, drive=st_drive, status=st_status)

        db.session.add(new_pp)
        db.session.commit()
        flash('File successfully uploaded ' + file.filename)
        return redirect('/paper_presentation')
    else:
        flash('Invalid Upload only txt, pdf, png, jpg, jpeg, gif')
        return redirect('/paper_presentation')

class publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True)
    rollno = db.Column(db.String(20), index=True)
    email = db.Column(db.String(150), index=True)
    year = db.Column(db.Integer, index=True)
    department = db.Column(db.String(50), index=True)
    title = db.Column(db.String(150))
    journal = db.Column(db.String(150))
    publisher = db.Column(db.String(150))
    students = db.Column(db.Integer)
    submission_date = db.Column(db.Date)
    publication_date = db.Column(db.Date)
    index = db.Column(db.String(50))
    details = db.Column(db.String(300))
    drive = db.Column(db.String(300))
    proof = db.Column(db.String(150))


@app.route('/upload_publication', methods=['POST'])
def upload_publication():
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

        new_publication = publication(proof=file.filename, name=st_name, rollno=st_rollno, email=st_email,year=st_year, department=st_department,
                        title=st_title, journal=st_journal, publisher=st_publisher, students=st_students,
                         submission_date=st_submission_date, publication_date=st_publication_date, index=st_index,details=st_details,drive=st_drive)

        db.session.add(new_publication)
        db.session.commit()
        flash('File successfully uploaded ' + file.filename)
        return redirect('/paper_publication')
    else:
        flash('Invalid Upload only txt, pdf, png, jpg, jpeg, gif')
        return redirect('/paper_publication')

class project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True)
    rollno = db.Column(db.String(20), index=True)
    email = db.Column(db.String(120), index=True)
    year = db.Column(db.Integer, index=True)
    department = db.Column(db.String(50), index=True)
    title = db.Column(db.String(150), index=True)
    event = db.Column(db.String(150), index=True)
    organizer = db.Column(db.String(150), index=True)
    level = db.Column(db.String(50), index=True)
    students = db.Column(db.Integer, index=True)
    from_date = db.Column(db.Date, index=True)
    to_date = db.Column(db.Date, index=True)
    status = db.Column(db.String(50), index=True)
    drive = db.Column(db.String(300), index=True)
    proof = db.Column(db.String(150))

@app.route('/upload_project', methods=['POST'])
def upload_project():
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

        new_project = project(proof=file.filename, name=st_name, rollno=st_rollno,email=st_email, year=st_year, department=st_department,
                         title=st_title, event=st_event, organizer=st_organizer, level=st_level, students=st_students,
                         from_date=st_from_date, to_date=st_to_date, status=st_status,drive=st_drive)

        db.session.add(new_project)
        db.session.commit()
        flash('File successfully uploaded ' + file.filename)
        return redirect('/projects')
    else:
        flash('Invalid Upload only txt, pdf, png, jpg, jpeg, gif')
        return redirect('/projects')

class product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True)
    rollno = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(150), index=True)
    year = db.Column(db.Integer, index=True)
    department = db.Column(db.String(150), index=True)
    product_name = db.Column(db.String(300), index=True)
    category= db.Column(db.String(100), index=True)
    fund_amount = db.Column(db.Float, index=True)
    apex = db.Column(db.String(200), index=True)
    commercialized = db.Column(db.String(20), index=True)
    drive = db.Column(db.String(300), index=True)
    proof = db.Column(db.String(150))

@app.route('/upload_product', methods=['POST'])
def upload_product():
    file = request.files['proof']
    st_name = request.form['name']
    st_rollno = request.form['rollno']
    st_email = request.form['email']
    st_year = request.form['year']
    st_department = request.form['department']
    st_product_name = request.form['product_name']
    st_category = request.form['category']
    st_fund_amount = request.form['fund_amount']
    st_apex = request.form['apex']
    st_commercialized = request.form['commercialized']
    st_drive = request.form['drive']
    filename = secure_filename(file.filename)

    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_product = product(proof=file.filename, name=st_name, rollno=st_rollno,email=st_email, year=st_year, department=st_department,
                          product_name= st_product_name, category=st_category, fund_amount=st_fund_amount, apex=st_apex, commercialized=st_commercialized,
                         drive=st_drive)

        db.session.add(new_product)
        db.session.commit()
        flash('File successfully uploaded ' + file.filename)
        return redirect('/product')
    else:
        flash('Invalid Upload only txt, pdf, png, jpg, jpeg, gif')
    return redirect('/product')

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

@app.route('/upload_patent', methods=['POST'])
def upload_patent():
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

        new_patent=patent(proof=file.filename, name=st_name, rollno=st_rollno, email=st_email ,year=st_year,department=st_department,  idea=st_idea , title=st_title, app_number=st_app_number, level=st_level, students=st_students,reg_date=st_reg_date,approved_date=st_approved_date,  status= st_status, drive=st_drive)
        db.session.add(new_patent)
        db.session.commit()
        flash('File successfully uploaded ' + file.filename)
        return redirect('/patents')
    else:
        flash('Invalid Upload only txt, pdf, png, jpg, jpeg, gif')
        return redirect('/patents')

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

@app.route('/upload_course', methods=['POST'])
def upload_course():
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

        new_course = onlinecourse(proof=file.filename, name=st_name, rollno=st_rollno, email=st_email, year=st_year,
                               department=st_department, coursename=st_coursename, organizer=st_organizer,
                               duration=st_duration, fromdate=st_fromdate, todate=st_todate, score=st_score,
                               drive=st_drive)

        db.session.add(new_course)
        db.session.commit()
        flash('File successfully uploaded ' + file.filename)
        return redirect('/course')
    else:
        flash('Invalid Upload only txt, pdf, png, jpg, jpeg, gif')
        return redirect('/course')


@app.route('/fetchs')
def fetchs():
    Email = session["email"]
    data = onlinecourse.query.all()
    Email1 = onlinecourse.query.filter_by(email=Email)

    if (Email1):
         return render_template('webbrowser.html', data=Email1)
    else:
        message="No Data to Display"
        return render_template('webbrowser.html', message=message)
    #

if __name__ == '__main__':
    app.run(debug=True)

