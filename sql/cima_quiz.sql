CREATE DATABASE IF NOT EXISTS cima_quiz
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE cima_quiz;



CREATE TABLE IF NOT EXISTS participantes (
    id_participante INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    equipo VARCHAR(50)
);



CREATE TABLE IF NOT EXISTS preguntas (
    id_pregunta INT AUTO_INCREMENT PRIMARY KEY,
    tema ENUM('HTML', 'MYSQL', 'PYTHON') NOT NULL,
    enunciado TEXT NOT NULL,
    opcion_a VARCHAR(255) NOT NULL,
    opcion_b VARCHAR(255) NOT NULL,
    opcion_c VARCHAR(255) NOT NULL,
    opcion_d VARCHAR(255) NOT NULL,
    respuesta_correcta ENUM('A', 'B', 'C', 'D') NOT NULL
);



CREATE TABLE IF NOT EXISTS intentos (
    id_intento INT AUTO_INCREMENT PRIMARY KEY,
    id_participante INT NOT NULL,
    fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    aciertos INT NOT NULL DEFAULT 0,
    total INT NOT NULL,
    puntaje INT NOT NULL DEFAULT 0,

    CONSTRAINT fk_intentos_participantes
        FOREIGN KEY (id_participante)
        REFERENCES participantes(id_participante),

    CONSTRAINT chk_total
        CHECK (total > 0),

    CONSTRAINT chk_puntaje
        CHECK (puntaje BETWEEN 0 AND 100)
);



TRUNCATE TABLE preguntas;



INSERT INTO preguntas (tema, enunciado, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta) VALUES
('HTML', '¿Qué etiqueta se usa para crear un enlace?', '<img>', '<a>', '<p>', '<link>', 'B'),
('HTML', '¿Qué etiqueta crea el título más grande de una página?', '<h6>', '<title>', '<h1>', '<head>', 'C'),
('HTML', '¿Qué etiqueta se usa para mostrar una imagen?', '<img>', '<image>', '<pic>', '<src>', 'A'),
('HTML', '¿Qué etiqueta crea una lista con viñetas?', '<ol>', '<ul>', '<li>', '<list>', 'B'),
('HTML', '¿Qué etiqueta se usa para crear un formulario?', '<input>', '<table>', '<div>', '<form>', 'D'),
('HTML', '¿Qué significan las siglas HTML?', 'HyperText Markup Language', 'High Text Machine Language', 'Home Tool Markup Language', 'HyperTransfer Mark Language', 'A'),
('HTML', '¿Qué etiqueta se usa para escribir un párrafo?', '<par>', '<text>', '<p>', '<paragraph>', 'C'),
('HTML', '¿Qué etiqueta da un salto de línea?', '<lb>', '<break>', '<nl>', '<br>', 'D'),
('HTML', '¿Qué etiqueta se usa para crear una tabla?', '<tr>', '<table>', '<td>', '<grid>', 'B'),
('HTML', '¿Cuál es la forma correcta de crear un botón de opción (radio)?', '<input type="radio">', '<input type="check">', '<radio>', '<select type="radio">', 'A');



INSERT INTO preguntas (tema, enunciado, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta) VALUES
('MYSQL', '¿Qué comando se usa para consultar datos de una tabla?', 'INSERT', 'DELETE', 'SELECT', 'UPDATE', 'C'),
('MYSQL', '¿Qué comando agrega un nuevo registro a una tabla?', 'INSERT INTO', 'SELECT', 'DROP', 'ORDER BY', 'A'),
('MYSQL', '¿Qué cláusula se usa para filtrar resultados?', 'ORDER BY', 'LIMIT', 'JOIN', 'WHERE', 'D'),
('MYSQL', '¿Qué cláusula ordena los resultados de una consulta?', 'GROUP', 'ORDER BY', 'WHERE', 'FROM', 'B'),
('MYSQL', '¿Para qué sirve una llave primaria?', 'Identificar de forma única cada registro', 'Guardar contraseñas', 'Borrar una tabla', 'Unir dos bases de datos', 'A'),
('MYSQL', '¿Qué comando modifica registros que ya existen?', 'MODIFY', 'UPDATE', 'CHANGE', 'ALTER', 'B'),
('MYSQL', '¿Qué comando elimina registros de una tabla?', 'REMOVE', 'DROP ROW', 'DELETE', 'CLEAR', 'C'),
('MYSQL', '¿Qué hace LIMIT 10 en una consulta?', 'Muestra solo los primeros 10 resultados', 'Borra 10 registros', 'Ordena 10 registros', 'Crea 10 tablas', 'A'),
('MYSQL', '¿Qué se usa para combinar datos de dos tablas?', 'LIMIT', 'WHERE', 'COUNT', 'JOIN', 'D'),
('MYSQL', '¿Qué función cuenta cuántos registros hay?', 'SUM', 'COUNT', 'MAX', 'AVG', 'B');



INSERT INTO preguntas (tema, enunciado, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta) VALUES
('PYTHON', '¿Qué función se usa para mostrar datos en pantalla en Python?', 'echo', 'print()', 'console.log()', 'printf', 'B'),
('PYTHON', '¿Cuál es la extensión correcta de un archivo de Python?', '.py', '.pyt', '.pyth', '.pt', 'A'),
('PYTHON', '¿Qué palabra se usa para crear una condición en Python?', 'if', 'when', 'condition', 'check', 'A'),
('PYTHON', 'En Python, ¿cómo se declara una lista?', 'lista = {}', 'lista = []', 'lista = ()', 'lista = < >', 'B'),
('PYTHON', '¿Qué hace el operador % en Python?', 'Calcula porcentaje', 'Divide dos números', 'Devuelve el residuo de una división', 'Multiplica', 'C'),
('PYTHON', '¿Python es un lenguaje compilado o interpretado?', 'Solo compilado', 'Interpretado', 'Solo de marcado', 'Solo de bases de datos', 'B'),
('PYTHON', '¿Qué ciclo se usa para repetir código un número determinado de veces?', 'for', 'repeat', 'loop', 'while only', 'A'),
('PYTHON', '¿Qué valor devuelve la expresión 3 > 5?', 'True', 'False', '0', 'Error', 'B'),
('PYTHON', '¿Cómo se pide un dato al usuario por teclado?', 'input()', 'get()', 'read()', 'scan()', 'A'),
('PYTHON', 'Completa el código para sumar números impares: if num % 2 ___ 0:', '==', '!=', '>', '<', 'B');



SELECT tema, COUNT(*) AS total FROM preguntas GROUP BY tema;