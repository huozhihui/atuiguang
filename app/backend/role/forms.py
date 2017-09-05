#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from app.flask_ext.forms import LinkField


class RoleForm(FlaskForm):
    name = StringField(u'角色名称', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField(u'提交')
    return_link = LinkField(u'返回', '/backend/role/index')
