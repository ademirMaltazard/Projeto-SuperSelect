from flask import Flask, render_template, request

app = Flask(__name__)

# dados para testes
user = [{
    'name': 'Ademir',
    'type': 'admin',
    'username': 'Maltazard'
    },{
    'name': 'Zard',
    'type': 'usuario',
    'username': 'Zard'
    }
]

products = [{'id':'00', 'name': 'teste', 'description': 'teste', 'category': 'teste', 'price': 'teste', 'expiration': 'teste'},
            {'id':'00', 'name': 'teste', 'description': 'teste', 'category': 'teste', 'price': 'teste', 'expiration': 'teste'},
            {'id':'00', 'name': 'teste', 'description': 'teste', 'category': 'teste', 'price': 'teste', 'expiration': 'teste'}]



@app.route("/login")
def login():
    return render_template("login/index.html")

@app.route("/")
def home():
    print(user[1])
    if user[1].get('type') == 'admin':
        print('administrador')
    return render_template("Home/index.html", user= user[1])

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
    return render_template("Products/index.html", products= products)


if __name__ == "__main__":
    app.run()
