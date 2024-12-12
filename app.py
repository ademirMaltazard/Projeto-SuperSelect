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
            {'id':'01', 'name': 'teste1', 'description': 'teste', 'category': 'teste1', 'price': 'teste', 'expiration': 'teste'},
            {'id':'02', 'name': 'teste2', 'description': 'teste', 'category': 'teste2', 'price': 'teste', 'expiration': 'teste'},
            {'id':'03', 'name': 'teste3', 'description': 'teste', 'category': 'teste3', 'price': 'teste', 'expiration': 'teste'},
            {'id':'04', 'name': 'teste4', 'description': 'teste', 'category': 'teste4', 'price': 'teste', 'expiration': 'teste'},
            {'id':'05', 'name': 'teste5', 'description': 'teste', 'category': 'teste5', 'price': 'teste', 'expiration': 'teste'},
            {'id':'06', 'name': 'teste6', 'description': 'teste', 'category': 'teste6', 'price': 'teste', 'expiration': 'teste'},
            {'id':'07', 'name': 'teste7', 'description': 'teste', 'category': 'teste6', 'price': 'teste', 'expiration': 'teste'},
            {'id':'08', 'name': 'teste8', 'description': 'teste', 'category': 'teste6', 'price': 'teste', 'expiration': 'teste'},
            {'id':'09', 'name': 'teste9', 'description': 'teste', 'category': 'teste6', 'price': 'teste', 'expiration': 'teste'},
            {'id':'10', 'name': 'teste10', 'description': 'teste', 'category': 'teste6', 'price': 'teste', 'expiration': 'teste'},
            {'id':'11', 'name': 'teste11', 'description': 'teste', 'category': 'teste6', 'price': 'teste', 'expiration': 'teste'},
            {'id':'12', 'name': 'teste12', 'description': 'teste', 'category': 'teste6', 'price': 'teste', 'expiration': 'teste'},
            {'id':'13', 'name': 'teste13', 'description': 'teste', 'category': 'teste7', 'price': 'teste', 'expiration': 'teste'}
            ]



@app.route("/login")
def login():
    return render_template("login/index.html")

@app.route("/")
def home():
    print(user[1])
    if user[1].get('type') == 'admin':
        print('administrador')
    return render_template("Home/index.html", user= user[0])

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
                           user= user[0])


if __name__ == "__main__":
    app.run()
