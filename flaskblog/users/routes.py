from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt, app
from flaskblog.models import User, Post
from flaskblog.users.forms import *
from flaskblog.users.utils import save_picture, send_reset_email

import os

users = Blueprint('users', __name__)
profile_root_path = os.path.join(app.root_path, 'static/profile_img')

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit(): 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=form.email.data).first()
        user_profile_path = os.path.join(profile_root_path, str(user.id))
        default_img_path = os.path.join(profile_root_path, 'default.png')
        default_img_path_user = os.path.join(user_profile_path, 'default.png')
        os.mkdir(user_profile_path)
        #print(f'copy {default_img_path} {default_img_path_user}')
        #os.system(f'copy {default_img_path} {default_img_path_user}')
        flash(f'Account create for {form.username.data}! Now you can login :)', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title="register", form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit(): 
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'You have logged in, welcome back :)', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else: 
            flash(f'Unsuccessful, please check email and password', 'danger')
    return render_template('login.html', title="login", form=form)

@users.route('/logout')
def logout():
    logout_user()
    flash(f'You have logged out', 'info')
    return redirect(url_for('main.home'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account(): 
    form = UpdateAccountForm()
    if form.validate_on_submit(): 
        if form.picture.data: 
            pic_fn = save_picture(form.picture.data)
            current_user.image_file = pic_fn
        current_user.username = form.username.data 
        current_user.email = form.email.data 
        db.session.commit()
    elif request.method == 'GET': 
        form.username.data = current_user.username
        form.email.data = current_user.email
    #user_profile_img_fn = os.path.join('profile_img', str(current_user.id), current_user.image_file)
    user_profile_img_fn = 'profile_img/' + str(current_user.id) + '/' + current_user.image_file
    if current_user.image_file == "default.png":
        #user_profile_img_fn = os.path.join('profile_img', 'default.png')
        user_profile_img_fn = 'profile_img/' + 'default.png'
    print(user_profile_img_fn)
    img = url_for('static', filename=user_profile_img_fn)
    print(img)
    return render_template('account.html', title="Account", image_file=img, form=form)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request(): 
    if current_user.is_authenticated: 
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit(): 
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent, please check your mailbox", "info")

    return render_template('reset_request.html', form=form, title='Reset Password')

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated: 
        return redirect(url_for('main.home'))
    
    user = User.verify_reset_token(token)
    if user is None: 
        flash('This is an invalid and expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit(): 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password 
        db.session.commit() 
        flash(f'Account create for {form.username.data}! Now you can login :)', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', form=form, title='Reset Password')

@users.route('/home/<string:username>')
def user_post(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)