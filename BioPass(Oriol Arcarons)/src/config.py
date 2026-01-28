import os

class Config:
    _env_data = {}

    @staticmethod
    def _cargar_manual():
        """Lee el .env línea a línea con manejo robusto de codificación"""
        if not Config._env_data:
            if os.path.exists(".env"):
                for encoding in ["utf-8", "latin-1", "cp1252"]:
                    try:
                        with open(".env", "r", encoding=encoding) as f:
                            for line in f:
                                l = line.strip()
                                if l and "=" in l and not l.startswith("#"):
                                    k, v = l.split("=", 1)
                                    Config._env_data[k.strip()] = v.strip()
                        break
                    except (UnicodeDecodeError, LookupError):
                        Config._env_data = {}
                        continue

    @staticmethod
    def get_db_params():
        Config._cargar_manual()
        return {
            "host": Config._env_data.get("DB_HOST"),
            "database": Config._env_data.get("DB_NAME"),
            "user": Config._env_data.get("DB_USER"),
            "password": Config._env_data.get("DB_PASS"),
            "port": Config._env_data.get("DB_PORT")
        }