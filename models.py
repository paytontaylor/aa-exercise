from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True,
                         nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship('Feedback', backref="users")

    @classmethod
    def register(cls, username, password, email, first_name, last_name):

        # generates a bcrypt hashed password
        hashed_pw = bcrypt.generate_password_hash(password)

        # converts the hashed password into the correct format
        utf8_pw = hashed_pw.decode('utf8')

        return cls(username=username, password=utf8_pw, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Feedback(db.Model):

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    username = db.Column(db.Text(), db.ForeignKey('users.username'))
