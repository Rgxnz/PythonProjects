import json
from src.conexion_db import ConexionDB

class AuthDAO:
    def __init__(self):
        self.db_manager = ConexionDB()

    def registrar_usuario(self, username, phrase, confianza):
        conn = self.db_manager.get_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios_voz (username, passphrase) VALUES (%s, %s) RETURNING id", (username, phrase))
            u_id = cursor.fetchone()[0]
            log = {"status": "REGISTERED", "confianza": confianza}
            cursor.execute("INSERT INTO log_accesos_voz (usuario_id, resultado_json) VALUES (%s, %s)", (u_id, json.dumps(log)))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error DAO: {e}")
            return False

    def validar_login(self, username, frase_voz, confianza):
        conn = self.db_manager.get_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, passphrase, intentos_fallidos FROM usuarios_voz WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user: return "USER_NOT_FOUND"
        u_id, real_phrase, intentos = user
        if intentos >= 3: return "USER_LOCKED"

        if frase_voz == real_phrase.lower():
            cursor.execute("UPDATE usuarios_voz SET intentos_fallidos = 0 WHERE id = %s", (u_id,))
            log = {"status": "OK", "confianza": confianza}
            res = "SUCCESS"
        else:
            nuevos_intentos = intentos + 1
            cursor.execute("UPDATE usuarios_voz SET intentos_fallidos = %s WHERE id = %s", (nuevos_intentos, u_id))
            log = {"status": "FAIL", "confianza": confianza, "intentos_restantes": 3 - nuevos_intentos}
            res = "WRONG" if nuevos_intentos < 3 else "USER_LOCKED"

        cursor.execute("INSERT INTO log_accesos_voz (usuario_id, resultado_json) VALUES (%s, %s)", (u_id, json.dumps(log)))
        conn.commit()
        return res

    def obtener_auditoria(self):
        conn = self.db_manager.get_conexion()
        cursor = conn.cursor()
        query = """
            SELECT u.username, l.fecha_intento, l.resultado_json->>'status', l.resultado_json->>'confianza'
            FROM log_accesos_voz l JOIN usuarios_voz u ON l.usuario_id = u.id
            ORDER BY l.fecha_intento DESC LIMIT 10
        """
        cursor.execute(query)
        return cursor.fetchall()