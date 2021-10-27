from os import error
import os
import re
from sqlite3.dbapi2 import IntegrityError
from flask import Flask,redirect,url_for, render_template, request , flash , session, send_file
from clases import Persona
import sqlite3
from sqlite3 import Error
from metodos import buscar_comentarios, editar_datos, eliminar_comentario, eliminar_datos, sql_consultar_datos_existentes, crear_nueva_persona, sql_consultar_datos_usuario, consulta_de_imagenes_general, crearComentario, eliminar_publicacion, busqueda_de_usuarios, buscar_foto_perfil
from werkzeug.security import generate_password_hash, check_password_hash
from s3_functions import upload_file, show_image, upload_file_foto_perfil, show_image_perfil
from werkzeug.utils import secure_filename
import time


app=Flask(__name__)

app.secret_key = "click10"

app.before_request
def session_management():
    session.permanent = True
    
UPLOAD_FOLDER = "uploads"
BUCKET = "click10"

@app.route("/")
@app.route('/Templates/pantallaInicio',methods=['GET','POST'])
def inicio():
    if request.method=='POST':
        # Handle POST Request here
        p = Persona('nombre', 'apellido', request.form['nombreDeUsuario'], 'email', request.form['contrasena'], False, False, False, "url", "txt")

        # 
        usuario_encontrado = sql_consultar_datos_existentes('click10.db', p.nombre_de_usuario)
        # print(check_password_hash(usuario_encontrado[0][0], p.contrasena))
        
        if usuario_encontrado:
            if check_password_hash(usuario_encontrado[0][0], p.contrasena):
                # return redirect('/Perfil/{}/'.format(p.nombre_de_usuario))
                #session.clear()
                session["user"] = p.nombre_de_usuario
                session["auth"] = 1
                user = session["user"]
                #return pantallaPerfilUsuario()
                return redirect("pantallaPerfilUsuario.html/"+user)
            else:
                error = 'Contraseña incorrecta'
                return render_template("pantallaInicio.html")
        else:
            return render_template("pantallaInicio.html")
        # except:
            # return render_template('pantallaRegistro.html')
    return render_template('pantallaInicio.html')

@app.route('/Templates/pantallaContrasena.html',methods=['GET','POST'])
def contrasena():
    if request.method=='POST':
        # Handle POST Request here
        pass
    return render_template('pantallaContrasena.html')

@app.route('/Templates/pantallaRegistro.html',methods=['GET','POST'])
def registro():
    if request.method=='POST':
        # Handle POST Request here
        p = Persona(request.form['nombre'], request.form['apellido'], request.form['nombreDeUsuario'], request.form['email'], request.form['contrasena'], False, False,False, "uploads/3ebd143ecb03c556219e59fb4bada120278f872e7dfdad4d04bcc74c82cd3575412.jpg", "")
        p.contrasena = generate_password_hash(p.contrasena)
        try:
            crear_nueva_persona('click10.db', p.nombre, p.apellido, p.nombre_de_usuario, p.email, p.contrasena)
            session["user"] = p.nombre_de_usuario
            session["auth"] = 1
            user = session["user"]
            return redirect("pantallaPerfilUsuario.html/"+user)
        except IntegrityError:

            return render_template("pantallaRegistro.html")
        
            
    return render_template("pantallaRegistro.html")

@app.route('/Templates/pantalla1GestionPerfil.html',methods=['GET','POST'])
def editar():
    # sesión
    try:
        user = session["user"]
        auth = session["auth"]
    except:
        user = "unknown"
        auth = 0
    if user == "unknown":
        return redirect(url_for('inicio'))
    
    consulta = sql_consultar_datos_usuario('click10.db', user)
    print(consulta)
    p = Persona(consulta[0][1], consulta[0][2], consulta[0][6], consulta[0][8], consulta[0][9], consulta[0][3], consulta[0][4], consulta[0][5], consulta[0][7], consulta[0][10])

    # url foto de perfil
    foto_man_o_nena = show_image_perfil(BUCKET, buscar_foto_perfil(user))


    if request.method=='POST':
        # Handle POST Request here
        pP = Persona(request.form['nombre'], request.form['apellido'], request.form['nombreDeUsuario'], request.form['email'], 'contrasena', False, False,False, "URL",request.form['biografia'] )
        try:
            editar_datos('click10.db', pP.nombre, pP.apellido, pP.email, pP.nombre_de_usuario, pP.biografia)
            return render_template("pantallaPerfilUsuario.html")
        except IntegrityError:
            return render_template("pantalla1GestionPerfil.html", foto_man_o_nena=foto_man_o_nena)
        
    return render_template("pantalla1GestionPerfil.html", user=user, nombre=p.nombre, apellido=p.apellido, email=p.email, biografia=p.biografia , foto_man_o_nena=foto_man_o_nena )

