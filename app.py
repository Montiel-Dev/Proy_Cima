"""Servidor web local de CIMA Quiz.

Une las páginas HTML con MySQL (conexion.py) y la calificación (calificacion.py).
Solo usa la librería estándar de Python (http.server); lo único que se instala
es mysql-connector-python.

Ejecutar:  python app.py   y abrir  http://localhost:8000
"""
import os
import sys
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

# conexion.py y config.py viven en modulo_m2/
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "modulo_m2"))

from conexion import consultar, guardar  # noqa: E402
from calificacion import calificar  # noqa: E402

PUERTO = 8000
NUM_PREGUNTAS = 10
MENSAJE_ERROR = "No se pudo completar la operación con la base de datos. Intenta de nuevo."


# ---------- plantilla base ----------
def pagina(titulo, contenido):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{escape(titulo)} - CIMA Quiz</title>
    <link rel="stylesheet" href="/estilos.css">
</head>
<body>
    <header>
        <h1>CIMA Quiz System</h1>
        <p>Sistema evaluador de conocimientos (HTML, MySQL y Python)</p>
    </header>
    <nav>
        <b>Ir a:</b>
        <a href="/">Inicio</a> |
        <a href="/ranking">Ranking</a>
    </nav>
    <hr>
    <section class="seccion">
{contenido}
    </section>
