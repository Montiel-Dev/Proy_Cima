CREATE DATABASE IF NOT EXISTS cima_quiz
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE cima_quiz;

-- 1. Tabla de participantes
CREATE TABLE IF NOT EXISTS participantes (
    id_participante INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    equipo VARCHAR(50)
);

-- 2. Tabla de preguntas
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

-- 3. Tabla de intentos
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
