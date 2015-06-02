# -*- coding:Utf8 -*-


"""
    Flask from handler and checker for tasks.
"""

# Import
from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, SelectField
from wtforms.validators import InputRequired


class AddTaskForm(Form):
    """
        Create a form handler/validator
    """
    # task_id = IntegerField('Priority')
    name = StringField('Task Name', validators=[InputRequired(), ])
    due_date = DateField('Due Date (dd/mm/yyyy)', validators=[InputRequired(), ],
                         format='%d/%m/%Y')
    priority = SelectField('Priority', validators=[InputRequired(), ],
                           choices=[('1', '1'), ('2', '2'), ('3', '3'),
                                    ('4', '4'), ('5', '5'), ('6', '6'),
                                    ('7', '7'), ('8', '8'), ('9', '9'),
                                    ('10', '10')])
    status = IntegerField('Status')
