from flask import render_template, redirect, request, session, flash
from flask_app import app, bcrypt
from flask_app.models.usuario import Usuario

@app.route("/")
def index():
    if 'usuario_id' in session:
        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/registro")
def vista_registro():
    if 'usuario_id' in session:
        return redirect("/dashboard")
    return render_template("registro.html")

@app.route("/registrar", methods=["POST"])
def registrar():
    pass_hasheado = bcrypt.generate_password_hash(request.form['password'])

    formulario = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email'],
        "password": pass_hasheado
    }

    nuevo_id = Usuario.guardar(formulario)
    session['usuario_id'] = nuevo_id

    return redirect("/dashboard")

@app.route("/login", methods=["POST"])
def login():
    usuario = Usuario.buscar_por_email(request.form)

    if not usuario:
        flash("E-mail no registrado", "login")
        return redirect("/")

    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Password incorrecto", "login")
        return redirect("/")

    session['usuario_id'] = usuario.id
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if 'usuario_id' not in session:
        return redirect("/")

    datos = {"id": session['usuario_id']}
    usuario_actual = Usuario.buscar_por_id(datos)

    return render_template("dashboard.html", usuario=usuario_actual)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
