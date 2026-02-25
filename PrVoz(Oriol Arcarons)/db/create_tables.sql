-- 1. Tabla de Usuarios (Datos Relacionales Estáticos) [cite: 79]
CREATE TABLE IF NOT EXISTS usuarios_voz (
    id SERIAL PRIMARY KEY, 
    username VARCHAR(50) UNIQUE NOT NULL, 
    passphrase TEXT NOT NULL, 
    intentos_fallidos INT DEFAULT 0, 
    bloqueado_hasta TIMESTAMP NULL 
);

-- 2. Tabla de Logs de Acceso (Datos Objeto-Relacionales Dinámicos con JSONB) 
CREATE TABLE IF NOT EXISTS log_accesos_voz (
    id SERIAL PRIMARY KEY, 
    usuario_id INT REFERENCES usuarios_voz(id) ON DELETE CASCADE, 
    fecha_intento TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    resultado_json JSONB NOT NULL 
);