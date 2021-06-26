from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, IntegerField, SelectField, DecimalField
from wtforms.fields.html5 import DateTimeField, DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Location, Game

class LoginForm(FlaskForm):
	username = StringField('Username', validators = [DataRequired()])
	password = PasswordField('Password', validators = [DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class CreateLocation(FlaskForm):
	user_id = HiddenField('user_id')
	location_name = StringField('Location Name', validators=[DataRequired()])
	submit = SubmitField('Create Location')

	def validate_location_name(self, location_name):
		location = Location.query.filter_by(user_id = self.user_id.data, name = self.location_name.data).first()
		if location is not None:
			raise ValidationError('Location with this name already exists')


class CreateGame(FlaskForm):
	user_id = HiddenField('user_id')
	format = SelectField('Game Format', choices=['Hold''em', 'Omaha', '7-card Stud'])
	limit = SelectField('Limit Type', choices = ['No-limit', 'Pot-limit', 'Fixed Limit'])
	small_blind = IntegerField('Small Blind', validators = [DataRequired()])
	big_blind = IntegerField('Big Blind', validators = [DataRequired()])
	ante = IntegerField('Ante')
	straddle = IntegerField('Straddle')
	submit = SubmitField('Create Game Type')


class CreateSession(FlaskForm):
	user_id = HiddenField('user_id')
	buy_in = IntegerField('Buy-in', validators = [DataRequired()])
	cash_out = IntegerField('Cashout', validators = [DataRequired()])
	date = DateField('Start Time', validators = [DataRequired()])
	duration = DecimalField('Duration', validators = [DataRequired()])
	location = SelectField('Session Location', validators = [DataRequired()])
	game_type = SelectField('Session Game Type', validators = [DataRequired()])
	submit = SubmitField('Create Session')
