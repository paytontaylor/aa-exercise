from flask import Flask, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterForm, LoginForm, AddFeedbackForm, EditFeedbackForm
from models import User, connect_db, db, Feedback
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'secret'
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def send_to_register():
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def show_register_form():

    if 'username' in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username=username, password=password,
                                 email=email, first_name=first_name, last_name=last_name)

        db.session.commit()
        session['username'] = new_user.username

        return redirect(f'/users/{new_user.username}')

    return render_template('/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()

    if 'username' in session:
        return redirect(f"/users/{session['username']}")

    if form.validate_on_submit():

        username = form.username.data
        password = form.passowrd.data

        user = User.authenticate(username=username, password=password)

        if user:

            flash(f'Welcome Back! {user.username}')
            session['username'] = user.username
            return redirect(f'/users/{user.username}')

        else:
            form.username.errors = ['INVALID USERNAME/PASSWORD']
            session['username'] = user.username

    return render_template('login.html', form=form)


@app.route('/users/<username>')
def show_user(username):
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get_or_404(username)

    return render_template('show_user.html', user=user)


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):

    form = AddFeedbackForm()
    user = User.query.get_or_404(username)
    feedback = user.feedback

    if 'username' not in session or username != session['username']:
        raise Unauthorized()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content,
                            username=user.username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f'/users/{user.username}')

    return render_template('feedback_form.html', form=form, user=user, feedback=feedback)


@app.route('/feedback/<int:id>/update', methods=['GET', 'POST'])
def edit_feedback(id):

    form = EditFeedbackForm()
    feedback = Feedback.query.get_or_404(id)
    username = feedback.username

    if 'username' not in session or username != session['username']:
        raise Unauthorized()

    if form.validate_on_submit():

        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()

        return redirect(f'/users/{feedback.username}')

    return render_template('edit_feedback_form.html', form=form, username=username)


@app.route('/feedback/<int:id>/delete')
def delete_feedback(id):

    feedback = Feedback.query.get(id)
    user = feedback.username

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f'/users/{user}')


@app.route('/logout')
def logout_user():

    session.pop('username')

    return redirect('/login')