@app.route('/Templates/pantalla2GestionPerfil.html',methods=['GET','POST'])
def cambiarContrasena():
    # sesión
    try:
        user = session["user"]
        auth = session["auth"]
    except:
        user = "unknown"
        auth = 0
    if user == "unknown":
        return redirect(url_for('inicio'))
    
    # url foto de perfil
    foto_man_o_nena = show_image_perfil(BUCKET, buscar_foto_perfil(user))
    
    
    if request.method=='POST':
        # Handle POST Request here
        p = Persona('nombre', 'apellido', request.form['nombreDeUsuario'], 'email', request.form['contrasena'], False, False,False, "URL", "text")
        p.contrasena = generate_password_hash(p.contrasena)
        
        try:
            editar_datos('click10.db', p.contrasena, p.nombre_de_usuario)
            return render_template("pantallaPerfilUsuario.html")
        except IntegrityError:

            return render_template("pantalla2GestionPerfil.html", foto_man_o_nena=foto_man_o_nena)
    return render_template("pantalla2GestionPerfil.html", user=user, foto_man_o_nena=foto_man_o_nena)

@app.route('/Templates/pantalla3GestionPerfil.html',methods=['GET','POST'])
def eliminar():
    
    # sesión
    try:
        user = session["user"]
        auth = session["auth"]
    except:
        user = "unknown"
        auth = 0
    if user == "unknown":
        return redirect(url_for('inicio'))
    
    # url foto de perfil
    foto_man_o_nena = show_image_perfil(BUCKET, buscar_foto_perfil(user))
    
    
    if request.method=='POST':
        # Handle POST Request here
        p = Persona('nombre', 'apellido', request.form['nombreDeUsuario'], request.form['email'], 'contrasena', False, False,False, "URL", "txt")
       
        try:
            eliminar_datos('click10.db', p.nombre_de_usuario)
            return render_template("pantallaPerfilUsuario.html")
        except IntegrityError:

            return render_template("pantalla3GestionPerfil.html", foto_man_o_nena=foto_man_o_nena)
    return render_template("pantalla3GestionPerfil.html", user=user, foto_man_o_nena=foto_man_o_nena)


# -------RUTAS DASHBOARD ADMIN---------------
@app.route('/Templates/dashboardAdmin.html',methods=['GET','POST'])
def dashboardAdmin():
    if request.method=='POST':
        # Handle POST Request here
        pass
    return render_template("dashboardAdmin.html")


@app.route('/Templates/dashAdmin__Config.html',methods=['GET','POST'])
def dashAdmin__Config():
    if request.method=='POST':
        # Handle POST Request here
        pass
    return render_template("dashAdmin__Config.html")


@app.route('/Templates/dashAdmin__listaPubli.html',methods=['GET','POST'])
def dashAdmin__listaPubli():
    if request.method=='POST':
        # Handle POST Request here
        pass
    return render_template("dashAdmin__listaPubli.html")


@app.route('/Templates/dashAdmin__listaUsuario.html',methods=['GET','POST'])
def dashAdmin__listaUsuario():
    if request.method=='POST':
        # Handle POST Request here
        pass
    return render_template("dashAdmin__listaUsuario.html")



# -------RUTAS DASHBOARD SUPER ADMIN---------------
@app.route('/Templates/dashboardSuperadmin.html',methods=['GET','POST'])
def dashboardSuperAdmin():
    if request.method=='POST':
        # Handle POST Request here
        pass
    return render_template("dashboardSuperadmin.html")

