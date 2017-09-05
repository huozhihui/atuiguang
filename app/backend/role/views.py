#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash, redirect, url_for
from flask_login import login_required, current_user
from . import role
from app.models import Role
from .forms import RoleForm
from app import db


@role.route('/index', methods=['GET'])
@login_required
def index():
    header = u'角色管理'
    objects = Role.query.all()
    return _render('index', locals())


@role.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    header = u'角色添加'
    form = RoleForm()
    if request.method == "POST":
        if form.validate_on_submit():
            form_data = dict(name=form.name.data)
            exist_role = Role.query.filter_by(name=form_data['name']).first()
            if exist_role:
                flash(u'角色名称已存在!', 'danger')
                return _render('form', locals())
            else:
                new_object = Role(**form_data)
                db.session.add(new_object)
                try:
                    db.session.commit()
                    flash(u'角色添加成功!')
                    return redirect(url_for('.index'))
                except Exception, e:
                    flash(u'角色保存失败, 请联系管理员!', 'danger')
                    print e.message
                    db.session.rollback()
        else:
            flash(u'表单验证失败!', 'danger')
    return _render('form', locals())


@role.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    header = u'角色编辑'
    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if request.method == "POST":
        if form.validate_on_submit():
            exist_role = Role.query.filter_by(name=form.name.data).first()
            if exist_role and role.id != exist_role.id:
                flash(u'角色名称已存在!', 'danger')
                return _render('form', locals())
            else:
                form.populate_obj(role)
                flash(u'角色编辑成功!')
                return redirect(url_for(".index"))
        else:
            flash(u'表单验证失败!', 'danger')
    return _render("form", locals())


@role.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    obj = Role.query.get(id)
    db.session.delete(obj)
    db.session.commit()
    flash(u'数据删除成功!')
    return redirect(url_for('.index'))


def _render(page, kwargs={}):
    html = "backend/role/%s.html" % page
    return render_template(html, **kwargs)
