import mysql.connector
import config

def conectar():
    return mysql.connector.connect(
        host=config.host,
        user=config.usuario,
        password=config.password,
        database=config.base_datos
    )

def consultar(sql, datos=()):
    try:
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, datos)
        resultado = cursor.fetchall()
        conexion.close()
        return resultado
    
    except Exception as e:
        print("error", e)
        return None

def guardar(sql, datos=()):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute(sql, datos)
        conexion.commit()
        id_nuevo = cursor.lastrowid
        conexion.close()
        return id_nuevo
    except:
        return None

if __name__=="__main__": 
    print(consultar("SELECT COUNT(*) as total from preguntas"))
