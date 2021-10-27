import datetime
import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import Cursor

def sql_connection(db):
    try:
        con = sqlite3.connect(db)
        return con;
    except Error:
        print(Error)
        
def sql_consultar_datos_existentes(bd, nombreDeUsuario):
    strsql = "select contrasena from persona where nombreDeUsuario='{0}';".format(nombreDeUsuario)
    con = sql_connection(bd)
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    registros_existentes = cursorObj.fetchall()
    return registros_existentes

def crear_nueva_persona(bd, nombre, apellido, nombreDeUsuario, email, contrasena):
    #crear prepared statement
    strsql = "insert into persona (nombre, apellido, permisoAdmin, permisoSuperadmin, usuarioActivo, nombreDeUsuario, URL_fotoDePerfil, email, contrasena, biografia) values('{0}', '{1}', {2}, {3}, {4}, '{5}', '{6}', '{7}', '{8}', 'Edita tu perfil para agregar tu biografía.')".format(nombre, apellido, 'FALSE', 'FALSE', 'TRUE', nombreDeUsuario, 'uploads/3ebd143ecb03c556219e59fb4bada120278f872e7dfdad4d04bcc74c82cd3575412.jpg', email, contrasena)
    #conexion
    con = sql_connection(bd)
    #variable para ejecutar queries
    cursor_obj = con.cursor()
    #ejecutar query
    cursor_obj.execute(strsql)
    #actualizar base de datos
    con.commit()
    con.close()
    
def sql_consultar_datos_usuario(bd, nombreDeUsuario):
    strsql = "select * from persona where nombreDeUsuario='{0}';".format(nombreDeUsuario)
    con = sql_connection(bd)
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    registros_existentes = cursorObj.fetchall()
    return registros_existentes
       
def editar_datos(bd, nombre, apellido, email, nombre_de_usuario, biografia):
    strsql = "update persona set nombre='{0}', apellido='{1}', email='{2}', biografia='{4}' where nombreDeUsuario='{3}';".format(nombre,apellido,email,nombre_de_usuario, biografia)
    con = sql_connection(bd)
    cursor_obj = con.cursor()
    cursor_obj.execute(strsql)
    con.commit()
    con.close()
    

def eliminar_datos(bd, nombreDeUsuario):
    strsql = "update persona set usuarioActivo=0 where nombreDeUsuario='{0}';".format(nombreDeUsuario)
    con = sql_connection(bd)
    cursor_obj = con.cursor()
    cursor_obj.execute(strsql)
    con.commit()
    con.close()

def cambiar_contrasena(bd, contrasena, nombreDeUsuario):
    strsql = "update persona set contrasena='{0}' where nombreDeUsuario='{1}';".format(contrasena, nombreDeUsuario)
    con = sql_connection(bd)
    cursor_obj = con.cursor()
    cursor_obj.execute(strsql)
    con.commit()
    con.close()
    
def crear_nueva_publicacion(bd, usuario, timestamp, ULR_imagen, descripcion):
    #crear prepared statement
    strsql = "insert into publicaciones (ID_usuario, timeStampImagenes, URL_imagen, descripcion ) values({0}, {1}, '{2}', '{3}')".format(usuario, timestamp, ULR_imagen,descripcion)
    #conexion
    con = sql_connection(bd)
    #variable para ejecutar queries
    cursor_obj = con.cursor()
    #ejecutar query
    cursor_obj.execute(strsql)
    #actualizar base de datos
    con.commit()
    con.close()
 
def cargar_foto_usuario(bd, ID_usuario, URL_imagen):
        #crear prepared statement
    strsql = "UPDATE persona SET URL_fotoDePerfil='{0}' WHERE ID_usuario='{1}'".format(URL_imagen,ID_usuario)
    #conexion
    con = sql_connection(bd)
    #variable para ejecutar queries
    cursor_obj = con.cursor()
    #ejecutar query
    cursor_obj.execute(strsql)
    #actualizar base de datos
    con.commit()
    con.close()   


def obtener_id_usuario(bd, usuario):
    strsql = "select ID_usuario from persona where nombreDeUsuario='{0}';".format(usuario)
    con = sql_connection(bd)
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    registros_existentes = cursorObj.fetchall()
    return registros_existentes[0][0]
    
# funcion para cargar las imagenes encontradas en la BDD
def consulta_de_imagenes_general(bd):
    strsql = "select publicaciones.URL_imagen, publicaciones.descripcion, persona.nombreDeUsuario, publicaciones.ID_publicacion from publicaciones INNER JOIN persona ON publicaciones.ID_usuario=persona.ID_usuario;"
    con = sql_connection(bd)
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    registros_existentes = cursorObj.fetchall()
    return registros_existentes
    
def crearComentario(ID_publicacion, user, comentario ):
    ID_usuario_comentante = obtener_id_usuario('click10.db', user)
    #crear prepared statement
    ts = datetime.datetime.now().timestamp()
    strsql = "insert into comentarios (timeStampComentario, ID_publicacion, ID_usuario_comentante, comentario) values({0}, {1}, {2}, '{3}')".format(ts, ID_publicacion, ID_usuario_comentante,comentario)
    #conexion
    con = sql_connection('click10.db')
    #variable para ejecutar queries
    cursor_obj = con.cursor()
    #ejecutar query
    cursor_obj.execute(strsql)
    #actualizar base de datos
    con.commit()
    con.close()
    
def buscar_comentarios(ID_publicacion):
    
    strsql = "select comentarios.comentario, persona.nombreDeUsuario, comentarios.ID_publicacion, comentarios.ID_comentario from comentarios INNER JOIN persona ON  ID_usuario_comentante=ID_usuario where ID_publicacion={}".format(ID_publicacion)
    con = sql_connection('click10.db')
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    registros_existentes = cursorObj.fetchall()
    return registros_existentes

def eliminar_comentario(ID_comentario):
    strsql = "DELETE FROM comentarios WHERE ID_comentario={}".format(ID_comentario)
    con = sql_connection('click10.db')
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    #actualizar base de datos
    con.commit()
    con.close() 
    

def eliminar_publicacion(id_publicacion):
    strsql = "DELETE FROM publicaciones WHERE ID_publicacion={}".format(id_publicacion)
    con = sql_connection('click10.db')
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    #actualizar base de datos
    con.commit()
    con.close()
    
    
def busqueda_de_usuarios(busqueda):
    strsql = "SELECT nombreDeUsuario, URL_fotoDePerfil FROM persona WHERE nombre LIKE  '%{0}%' OR apellido LIKE '%{0}%' OR nombreDeUsuario LIKE '%{0}%' OR email LIKE '%{0}%';".format(busqueda)
    con = sql_connection('click10.db')
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    registros_existentes = cursorObj.fetchall()
    return registros_existentes

# print(busqueda_de_usuarios('cam'))

def buscar_foto_perfil(user):
    strsql = "select URL_fotoDePerfil from persona where nombreDeUsuario='{0}';".format(user)
    con = sql_connection('click10.db')
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    registros_existentes = cursorObj.fetchall()
    return registros_existentes[0][0]
