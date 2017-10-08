#!/usr/bin/env python

import pymysql, string, sys, random, binascii, os, configparser

from flask import Flask, abort, flash, g, jsonify, render_template, redirect, url_for, session, request

from flask_seasurf import SeaSurf
from flask_mail import Mail, Message
from functools import wraps
from passlib.hash import bcrypt
from validate_email import validate_email

app = Flask(__name__)
csrf = SeaSurf(app)
mail = Mail()

def load_config():
	config = configparser.ConfigParser()
	config.read('config.txt')
	secret_key = config.get('Main','secret_key')
	if secret_key == 'urandom':
		secret_key = os.urandom(24)
	db_host = config.get('db', 'dbhost')
	db_user = config.get('db', 'dbuser')
	db_passwd = config.get('db', 'dbpasswd')
	db_name = config.get('db', 'dbname')
	m_server = config.get('mail', 'mail_server')
	m_port =  config.get('mail', 'mail_port')
	m_tls = config.getboolean('mail', 'mail_tls')
	m_ssl = config.getboolean('mail', 'mail_ssl')
	m_user = config.get('mail', 'mail_username')
	m_pass = config.get('mail', 'mail_password')
	return (db_user, db_passwd, db_name, db_host, m_server, m_port,
			m_tls, m_ssl, m_user, m_pass, secret_key)

def get_db():
	dbcon = pymysql.connect(host=app.config['MYSQL_DATABASE_HOST'],
							user=app.config['MYSQL_DATABASE_USER'],
							password=app.config['MYSQL_DATABASE_PASSWORD'],
							db=app.config['MYSQL_DATABASE_DB'],
							charset='utf8mb4',
							cursorclass=pymysql.cursors.DictCursor)
	return dbcon

@app.before_request
def FUCK(): # otherwise g._database doesn't seem to fucking exist...
	try:
		dbconn().cursor()
	except:
		pass # should probably render_template('yourmysqlisbroken.html')

def dbconn():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = get_db()
	return db

@app.teardown_request
def db_disconnect(exception=None):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

def flash_errors(form_info):
	for errors in form_info['errors']:
		for field, error in errors.items():
			flash(u"Error: (%s) %s" % (field.title(), error))

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			return redirect(url_for('login_route'))
	return wrap

def send_verify(to_email, verify_key, event_info, div_info):
	msg = Message("CodeWarz Event Registration", sender=app.config['MAIL_USERNAME'], recipients=[to_email])
	msg.body = '''You (or someone using your email address) are almost completely registered for the %s Division for the %s event.\n\nTo finish up your registration, please validate your email by following this link:\n\n%s\n\nIf you have any questions, feel free to mail us back or drop into slack\n\n
	~CodeWarz Ninjas~''' % (div_info.get('name'), event_info.get('name'),'https://signup.codewarz.ninja/validate/' + verify_key)
	if mail.send(msg):
		return True
	return False

def gen_key():
	return binascii.hexlify(os.urandom(24)).decode('utf-8')

def validate_form(form):
	username,email,div_id,lang,event_id = form.get('username'),form.get('email'),form.get('div_id'),form.get('lang'),form.get('event_id')
	if not all([username, email, div_id, lang, event_id]):
		return {'error': 'Please fill out all the fields'}
	# validate event
	try:
		events = get_events()
		if not any(e.get('id') == int(event_id) for e in events):
			return {'error': "I don't know about that event"}
	except:
		# non int event_id?
		return {'error': "I don't know about that event"}
	# validate username
	for char in username:
		if char not in string.ascii_letters + string.digits + "_-=":
			return {'error': 'Illegal chars in username'}
	if len(username.strip()) == '':
		return {'error': 'No username?'}
	if username_exists(username.strip()):
		return {'error': 'That username is taken'}
	# validate email
	if not validate_email(email):
		return {'error': 'Invalid Email'}
	# validate division
	try:
		divisions = get_divisions(event_id)
		if not any(d.get('id') == int(div_id) for d in divisions):
			return {'error': "I don't know about that division"}
	except:
		# non int div_id?
		return {'error': "I don't know about that division"}
	# validate lang (kinda, not really...)
	for char in lang:
		if char not in string.printable.strip():
			return {'error': "Lang is free form, but it's gotta be printable ascii.."}
	return {'error': False}

