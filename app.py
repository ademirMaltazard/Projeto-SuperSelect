from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/login")
def login():
    return render_template("login/index.html")

@app.route("/")
def home():
    return render_template("Home/index.html")

@app.route("/admCadastrarProdutos")
def productRegister():
    return render_template("productRegister/index.html")

if __name__ == "__main__":
    app.run()
