from flask import Flask, render_template, flash, request, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import psycopg2
from models import User, Image, db,  Appoint

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']
app.config['UPLOAD_PATH'] = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = 'static/uploads'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.config['SECRET_KEY'] = 'thisismysecretkeydonotstealit'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dhari3@localhost/users'
db = SQLAlchemy(app)

con = psycopg2.connect(database="users", user="postgres", password="dhari3", host="127.0.0.1", port="5432")
cursor = con.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def product():
    return render_template('products.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/signup')
def newhome():
    return render_template('signup.html')



@app.route('/appointment')
def appoint():
    return render_template('appointment.html')


@app.route('/form')
def form():
    return render_template('form.html')


# Registration form
@app.route('/signup', methods=['POST'])
def signup_post():
    Hid = request.form.get('Hid')
    Hemail = request.form.get('Hemail')
    Hname = request.form.get('Hname')
    Password = request.form.get('Password')
    user = User.query.filter_by(Hid=Hid).first()
    password = User.query.filter_by(Password=Password).first()
    if user:
        flash('HID  already exists.')
        return render_template('signup.html')
    if password:
        flash('Password already exist')
        return render_template('signup.html')
    if user and password:
        flash('Hid and Password already exist')
        return render_template('signup.html')

    new_user = User(Hemail=Hemail, Hid=Hid, Hname=Hname, Password=Password)

    db.session.add(new_user)
    db.session.commit()

    return render_template('login.html')


# login form
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    Hid = request.form.get('Hid')
    Hname = request.form.get('Hname')
    Password = request.form.get('Password')
    password = User.query.filter_by(Password=Password).first()
    user = User.query.filter_by(Hid=Hid, Hname=Hname).first()

    if not user:
        flash('Invalid Hospital Id')
        return render_template('login.html')
    if not password:
        flash('Invalid Password')
        return render_template('login.html')
    if not user or not password:
        flash('Invalid Hospital Id and Password')
        return render_template('login.html')
    return render_template('home.html')

