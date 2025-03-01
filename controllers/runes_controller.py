import mysql.connector
from config.database import DatabaseConfig
from models.runes import Rune

class RuneController:
    def __init__(self):
        self.db_config = DatabaseConfig.get_config()
        
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
                r.id,
                r.rune_id,
                r.wizard_id,
                r.slot_no,
                r.set_id,
                r.quality,
                r.level,
                r.is_ancient,
                r.main_stat_type,
                r.main_stat_value,
                r.prefix_stat_type,
                r.prefix_stat_value,
                r.prefix_grind_value,
                r.prefix_is_gemmed,
                r.sub_stat1_type,
                r.sub_stat1_value,
                r.sub_stat1_grind_value,
                r.sub_stat1_is_gemmed,
                r.sub_stat1_original_type,
                r.sub_stat2_type,
                r.sub_stat2_value,
                r.sub_stat2_grind_value,
                r.sub_stat2_is_gemmed,
                r.sub_stat2_original_type,
                r.sub_stat3_type,
                r.sub_stat3_value,
                r.sub_stat3_grind_value,
                r.sub_stat3_is_gemmed,
                r.sub_stat3_original_type,
                r.sub_stat4_type,
                r.sub_stat4_value,
                r.sub_stat4_grind_value,
                r.sub_stat4_is_gemmed,
                r.sub_stat4_original_type,
                r.equipped_monster_id,
                COUNT(*) OVER() as total_count
            FROM runes r
            WHERE 1=1
        """

    def _get_db_connection(self):
        """Établit une connexion à la base de données"""
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as err:
            raise Exception(f"Erreur de connexion à la base de données: {err}")

    def get_runes(self, set_filter=None, slot_filter=None, order_by=None, page=1, per_page=50):
        """Récupère les runes avec filtres et pagination"""
        conn = None
        cursor = None
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()
            
            # Construction de la requête avec les filtres
            query = self._base_query
            params = []
            
            if set_filter and set_filter != "Tous":
                set_id = next((k for k, v in self.rune_sets.items() 
                             if v.lower() == set_filter.lower()), None)
                if set_id:
                    query += " AND r.set_id = %s"
                    params.append(set_id)
            
            if slot_filter and slot_filter != "Tous":
                query += " AND r.slot_no = %s"
                params.append(int(slot_filter))
            
            # Tri par défaut
            query += """
                ORDER BY 
                    CASE r.quality
                        WHEN 'legendary' THEN 1
                        WHEN 'heroic' THEN 2
                        WHEN 'rare' THEN 3
                        WHEN 'magic' THEN 4
                        ELSE 5
                    END,
                    r.level DESC,
                    r.slot_no ASC
            """
            
            # Pagination
            offset = (page - 1) * per_page
            query += " LIMIT %s OFFSET %s"
            params.extend([per_page, offset])
            
            # Exécution de la requête
            cursor.execute(query, params)
            runes_data = cursor.fetchall()
            
            # Création des objets Rune
            runes = []
            total_count = runes_data[0][-1] if runes_data else 0
            
            for data in runes_data:
                rune = Rune(data[:-1])  # Exclure le total_count
                
                # Si la rune est équipée, récupérer les infos du monstre
                if rune.equipped_monster_id:
                    # Appel de la procédure stockée
                    cursor.execute("CALL getInfoMonstre_par_rune(%s)", (rune.id,))
                    monster_data = cursor.fetchone()
                    
                    # Nécessaire pour récupérer toutes les données
                    # car après un CALL, nous devons réinitialiser le curseur
                    if cursor.nextset():
                        pass
                    
                    # Ajout des infos du monstre à l'objet rune
                    if monster_data:
                        rune.monster_info = {
                            'com2us_id': monster_data[0],
                            'name': monster_data[1],
                            'image_filename': monster_data[2]
                        }
                    else:
                        rune.monster_info = None
                else:
                    rune.monster_info = None
                
                runes.append(rune)
            
            return runes, total_count
            
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()