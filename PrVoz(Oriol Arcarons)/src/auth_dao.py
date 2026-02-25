import json
from src.conexion_db import ConexionDB

class AuthDAO:
    def __init__(self):
        self.db = ConexionDB().get_conexion()

    def registrar_usuario(self, username, passphrase, log_inicial):
        """Inserta usuario y crea el log inicial en formato JSONB"""
        cursor = self.db.cursor()
        try:
            # 1. Insertar en tabla de datos estáticos 
            cursor.execute(
                "INSERT INTO usuarios_voz (username, passphrase) VALUES (%s, %s) RETURNING id",
                (username, passphrase)
            )
            user_id = cursor.fetchone()[0]
            
            # 2. Insertar en tabla de datos dinámicos (JSONB) 
            cursor.execute(
                "INSERT INTO log_accesos_voz (usuario_id, resultado_json) VALUES (%s, %s)",
                (user_id, json.dumps(log_inicial))
            )
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error DAO: {e}")
            return False
        finally:
            cursor.close()

    def obtener_auditoria_critica(self):
        """Consulta avanzada que 'bucea' en el JSONB"""
        query = """
            SELECT u.username, l.resultado_json->>'status' as status
            FROM log_accesos_voz l
            JOIN usuarios_voz u ON l.usuario_id = u.id
            WHERE l.resultado_json->>'status' = 'FAIL'
            OR (l.resultado_json->>'confianza')::float < 0.6;
        """
        cursor = self.db.cursor()
        cursor.execute(query)
        return cursor.fetchall()