from conexion import consultar

def calificar(respuestas):
    aciertos = 0
    total = len(respuestas)

    for id_pregunta in respuestas:
        sql = "SELECT respuesta_correcta FROM preguntas WHERE id_pregunta = %s"
        resultado = consultar(sql, (id_pregunta,))

        if resultado:
            correcta = resultado[0]["respuesta_correcta"]
            if respuestas[id_pregunta] == correcta:
                aciertos = aciertos + 1

    if total == 0:
        return 0, 0, 0

    puntaje = round(aciertos / total * 100)
    return aciertos, total, puntaje

# Prueba (solo corre si ejecutas este archivo)
if __name__ == "__main__":
    mis_respuestas = {1: "", 2: "", 3: ""}
    aciertos, total, puntaje = calificar(mis_respuestas)
    print("Aciertos:", aciertos)
    print("Total:", total)
    print("Puntaje:", puntaje)