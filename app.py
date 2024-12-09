from flask import Flask, render_template, request

app = Flask(__name__)

produtos = []

@app.route("/login")
def login():
    return render_template("login/index.html")

@app.route("/")
def home():
    return render_template("Home/index.html")

@app.route("/admCadastrarProdutos", methods = ['GET', 'POST'])
def productRegister():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        price = request.form.get('price')
        expiration = request.form.get('expiration')
        produto = {'name': name, 'description': description, 'category': category, 'price': price, 'expiration': expiration}
        produtos.append(produto)

    return render_template("productRegister/index.html", produtos= produtos, name= request.form.get('name'))

if __name__ == "__main__":
    app.run()
