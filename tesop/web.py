from flask import Blueprint, render_template, request, redirect, session, url_for
from tesop import models
import json


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
    message = request.args.get('message')
    if message:
        messages = [message]
    else:
        messages = None
    return render_template('login.html', messages=messages)


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
        return redirect(url_for('web.login', message='Rejestracja udana'))
    else:
        return render_template('sign_up.html', errors=result['errors'])


@web.route('/posts', methods=['GET', 'POST'])
def blogposts():
    if request.method == 'GET':
        posts = models.BlogPost.query.all()
        return render_template('blogposts.html', posts=posts)
    elif request.method == 'POST':
        user = models.Session.query.get(session['sid']).user
        data = request.form.to_dict()
        data['user_id'] = user.id
        post = models.BlogPost.create(**data)
        return redirect(url_for('web.blogpost_detail', post_id=post.id))


@web.route('/posts/new')
def blogpost_new():
    return render_template('new_blogpost.html')


@web.route('/posts/<post_id>')
def blogpost_detail(post_id):
    post = models.BlogPost.query.get(post_id)
    return render_template('blogpost.html', post=post)
