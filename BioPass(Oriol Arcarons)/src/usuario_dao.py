from src.conexion_db import DBConnection

class UsuarioDAO:
    def __init__(self):
        pass

    def registrar_usuario(self, nombre, foto_bytes, cara_bytes):
        """
        Registra un usuario y sus imágenes en la base de datos.
        Lanza automáticamente una verificación del tamaño de los datos guardados.
        """
        conn = DBConnection.get_connection()
        
        if conn is None:
            print("ERROR: El DAO no tiene conexión a la BD. Revisa el .env y el Singleton.")
            return

        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO usuarios (nombre, foto, cara) VALUES (%s, %s, %s)"
                
                cursor.execute(sql, (
                    nombre, 
                    foto_bytes, 
                    cara_bytes
                ))
            
            conn.commit()
            print(f"\n[DAO] Usuario '{nombre}' insertado correctamente.")
            
            self.ejecutar_verificacion_automatica()

        except Exception as e:
            if conn:
                conn.rollback()
            print(f"[DAO] Error al registrar en la BD: {e}")

    def ejecutar_verificacion_automatica(self):
        """
        Lanza la sentencia SELECT nombre, octet_length(foto) 
        para confirmar la persistencia real.
        """
        conn = DBConnection.get_connection()
        if not conn:
            return

        try:
            with conn.cursor() as cursor:
                sql_verificar = "SELECT nombre, octet_length(foto) FROM usuarios ORDER BY id DESC LIMIT 1;"
                cursor.execute(sql_verificar)
                resultado = cursor.fetchone()
                
                if resultado:
                    print("==========================================")
                    print(f" VERIFICACIÓN AUTOMÁTICA DE PERSISTENCIA")
                    print(f" Nombre en DB: {resultado[0]}")
                    print(f" Tamaño de foto: {resultado[1]} bytes")
                    print("==========================================\n")
        except Exception as e:
            print(f"[DAO] Error en la verificación: {e}")

    def obtener_todos(self):
        """
        Obtiene todos los usuarios de la base de datos.
        Retorna una lista de tuplas (id, nombre, foto_bytes, cara_bytes).
        """
        conn = DBConnection.get_connection()
        if conn is None:
            print("ERROR: El DAO no tiene conexión a la BD.")
            return []

        try:
            usuarios = []
            with conn.cursor() as cursor:
                sql = "SELECT id, nombre, foto, cara FROM usuarios"
                cursor.execute(sql)
                usuarios = cursor.fetchall()
            return usuarios
        except Exception as e:
            print(f"[DAO] Error al obtener usuarios: {e}")
            return []