from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from database.db import db
from database.Models import *

app = Flask(__name__)
ln = LoginManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/superselect'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'chaveTeste'
db.init_app(app)
ln.login_view = 'login'

# dados para testes
products = [{'id':'00', 'name': 'teste', 'description': 'teste', 'category': 'teste', 'price': 'teste', 'expiration': 'teste'}]

@ln.user_loader
def userLoader(id):
    user = db.session.query(User).filter_by(id=id).first()
    return user

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = db.session.query(User).filter_by(email=email, senha=password).first()
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

@app.route("/")
@login_required
def home():
    return render_template("Home/index.html", user = {"type": "admin" })

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
                           currentPage= currentPage,
                           user= currentUser)


if __name__ == "__main__":
    app.run(debug=True)
