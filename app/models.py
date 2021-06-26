from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    sessions = db.relationship('Session', backref = 'User', lazy = 'dynamic')
    locations = db.relationship('Location', backref = 'User', lazy = 'dynamic')
    game_types = db.relationship('Game', backref = 'User', lazy = 'dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    format = db.Column(db.String(24), index = True)
    limit = db.Column(db.String(24), index = True)
    small_blind = db.Column(db.Integer)
    big_blind = db.Column(db.Integer)
    ante = db.Column(db.Integer)
    straddle = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sessions = db.relationship('Session', backref ='Game Type', lazy = 'dynamic')

    def __repr__(self):
        return f'{self.small_blind}-{self.big_blind} {self.limit} {self.format}'

    def to_dict(self):
        return {'id': self.id
                ,'format': self.format
                ,'limit': self.limit
                ,'small_blind': self.small_blind
                ,'big_blind': self.big_blind
                ,'ante': self.ante
                ,'straddle': self.straddle
                ,'user_id': self.user_id}


class Location(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sessions = db.relationship('Session', backref = 'Location', lazy = 'dynamic')

    def __repr__(self):
        return f'{self.name}'

    def to_dict(self):
        return {'id': self.id
                , 'name': self.name
                , 'user_id': self.user_id}


class Session(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    buy_in = db.Column(db.Integer)
    cash_out = db.Column(db.Integer)
    date = db.Column(db.Date, index = True)
    duration = db.Column(db.Float)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Session at {self.date}'

    def to_dict(self):
        return {'id': self.id
                , 'buy_in': self.buy_in
                , 'cash_out':self.cash_out
                , 'date': self.date
                , 'duration': self.duration
                , 'location_id': self.location_id
                , 'game_id': self.game_id
                , 'user_id': self.user_id}
