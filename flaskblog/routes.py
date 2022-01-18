from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
posts = [
    {
        'author': 'luhuhu',
        'content': 'first content', 
        'title': 'first blog',
        'date':'2021-12-19'
    }, 

    {
        'author': 'xiaoerbao', 
        'content': 'second content',
        'title':'dummy second blog',
        'date':'2021-12-20'
    }
] 


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts, title="home")

@app.route('/about')
def about(): 
    return render_template('about.html', title="about")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit(): 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account create for {form.username.data}! Now you can login :)', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="register", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit(): 
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'You have logged in, welcome back :)', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else: 
            flash(f'Unsuccessful, please check email and password', 'danger')
    return render_template('login.html', title="login", form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash(f'You have logged out', 'info')
    return redirect(url_for('home'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account(): 
    form = UpdateAccountForm()
    img = url_for('static', filename=f'profile_img/{current_user.image_file}')
    if form.validate_on_submit(): 
        current_user.username = form.username.data 
        current_user.email = form.email.data 
        db.session.commit()
    elif request.method == 'GET': 
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title="Account", image_file=img, form=form)

