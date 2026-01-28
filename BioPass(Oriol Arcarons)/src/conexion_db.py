import psycopg
import traceback
from src.config import Config

class DBConnection:
    _connection = None

    @classmethod
    def get_connection(cls):
        if cls._connection is None or cls._connection.closed != 0:
            try:
                params = Config.get_db_params()
                
                dsn_parts = []
                if params.get('host'):
                    dsn_parts.append(f"host={params['host']}")
                if params.get('database'):
                    dsn_parts.append(f"dbname={params['database']}")
                if params.get('user'):
                    dsn_parts.append(f"user={params['user']}")
                if params.get('password'):
                    pwd = params['password'].replace("\\", "\\\\").replace("'", "\\'")
                    dsn_parts.append(f"password={pwd}")
                if params.get('port'):
                    dsn_parts.append(f"port={params['port']}")
                
                dsn = " ".join(dsn_parts)
                cls._connection = psycopg.connect(dsn)
                print("Conexión establecida con éxito a PostgreSQL.")
            except Exception as e:
                print(f"Error crítico al conectar: {e}")
                traceback.print_exc()
                cls._connection = None
        return cls._connection

    @classmethod
    def _verificar_tabla(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            foto BYTEA NOT NULL,
            cara BYTEA NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        with cls._connection.cursor() as cur:
            cur.execute(sql)
        cls._connection.commit()