@app.route('/Templates/dashSuperAdmin__listaAdmin.html',methods=['GET','POST'])
def dashSuperAdmin__listaAdmin():
    if request.method=='POST':
        # Handle POST Request here
        pass
    return render_template("dashSuperAdmin__listaAdmin.html")

@app.route('/Templates/dashSuperAdmin__listaPubli.html',methods=['GET','POST'])
def dashSuperAdmin__listaPubli():
    if request.method=='POST':
        # Handle POST Request here
        pass
    return render_template("dashSuperAdmin__listaPubli.html")

@app.route('/Templates/dashSuperAdmin__listaUsuario.html',methods=['GET','POST'])
def dashSuperAdmin__listaUsuario():
    if request.method=='POST':
        # Handle POST Request here
        pass
    return render_template("dashSuperAdmin__listaUsuario.html")
# -------RUTAS DASHBOARD SUPER ADMIN---------------

@app.route('/Templates/pantallaGestionPublicaciones.html',methods=['GET','POST'])
def pantallaGestionPublicaciones():
    try:
        user = session["user"]
        auth = session["auth"]
    except:
        user = "unknown"
        auth = 0
    # Hacer algo si auth == 0
    if user == "unknown":
        return redirect(url_for('inicio'))
    
    # crear variable lista de elementos
    
    lista = consulta_de_imagenes_general('click10.db')
    lista_comentarios = []
    for item in lista:
        lista_comentarios.append(buscar_comentarios(item[3]))
        # lista.append(list(item))

    print("La lista es --> ")
    print(lista)

    # disponer lista para LIFO
    lista.reverse()
    lista_comentarios.reverse()
    
    
    # crear variable de depliegue de imagenes
    elements = show_image(BUCKET, lista)
    
    # url foto de perfil
    foto_man_o_nena = show_image_perfil(BUCKET, buscar_foto_perfil(user))

    
    # manejar consultas POST
    if request.method=='POST':
        # Handle POST Request here
        
        # crear un nuevo comentario en la tabla si se llena un comentario en un formulario
        crearComentario(request.form['publicacion'], request.form['comentarista'],request.form['escribirComentario'])
    
        pass
    return render_template("pantallaGestionPublicaciones.html", elements=elements, user=user, lista=lista, lista_comentarios=lista_comentarios, foto_man_o_nena=foto_man_o_nena)

@app.route('/Templates/pantallaMensajes.html',methods=['GET','POST'])
def pantallaMensajes():
    
    try:
        user = session["user"]
        auth = session["auth"]
    except:
        user = "unknown"
        auth = 0
    if user == "unknown":
        return redirect(url_for('inicio'))
    
    # url foto de perfil
    foto_man_o_nena = show_image_perfil(BUCKET, buscar_foto_perfil(user))
            
    if request.method=='POST':
        # Handle POST Request here
        busqueda = request.form['q']
        resultados_parciales = busqueda_de_usuarios(busqueda)
        # print(resultados)
        resultados=[]
        for item in resultados_parciales:
            resultados.append([item[0], item[1]])
        for item in resultados:
            item[1] = show_image_perfil(BUCKET, buscar_foto_perfil(item[0]))
        
        
        
        return render_template("pantallaMensajes.html", resultados=resultados, user=user, foto_man_o_nena=foto_man_o_nena)
    return render_template("pantallaMensajes.html", foto_man_o_nena=foto_man_o_nena, user=user)

@app.route('/Templates/pantallaPerfilUsuario.html',methods=['GET','POST'])
@app.route('/Templates/pantallaPerfilUsuario.html/<user>',methods=['GET','POST'])
def pantallaPerfilUsuario(user = None):
    # if request.method=='POST':
    #     # Handle POST Request here
    #     pass
    # return render_template("pantallaPerfilUsuario.html")
    try:
        user = session["user"]
        auth = session["auth"]
    except:
        user = "unknown"
        auth = 0
    # Hacer algo si auth == 0
    if user == "unknown":
        return redirect(url_for('inicio'))
    # Por ejemplo cargar el template de login
    #return "<p>¡Hola %s!</p>" % user
    
    consulta = sql_consultar_datos_usuario('click10.db', user)
    # print(consulta)
    
    # url foto de perfil
    foto_man_o_nena = show_image_perfil(BUCKET, buscar_foto_perfil(user))
    
    p = Persona(consulta[0][1], consulta[0][2], consulta[0][6], consulta[0][8], consulta[0][9], consulta[0][3], consulta[0][4], consulta[0][5], consulta[0][7], consulta[0][10])
    
    return render_template("pantallaPerfilUsuario.html", user = user, biografia=p.biografia, foto_man_o_nena=foto_man_o_nena)

