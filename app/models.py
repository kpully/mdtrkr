from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager

class Script(db.Model):
    __tablename__ = 'scripts'
    id = db.Column(db.Integer, primary_key=True)
    drug = db.Column(db.String(20))
    dose = db.Column(db.Float)
    start = db.Column(db.Date)
    end_date = db.Column(db.Date)
    side_effects = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #date field

class Mood(db.Model):
    __tablename__ = 'moods'
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.Integer)
    date = db.Column(db.Date)
    side_effects = db.Column(db.String(100))
    notes = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64))
    weight = db.Column(db.Integer)
    gender=db.Column(db.String(64))
    age = db.Column(db.Integer)
    role = db.Column(db.String(20))
    age_group = db.Column(db.Integer)
    scripts = db.relationship('Script', backref='user', lazy='dynamic')
    moods = db.relationship('Mood', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
