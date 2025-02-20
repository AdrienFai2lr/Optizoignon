from config.database import DatabaseConfig
import mysql.connector
from models.runes import Rune, RuneSubstat

class RuneController:
    def __init__(self):  # Plus de paramètre cursor requis
        self.db_config = DatabaseConfig.get_config()  # Stockage de la configuration
        self.rune_sets = {
            1: "energy",
            2: "guard",
            3: "swift",
            4: "blade",
            5: "rage",
            6: "focus",
            7: "endure",
            8: "fatal",
            10: "despair",
            11: "vampire",
            13: "violent",
            14: "nemesis",
            15: "will",
            16: "shield",
            17: "revenge",
            18: "destroy",
            19: "fight",
            20: "determination",
            21: "enhance",
            22: "accuracy",
            23: "tolerance"
        }

    def _get_db_connection(self):
        """Crée et retourne une nouvelle connexion à la base de données"""
        return mysql.connector.connect(**self.db_config)

    def _get_base_query(self):
        """Retourne la requête SQL de base pour sélectionner les runes"""
        return """
            SELECT 
                id, 
                rune_id, 
                wizard_id, 
                slot_no, 
                `rank`, 
                `class`, 
                set_id, 
                upgrade_limit, 
                upgrade_curr, 
                base_value, 
                sell_value, 
                pri_eff_type, 
                pri_eff_value, 
                prefix_eff_type, 
                prefix_eff_value, 
                quality, 
                COALESCE(locked, 0) as locked, 
                level, 
                original_grade, 
                current_grade, 
                original_quality
            FROM runes
            WHERE wizard_id = %s
        """

    def get_runes(self, wizard_id, set_filter=None, slot_filter=None, order_by=None):
        """
        Récupère les runes selon les filtres spécifiés
        """
        conn = None
        cursor = None
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            
            query = self._get_base_query()
            params = [wizard_id]
            
            if set_filter and set_filter != "Tous":
                query += " AND set_id = %s"
                set_id = next((k for k, v in self.rune_sets.items() if v.lower() == set_filter.lower()), None)
                params.append(set_id)
            
            if slot_filter and slot_filter != "Tous":
                query += " AND slot_no = %s"
                params.append(int(slot_filter))
            
            # Gestion du tri
            if order_by:
                if order_by == "quality":
                    query += " ORDER BY quality DESC"
                elif order_by == "efficiency":
                    query += " ORDER BY pri_eff_value DESC"
                elif order_by == "set":
                    query += " ORDER BY set_id ASC"
                elif order_by == "slot":
                    query += " ORDER BY slot_no ASC"
            else:
                query += " ORDER BY set_id ASC, slot_no ASC, quality DESC"
            
            cursor.execute(query, params)
            runes_data = cursor.fetchall()
            
            runes = [Rune(data) for data in runes_data]
            
            # Récupération des substats pour chaque rune
            for rune in runes:
                substats = self.get_rune_substats(cursor, rune.id)
                rune.set_substats(substats)
            
            return runes
            
        except mysql.connector.Error as err:
            print(f"Erreur SQL détaillée: {err}")
            raise DatabaseError(f"Erreur de base de données: {err}")
        
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_rune_substats(self, cursor, rune_id):
        """Récupère les sous-statistiques d'une rune"""
        substat_query = """
            SELECT id, rune_id, stat_type_id, stat_value, upgrade_count, initial_value
            FROM rune_substats
            WHERE rune_id = %s
            ORDER BY id ASC
        """
        cursor.execute(substat_query, (rune_id,))
        substats_data = cursor.fetchall()
        return [RuneSubstat(data) for data in substats_data]

    def get_rune_by_id(self, rune_id, wizard_id):
        """Récupère une rune spécifique par son ID"""
        conn = None
        cursor = None
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            
            query = self._get_base_query() + " AND rune_id = %s"
            cursor.execute(query, (wizard_id, rune_id))
            
            rune_data = cursor.fetchone()
            if not rune_data:
                return None
                
            rune = Rune(rune_data)
            substats = self.get_rune_substats(cursor, rune.id)
            rune.set_substats(substats)
            
            return rune
            
        except mysql.connector.Error as err:
            raise DatabaseError(f"Erreur de base de données: {err}")
            
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_set_name(self, set_id):
        """Retourne le nom du set de runes"""
        return self.rune_sets.get(set_id, "unknown")

    def get_set_id(self, set_name):
        """Retourne l'ID du set à partir de son nom"""
        set_name = set_name.lower()
        for set_id, name in self.rune_sets.items():
            if name.lower() == set_name:
                return set_id
        return None

    def update_rune_lock(self, rune_id, wizard_id, locked):
        """Met à jour le statut de verrouillage d'une rune"""
        conn = None
        cursor = None
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE runes 
                SET locked = %s 
                WHERE rune_id = %s AND wizard_id = %s
            """
            cursor.execute(query, (locked, rune_id, wizard_id))
            conn.commit()
            
            return cursor.rowcount > 0
            
        except mysql.connector.Error as err:
            raise DatabaseError(f"Erreur de base de données: {err}")
            
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

class DatabaseError(Exception):
    """Exception personnalisée pour les erreurs de base de données"""
    pass