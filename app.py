import yagmail as yagmail
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class Arquivo(db.Model):
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)

    __tablename__ = 'Arquivo'

    def __init__(self, name, data):
        self.name = name
        self.data = data


class Pessoa(db.Model):

    __tablename__ = 'Pessoa'

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    senha = db.Column(db.String)

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha


db.create_all()


@app.route('/')
def index():
    return render_template('Index.html')


@app.route('/crud')
def crud():
    return render_template('Crud.html')


@app.route('/insert')
def insert():
    return render_template('insert.html')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        if nome and email and senha:
            p = Pessoa(nome, email, senha)
            db.session.add(p)
            db.session.commit()

    return redirect(url_for('crud'))


@app.route("/list")
def list():
    pessoas = Pessoa.query.all()
    return render_template("list.html", pessoas=pessoas)


@app.route("/excluir/<int:id>")
def excluir(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()

    db.session.delete(pessoa)
    db.session.commit()

    pessoas = Pessoa.query.all()
    return render_template("list.html", pessoas=pessoas)


@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()

    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        if nome and email and senha:
            pessoa.nome = nome
            pessoa.email = email
            pessoa.senha = senha

            db.session.commit()

            return redirect(url_for("list"))

    return render_template("update.html", pessoa=pessoa)


@app.route("/upload_tp")
def upload_tp():
    return render_template('uploadFile.html')


@app.route("/upload", methods=['POST'])
def upload():
    file = request.files['inputFile']
    newfile = Arquivo(name=file.filename, data=file.read())
    db.session.add(newfile)
    db.session.commit()

    return render_template("uploadFile.html")


@app.route("/list_files")
def list_files():
    arquivos = Arquivo.query.all()
    return render_template("list_files.html", arquivos=arquivos)


@app.route("/excluir_img/<int:id>")
def excluir_img(id):
    file = Arquivo.query.filter_by(pid=id).first()

    db.session.delete(file)
    db.session.commit()

    arquivos = Arquivo.query.all()
    return render_template("list_files.html", arquivos=arquivos)


@app.route("/email/<int:id>")
def email(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()

    receiver = pessoa.email
    body = " :) "

    yag = yagmail.SMTP("befranceschina@gmail.com", 'P@ke1mon123')
    yag.send(
        to=receiver,
        subject="Email enviado com sucesso!!!",
        contents=body,
    )
    pessoa = Pessoa.query.all()
    return render_template('list.html', pessoa=pessoa)


if __name__ == '__main__':
    app.run()
