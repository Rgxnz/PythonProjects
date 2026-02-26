import psycopg2
import os
from dotenv import load_dotenv

class ConexionDB:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConexionDB, cls).__new__(cls)
            load_dotenv()
            try:
                cls._instancia.conn = psycopg2.connect(
                    host=os.getenv("DB_HOST"),
                    database=os.getenv("DB_NAME"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASS"),
                    port=os.getenv("DB_PORT", "5432")
                )
            except Exception as e:
                print(f"Error de conexión: {e}")
                cls._instancia.conn = None
        return cls._instancia

    def get_conexion(self):
        return self.conn