#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash, redirect, url_for
from flask_login import login_required
from . import home


@home.route('/', methods=['GET'])
@login_required
def index():
    header = u'首页'
    # objects = Info.query.all()
    return _render('index', locals())


def _render(page, kwargs={}):
    html = "home/%s.html" % page
    return render_template(html, **kwargs)
