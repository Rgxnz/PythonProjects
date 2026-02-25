import psycopg2
from src.config import Config

class ConexionDB:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConexionDB, cls).__new__(cls)
            try:
                cls._instancia.conn = psycopg2.connect(
                    host=Config.DB_HOST,
                    database=Config.DB_NAME,
                    user=Config.DB_USER,
                    password=Config.DB_PASS,
                    port=Config.DB_PORT
                )
            except Exception as e:
                print(f"Error crítico de conexión: {e}")
        return cls._instancia

    def get_conexion(self):
        return self.conn