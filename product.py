from flask import Flask, render_template, flash, redirect, url_for, request, Blueprint
from flask_sqlalchemy import SQLAlchemy
import urllib.request
from werkzeug.utils import secure_filename
import os

product= Blueprint("product",__name__,static_folder="static",template_folder="templates")

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

@app.route('/')
def products():
    return render_template('product.html')

@app.route('/upload', methods=['POST'])
def upload():
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

        newFile = product(proof=file.filename, name=st_name, rollno=st_rollno,email=st_email, year=st_year, department=st_department,
                          product_name= st_product_name, category=st_category, fund_amount=st_fund_amount, apex=st_apex, commercialized=st_commercialized,
                         drive=st_drive)
        db.session.add(newFile)
        db.session.commit()
        flash('File successfully uploaded ' + file.filename)
        return redirect('/')
    else:
        flash('Invalid Upload only txt, pdf, png, jpg, jpeg, gif')
    return redirect('/')
