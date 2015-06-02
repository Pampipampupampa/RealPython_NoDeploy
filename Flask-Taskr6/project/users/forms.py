# -*- coding:Utf8 -*-

"""
    Forms for users.
"""


# Imports
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo, Email


# Forms
class RegisterForm(Form):
    """
        Create a form handler/validator for registration
    """
    name = StringField('Username', validators=[InputRequired(),
                       Length(min=6, max=25)])
    email = StringField('Email', validators=[InputRequired(), Email(),
                                             Length(min=6, max=40)])
    password = PasswordField('Password', validators=[InputRequired(),
                                                     Length(min=6, max=40)])
    confirm = PasswordField('Password',
                            validators=[InputRequired(),
                                        EqualTo('password',
                                                message='Passwords must match')])


class LoginForm(Form):
    """
        Create a form handler/validator for Login
    """
    name = StringField('Username', validators=[InputRequired(), ])
    password = PasswordField('Password', validators=[InputRequired(), ])
