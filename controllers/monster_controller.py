import mysql.connector
from config.database import DatabaseConfig
from models.monster import Monster
from models.skills import Skill

class MonsterController:
    def __init__(self):
        self.element_map = {
            "Eau": "water",
            "Feu": "fire",
            "Vent": "wind",
            "Lumière": "light",
            "Ténèbres": "dark"
        }

    def _get_base_query(self):
        return """
            SELECT id, name, natural_stars, hp, attack, defense, speed,
            crit_rate, crit_damage, element, image_filename, resistance, accuracy
            FROM monsters
            WHERE obtainable = 1
        """

    def get_monsters(self, element_filter=None, stars_filter=None):
        try:
            conn = mysql.connector.connect(**DatabaseConfig.get_config())
            cursor = conn.cursor()
            
            query = self._get_base_query()
            params = []
            
            if element_filter and element_filter != "Tous":
                query += " AND element = %s"
                params.append(self.element_map[element_filter])
            
            if stars_filter and stars_filter != "Toutes":
                query += " AND natural_stars = %s"
                params.append(int(stars_filter[0]))
            
            query += " ORDER BY natural_stars DESC, name ASC"
            
            cursor.execute(query, params)
            monsters_data = cursor.fetchall()
            
            return [Monster(data) for data in monsters_data]
            
        except mysql.connector.Error as err:
            raise DatabaseError(f"Erreur de base de données: {err}")
        
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

class DatabaseError(Exception):
    pass
