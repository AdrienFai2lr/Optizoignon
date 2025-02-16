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

    def get_monster_with_skills(self, monster_id):  # 🟢 Fonction bien indentée maintenant
        try:
            conn = mysql.connector.connect(**DatabaseConfig.get_config())
            cursor = conn.cursor()

            # Récupération du monstre
            monster_query = """
                SELECT m.name, m.natural_stars, m.hp, m.attack, m.defense, m.speed, 
                       m.crit_rate, m.crit_damage, m.element, m.image_filename,
                       m.resistance, m.accuracy, m.id
                FROM monsters m
                WHERE m.id = %s
            """
            cursor.execute(monster_query, (monster_id,))
            monster_data = cursor.fetchone()
            
            if not monster_data:
                print(f"❌ No monster found with ID {monster_id}")
                return None

            # Récupération des compétences
            skills_query = """
                SELECT s.id, s.name, s.description, s.cooldown, s.hits, 
                       s.aoe, s.passive, s.icon_filename, s.level_progress_description
                FROM skills s
                JOIN monster_skills ms ON s.id = ms.skill_id
                WHERE ms.monster_id = %s
                ORDER BY ms.slot
            """
            cursor.execute(skills_query, (monster_id,))
            skills_data = cursor.fetchall()
            
            print(f"🔍 Found {len(skills_data)} skills for Monster ID {monster_id}")  # Debug
            
            monster = Monster(monster_data)
            monster.skills = [Skill(skill_data) for skill_data in skills_data]
            
            print(f"✅ Monster {monster.name} now has {len(monster.skills)} skills")  # Debug

            return monster
                
        except mysql.connector.Error as err:
            print(f"❌ Database error: {err}")
            raise DatabaseError(f"Erreur de base de données: {err}")
        
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

class DatabaseError(Exception):
    pass
