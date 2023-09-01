from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.models import users
from main.func import moviedata, theatredata

class Superadmin_signup(FlaskForm):
    Name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired()])
    Confirm_Password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('Password')])
    Submit = SubmitField('Register')

    def validate_email(self, Email):
        user = users.query.filter_by(Email=Email.data).first()
        if user:
            print('Something here')
            raise ValidationError('The Email is taken. Please choose a different one!')
 
class LoginForm(FlaskForm):
    Email = StringField('Email', validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired()])
    Remember = BooleanField('Remember Me')
    Submit = SubmitField('Login') 

class Create_admin(FlaskForm):
    Name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired()])
    Submit = SubmitField('Register')

class Create_Theatre(FlaskForm):
    Name = StringField('Theatre Name', validators=[DataRequired(), Length(min=2, max=30)])
    Location = StringField('Theatre Location', validators=[DataRequired()])
    #Status = BooleanField('Theatre Status')
    Submit = SubmitField('Add Theatre')

class Create_Movies(FlaskForm):
    Name = StringField('Movie Name', validators=[DataRequired()])
    Rating = StringField('Rating')
    #Status = BooleanField('Theatre Status')
    Submit = SubmitField('Add Movie')

class Create_Show(FlaskForm):
    movies = moviedata
    theatres = theatredata
    The_Name = SelectField('Theatre Name(Select)', choices=theatres, validators=[DataRequired()])
    Mov_Name = SelectField('Movie Name(Select)',choices=movies, validators= [DataRequired()])
    Total_Seats = StringField('Total Seats', validators = [DataRequired()])
    Time = StringField('Show Time')
    Submit = SubmitField('Add Show')
    

