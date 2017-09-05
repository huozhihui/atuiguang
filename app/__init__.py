#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy, Model
from config import config
from flask_login import LoginManager, login_required

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

# 设置登陆
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = u"请登录系统"


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .backend.user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/backend/user')

    from .backend.home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .backend.info_type import info_type as info_type_blueprint
    app.register_blueprint(info_type_blueprint, url_prefix='/backend/info_type')

    from .backend.info import info as info_blueprint
    app.register_blueprint(info_blueprint, url_prefix='/backend/info')

    return app
