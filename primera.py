import hashlib
from random import randint
from flask import Flask, redirect, render_template, request, send_from_directory,session
from flaskext.mysql import MySQL
from datetime import datetime,timedelta
from cliente import Cliente
from articulos import Articulos
import os


empresa_app = Flask(__name__)
empresa_app.secret_key=str(randint(100000,999999))
empresa_app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=5)
mysql = MySQL()

empresa_app.config['MYSQL_DATABASE_HOST'] = 'localhost'
empresa_app.config['MYSQL_DATABASE_PORT'] = 3306
empresa_app.config['MYSQL_DATABASE_USER'] = 'root'
empresa_app.config['MYSQL_DATABASE_PASSWORD'] = ''
empresa_app.config['MYSQL_DATABASE_DB'] = 'empresa'
mysql.init_app(empresa_app)
cliente = Cliente(mysql)
misArticulos = Articulos(empresa_app,mysql)


CARPETAUP = os.path.join('uploads')
empresa_app.config['CARPETAUP']=CARPETAUP

@empresa_app.route('/uploads/<nombre>')
def uploads(nombre):
    return send_from_directory(empresa_app.config['CARPETAUP'],nombre)

@empresa_app.route("/")
def index():
    return render_template('index.html',msg="")

@empresa_app.route("/registrar")
def registar():
    return render_template("registrar.html")

@empresa_app.route("/guardarcliente", methods=['POST'])
def guardarcliente():
    id = request.form['id']
    nombre = request.form['nombre']
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    cifrada = hashlib.sha512(contraseña.encode("utf-8")).hexdigest()
    contraseña = cifrada
    if cliente.buscar(id):
        return render_template('registar.html',msg="Id ya existente")
    cliente.agregar([id,nombre,correo,contraseña])
    return redirect('/')

@empresa_app.route("/articulos")
def articulos():
    resultado = misArticulos.consultar()
    return render_template("/articulos.html",res=resultado)

@empresa_app.route("/login", methods=['POST'])
def login():
    id = request.form['id']
    contraseña = request.form['contraseña']
    cifrada = hashlib.sha512(contraseña.encode("utf-8")).hexdigest()
    sql = f"SELECT nombre FROM cliente WHERE id='{id}' AND contraseña='{cifrada}' AND activo=1"
    con = mysql.connect()
    cur = con.cursor()
    cur.execute(sql)
    resultado = cur.fetchall()
    con.commit()
    if len(resultado)==0:
        return render_template("index.html",msg="Credenciales incorrectas o usuario inactivo")
    else:
        session['loginCorrecto'] = True
        session['nombreUsuario'] = resultado[0][0]

        return render_template("articulos.html",nom=resultado[0][0])
    
@empresa_app.route("/agregararticulo")
def agregaarticulo():
    return render_template("agregaarticulo.html",msg="")

@empresa_app.route("/guardaarticulo",methods=['POST'])
def guardaarticulo():
    ida = request.form['ida']
    nombrea = request.form['nombrea']
    precio = request.form['precio']
    saldo = request.form['saldo']
    foto = request.files['foto']
    if misArticulos.buscar(ida):
        return render_template("agregaarticulo.html",msg="Id de artículo ya existente")
    ahora = datetime.now()
    nombref, fextension = os.path.splitext(foto.filename)
    nombreFoto = "A"+ahora.strftime("%Y%m%d%H%M%S")+fextension
    print(foto.filename,nombreFoto)
    foto.save("uploads/"+nombreFoto)
    print(nombreFoto)
    misArticulos.agregar([ida,nombrea,precio,saldo,nombreFoto])
    return redirect("/articulos")

@empresa_app.route('/borrararticulo/<ida>')
def borrararticulo(ida):
    misArticulos.borrar(ida)
    return redirect('/articulos')

@empresa_app.route('/editararticulo/<ida>')
def editararticulo(ida):
        articulo = misArticulos.buscar(ida)
        return render_template("editaarticulo.html",art=articulo[0])

@empresa_app.route('/actualizaarticulo',methods=['POST'])
def actualizaarticulo():
    ida = request.form['ida']
    nombrea = request.form['nombrea']
    precio = request.form['precio']
    saldo = request.form['saldo']
    foto = request.files['foto']
    art = [ida,nombrea,precio,saldo,foto]
    misArticulos.modificar(art)
    return redirect("/articulos")



if __name__=='__main__':
    empresa_app.run(host='0.0.0.0',debug=True,port=2645)