#patient intake form
class Formm(db.Model):
    __tablename__ = 'formm'
    id = db.Column(db.Integer, primary_key=True)
    Hid=db.Column(db.String(40), nullable=False)
    Pname = db.Column(db.String(40), nullable=False)
    Pemail = db.Column(db.String(40), unique=True)
    Dob = db.Column(db.String(40),  nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Height = db.Column(db.String(40), nullable=False)
    Weight = db.Column(db.String(40), nullable=False)
    Bp= db.Column(db.String(40), nullable=False)
    Sugar= db.Column(db.String(40), nullable=False)
    Mdate= db.Column(db.String(40), nullable=False)
    Pexp= db.Column(db.String(4000), nullable=False)
    Protocol= db.Column(db.String(4000), nullable=False)


def __init__(self, Hid, Pname, Pemail, Dob, Age, Height, Weight, Bp, Sugar, Mdate, Pexp, Protocol):
    self.Hid = Hid
    self.Pname = Pname
    self.Pemail = Pemail
    self.Dob = Dob
    self.Age = Age
    self.Height = Height
    self.Weight =Weight
    self.Bp = Bp
    self.Sugar = Sugar
    self.Mdate = Mdate
    self.Pexp = Pexp
    self. Protocol=Protocol

# patient intake form
@app.route('/form', methods=['POST', 'GET'])
def form_fill():
    Hid = request.form.get('Hid')
    Pname = request.form.get('Pname')
    Pemail = request.form.get('Pemail')
    Dob = request.form.get('Dob')
    Age = request.form.get('Age')
    Height = request.form.get('Height')
    Weight = request.form.get('Weight')
    Bp = request.form.get('Bp')
    Sugar = request.form.get('Sugar')
    Mdate = request.form.get('Mdate')
    Pexp = request.form.getlist('Pexp')
    Protocol = request.form.getlist('Protocol')
    new_formm = Formm(Hid=Hid, Pname=Pname, Pemail=Pemail, Dob=Dob, Age=Age, Height=Height, Weight=Weight, Bp=Bp,
                    Sugar=Sugar, Mdate=Mdate, Pexp=Pexp, Protocol=Protocol)
    db.session.add(new_formm)
    db.session.commit()

    return render_template('form.html')

# Process
@app.route('/process')
def process():
    return render_template('process.html')

@app.route('/process', methods=['POST'])
def upload():
    Hid = request.form.get('Hid')
    Pname = request.form.get('Pname')
    file = request.files['file']
    filename = secure_filename(file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        new_form = Image(Hid=Hid, Pname=Pname)
        db.session.add(new_form)
        db.session.commit()
        file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('Image successfully uploaded and displayed below')
        return render_template('process.html', filename=filename)
    return render_template('process.html')

# Appointment
@app.route('/appoint', methods=['POST', 'GET'])
def appoint_fill():
    Hid = request.form.get('Hid')
    Pname = request.form.get('Pname')
    Pdate = request.form.get('Pdate')
    Ptime = request.form.get('Ptime')
    Pcontact = request.form.get('Pcontact')
    new_appoint = Appoint(Hid=Hid, Pname=Pname, Pcontact=Pcontact, Pdate=Pdate, Ptime=Ptime)
    db.session.add(new_appoint)
    db.session.commit()
    return render_template('appointment.html')


@app.route('/upload')
def upload_form():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    Hid = request.form.get('Hid')
    Pname = request.form.get('Pname')
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        print('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload_image filename: ' + filename)
        print('Image successfully uploaded and displayed below')
        new_form = Image(Hid=Hid, Pname=Pname)
        db.session.add(new_form)
        db.session.commit()
        return render_template('upload.html', filename=filename)
    else:
        print('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/upload', methods=['GET','POST'])
def display_image(filename):
    print('display_image filename: ' + filename)
    return render_template('upload.html', filename=filename)

# report page
@app.route('/reports')
def report():
    return render_template('report.html')

class Report(db.Model):
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True)
    standard= db.Column(db.String(4000),nullable=False)
    Pname= db.Column(db.String(100),nullable=False)
    Page= db.Column(db.String(100),nullable=False)
    stage= db.Column(db.String(100),nullable=False)
    report=db.Column(db.String(100),nullable=False)

def __init__(self, standard, Pname, Page, stage,report):
    self.standard = standard
    self.Pname = Pname
    self.Page = Page
    self.stage = stage
    self.report = report


# Report
stagel=['STAGE1','STAGE2','STAGE3','STAGE4']
@app.route('/reports',methods=['GET','POST'])
def report_form():
    standard = request.form.get('standard')
    Pname = request.form.get('Pname')
    Page = request.form.get('Page')
    stage = request.form.get('stage')
    report = request.form.get('report')

    new_standard = Report(standard=standard, Pname=Pname, Page=Page, stage=stage, report=report)
    db.session.add(new_standard)
    db.session.commit()
    return render_template('report.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


# Patient report record
@app.route('/profilerep')
def profile_rep():
        cursor.execute("SELECT * FROM report")
        data = cursor.fetchall()
        return render_template('profilerep.html', data=data)

# Patient details record
@app.route('/profiledetail')
def profile_detail():
        cursor.execute("SELECT * FROM formm")
        detail = cursor.fetchall()
        return render_template('profiledetail.html', data=detail)

#patient new upload and report
@app.route('/details')
def upload_newform():
    return render_template('details.html')


@app.route('/details', methods=['POST'])
def upload_newimage():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        result = request.form
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Click the preview button to view the uploaded thermal image')
        return render_template('uploaded.html', filename=filename, result=result)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/details/display/<filename>')
def display_newimage(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/details')
def detail_newform():
    return render_template('details.html')

if __name__ == '__main__':
    app.run(debug=True)
