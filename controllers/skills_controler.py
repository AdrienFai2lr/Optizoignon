import mysql.connector
from config.database import DatabaseConfig
from models.skills import Skill

class SkillsController:
    def get_skills_by_monster_id(self, monster_id):
        """Récupère toutes les compétences d'un monstre par son ID.
        
        Args:
            monster_id (int): L'ID du monstre
            
        Returns:
            list[Skill]: Liste des compétences du monstre
        """
        try:
            conn = mysql.connector.connect(**DatabaseConfig.get_config())
            cursor = conn.cursor()

            skills_query = """
                SELECT s.id, s.name, s.description, s.cooldown, s.hits, s.multiplier_formula_raw,s.aoe,s.passive,s.icon_filename,s.level_progress_description
                FROM skills s
                JOIN monster_skills ms ON s.id = ms.skill_id
                WHERE ms.monster_id = %s
                ORDER BY ms.level
            """
            
            cursor.execute(skills_query, (monster_id,))
            skills_data = cursor.fetchall()
            
            print(f"🔢 Found {len(skills_data)} skills for monster ID {monster_id}")
            
            return [Skill(skill_data) for skill_data in skills_data]
            
        except mysql.connector.Error as err:
            print(f"❌ Database error while fetching skills: {err}")
            raise DatabaseError(f"Erreur lors de la récupération des skills: {err}")
        
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

class DatabaseError(Exception):
    pass