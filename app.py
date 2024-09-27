from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError, NoResultFound
from settings import url, db
from models import Response, User, Form, Question_f

app = Flask(__name__)
cors = CORS(app)
app.secret_key = b'ede658e5f53b85f2c4dbac1588c6328efab1d8a28160c6a9c15645a71577cb14'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1122vr@localhost:3306/db_form'
'''app.config['SQLALCHEMY_DATABASE_URI'] = url'''
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/hello/", methods=['GET', 'POST'])
def hello():
    if 'username' in session:
        return render_template('hello.html', name=session['username'])
    return render_template('hello.html')

@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html', msg="GET")
    elif request.method == "POST":
        print(request.form)
        if request.form.get("username") and request.form.get("password"):
            username = request.form.get('username')
            password = request.form.get("password")
            try:
                user = db.session.execute(db.select(User).filter_by(username=username, password=password)).scalar_one()
                if user is not None:
                    session['username'] = user.username
                    return render_template('hello.html', name=user.name, success='Usuário logado!')
                else:
                    return render_template('cadastro.html', error='Usuário não existe! Faça o cadastro!')
            except NoResultFound:
                print('No result found')
                return render_template('cadastro.html', fields=['nome', 'username', 'e-mail', 'senha'], error='Usuário não existe!')
            except Exception as e:
                print(e)
                return render_template('cadastro.html', fields=['nome', 'username', 'e-mail', 'senha'], error='Usuário não existe!')
            
        return render_template('login.html', error='Os campos não podem ser vazios!')

@app.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    fields = ['nome', 'username', 'email', 'password']
    if request.method == "GET":
        return render_template('cadastro.html', fields=fields)
    elif request.method =="POST":
        name = request.form.get("nome")
        password = request.form.get("password")
        email = request.form.get("email")
        username = request.form.get("username")
        if name and password and email and username:
            try:
                user = User(name=name, password=password, email=email, username=username)
                db.session.add(user)
                db.session.commit()
                return render_template('login.html', success='Usuário cadastrado com sucesso!')
            except IntegrityError as ie:
                print(ie)
                return render_template('cadastro.html', fields=fields, error='Usuário já cadastrado!')
            except Exception as e:
                print(e)
                return render_template('cadastro.html', fields=fields, error='Usuário não foi cadastrado!')
        return render_template('cadastro.html', fields=fields, error='Os campos não podem ser vazios!')
        
@app.route('/logout/')
def logout():
    session.pop("username, None")
    return render_template('hello.html', success='Usuário deslogado!')

@app.route('/')
def index():
    forms = Form.query.all()
    return render_template('index.html', forms=forms)

@app.route('/form', methods=['GET', 'POST'])
def create_form():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_form = Form(title=title, description=description)
        db.session.add(new_form)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('form.html')

@app.route('/form/<int:form_id>', methods=['GET', 'POST'])
def edicao_form(form_id):
    form = Form.query.get_or_404(form_id)
    if request.method == 'POST':
        form.title = request.form['title']
        form.description = request.form['description']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edicao_form.html', form=form)

@app.route('/form/<int:form_id>/add_question', methods=['POST'])
def add_question(form_id):
    form = Form.query.get_or_404(form_id)
    question_text = request.form['question_text']
    question_type = request.form['question_type']
    options = request.form.get('options', None)

    new_question = Question_f(
        question_text=question_text, 
        question_type=question_type, 
        options=options, 
        form_id=form_id)
    db.session.add(new_question)
    db.session.commit()
    return redirect(url_for('edicao_form', form_id=form_id))

@app.route('/form/<int:form_id>/submit', methods=['POST'])
def submit_response(form_id):
    form = Form.query.get_or_404(form_id)
    for question in form.questions_form:
        answer = request.form.get(f'question_{question.id}')
        if answer:
            if question.question_type == 'short' and len(answer) > 200:
                return "Erro: Resposta muito longa para a pergunta"
            if question.question_type == 'long' and not answer:
                return "Erro: Campo precisa de resposta", 400
            new_response = Response(question_id=question.id, answer=answer)
            db.session.add(new_response)
    db.session.commit()
    return redirect(url_for('view_responses', form_id=form_id))
    
@app.route('/form/<int:form_id>/responses')
def view_responses(form_id):
    form = Form.query.get_or_404(form_id)
    responses = {q.id: q.responses for q in form.questions_forms}
    return render_template('responses.html', form=form, responses=responses)


