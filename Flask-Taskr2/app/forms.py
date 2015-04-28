

# -*- coding:Utf8 -*-

"""
    Flask from handler and checker
"""

from flask_wtf import Form
from wtforms import TextField, DateField, IntegerField, SelectField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo


class AddTaskForm(Form):
    """
        Create a form handler/validator
    """
    # task_id = IntegerField('Priority')
    name = TextField('Task Name', validators=[InputRequired(), ])
    due_date = DateField('Due Date (dd/mm/yyyy)', validators=[InputRequired(), ],
                         format='%d/%m/%Y')
    priority = SelectField('Priority', validators=[InputRequired(), ],
                           choices=[('1', '1'), ('2', '2'), ('3', '3'),
                                    ('4', '4'), ('5', '5'), ('6', '6'),
                                    ('7', '7'), ('8', '8'), ('9', '9'),
                                    ('10', '10')])
    status = IntegerField('Status')


class RegisterForm(Form):
    """
        Create a form handler/validator for registration
    """
    name = TextField('Username', validators=[InputRequired(),
                     Length(min=6, max=25)])
    email = TextField('Email', validators=[InputRequired(),
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
    name = TextField('Username', validators=[InputRequired(), ])
    password = PasswordField('Password', validators=[InputRequired(), ])
