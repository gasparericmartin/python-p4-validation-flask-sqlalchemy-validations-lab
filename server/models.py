from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, string):
        if len(string) < 1:
            raise ValueError('Must have name')
        elif Author.query.filter_by(name=string).first():
            raise ValueError('Name must be unique')
        return string

    @validates('phone_number')
    def validate_phone_number(self, key, num):
        if len(num) != 10:
            raise ValueError('Number must contain exactly 10 digits')
        elif not int(num):
            raise ValueError('Must be all numbers')
        return num


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, string):
        if len(string) < 250:
            raise ValueError('Content must be at least 250 chars')
        return string

    @validates('summary')
    def validate_summary(self, key, string):
        if len(string) > 250:
            raise ValueError('Summary must be 250 chars max')
        return string

    @validates('category')
    def validate_category(self, key, string):
        categories = ['Fiction', 'Non-Fiction']
        if string not in categories:
            raise ValueError('Invalid category')

    @validates('title')
    def validate_title(self, key, string):
        keywords = ['Won\'t Believe', 'Secret', 'Top', 'Guess']
        for word in keywords:
            if re.search(rf'{word}', string):
                return string
        raise ValueError('Title must be click-baity')


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
