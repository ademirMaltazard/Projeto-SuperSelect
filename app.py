import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from dotenv import load_dotenv
from database.db import db
from database.Models import *
import hashlib

app = Flask(__name__)
ln = LoginManager(app)
load_dotenv()

MYSQL_URI = os.getenv('MYSQL_URI')
APP_SECRET_KEY = os.getenv('APP_SECRET_KEY')
KEY_ADMIN = os.getenv('KEY_ADMIN')

app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = APP_SECRET_KEY
db.init_app(app)
ln.login_view = 'login'

# dados para testes
products = [{'id':'00', 'name': 'teste', 'description': 'teste', 'category': 'teste', 'price': 'teste', 'expiration': 'teste'}]

#criptografar senha
def hash(text):
    hash_obj = hashlib.sha256(text.encode('utf8'))
    return hash_obj.hexdigest()

@ln.user_loader
def userLoader(id):
    user = db.session.query(User).filter_by(id=id).first()
    return user

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = db.session.query(User).filter_by(email=email, senha=hash(password)).first()
        if not user:
            print('erro')
            alert = "Usuario ou senha invalidos!"
            return render_template('login/index.html', alert= alert)

        login_user(user)
        return redirect(url_for('home'))

    return render_template("login/index.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/registrar-se', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        userName = request.form.get('userName')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        code = request.form.get('code')
        type = 'comum'

        if code == KEY_ADMIN:
            type = 'admin'

        search_user = db.session.query(User).filter_by(email=email).first()
        if search_user:
            alert = 'email já cadastrado, realize o login!'
            return redirect(url_for('login', alert=alert))

        password_hash = hash(password)
        newUser = User(nome= name, senha=password_hash, nomeUsuario=userName, tipo=type, email=email, telefone=phone)
        db.session.add(newUser)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("register/index.html")


@app.route("/")
@login_required
def home():
    return render_template("Home/index.html")

@app.route("/admCadastrarProdutos", methods= ['GET', 'POST'])
def productRegister():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        price = request.form.get('price')
        expiration = request.form.get('expiration')
        #ID deve ser adicionada automatimente pelo banco de dados
        product = {'id' : '00', 'name': name, 'description': description, 'category': category, 'price': price, 'expiration': expiration}
        products.append(product)

    return render_template("productRegister/index.html", products= products, name= request.form.get('name'))

@app.route("/listagemProdutos", methods= ['GET', 'POST'])
def productsList():
    startPoint = 0
    totalPages = 0
    currentPage = request.args.get('currentPage', 1, type=int)

    if startPoint < 0: startPoint = 0

    for i in range(0, len(products)):
        if i % 5 == 0:
            totalPages+=1

    startPoint = (currentPage - 1) * 5

    productsToShow = products[startPoint : startPoint+5]
    print(len(products))
    return render_template("Products/index.html",
                           products= productsToShow,
                           length= len(products),
                           totalPages= totalPages,
                           currentPage= currentPage,)


if __name__ == "__main__":
    app.run(debug=True)
