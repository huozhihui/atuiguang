#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash, redirect, url_for
from flask_login import login_required, current_user
from . import info
from app.models import Info, InfoType
from .forms import InfoForm
from app import db


@info.route('/index', methods=['GET'])
@login_required
def index():
    header = u'信息管理'
    objects = Info.query.all()
    return _render('index', locals())


@info.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    header = u'信息添加'
    form = InfoForm()
    form.info_type_id.choices = [(info_type.id, info_type.name) for info_type in InfoType.query.all()]
    if request.method == "POST":
        if form.validate_on_submit():
            form_data = dict(content=form.content.data,
                             contact_name=form.contact_name.data,
                             telphone=form.telphone.data,
                             wx=form.wx.data,
                             info_type_id=form.info_type_id.data)
            exist_info = Info.query.filter_by(content=form_data['content'], user_id=current_user.id).first()
            if exist_info:
                flash(u'信息已存在!', 'danger')
                return _render('form', locals())
            else:
                form_data.update(dict(user_id=current_user.id))
                new_object = Info(**form_data)
                db.session.add(new_object)
                try:
                    db.session.commit()
                    flash(u'信息添加成功!')
                    return redirect(url_for('.index'))
                except Exception, e:
                    flash(u'信息保存失败, 请联系管理员!', 'danger')
                    print e.message
                    db.session.rollback()
        else:
            flash(u'表单验证失败!', 'danger')
    return _render('form', locals())


@info.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    header = u'信息编辑'
    info = Info.query.get_or_404(id)
    form = InfoForm(obj=info)
    form.info_type_id.choices = [(info_type.id, info_type.name) for info_type in InfoType.query.all()]
    if request.method == "POST":
        if form.validate_on_submit():
            exist_info = Info.query.filter_by(content=form.content.data, user_id=current_user.id).first()
            if exist_info and info.id != exist_info.id:
                flash(u'信息{}已存在!', 'danger')
                return _render('form', locals())
            else:
                form.populate_obj(info)
                flash(u'信息编辑成功!')
                return redirect(url_for(".index"))
        else:
            flash(u'表单验证失败!', 'danger')
    return _render("form", locals())


@info.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    obj = Info.query.get(id)
    db.session.delete(obj)
    db.session.commit()
    flash(u'数据删除成功!')
    return redirect(url_for('.index'))


def _render(page, kwargs={}):
    html = "backend/info/%s.html" % page
    return render_template(html, **kwargs)
