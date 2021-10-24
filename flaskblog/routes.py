from flask import render_template, url_for, flash, redirect, jsonify, request, make_response
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import Users
import jwt
import datetime
from functools import wraps
from flaskblog import db


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        new_user = Users(f'{form.username.data}', f'{form.email.data}', f'{form.password.data}', f'')
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return '<h1>Hello, token is missing </h1>', 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return '<h1>Hello, Could not verify the token</h1>', 403

        return f(*args, **kwargs)

    return decorated


@app.route("/unprotected")
def unprotected():
    return '<h1>Hello, this page viewed by anyone</h1>'


@app.route("/protected")
@token_required
def protected():
    return '<h1>Hello, token which is provided is correct</h1>'


@app.route("/login")
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = Users.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if auth and auth.password == user.password:
        token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'])
        user = Users.query.filter_by(username=auth.username).first()
        user.token = token
        db.session.commit()
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required'})

    # form = LoginForm()
    # if form.validate_on_submit():
    #     if form.email.data == 'ray@gmail.com' and form.password.data == 'password':
    #         flash('You have been logged in!', 'success')
    #         return redirect(url_for('home'))
    #     else:
    #         flash('Login Unsuccessful. Please check username and password', 'danger')
    # return render_template('login.html', title='Login', form=form)
