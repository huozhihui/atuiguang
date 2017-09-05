#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User, Role
from .. import db
from .forms import LoginForm, RegistrationForm
from ..email import send_email


# 登陆
@auth.route('/login', methods=['GET', 'POST'])
def login():
    header = u"登录"
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.telphone == form.tel_email.data) | (User.email == form.tel_email.data)).first()
        if user is None:
            flash(u'邮箱或手机号不存在!')
        elif user.freezed:
            flash(u'您已被冻结,请联系管理员!')
        else:
            if user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(request.args.get('next') or url_for('home.index'))
            else:
                flash(u'密码错误,请重新输入!')
    return _render('login', locals())


# 登出
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已经退出登录!')
    return redirect(url_for('.login'))


# 注册
@auth.route('/register', methods=['GET', 'POST'])
def register():
    header = u'注册'
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            form_data = dict(
                telphone=form.telphone.data,
                email=form.email.data,
                password=form.password.data,
                identity=form.identity.data,
                role_id=Role.USER
            )
            user = User(**form_data)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(user.email, u'确认账户',
                       'auth/email/confirm', user=user, token=token)
            flash(u'确认邮件已经发送到您的邮箱!')
            return redirect(url_for('home.index'))
    return _render('register', locals())


# 确认邮件方法
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        if current_user.is_admin():
            return redirect(url_for('home.index'))
        else:
            return redirect(url_for('home.index'))
    if current_user.confirm(token):
        flash(u'您已经确认了您的账号,谢谢!')
    else:
        flash(u'确认链接无效或已过期!')
    return redirect(url_for('home.index'))


# 重新发送邮件
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('home.index'))


# 判断请求链接
@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        if not current_user.confirmed \
                and request.endpoint \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


# 已登陆但为确认用户身份
@auth.route('/unconfirmed')
def unconfirmed():
    header = u'亲爱的用户,您好!'
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('home.index'))
    return _render('unconfirmed', locals())


def _render(content, kwargs={}):
    html = "auth/%s.html" % content
    return render_template(html, **kwargs)
