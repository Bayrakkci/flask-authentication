from market import db, bcrypt, login_manager
from flask_login import UserMixin
'''
    LoginManager is a simple but efficient flask module that helps to prevent hard-coding all
    the login form entities.
'''
@login_manager.user_loader
def load_user(user_id):

    # return User.query.all()
    return User.query.get(int(user_id))

    #Simple database structure for SQLALCHEMY

class User(db.Model, UserMixin):
    # UserMixin provides multiple prevention for vulnerabilities

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)
    '''
        Property is a class that inside of builtins.pyi
        It includes so many methods and one of them is SETTER and its purpose is str -> int
    '''
    @property
    def prettier_budget(self):
        if len(str(self.budget)) >=4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f'{self.budget}$'
    @property
    def password(self):
        return self.password
    @password.setter
    # Encdoing password with SHA-256

    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    # Decrypting the password

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def can_purchase(self, item_object):
        return self.budget >= item_object.price

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
    # __repr__ is a special method used to represent a class's objects as a string
    # It collects objects in to a build-in string <3
        return f'Item {self.name}'

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()