#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash, redirect, url_for
from flask_login import login_required, current_user
from . import info_type
from app.models import InfoType
from .forms import InfoTypeForm
from app import db


@info_type.route('/index', methods=['GET'])
@login_required
def index():
    header = u'信息类管理'
    objects = InfoType.query.all()
    return _render('index', locals())


@info_type.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    header = u'添加'
    form = InfoTypeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            exist_info_type = InfoType.query.filter_by(name=form.name.data).first()
            if exist_info_type:
                flash(u'名称{}已存在!'.format(form.name.data), 'danger')
                return _render('form', locals())
            else:
                form_data = dict(name=form.name.data,
                                 user_id=current_user.id
                                 )

                new_object = InfoType(**form_data)
                db.session.add(new_object)
                try:
                    db.session.commit()
                    flash(u'信息类{}添加成功!'.format(form_data['name']))
                    return redirect(url_for('.index'))
                except Exception, e:
                    flash(u'信息类{}保存失败, 请联系管理员!'.format(form_data['name']), 'danger')
                    print e.message
                    db.session.rollback()
        else:
            flash(u'表单验证失败!', 'danger')
    return _render('form', locals())


@info_type.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    header = u'编辑'
    info_type = InfoType.query.get_or_404(id)
    form = InfoTypeForm(request.form, obj=info_type)
    print form.validate_on_submit()
    if request.method == "POST":
        if form.validate_on_submit():
            exist_info_type = InfoType.query.filter_by(name=form.name.data).first()
            if exist_info_type and exist_info_type.id != info_type.id:
                flash(u'名称{}已存在!'.format(form.name.data), 'danger')
                return _render('form', locals())
            else:
                form.populate_obj(info_type)
                flash(u'信息类{}编辑成功!'.format(info_type.name))
                return redirect(url_for(".index"))
        else:
            flash(u'表单验证失败!', 'danger')
    return _render("form", locals())


@info_type.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    obj = InfoType.query.get_or_404(id)
    db.session.delete(obj)
    db.session.commit()
    flash(u'数据删除成功!')
    return redirect(url_for('.index'))


def _render(page, kwargs={}):
    html = "backend/info_type/%s.html" % page
    return render_template(html, **kwargs)
