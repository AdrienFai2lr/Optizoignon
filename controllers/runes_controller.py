import mysql.connector
from config.database import DatabaseConfig
from models.runes import Rune, RuneSubstat

class RuneController:
    def __init__(self):
        self.db_config = DatabaseConfig.get_config()
        self.stat_types = {}
        self._load_stat_types()
        
        # Dictionnaire des sets de runes
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
            23: "Tolerance",
            24: "Seal",
            25: "Intangible"
        }
        
        self._base_query = """
            SELECT 
                r.*,
                st_pri.name as pri_stat_name,
                st_pre.name as prefix_stat_name,
                COUNT(*) OVER() as total_count
            FROM runes r
            LEFT JOIN stat_types st_pri ON r.pri_eff_type = st_pri.id
            LEFT JOIN stat_types st_pre ON r.prefix_eff_type = st_pre.id
        """
        
        self._substat_query = """
            SELECT 
                rs.*, 
                st.code as stat_code,
                st.name as stat_name
            FROM rune_substats rs
            JOIN stat_types st ON rs.stat_type_id = st.id
            WHERE rs.rune_id IN ({})
            ORDER BY rs.rune_id, rs.upgrade_count DESC
        """

    def _load_stat_types(self):
        """Charge les types de statistiques depuis la base de données"""
        conn = None
        cursor = None
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT id, code, name FROM stat_types"
            cursor.execute(query)
            
            for stat_id, code, name in cursor.fetchall():
                self.stat_types[stat_id] = {'code': code, 'name': name}
                
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def _get_db_connection(self):
        """Établit une connexion à la base de données en utilisant la configuration"""
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            raise Exception(f"Erreur de connexion à la base de données: {err}")

    def get_stat_type_name(self, stat_type_id):
        """Retourne le nom du type de statistique"""
        if stat_type_id in self.stat_types:
            return self.stat_types[stat_type_id]['name']
        return f"Unknown({stat_type_id})"

    def get_runes(self, set_filter=None, slot_filter=None, order_by=None, page=1, per_page=50):
        conn = None
        cursor = None
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            
            # Première requête pour obtenir le nombre total de runes
            count_query = """
                SELECT COUNT(*) 
                FROM runes r
                WHERE 1=1
            """
            count_params = []
            
            if set_filter and set_filter != "Tous":
                count_query += " AND r.set_id = %s"
                set_id = next((k for k, v in self.rune_sets.items() 
                             if v.lower() == set_filter.lower()), None)
                count_params.append(set_id)
            
            if slot_filter and slot_filter != "Tous":
                count_query += " AND r.slot_no = %s"
                count_params.append(int(slot_filter))
            
            cursor.execute(count_query, count_params)
            total_count = cursor.fetchone()[0]
            
            # Requête principale pour les runes de la page courante
            query = self._base_query + " WHERE 1=1"
            params = []
            
            if set_filter and set_filter != "Tous":
                query += " AND r.set_id = %s"
                params.append(set_id)
            
            if slot_filter and slot_filter != "Tous":
                query += " AND r.slot_no = %s"
                params.append(int(slot_filter))
            
            query += """
                ORDER BY 
                    CASE r.quality
                        WHEN 'legendary' THEN 1
                        WHEN 'heroic' THEN 2
                        WHEN 'rare' THEN 3
                        ELSE 4
                    END,
                    r.level DESC,
                    r.slot_no ASC
            """
            
            offset = (page - 1) * per_page
            query += " LIMIT %s OFFSET %s"
            params.extend([per_page, offset])
            
            cursor.execute(query, params)
            runes_data = cursor.fetchall()
            
            rune_ids = [data[0] for data in runes_data]
            substats = {}
            if rune_ids:
                substats = self.get_bulk_substats(cursor, rune_ids)
            
            runes = []
            for data in runes_data:
                rune = Rune(data[:-1])  # Exclure le total_count
                rune.set_substats(substats.get(rune.id, []))
                runes.append(rune)
            
            return runes, total_count
            
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def get_bulk_substats(self, cursor, rune_ids):
        if not rune_ids:
            return {}
            
        query = self._substat_query.format(','.join(['%s'] * len(rune_ids)))
        cursor.execute(query, rune_ids)
        all_substats = cursor.fetchall()
        
        substats_by_rune = {}
        for substat_data in all_substats:
            rune_id = substat_data[1]
            if rune_id not in substats_by_rune:
                substats_by_rune[rune_id] = []
            substats_by_rune[rune_id].append(RuneSubstat(substat_data))
        
        return substats_by_rune