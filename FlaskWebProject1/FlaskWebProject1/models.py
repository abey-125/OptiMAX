
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Shopdata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,db.Sequence('seq_reg_id', start=1001, increment=1), primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    store_name = db.Column(db.String(150))
