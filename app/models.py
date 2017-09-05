#!/usr/bin/python
# -*- coding: utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import db
from . import login_manager
from datetime import datetime


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __getitem__(self, item):
        return self.__dict__[item]


# 定义数据库模型
class Role(Base):
    __tablename__ = 'roles'
    name = db.Column(db.String(30), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy='dynamic')

    SUPER_ADMIN = 1
    ADMIN = 2
    USER = 3

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, Base):
    __tablename__ = 'users'
    telphone = db.Column(db.String(11), unique=True, nullable=False, index=True)
    email = db.Column(db.String(30), unique=True, index=True)
    username = db.Column(db.String(30), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    identity = db.Column(db.String(10), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # 邮件确认字段
    confirmed = db.Column(db.Boolean, default=False)
    # 冻结
    freezed = db.Column(db.Boolean, default=False)

    info_types = db.relationship('InfoType', backref='info_type', lazy='dynamic',
                                 primaryjoin="User.id == InfoType.user_id")
    infos = db.relationship('Info', backref='user', lazy='dynamic', primaryjoin="User.id == Info.user_id")

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 登陆时,加载用户的回调函数
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # 发送邮件时生成token
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    # 判断是否管理员
    def is_admin(self):
        return True if self.role_id == 1 else False


class InfoType(Base):
    __tablename__ = 'info_types'
    name = db.Column(db.String(30), unique=True, nullable=False)
    infos = db.relationship('Info', backref='info_type', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<InfoType %r>' % self.name


# 信息表
class Info(Base):
    __tablename__ = 'infos'
    content = db.Column(db.TEXT())
    contact_name = db.Column(db.String(30))
    telphone = db.Column(db.String(11), nullable=False, index=True)
    wx = db.Column(db.String(30))
    # 审核人
    audit_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 是否审核
    audited = db.Column(db.Boolean, default=False)
    # 是否发布
    show = db.Column(db.Boolean, default=True)
    info_type_id = db.Column(db.Integer, db.ForeignKey('info_types.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Info %r: %r>' % (self.type, self.content)
