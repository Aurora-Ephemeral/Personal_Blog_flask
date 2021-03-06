from datetime import datetime
from flaskblog import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800): 
        with app.app_context():
            s = Serializer(app.config['SECRET_KEY'], 1800)
        return s.dumps({'user_id':self.id})

    @staticmethod
    def verify_reset_token(token): 
        with app.app_context():
            s = Serializer(app.config['SECRET_KEY'], 1800) 
        try: 
            user_id = s.loads(token)['user_id']
        except: 
            return None
        return User.query.get(user_id)

    def __init__(self, username, email, password):
        self.username = username 
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User({self.username}, {self.email}, {self.image_file})"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self): 
        return f'Post({self.title}, {self.date_posted})'

    def is_active(self): 
        return True