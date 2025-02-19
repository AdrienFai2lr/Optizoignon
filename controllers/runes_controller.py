import mysql.connector
from config.database import DatabaseConfig
from models.runes import Rune, RuneSubstat

class RuneController:
    def __init__(self):
        self.rune_sets = {
            1: "Energy",
            2: "Guard",
            3: "Swift",
            4: "Blade",
            5: "Rage",
            6: "Focus",
            7: "Endure",
            8: "Fatal",
            10: "Despair",
            11: "Vampire",
            13: "Violent",
            14: "Nemesis",
            15: "Will",
            16: "Shield",
            17: "Revenge",
            18: "Destroy",
            19: "Fight",
            20: "Determination",
            21: "Enhance",
            22: "Accuracy",
            23: "Tolerance"
        }

    def _get_base_query(self):
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

    def get_runes(self, wizard_id, set_filter=None, slot_filter=None):
        try:
            conn = mysql.connector.connect(**DatabaseConfig.get_config())
            cursor = conn.cursor()
            
            query = self._get_base_query()
            params = [wizard_id]
            
            if set_filter and set_filter != "Tous":
                query += " AND set_id = %s"
                set_id = next((k for k, v in self.rune_sets.items() if v == set_filter), None)
                params.append(set_id)
            
            if slot_filter and slot_filter != "Tous":
                query += " AND slot_no = %s"
                params.append(int(slot_filter))
            
            query += " ORDER BY set_id ASC, slot_no ASC, quality DESC"
            
            cursor.execute(query, params)
            runes_data = cursor.fetchall()
            
            runes = [Rune(data) for data in runes_data]
            
            # Fetch substats for each rune
            for rune in runes:
                substats = self.get_rune_substats(cursor, rune.id)
                rune.set_substats(substats)
            
            return runes
            
        except mysql.connector.Error as err:
            print(f"Erreur SQL détaillée: {err}")  # Pour le débogage
            raise DatabaseError(f"Erreur de base de données: {err}")
        
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def get_rune_substats(self, cursor, rune_id):
        """Récupère les sous-statistiques d'une rune."""
        substat_query = """
            SELECT id, rune_id, stat_type_id, stat_value, upgrade_count, initial_value
            FROM rune_substats
            WHERE rune_id = %s
            ORDER BY id ASC
        """
        cursor.execute(substat_query, (rune_id,))
        substats_data = cursor.fetchall()
        return [RuneSubstat(data) for data in substats_data]

class DatabaseError(Exception):
    pass