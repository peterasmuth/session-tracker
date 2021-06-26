from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, CreateLocation, CreateGame, CreateSession
from app.models import User, Location, Game, Session
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@app.route('/')
@app.route('/index')
@login_required
def index():
	return render_template('index.html', title = 'Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
        	next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/create_location', methods = ['GET','POST'])
@login_required
def create_location():
	form = CreateLocation()
	form.user_id.data = current_user.id
	locations = Location.query.filter_by(user_id = current_user.id).all()
	if form.validate_on_submit():
		location = Location(name = form.location_name.data, user_id = current_user.id)
		db.session.add(location)
		db.session.commit()
		flash('New location created')
		return redirect(url_for('create_location'))
	return render_template('create.html'
							, title = 'Create New Location'
							, form = form
							, entity_type = 'Location'
							, items = locations)



@app.route('/create_game', methods = ['GET','POST'])
@login_required
def create_game():
	form = CreateGame()
	form.user_id.data = current_user.id
	games = Game.query.filter_by(user_id = current_user.id).all()
	if form.validate_on_submit():
		game = Game.query.filter_by(format = form.format.data
					, limit = form.limit.data
					, small_blind = form.small_blind.data
					, big_blind = form.big_blind.data
					, ante = form.ante.data
					, straddle = form.straddle.data
					, user_id = form.user_id.data).first()
		# raise
		if game is None:
			new_game = Game(format = form.format.data
					, limit = form.limit.data
					, small_blind = form.small_blind.data
					, big_blind = form.big_blind.data
					, ante = form.ante.data
					, straddle = form.straddle.data
					, user_id = form.user_id.data)
			db.session.add(new_game)
			db.session.commit()
			flash('New game type created')
			return redirect(url_for('create_game'))
		else:
			flash('That game type already exists')
	return render_template('create.html'
							, title = 'Create New Game Type'
							, form = form
							, entity_type = 'Game'
							, items = games)



@app.route('/create_session', methods = ['GET','POST'])
@login_required
def create_session():
	sessions = Session.query.filter_by(user_id = current_user.id).all()
	locations = Location.query.filter_by(user_id = current_user.id).all()
	games = Game.query.filter_by(user_id = current_user.id).all()
	form = CreateSession()
	form.location.choices = [(l.id, l.name) for l in locations]
	form.game_type.choices = [(g.id, g.__repr__()) for g in games]
	if form.validate_on_submit():
		new_sesh = Session(buy_in = form.buy_in.data
						  , cash_out = form.cash_out.data
						  , date = form.date.data
						  , duration = form.duration.data
						  , location_id = form.location.data
						  , game_id = form.game_type.data
						  , user_id = current_user.id)
		db.session.add(new_sesh)
		db.session.commit()
		return redirect(url_for('create_session'))
	return render_template('create.html'
							, title = 'Create New Session'
							, form = form
							, entity_type = 'Session'
							, items = sessions)


@app.route('/dashboard', methods = ['GET','POST'])
@login_required
def dashboard():
	sessions = Session.query.filter_by(user_id = current_user.id).all()
	locations = Location.query.filter_by(user_id = current_user.id).all()
	games = Game.query.filter_by(user_id = current_user.id).all()
	s = pd.DataFrame.from_records([sesh.to_dict() for sesh in sessions])
	l = pd.DataFrame.from_records([loc.to_dict() for loc in locations])
	g = pd.DataFrame.from_records([g.to_dict() for g in games])
	first_join = pd.merge(s,l, how = 'inner', left_on = 'location_id', right_on = 'id')
	data = pd.merge(first_join,g, how = 'inner', left_on = 'game_id', right_on = 'id')
	data['profit'] = data.cash_out - data.buy_in

	total_profit = data.profit.sum()
	total_hours = data.duration.sum()

	data.sort_values(by = 'date', inplace = True)
	data['Cumulative Sum'] = data.profit.cumsum()
	plot = sns.lineplot(x = 'date', y = 'Cumulative Sum', data = data)
	plt.savefig('output.png')


	# raise
	return render_template('dashboard.html'
							, title = 'Session Dashboard'
							, profit = total_profit
							, hours = total_hours)
