from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Length


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Length(max=50)])
    first_name = StringField('First Name', validators=[
                             InputRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[
                            InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(max=20)])
    passowrd = PasswordField('Password', validators=[InputRequired()])


class AddFeedbackForm(FlaskForm):
    title = StringField('Title', validators=[Length(max=50)])
    content = TextAreaField('Content', validators=[Length(max=400)])


class EditFeedbackForm(FlaskForm):
    title = StringField('Title', validators=[Length(max=50)])
    content = TextAreaField('Content', validators=[Length(max=400)])
