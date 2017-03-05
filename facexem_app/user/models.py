from ..extensions import db
from .constans import ROLES
from werkzeug.security import generate_password_hash, check_password_hash
from config import SECRET_KEY

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120),  unique=True)
    name = db.Column(db.String(64), nullable=False)
    pw_hash = db.Column(db.String(255))
    role = db.Column(db.SmallInteger, default=ROLES['USER'])

    def __init__(self, name=None, password=None, email=None, role=None):
        self.name = name
        if password:
            self.set_password(password)
        self.set_token(email, SECRET_KEY)
        self.email = email
        self.role = role

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<User %r>' % (self.name)

