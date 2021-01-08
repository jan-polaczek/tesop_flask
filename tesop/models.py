from flask_sqlalchemy import SQLAlchemy
import bcrypt
import uuid
from email_validator import validate_email, EmailNotValidError


from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()


def generate_uuid():
    return str(uuid.uuid4())


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(60))
    email = db.Column(db.String(50))

    def __init__(self, **kwargs):
        if 'password' in kwargs:
            kwargs['password'] = User.hash_password(kwargs['password'])
        super().__init__(**kwargs)

    def check_password(self, password):
        return password and bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def __repr__(self):
        return f'User: {self.email}'

    def as_dict(self):
        res = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }
        return res

    @hybrid_property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    @staticmethod
    def authorize(email, password):
        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            return None
        else:
            return user

    @staticmethod
    def check_email(email):
        res = {}
        if User.query.filter_by(email=email).first() is None:
            res[email] = 'available'
        else:
            res[email] = 'unavailable'
        return res

    @staticmethod
    def register(**kwargs):
        errors = []
        user_data = {}
        if User.is_valid('email', kwargs.get('email', '')):
            user_data['email'] = kwargs.get('email')
        else:
            errors.append('Nieprawidowy adres e-mail')
        if User.is_valid('password', kwargs.get('password', '')):
            user_data['password'] = kwargs.get('password')
        else:
            errors.append('Hasło musi mieścić się między 8 a 60 znakami')
        if User.is_valid('username', kwargs.get('username', '')):
            user_data['username'] = kwargs.get('username')
        else:
            errors.append('Nazwa użytkownika musi mieścić się między 4 a 30 znakami')
        if User.check_email(kwargs.get('email'))[kwargs.get('email')] == 'unavailable':
            errors.append('Na ten email istnieje już założone konto')

        if len(errors) == 0:
            user = User(**user_data)
            db.session.add(user)
            db.session.commit()
        else:
            user = None
        return {'user': user, 'errors': errors}

    @staticmethod
    def is_valid(field, value):
        if field == 'username':
            return 3 < len(value) <= 30
        if field == 'password':
            return 7 < len(value) <= 60
        if field == 'email':
            try:
                validate_email(value)
                return True
            except EmailNotValidError as e:
                return False
        return False


class Session(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def create(**kwargs):
        s = Session(**kwargs)
        db.session.add(s)
        db.session.commit()
        return s
