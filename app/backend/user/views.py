#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, session, flash, redirect, url_for
from flask_login import login_required
from . import user
from app.models import User, Role
from .forms import UserForm, UserEditForm, ChangePasswordForm
from app import db


@user.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    header = u'用户管理'
    objects = User.query.all()
    return _render('index', locals())


@user.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    header = u'用户添加'
    form = UserForm()
    form.role_id.choices = [(role.id, role.name) for role in Role.query.filter(Role.id > 1).all()]
    if request.method == "POST":
        if form.validate_on_submit():
            form_data = dict(identity=form.identity.data,
                             username=form.username.data,
                             telphone=form.telphone.data,
                             email=form.email.data,
                             password=form.password.data,
                             role_id=form.role_id.data,
                             confirmed=1
                             )
            exist_telphone = User.query.filter_by(telphone=form.telphone.data).first()
            exist_email = User.query.filter_by(email=form.email.data).first()
            if exist_telphone:
                flash(u'手机号已存在!', 'danger')
                return _render('form', locals())
            elif exist_email:
                flash(u'邮箱已存在!', 'danger')
                return _render('form', locals())
            else:
                new_object = User(**form_data)
                db.session.add(new_object)
                try:
                    db.session.commit()
                    flash(u'用户添加成功!')
                    return redirect(url_for('.index'))
                except Exception, e:
                    flash(u'用户保存失败, 请联系管理员!', 'danger')
                    print e.message
                    db.session.rollback()
        else:
            flash(u'表单验证失败!', 'danger')
    return _render('form', locals())


@user.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    header = u'用户编辑'
    user = User.query.get_or_404(id)
    form = UserEditForm(obj=user)
    form.role_id.choices = [(role.id, role.name) for role in Role.query.all()]
    if request.method == "POST":
        if form.validate_on_submit():
            exist_telphone = User.query.filter_by(telphone=form.telphone.data).first()
            exist_email = User.query.filter_by(email=form.email.data).first()
            if exist_telphone and user.id != exist_telphone.id:
                flash(u'手机号已存在!', 'danger')
                return _render('form', locals())
            if exist_email and user.id != exist_email.id:
                flash(u'邮箱已存在!', 'danger')
                return _render('form', locals())

            form.populate_obj(user)
            flash(u'用户编辑成功!')
            return redirect(url_for(".index"))
        else:
            flash(u'表单验证失败!', 'danger')
    return _render("form", locals())


# 修改用户密码
@user.route('/change_password/<int:id>', methods=['GET', 'POST'])
@login_required
def change_password(id):
    header = u'修改用户密码'
    user = User.query.get_or_404(id)
    form = ChangePasswordForm(obj=user)
    if request.method == "POST":
        if form.validate_on_submit():
            form.populate_obj(user)
            flash(u'密码修改成功!')
            return redirect(url_for(".index"))
        else:
            flash(u'表单验证失败!', 'danger')
    return _render("change_passwd", locals())


# 冻结用户
@user.route('/freezed_user/<int:id>', methods=['GET', 'POST'])
@login_required
def freezed_user(id):
    user = User.query.get_or_404(id)
    user.freezed = 1
    flash(u'用户{} {}已冻结'.format(user.username, user.telphone))
    return redirect(url_for('.index'))


# 取消冻结
@user.route('/cancel_freezed/<int:id>', methods=['GET', 'POST'])
@login_required
def cancel_freezed(id):
    user = User.query.get_or_404(id)
    user.freezed = 0
    flash(u'用户{} {}已取消冻结'.format(user.username, user.telphone))
    return redirect(url_for('.index'))


@user.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    obj = User.query.get(id)
    db.session.delete(obj)
    db.session.commit()
    flash(u'数据删除成功!')
    return redirect(url_for('.index'))


def _render(page, kwargs={}):
    html = "backend/user/%s.html" % page
    return render_template(html, **kwargs)
