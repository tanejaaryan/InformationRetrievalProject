from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.script import func
 
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
@app.route('/home', methods=['POST'])
def my_form_post():
    variable = request.form['variable']
    output = func(variable)
    return render_template('home.html', output = output)

@app.route("/general")
@app.route('/general', methods=['GET','POST'])
def general():
    code = None
    name = None
    if request.method == 'POST':
        code = request.form['ByCode']
        name = request.form['By_Name']
        print(code + name)
    return render_template('general.html', title='general')

@app.route("/about")
@app.route('/about', methods=['GET','POST'])
def about():
    branch = []
    level = []
    interests = None
    exclude = None
    major_comp = []
    minor_comp = []
    if request.method == 'POST':
        branch = request.form.getlist('Branch')
        level = request.form.getlist('Level')
        interests = request.form['Interests']
        exclude = request.form['Exclude_Topics']
        major_comp = request.form.getlist('Majority')
        minor_comp = request.form.getlist('Minority')
        #print(major_comp)
        #print(minor_comp)
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')