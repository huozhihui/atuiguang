#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from wtforms.fields.html5 import TelField
from app.flask_ext.forms import LinkField


class InfoForm(FlaskForm):
    info_type_id = SelectField(u'信息类型', coerce=int, choices=[])
    content = TextAreaField(u'内容', validators=[DataRequired()])
    contact_name = StringField(u'联系人', validators=[DataRequired(), Length(1, 30)])
    telphone = TelField(u'手机号', validators=[DataRequired(), Length(1, 11)])
    wx = StringField(u'微信号', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField(u'提交')
    return_link = LinkField(u'返回', '/backend/info/index')
