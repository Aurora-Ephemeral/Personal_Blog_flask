import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from flaskblog import mail, app
from flask_login import current_user
with app.app_context():
    profile_root_path = os.path.join(app.root_path, 'static/profile_img')
def save_picture(form_picture): 
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    pic_fn = random_hex + f_ext
    pic_path = os.path.join(profile_root_path, str(current_user.id), pic_fn)
    form_picture.save(pic_path)
    return pic_fn

def send_reset_email(user): 
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                  sender='noreply@luxpersonal.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: 
    {url_for('users.reset_token', token=token, _external=True)}

    If you do not make this requestm please ignore this email
    '''
    mail.send(msg)