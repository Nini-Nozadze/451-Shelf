from ext import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

favorites_reviews = db.Table('favorites_reviews',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('review_id', db.Integer, db.ForeignKey('review.id'))
)


favorites_quotes = db.Table('favorites_quotes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('quote_id', db.Integer, db.ForeignKey('quote.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    image = db.Column(db.String(255), nullable=True)

    reviews = db.relationship('Review', backref='user', lazy=True)
    quotes = db.relationship('Quote', backref='user', lazy=True)



    @property
    def review_count(self):
        return len(self.reviews)

    @property
    def quote_count(self):
        return len(self.quotes)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    cover_url = db.Column(db.String(300))

    reviews = db.relationship('Review', backref='book', lazy=True)
    quotes = db.relationship('Quote', backref='book', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(100))
    image = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    liked_by_users = db.relationship('User', secondary=favorites_reviews, backref='favorite_reviews')

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100))
    book_title = db.Column(db.String(150))

    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=True)

    likes = db.Column(db.Integer, default=0)

    liked_by_users = db.relationship('User', secondary=favorites_quotes, backref='favorite_quotes')


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='posts')