</body>
</html>"""


def pagina_error(mensaje, codigo=200):
    return codigo, pagina("Aviso", f"<h2>Aviso</h2><p>{escape(mensaje)}</p>"
                                   '<p><a href="/">Volver al inicio</a></p>')


# ---------- páginas ----------
def vista_inicio(aviso=""):
    extra = f'<p style="color:red;">{escape(aviso)}</p>' if aviso else ""
    return 200, pagina("Inicio", f"""
        <h2>Registro de Participante</h2>
        <p>Ingresa tus datos para comenzar:</p>
        {extra}
        <form method="post" action="/iniciar">
            <label>Nombre completo:</label><br>
            <input type="text" name="nombre" maxlength="100" required><br><br>
            <label>Equipo:</label><br>
            <input type="text" name="equipo" maxlength="50" placeholder="Equipo 2"><br><br>
            <button type="submit">Comenzar examen</button>
        </form>""")


def vista_cuestionario(id_participante):
    filas = consultar("SELECT nombre FROM participantes WHERE id_participante = %s",
                      (id_participante,))
    if not filas:
        return pagina_error("Participante no encontrado. Regístrate de nuevo.")

    # Ojo: NO se selecciona respuesta_correcta; la calificación es solo en Python.
    preguntas = consultar(
        "SELECT id_pregunta, tema, enunciado, opcion_a, opcion_b, opcion_c, opcion_d "
        "FROM preguntas ORDER BY RAND() LIMIT %s", (NUM_PREGUNTAS,))
    if not preguntas:
        return pagina_error(MENSAJE_ERROR)

    bloques = []
    ids = []
    for n, p in enumerate(preguntas, start=1):
        ids.append(str(p["id_pregunta"]))
        nombre_campo = f"p_{p['id_pregunta']}"
        opciones = ""
        for letra in "abcd":
            opciones += (f'<label><input type="radio" name="{nombre_campo}" value="{letra.upper()}"> '
                         f'{letra.upper()}) {escape(p["opcion_" + letra])}</label><br>\n')
        bloques.append(f"""
        <div class="bloque">
            <h3>{n}. [{escape(p["tema"])}]</h3>
            <p>{escape(p["enunciado"])}</p>
            {opciones}
        </div>""")

    return 200, pagina("Cuestionario", f"""
        <h2>Cuestionario</h2>
        <p>Participante: <b>{escape(filas[0]["nombre"])}</b>. Responde las {len(preguntas)} preguntas:</p>
        <form method="post" action="/calificar">
            <input type="hidden" name="id_participante" value="{int(id_participante)}">
            <input type="hidden" name="ids" value="{','.join(ids)}">
            {''.join(bloques)}
            <button type="submit">Enviar cuestionario</button>
        </form>""")


def vista_resultado(id_intento):
    filas = consultar(
        "SELECT i.aciertos, i.total, i.puntaje, i.fecha_hora, i.id_participante, p.nombre "
        "FROM intentos i JOIN participantes p ON p.id_participante = i.id_participante "
        "WHERE i.id_intento = %s", (id_intento,))
    if not filas:
        return pagina_error("No se encontró el resultado.")
    r = filas[0]
    return 200, pagina("Resultado", f"""
        <h2>Resultado</h2>
        <p>Participante: <b>{escape(r["nombre"])}</b></p>
        <p>Aciertos: <b>{r["aciertos"]}</b> de <b>{r["total"]}</b></p>
        <p>Puntaje: <b>{r["puntaje"]}</b> / 100</p>
        <p>Fecha: {escape(str(r["fecha_hora"]))}</p>
        <p><a href="/historial?id={r["id_participante"]}">Ver mi historial</a> |
           <a href="/cuestionario?id={r["id_participante"]}">Intentar de nuevo</a> |
           <a href="/ranking">Ver ranking</a></p>""")


def vista_historial(id_participante):
    filas = consultar(
        "SELECT i.id_intento, i.fecha_hora, i.aciertos, i.total, i.puntaje, p.nombre "
        "FROM intentos i JOIN participantes p ON p.id_participante = i.id_participante "
        "WHERE i.id_participante = %s ORDER BY i.fecha_hora DESC", (id_participante,))
    if filas is None:
        return pagina_error(MENSAJE_ERROR)
    if not filas:
        return pagina_error("Este participante todavía no tiene intentos.")
    renglones = "".join(
        f"<tr><td>{escape(str(f['fecha_hora']))}</td><td>{f['aciertos']}/{f['total']}</td>"
        f"<td>{f['puntaje']}</td></tr>" for f in filas)
    return 200, pagina("Historial", f"""
        <h2>Historial de {escape(filas[0]["nombre"])}</h2>
        <table border="1" cellpadding="8">
            <tr><th>Fecha</th><th>Aciertos</th><th>Puntaje</th></tr>
            {renglones}
        </table>""")


def vista_ranking():
    filas = consultar(
        "SELECT p.nombre, p.equipo, i.puntaje, i.aciertos, i.total, i.fecha_hora "
        "FROM intentos i JOIN participantes p ON p.id_participante = i.id_participante "
        "ORDER BY i.puntaje DESC, i.fecha_hora ASC LIMIT 10")
    if filas is None:
        return pagina_error(MENSAJE_ERROR)
    if filas:
        renglones = "".join(
            f"<tr><td>{n}</td><td>{escape(f['nombre'])}</td><td>{escape(f['equipo'] or '')}</td>"
            f"<td>{f['puntaje']}</td></tr>" for n, f in enumerate(filas, start=1))
    else:
        renglones = ('<tr><td colspan="4" align="center" style="color: gray;">'
                     "Aún no hay registros en el sistema.</td></tr>")
    return 200, pagina("Ranking", f"""
        <h2>Ranking Top 10</h2>
        <table border="1" cellpadding="8">
            <tr><th>Posición</th><th>Nombre</th><th>Equipo</th><th>Puntaje</th></tr>
            {renglones}
        </table>""")


# ---------- acciones (POST) ----------
def accion_iniciar(datos):
    nombre = datos.get("nombre", [""])[0].strip()
    equipo = datos.get("equipo", [""])[0].strip()
    if not nombre:
        return vista_inicio("Escribe tu nombre para continuar.")
    id_participante = guardar(
        "INSERT INTO participantes (nombre, equipo) VALUES (%s, %s)",
        (nombre[:100], equipo[:50] or None))
    if not id_participante:
        return pagina_error(MENSAJE_ERROR)
    return 303, f"/cuestionario?id={id_participante}"


def accion_calificar(datos):
    try:
        id_participante = int(datos.get("id_participante", [""])[0])
        ids = [int(x) for x in datos.get("ids", [""])[0].split(",") if x]
    except ValueError:
        return pagina_error("Datos del cuestionario inválidos.")
    if not ids:
        return pagina_error("Datos del cuestionario inválidos.")

    # Toda pregunta enviada cuenta en el total; sin respuesta = "" (incorrecta).
    respuestas = {}
    for id_pregunta in ids:
        valor = datos.get(f"p_{id_pregunta}", [""])[0].upper()
        respuestas[id_pregunta] = valor if valor in ("A", "B", "C", "D") else ""

    aciertos, total, puntaje = calificar(respuestas)
    if total == 0:
        return pagina_error(MENSAJE_ERROR)

    id_intento = guardar(
        "INSERT INTO intentos (id_participante, aciertos, total, puntaje) VALUES (%s, %s, %s, %s)",
        (id_participante, aciertos, total, puntaje))
    if not id_intento:
        return pagina_error(MENSAJE_ERROR)
    return 303, f"/resultado?id={id_intento}"


# ---------- servidor ----------
def id_de(consulta):
    try:
        return int(consulta.get("id", [""])[0])
    except ValueError:
        return None


class Manejador(BaseHTTPRequestHandler):
    def responder(self, resultado):
        codigo, cuerpo = resultado
        if codigo == 303:  # redirección
            self.send_response(303)
            self.send_header("Location", cuerpo)
            self.end_headers()
            return
        datos = cuerpo.encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def do_GET(self):
        url = urlparse(self.path)
        consulta = parse_qs(url.query)
        ruta = url.path
        try:
            if ruta == "/estilos.css":
                with open(os.path.join(BASE, "estilos.css"), "rb") as f:
                    datos = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/css; charset=utf-8")
                self.send_header("Content-Length", str(len(datos)))
                self.end_headers()
                self.wfile.write(datos)
                return
            if ruta == "/":
                return self.responder(vista_inicio())
            if ruta == "/ranking":
                return self.responder(vista_ranking())
            id_ = id_de(consulta)
            if ruta in ("/cuestionario", "/resultado", "/historial") and id_ is None:
                return self.responder(pagina_error("Falta el identificador."))
            if ruta == "/cuestionario":
                return self.responder(vista_cuestionario(id_))
            if ruta == "/resultado":
                return self.responder(vista_resultado(id_))
            if ruta == "/historial":
                return self.responder(vista_historial(id_))
            self.responder(pagina_error("Página no encontrada.", 404))
        except Exception:
            self.responder(pagina_error(MENSAJE_ERROR, 500))

    def do_POST(self):
        try:
            largo = int(self.headers.get("Content-Length", 0))
            datos = parse_qs(self.rfile.read(largo).decode("utf-8"))
            if self.path == "/iniciar":
                return self.responder(accion_iniciar(datos))
            if self.path == "/calificar":
                return self.responder(accion_calificar(datos))
            self.responder(pagina_error("Página no encontrada.", 404))
        except Exception:
            self.responder(pagina_error(MENSAJE_ERROR, 500))


if __name__ == "__main__":
    print(f"CIMA Quiz en http://localhost:{PUERTO}  (Ctrl+C para detener)")
    HTTPServer(("localhost", PUERTO), Manejador).serve_forever()