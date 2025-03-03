# config/database.py
class DatabaseConfig:
    HOST = "localhost"
    DATABASE = "summoners_war"
    USER = "root"  # À modifier selon votre configuration
    PASSWORD = ""  # À modifier selon votre configuration
    PORT = 3306

    @staticmethod
    def get_config():
        return {
            'host': DatabaseConfig.HOST,
            'database': DatabaseConfig.DATABASE,
            'user': DatabaseConfig.USER,
            'password': DatabaseConfig.PASSWORD,
            'port': DatabaseConfig.PORT
        }