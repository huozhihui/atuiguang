#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import TelField
from app.flask_ext.forms import LinkField


class UserForm(FlaskForm):
    identity = RadioField(u'身份', choices=[('personal', u'个人'), ('company', u'管理员')], default='personal')
    username = StringField(u'用户名', validators=[DataRequired(), Length(1, 30)])
    telphone = TelField(u'手机号', validators=[DataRequired(), Length(1, 11)])
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 30), Email()])
    password = PasswordField(u'密码', validators=[DataRequired(), Length(6, 16), EqualTo('password2', message=u'密码不匹配')])
    password2 = PasswordField(u'确认密码', validators=[DataRequired()])
    role_id = SelectField(u'角色', coerce=int, choices=[])
    submit = SubmitField(u'提交')
    return_link = LinkField(u'返回', '/backend/user/index')


class UserEditForm(FlaskForm):
    identity = RadioField(u'身份', choices=[('personal', u'个人'), ('company', u'管理员')], default='personal')
    username = StringField(u'用户名', validators=[DataRequired(), Length(1, 30)])
    telphone = TelField(u'手机号', validators=[DataRequired(), Length(1, 11)])
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 30), Email()])
    role_id = SelectField(u'角色', coerce=int, choices=[])
    submit = SubmitField(u'提交')
    return_link = LinkField(u'返回', '/backend/user/index')


class ChangePasswordForm(FlaskForm):
    password = PasswordField(u'新密码', validators=[DataRequired(), Length(6, 16), EqualTo('password2', message=u'密码不匹配')])
    password2 = PasswordField(u'确认密码', validators=[DataRequired()])
    submit = SubmitField(u'提交')
    return_link = LinkField(u'返回', '/backend/user/index')