@app.route('/Templates/pantallaVistaPublicacion.html',methods=['GET','POST'])
def pantallaVistaPublicacion():
    if request.method=='POST':
        # Handle POST Request here
        pass
    return render_template("pantallaVistaPublicacion.html")

@app.route("/logout")
def logout():
  session.clear()
  session["user"] = "unknown"
  session["auth"] = 0
  return redirect(url_for('inicio'))

@app.route("/Templates/cargaDeImagenes.html", methods=['POST'])
def cargaDeImagenes():
        # sesión
    try:
        user = session["user"]
        auth = session["auth"]
    except:
        user = "unknown"
        auth = 0
    if user == "unknown":
        return redirect(url_for('inicio'))
    
    if request.method=='POST':
        # Handle POST Request here
        return render_template("cargaDeImagenes.html")
    return render_template("cargaDeImagenes.html")

@app.route("/Templates/cargaDeImagenDeUsuario.html", methods=['GET', 'POST'])
def cargaDeImagenesUsuario():
        # sesión
    try:
        user = session["user"]
        auth = session["auth"]
    except:
        user = "unknown"
        auth = 0
    if user == "unknown":
        return redirect(url_for('inicio'))
    
    if request.method=='POST':
        # Handle POST Request here
        return render_template("cargaDeImagenDeUsuario.html")
    return render_template("cargaDeImagenDeUsuario.html")

@app.route("/upload", methods=['POST'])
def upload():
        # sesión
    dir = 'uploads/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
        time.sleep(2)
    try:
        user = session["user"]
        auth = session["auth"]
    except:
        user = "unknown"
        auth = 0
    if user == "unknown":
        return redirect(url_for('inicio'))
    
    if request.method == "POST":
        f = request.files['file']
        descripcion = request.form['descripcion']
        f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        upload_file(f"{f.filename}", BUCKET, user, descripcion)
        # os.remove(f.filename)
        return redirect("/Templates/pantallaPerfilUsuario.html")
    
@app.route("/uploadFotoPerfil", methods=['POST'])
def uploadFotoPerfil():
        # borrar contenido carpeta uploads
    dir = 'uploads/'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
        time.sleep(2)
        
        # verificar sesion
    try:
        user = session["user"]
        auth = session["auth"]
    except:
        user = "unknown"
        auth = 0
    if user == "unknown":
        return redirect(url_for('inicio'))
    
    
    if request.method == "POST":
        f = request.files['file']
        # descripcion = request.form['descripcion']
        f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        upload_file_foto_perfil(f"{f.filename}", BUCKET, user)
        # os.remove(f.filename)
        return redirect("/Templates/pantallaPerfilUsuario.html")
    
@app.route("/pics")
def list():
    dummy = ["",""]
    contents = show_image(BUCKET, dummy)
    return render_template('collection.html', contents=contents)

@app.route("/Templates/eliminarPublicacion.html", methods=['POST'])
def eliminarPublicacion():
    if request.method == "POST":
        publicacion_a_elimiminar = request.form['publicacion_a_eliminar']
        eliminar_publicacion(publicacion_a_elimiminar)
        time.sleep(1)
        
        return redirect ("/Templates/pantallaGestionPublicaciones.html")
    return "..."

@app.route("/Templates/eliminarComentario.html", methods=['POST'])
def eliminarComentario():
    if request.method == "POST":
        comentario_a_elimiminar = request.form['comentario_a_eliminar']
        eliminar_comentario(comentario_a_elimiminar)
        time.sleep(1)
        
        return redirect ("/Templates/pantallaGestionPublicaciones.html")
    return "..."

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)
    
