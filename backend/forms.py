from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, email_validator

class PostForm(FlaskForm):
    title = StringField('Title', 
                        validators=[DataRequired(), Length(min=2, max=100)])
    company = StringField('Company',
                        validators=[DataRequired(), Length(min=1, max=80)])
    description = StringField('Description',
                        validators=[DataRequired(), Length(min=1, max=200)])

    submit = SubmitField('Post')


class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                        validators=[DataRequired()])
                        
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):
    firstName = StringField('First Name', 
                        validators=[DataRequired(), Length(min=1, max=25)])
    lastName = StringField('Last Name', 
                        validators=[DataRequired(), Length(min=1, max=25)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                        validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password',
                        validators=[DataRequired(), EqualTo('Password')])

    submit = SubmitField('Sign Up')
    