def create_signup(form):
	reg_key = gen_key()
	while is_legit_key(reg_key):
		reg_key = gen_key()
	username,email,div_id,lang = form.get('username').strip(),form.get('email').strip(),form.get('div_id').strip(),form.get('lang').strip()
	event_id = form.get('event_id')
	# put them in the db
	cur = g._database.cursor()
	cmd = '''INSERT INTO signups (username, email, verified, hash, division, lang, event_id) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
	cur.execute(cmd,(username,email,0,reg_key,div_id,lang,event_id))
	cur.connection.commit()
	# send them the validate email
	try:
		send_verify(email,reg_key,get_event(event_id),get_division(div_id))
		return True
	except:
		return False

def is_legit_key(some_key):
	cur = g._database.cursor()
	cur.execute('SELECT id FROM signups WHERE hash = %s LIMIT 1', (some_key))
	res = cur.fetchone()
	if res:
		return True
	return False

def username_exists(username):
	cur = g._database.cursor()
	cur.execute('SELECT id FROM signups WHERE username = %s LIMIT 1', (username))
	res = cur.fetchone()
	if res:
		return True
	return False

def get_user_by_key(some_key):
	cur = g._database.cursor()
	cur.execute('SELECT id, username, division, event_id FROM signups WHERE hash = %s LIMIT 1', (some_key))
	res = cur.fetchone()
	return res

def mark_user_reg_complete(userid):
	cur = g._database.cursor()
	cmd = '''UPDATE signups SET verified = '1' WHERE id = %s LIMIT 1'''
	cur.execute(cmd,(userid))
	cur.connection.commit()
	return True

def check_login(form):
	username,password = form.get('username'),form.get('password')
	cur = g._database.cursor()
	cur.execute('SELECT id, password, level FROM admins WHERE name = %s LIMIT 1', (username))
	res = cur.fetchone()
	if not res:
		return False
	if bcrypt.verify(password, res.get('password')):
		session['id'] = res.get('id')
		session['level'] = res.get('level')
		return True
	return False

# future #
def urlify(some_text):
	res = ''
	ok_ascii = string.ascii_letters + string.digits + '_-'
	for char in some_text:
		res += char if char in ok_ascii else '_'
	return res
# end future #

def is_logged_in():
	if session.get('id'):
		return True
	return False

def get_contenders(event_id,div_id):
	cur = g._database.cursor()
	cur.execute('SELECT username, lang FROM signups WHERE verified = "1" AND event_id = %s AND division = %s ORDER BY id ASC', (event_id,div_id))
	res = cur.fetchall()
	return res

def get_events():
	cur = g._database.cursor()
	cur.execute('SELECT id, name, description_fp, start, stop FROM events ORDER BY start ASC')
	res = cur.fetchall()
	return res

def get_event(event_id):
	cur = g._database.cursor()
	cur.execute('SELECT id, name, description_full, start, stop FROM events WHERE id = %s LIMIT 1', (event_id))
	res = cur.fetchone()
	return res

def get_divisions(event_id):
	cur = g._database.cursor()
	cur.execute('SELECT id, name, description FROM divisions WHERE event_id = %s ORDER BY id ASC', (event_id))
	res = cur.fetchall()
	return res

def get_division(div_id):
	cur = g._database.cursor()
	cur.execute('SELECT id, name, description FROM divisions WHERE id = %s LIMIT 1', (div_id))
	res = cur.fetchone()
	return res


@app.route('/')
def index_route():
	events = get_events()
	return render_template('main.html',events=events,is_logged_in=is_logged_in())

@app.route('/event/<int:event_id>/<event_name>')
def event_route(event_id,event_name):
	events = get_events()
	if not any(e.get('id') == event_id for e in events):
		event_id = 1
	event_info = get_event(event_id)
	divisions = get_divisions(event_id)
	return render_template('event.html',events=events,event_info=event_info,divisions=divisions,is_logged_in=is_logged_in())

@app.route('/signup/<int:event_id>/<event_name>',methods=['GET','POST'])
def signup_route(event_id,event_name):
	if request.method == 'POST':
		for stuff in request.form:
			print(stuff,request.form[stuff])
		status = validate_form(request.form)
		if not status.get('error'):
			if create_signup(request.form):
				flash('Check your email to complete registration','success')
			else:
				flash('Added you to the db but could not send email','danger')
		else:
			flash(status.get('error'),'danger')
	events = get_events()
	if not any(e.get('id') == event_id for e in events):
		return 'i do not know about that event'
	event_info = get_event(event_id)
	divisions = get_divisions(event_id)
	return render_template('signup.html',events=events,divisions=divisions,event_info=event_info,is_logged_in=is_logged_in())

@app.route('/validate/<reg_key>')
def validate_route(reg_key):
	status = is_legit_key(reg_key)
	if not status:
		return render_template('validate.html',divisions=divisions,status='bad',is_logged_in=is_logged_in())
	user_datas = get_user_by_key(reg_key)
	events = get_events()
	event_info = get_event(user_datas.get('event_id'))
	div_info = get_division(user_datas.get('division'))
	mark_user_reg_complete(user_datas.get('id'))
	flash('Registration Complete!','success')
	return render_template('validate.html',events=events,event_info=event_info,div_info=div_info,user_datas=user_datas,status='good',is_logged_in=is_logged_in())

@app.route('/contenders/<int:event_id>/<int:div_id>/<event_name>/<div_name>')
def contenders_route(event_id,event_name,div_id,div_name):
	events = get_events()
	if not any(e.get('id') == event_id for e in events):
		event_id = 1
	event_info = get_event(event_id)
	divisions = get_divisions(event_id)
	if not any(d.get('id') == div_id for d in divisions):
		div_id = 1
	div_info = get_division(div_id)
	contenders = get_contenders(event_id,div_id)
	return render_template('contenders.html',events=events,event_info=event_info,contenders=contenders,div_info=div_info,is_logged_in=is_logged_in())


## this route can probably be removed ##
@app.route('/info/<int:div_id>/<div_name>')
def info_route(div_id,div_name):
	divisions = get_divisions()
	if not any(d.get('id') == div_id for d in divisions):
		return 'i do not know about that division'
	div_info = get_division(div_id)
	return render_template('info.html',divisions=divisions,div_info=div_info,is_logged_in=is_logged_in())
## end of probable removable route ##

@app.route('/login', methods=['GET','POST'])
def login_route():
	divisions = get_divisions()
	if request.method == 'POST':
		if check_login(request.form):
			flash('Logged in!', 'success')
			return redirect(url_for('index_route'))
		else:
			flash("I don't know you",'danger')
	return render_template('login.html',divisions=divisions,is_logged_in=is_logged_in())

@app.route('/logout')
def logout_route():
	session.clear()
	flash('Logged you out', 'info')
	return redirect(url_for('index_route'))

app.config['MYSQL_DATABASE_USER'],app.config['MYSQL_DATABASE_PASSWORD'], \
app.config['MYSQL_DATABASE_DB'],app.config['MYSQL_DATABASE_HOST'], \
app.config['MAIL_SERVER'],app.config['MAIL_PORT'],app.config['MAIL_USE_TLS'], \
app.config['MAIL_USE_SSL'],app.config['MAIL_USERNAME'],app.config['MAIL_PASSWORD'], \
app.secret_key = load_config()

mail.init_app(app)
if __name__ == '__main__':
	app.run(host='0.0.0.0',port=1301,debug=True)
