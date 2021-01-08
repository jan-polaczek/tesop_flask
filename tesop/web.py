from flask import Blueprint, render_template, request, redirect, session, url_for
from tesop import models
import datetime


web = Blueprint('web', __name__, template_folder='templates')


@web.context_processor
def session_info():
    logged_in = 'sid' in session
    if logged_in:
        try:
            s = models.Session.query.get(session['sid'])
            user = s.user.as_dict()
        except (TypeError, AttributeError):
            user = None
            logged_in = False
            session.clear()
    else:
        user = None
    return dict(logged_in=logged_in, user=user)


@web.route('/')
def index():
    return render_template('index.html')


@web.route('/sign-up')
def sign_up():
    return render_template('sign_up.html')


@web.route('/login')
def login():
    return render_template('login.html', messages=[request.args.get('messages', [])])


@web.route('/logout')
def logout():
    models.Session.query.get(session.get('sid')).delete()
    session.clear()
    return redirect(url_for('web.index'))


@web.route('/authorize', methods=['POST'])
def authorize():
    email = request.form.get('email')
    password = request.form.get('password')
    user = models.User.authorize(email, password)
    if user is None:
        error = 'Niewłaściwa nazwa użytkownika i/lub hasło'
        return render_template('login.html', errors=[error])
    else:
        ses = models.Session.create(user_id=user.id)
        session['sid'] = ses.id
        return redirect(url_for('web.index'))


@web.route('/register', methods=['POST'])
def register():
    data = request.form.to_dict()
    result = models.User.register(**data)
    if len(result['errors']) == 0:
        return redirect(url_for('web.login', messages=['Rejestracja udana']))
    else:
        return render_template('sign_up.html', errors=result['errors'])