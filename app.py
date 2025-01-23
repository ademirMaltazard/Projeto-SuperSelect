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
    user = User.query.filter_by(id=id).first()
    return user

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email, senha=hash(password)).first()
        if not user:
            print('erro')
            alert = "Usuario ou senha invalidos!"
            return render_template('login/index.html', email=email, alert= alert)

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

        search_user = User.query.filter_by(email=email).first()
        if search_user:
            alert = 'Email já cadastrado, realize o login!'
            return redirect(url_for('login', alert=alert))

        password_hash = hash(password)
        newUser = User(nome=name, senha=password_hash, nomeUsuario=userName, tipo=type, email=email, telefone=phone)
        db.session.add(newUser)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("register/index.html")


@app.route("/")
@login_required
def home():
    return render_template("Home/index.html", pageTitle=' - Home')

@app.route("/admCadastrarProdutos", methods= ['GET', 'POST'])
@login_required
def registerProduct():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        price = request.form.get('price')
        expiration = request.form.get('expiration')
        quantity = request.form.get('quantity')
        prodType = request.form.get('prodType')

        #ID deve ser adicionada automatimente pelo banco de dados
        newProduct = Product(nome=name, descricao=description,categoria=category, preco=price, validade=expiration, quantidade=quantity, tipo=prodType)

        db.session.add(newProduct)
        db.session.commit()

        return redirect(url_for('registerProduct'))

    return render_template("registerProduct/index.html", products= products, name= request.form.get('name'), pageTitle=' - Registrar produto')

@app.route("/listagemProdutos", methods= ['GET', 'POST'])
@login_required
def productsList():
    products = Product.query.all()

    startPoint = 0
    totalPages = 0
    currentPage = request.args.get('currentPage', 1, type=int)

    if startPoint < 0: startPoint = 0

    for i in range(0, len(products)):
        if i % 5 == 0:
            totalPages+=1

    startPoint = (currentPage - 1) * 5

    productsToShow = products[startPoint : startPoint+5]
    return render_template("Products/index.html",
                           products= productsToShow,
                           length= len(products),
                           totalPages= totalPages,
                           currentPage= currentPage,
                           pageTitle=' - Produtos')

@app.route('/atualizar-produto/<int:id>', methods=['GET', 'POST'])
@login_required
def editProduct(id):
    product = Product.query.filter_by(id=id).first()

    if request.method == 'POST':
        product.nome = request.form.get('name')
        product.descricao = request.form.get('description')
        product.categoria= request.form.get('category')
        product.preco = request.form.get('price')
        product.validade = request.form.get('expiration')
        product.quantidade = request.form.get('quantity')
        product.tipo = request.form.get('prodType')

        db.session.commit()
        return redirect(url_for('productsList'))

    return render_template('editProduct/index.html', product= product, pageTitle= ' - Editar Produto')


@app.route('/excluir-produto/<int:id>')
@login_required
def deleteProduct(id):
    productForDelete = Product.query.filter_by(id=id).first()

    db.session.delete(productForDelete)
    db.session.commit()
    return redirect(url_for('productsList'))


@app.route('/comentarios', methods=['GET', 'POST'])
@login_required
def comments():
    comments = Comment.query.all()

    return render_template('Comments/index.html', pageTitle=' - Comentários', comments= comments)


@app.route('/historico')
@login_required
def history():
    historyList = []
    products = Product.query.all()

    for product in products:
        commentsList= []
        comments = Comment.query.filter_by(produtoID = product.id).all()

        for comment in comments:
            user = User.query.filter_by(id = comment.usuarioID).first()
            print('user', user.nome)
            print('comment', comment.comentario)
            print('date', comment.dataHora)
            objComment = {
                'comment': comment.comentario,
                'user': user.nome,
                'date': comment.dataHora
            }
            commentsList.append(objComment)

        # for comment in commentsList:
        #     print()
        #     print('produto:', product.nome)
        #     print('comentario:',comment.comentario, comment.dataHora)

        objProduct = {
            'nameProduto': product.nome,
            'comentarios': commentsList
        }
        historyList.append(objProduct)
    for i in range(len(historyList)):
        for i in historyList[i].get('comentarios'):
            print('indice: ', i)
            print('date', i.get('date'))

    return render_template('history/index.html', pageTitle=' - Histórico')

if __name__ == "__main__":
    app.run(debug=True)
