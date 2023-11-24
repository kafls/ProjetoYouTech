from flask import Flask, render_template, request, redirect, session
import os
import sqlite3 as sql
import uuid #gera um núme aleatório único para o nome das imagens

app = Flask(__name__)
app.secret_key = "techyouequipe2k23"

usuario = "usuario"
senha = "senha0521"
login = False

def verifica_sessao():
    if "login" in session and session["login"]:
        return True
    else:
        return False

def conecta_database():
    conexao = sql.connect("db_youtech.db")
    conexao.row_factory = sql.Row 
    return conexao

def iniciar_db():
    conexao = conecta_database()
    with app.open_resource('esquema.sql', mode='r') as comandos:
        conexao.cursor().executescript(comandos.read())
    conexao.commit()
    conexao.close()

@app.route("/")
def index():
    iniciar_db()
    conexao = conecta_database()
    title = "Home"
    vagas = conexao.execute('SELECT * FROM vagas ORDER BY id_vaga DESC').fetchall()
    conexao.close()
    return render_template("home.html", title=title, vagas=vagas)

#LOGIN
@app.route("/login")
def login():
    return render_template("login.html")

#ROTA PARA VERIFICAR O ACESSO
@app.route("/acesso", methods=['POST'])
def acesso():
    global login, senha
    usuario_informado = request.form["usuario"]
    senha_informada = request.form["senha"]
    if usuario == usuario_informado and senha == senha_informada:
        session["login"] = True
        return redirect('/adm') #homepage
    else:
        return render_template("login.html", msg="Usuário/Senha estão incorretos!")

#ROTA DE LOGOFF
@app.route("/logout")
def logout():
    global login
    login = False
    session.clear()
    return redirect('/')

#ROTA PARA PÁG ADM
@app.route("/adm")
def adm():
    if verifica_sessao():
        iniciar_db()
        conexao = conecta_database()
        vagas = conexao.execute('SELECT * FROM vagas ORDER BY id_vaga DESC').fetchall()
        conexao.close()
        title = "Administração"
        return render_template("adm.html", vagas=vagas, title=title)
    else:
        return redirect("/login")

#CADASTRAR VAGAS
@app.route("/cadvagas")
def cadvagas():
    if verifica_sessao():
        title = "Cadastro de produto"
        return render_template("cadvagas.html", title=title)
    else:
        return redirect("/login")
    
#ROTA DA PÁGINA DE CADASTRO NO BANCO
@app.route("/cadastro", methods=["post"])
def cadastro():
    if verifica_sessao():
        cargo_vaga=request.form['cargo_vaga']
        tipo_vaga=request.form['tipo_vaga']
        requisitos_vaga=request.form['requisitos_vaga']
        salario_vaga=request.form['salario_vaga']
        local_vaga=request.form['local_vaga']
        email_vaga=request.form['email_vaga']
        img_vaga=request.files['img_vaga']
        id_foto=str(uuid.uuid4().hex)
        filename=id_foto+local_vaga+'.png'
        img_vaga.save("static/img/vagas/"+filename)
        conexao = conecta_database()
        conexao.execute('INSERT INTO vagas (cargo_vaga, tipo_vaga, requisitos_vaga, salario_vaga, local_vaga, email_vaga, img_vaga) VALUES (?, ?, ?, ?, ?, ?, ?)', (cargo_vaga, tipo_vaga, requisitos_vaga, salario_vaga, local_vaga, email_vaga, filename))
        conexao.commit()
        conexao.close()
        return redirect("/adm")
    else:
        return redirect("/login")

#EXCLUIR VAGA
@app.route("/excluir/<id_vaga>")
def excluir(id_vaga):
    if verifica_sessao():
        id_vaga = int(id_vaga)
        conexao = conecta_database()
        produto = conexao.execute('SELECT * FROM vagas WHERE id_vaga = ?', (id_vaga,)).fetchall()
        filename_old = produto[0]['img_vaga']
        excluir_arquivo = "static/img/vagas/"+filename_old
        os.remove(excluir_arquivo)
        conexao.execute('DELETE FROM vagas WHERE id_vaga = ?', (id_vaga,))
        conexao.commit()
        conexao.close()
        return redirect('/adm')
    else:
        return redirect("/login")

#ROTA EDITAR VAGA
@app.route("/editvagas/<id_vaga>")
def editar(id_vaga):
    if verifica_sessao():
        iniciar_db()
        conexao = conecta_database()
        vagas = conexao.execute('SELECT * FROM vagas WHERE id_vaga = ?', (id_vaga,)).fetchall()
        conexao.close()
        title = "Edição de vagas"
        return render_template("editvagas.html", vagas=vagas, title=title)
    else:
        return redirect("/login")

#EDITAR VAGAS
@app.route("/editarvagas", methods=['POST'])
def editvaga():
    id_vaga=request.form['id_vaga']
    cargo_vaga=request.form['cargo_vaga']
    tipo_vaga=request.form['tipo_vaga']
    requisitos_vaga=request.form['requisitos_vaga']
    salario_vaga=request.form['salario_vaga']
    local_vaga=request.form['local_vaga']
    email_vaga=request.form['email_vaga']
    img_vaga=request.files['img_vaga']
    conexao = conecta_database()
    if img_vaga:
        vaga = conexao.execute('SELECT * FROM vagas WHERE id_vaga = ?', (id_vaga,)).fetchall()
        filename = vaga[0]['img_vaga']
        img_vaga.save("static/img/vagas"+filename)
        conexao.execute('UPDATE vagas SET cargo_vaga = ?, tipo_vaga = ?, requisitos_vaga = ?, salario_vaga = ?, local_vaga = ?, email_vaga = ?, img_vaga = ? WHERE id_vaga = ?', (cargo_vaga, tipo_vaga, requisitos_vaga, salario_vaga, local_vaga, email_vaga,  filename, id_vaga))
    else:
        conexao.execute('UPDATE vagas SET cargo_vaga = ?, tipo_vaga = ?, requisitos_vaga = ?, salario_vaga = ?, local_vaga = ?, email_vaga = ? WHERE id_vaga = ?', (cargo_vaga, tipo_vaga, requisitos_vaga, salario_vaga, local_vaga, email_vaga, id_vaga))
    conexao.commit()
    conexao.close()
    return redirect('/adm')
    
#ROTA VER VAGA
@app.route("/vervaga/<id_vaga>")
def vervagas(id_vaga):
    iniciar_db()
    id_vaga = int(id_vaga)
    conexao = conecta_database()
    vagas = conexao.execute('SELECT * FROM vagas WHERE id_vaga = ?', (id_vaga,)).fetchall()
    title = "Ver vaga"
    conexao.close()
    return render_template("saibamais.html", vagas=vagas, title=title)
    
  
app.run(debug=True)