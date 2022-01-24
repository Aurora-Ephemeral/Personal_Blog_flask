from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User 

class RegistrationForm(FlaskForm): 
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                        validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def vaildate_username(self, username): 
        user = User.query.filter_by(username=username.data).first()
        if user: 
            raise ValidationError('This username is taken. Please choose a different name')

    def vaildate_email(self, email): 
        user = User.query.filter_by(email=email.data).first()
        if user: 
            raise ValidationError('This email is taken. Please choose a different email')
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                        validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')

class UpdateAccountForm(FlaskForm): 
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Your Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def vaildate_username(self, username): 
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user: 
                raise ValidationError('This username is taken. Please choose a different name')

    def vaildate_email(self, email): 
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user: 
                raise ValidationError('This email is taken. Please choose a different email')  