#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms.fields.html5 import TelField
from wtforms import ValidationError
from ..models import User
from ..flask_ext.forms import LinkField


class LoginForm(FlaskForm):
    tel_email = StringField(u'手机号/邮箱', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class RegistrationForm(FlaskForm):
    identity = RadioField(u'身份', choices=[('personal', u'个人'), ('company', u'管理员')], default='personal')
    telphone = TelField(u'手机号', validators=[DataRequired(), Length(1, 11)])
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 30), Email()])
    password = PasswordField(u'密码', validators=[DataRequired(), Length(6, 16), EqualTo('password2', message=u'密码不匹配')])
    password2 = PasswordField(u'确认密码', validators=[DataRequired()])
    submit = SubmitField(u'注册')
    # return_link = LinkField(u'返回')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已注册.')

    def validate_telphone(self, field):
        if User.query.filter_by(telphone=field.data).first():
            raise ValidationError(u'手机号已注册!')
