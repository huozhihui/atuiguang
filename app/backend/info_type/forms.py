#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from app.models import InfoType
from app.flask_ext.forms import LinkField


class InfoTypeForm(FlaskForm):
    name = StringField(u'名称', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField(u'提交')
    return_link = LinkField(u'返回', '/backend/info_type/index')

    def validate_name(self, field):
        if InfoType.query.filter_by(name=field.data).first():
            raise ValidationError(u'名称已存在.')
