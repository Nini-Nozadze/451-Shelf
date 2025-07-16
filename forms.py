from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

def validate_word_count(form, field):
    if len(field.data.split()) < 75:
        raise ValidationError('რეცენზია უნდა შეიცავდეს მინიმუმ 75 სიტყვას.')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    profile_picture = FileField('პროფილის სურათი', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'მხოლოდ JPG, JPEG ან PNG!')
    ])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class BlogPostForm(FlaskForm):
    title = StringField('სათაური', validators=[DataRequired(), Length(min=3, max=200)])
    content = TextAreaField('შინაარსი', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('დამატება')



class ChoiceForm(FlaskForm):
    post_type = SelectField("აირჩიე ტიპი", choices=[('review', 'რეცენზია'), ('quote', 'ციტატა')])
    submit = SubmitField("გაგრძელება")


class ReviewForm(FlaskForm):
    book_title = StringField("წიგნის სათაური", validators=[DataRequired()])
    book_author = StringField("ავტორი", validators=[DataRequired()])
    content = TextAreaField("რეცენზია", validators=[DataRequired(), Length(min=75)])
    genre = SelectField("ჟანრი", choices=[('მხატვრული', 'მხატვრული'), ('დოკუმენტური', 'დოკუმენტური'), ('საბავშვო', 'საბავშვო')])
    image = FileField("სურათი")
    submit = SubmitField("ატვირთვა")

class QuoteForm(FlaskForm):
    quote_text = StringField("ციტატა", validators=[DataRequired()])
    book_title = StringField("წიგნის სათაური", validators=[DataRequired()])
    submit = SubmitField("ატვირთვა")

