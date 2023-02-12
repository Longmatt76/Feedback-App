from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, EmailField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, Length

class UserForm(FlaskForm):
    """form for adding new user"""
    username = StringField('Username:', validators=[InputRequired()])
    password = PasswordField('Password:',validators=[InputRequired()])
    email = EmailField('Email:', validators=[InputRequired()])
    first_name = StringField('First Name:',validators=[InputRequired()] )
    last_name = StringField('Last Name:',validators=[InputRequired()] )


class LoginForm(FlaskForm):
    """form for logging in user"""
    username = StringField('Username:', validators=[InputRequired()])
    password = PasswordField('Password:',validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    """form for creating new feedback"""
    title = StringField('Title:', validators=[InputRequired()])
    content = TextAreaField('Feedback:', validators=[InputRequired()])
    

 