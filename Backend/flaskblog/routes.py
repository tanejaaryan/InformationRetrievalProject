from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.script import func, func1, func2
import pandas as pd
 
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

@app.route('/result/result')
def analysis(x):
    return render_template("result.html",name="result", data=x.to_html())

@app.route("/general")
@app.route('/general', methods=['GET','POST'])
def general():
    code = None
    name = None
    if request.method == 'POST':
        code = request.form['ByCode']
        name = request.form['By_Name']
        print(code + name)
        df = func1(code)
        print(name)
        df1 = func2(name)
        int_df = pd.DataFrame()
        print(df)
        print(df1)
        if len(code) != 0 and len(name) != 0:
            int_df = pd.merge(df1, df, how ='inner', on =df.columns)
        elif len(code) != 0:
            int_df = df
        else:
            int_df = df1
        print(df)
        return analysis(int_df)
    return render_template('general.html', title='general')



@app.route("/about")
@app.route('/about', methods=['GET','POST'])
def about():
    branch = []
    level = []
    credits = []
    interests = None
    prev_courses = None
    #exclude = None
    major_comp = None
    minor_comp = None
    if request.method == 'POST':
        print("segrfd")
        branch = request.form.getlist('Branch')
        level = request.form.getlist('Level')
        credits = request.form.getlist('Credits')
        interests = request.form['Interests']
        prev_courses = request.form['PreviousCourses']
        #exclude = request.form['Exclude_Topics']
        m = request.form.getlist('Majority')
        if len(m) > 0:
            major_comp = m[0]
        m = request.form.getlist('Minority')
        if len(m) > 0:
            minor_comp = m[0]
    #return render_template('about.html', recommendation=func(""))

        df = func(branch, interests, major_comp, minor_comp, level, prev_courses, credits)
        print(df)
        return analysis(df)
        #return render_template('about.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
    return render_template('about.html', title='about')

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
