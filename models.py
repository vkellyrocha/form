from settings import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, name, username, password, email):
        self.name = name
        self.username = username
        self.password = password
        self.email = email

'''Modelo para o formulário'''

class Question_f(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('form.id'), nullable=False)
    question_text = db.Column(db.String(200), nullable=False)
    question_type = db.Column(db.String(50), nullable=False) 
    options = db.Column(db.Text, nullable=True)

    form = db.relationship('Form', backref='questions')
    responses = db.relationship('Response', backref='question')

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    questions_form = db.relationship('Question_f', backref='form')

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question_f.id'), nullable=False)
    answer = db.Column(db.Text, nullable=False)

    question_response = db.relationship('Question_f', backref='responses')

    