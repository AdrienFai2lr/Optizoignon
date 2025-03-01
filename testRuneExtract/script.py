import json
from datetime import datetime
import sys
import logging
import os

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def sql_format(value):
    """Formate une valeur pour SQL"""
    if value is None:
        return 'NULL'
    elif isinstance(value, (int, float, bool)):
        return str(value)
    else:
        return f"'{str(value)}'"

def get_stat_code(stat_id):
    """Retourne le code de stat basé sur l'ID"""
    # Correction de la correspondance entre les IDs et les codes
    stat_type_mapping = {
        1: 'PV+',    # Points de vie fixes
        2: 'PV%',     # Pourcentage de points de vie
        3: 'ATK+',   # Attaque fixe
        4: 'ATK%',    # Pourcentage d'attaque
        5: 'DEF+',   # Défense fixe
        6: 'DEF%',    # Pourcentage de défense
        8: 'SPD',        # Vitesse (VIT)
        9: 'TC%',  # Taux Critique (TC)
        10: 'DC%',  # Dégâts Critiques (DC)
        11: 'RESIS%',       # Résistance
        12: 'PRECI%'        # Précision
    }
    return stat_type_mapping.get(stat_id, 'UNKNOWN')

def get_rune_quality(rank):
    """Détermine la qualité de la rune basée sur son rang"""
    quality_mapping = {
        1: 'normal',
        2: 'magic',
        3: 'rare',
        4: 'heroic',
        5: 'legendary'
    }
    return quality_mapping.get(rank, 'normal')

def validate_rune_data(rune_data):
    """Valide les données de base d'une rune"""
    required_fields = ['rune_id', 'wizard_id', 'slot_no', 'rank', 'class', 'set_id', 'pri_eff']
    return all(field in rune_data for field in required_fields)

def generate_rune_insert(rune_data, unit_master_id=None):
    """Génère la requête SQL pour une rune"""
    try:
        # Vérification des données
        if not validate_rune_data(rune_data):
            logger.error(f"Données de rune invalides pour rune_id: {rune_data.get('rune_id')}")
            return None, None

        # Déterminer si c'est une rune antique
        is_ancient = rune_data.get('rank') == 15 and rune_data.get('class') == 16
        
        # Normaliser le rang et obtenir la qualité
        normalized_rank = min(max(1, rune_data.get('rank', 5)), 5)
        quality = get_rune_quality(normalized_rank)

        # Construire la requête
        query = """
        INSERT INTO runes (
            rune_id, wizard_id, slot_no, set_id, quality, level, is_ancient,
            main_stat_type, main_stat_value,
            prefix_stat_type, prefix_stat_value,
            sub_stat1_type, sub_stat1_value, sub_stat1_grind_value, sub_stat1_is_gemmed,
            sub_stat2_type, sub_stat2_value, sub_stat2_grind_value, sub_stat2_is_gemmed,
            sub_stat3_type, sub_stat3_value, sub_stat3_grind_value, sub_stat3_is_gemmed,
            sub_stat4_type, sub_stat4_value, sub_stat4_grind_value, sub_stat4_is_gemmed,
            equipped_monster_id
        ) VALUES (
            %(rune_id)s, %(wizard_id)s, %(slot_no)s, %(set_id)s, %(quality)s, 
            %(level)s, %(is_ancient)s,
            %(main_stat_type)s, %(main_stat_value)s,
            %(prefix_stat_type)s, %(prefix_stat_value)s,
            %(sub_stat1_type)s, %(sub_stat1_value)s, %(sub_stat1_grind_value)s, %(sub_stat1_is_gemmed)s,
            %(sub_stat2_type)s, %(sub_stat2_value)s, %(sub_stat2_grind_value)s, %(sub_stat2_is_gemmed)s,
            %(sub_stat3_type)s, %(sub_stat3_value)s, %(sub_stat3_grind_value)s, %(sub_stat3_is_gemmed)s,
            %(sub_stat4_type)s, %(sub_stat4_value)s, %(sub_stat4_grind_value)s, %(sub_stat4_is_gemmed)s,
            %(equipped_monster_id)s
        )"""

        # Préparer les données de base
        data = {
            'rune_id': rune_data['rune_id'],
            'wizard_id': rune_data['wizard_id'],
            'slot_no': rune_data['slot_no'],
            'set_id': rune_data['set_id'],
            'quality': quality,
            'level': rune_data.get('upgrade_curr', 0),
            'is_ancient': is_ancient,
            'main_stat_type': get_stat_code(rune_data['pri_eff'][0]),
            'main_stat_value': rune_data['pri_eff'][1],
            'prefix_stat_type': get_stat_code(rune_data.get('prefix_eff', [0])[0]),
            'prefix_stat_value': rune_data.get('prefix_eff', [0, 0])[1],
            'equipped_monster_id': unit_master_id
        }

        # Traiter les sous-stats
        substats = rune_data.get('sec_eff', [])
        for i in range(4):
            base_key = f'sub_stat{i+1}'
            if i < len(substats):
                substat = substats[i]
                data[f'{base_key}_type'] = get_stat_code(substat[0])
                data[f'{base_key}_value'] = substat[1]
                data[f'{base_key}_grind_value'] = substat[3] if len(substat) > 3 else 0
                data[f'{base_key}_is_gemmed'] = 1 if (len(substat) > 3 and substat[2] == 1) else 0
                
                # Ajout du type original pour les stats gemmées
                if len(substat) > 3 and substat[2] == 1:
                    data[f'{base_key}_original_type'] = get_stat_code(substat[4]) if len(substat) > 4 else None
                else:
                    data[f'{base_key}_original_type'] = None
            else:
                data[f'{base_key}_type'] = None
                data[f'{base_key}_value'] = None
                data[f'{base_key}_grind_value'] = None
                data[f'{base_key}_is_gemmed'] = None
                data[f'{base_key}_original_type'] = None

        return query, data

    except Exception as e:
        logger.error(f"Erreur lors de la génération de la requête pour rune_id {rune_data.get('rune_id')}: {str(e)}")
        return None, None

def create_rune_inserts(data_json, output_file):
    """Crée le fichier SQL avec toutes les requêtes d'insertion"""
    try:
        queries = []
        params = []
        
        # Traiter les runes non équipées
        for rune in data_json.get('runes', []):
            query, data = generate_rune_insert(rune)
            if query and data:
                queries.append(query)
                params.append(data)

        # Traiter les runes équipées sur les monstres
        for monster in data_json.get('unit_list', []):
            for rune in monster.get('runes', []):
                query, data = generate_rune_insert(rune, monster.get('unit_master_id'))
                if query and data:
                    queries.append(query)
                    params.append(data)

        # Écrire dans le fichier
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("START TRANSACTION;\n\n")
            f.write("DELETE FROM runes;\n\n")
            
            for query, data in zip(queries, params):
                formatted_query = query % {k: sql_format(v) for k, v in data.items()}
                f.write(formatted_query + ";\n")
            
            f.write("\nCOMMIT;\n")

        logger.info(f"Fichier SQL généré : {output_file}")
        logger.info(f"Nombre total de runes traitées : {len(queries)}")

    except Exception as e:
        logger.error(f"Erreur lors de la création du fichier SQL : {str(e)}")

def main():
    """Fonction principale"""
    try:
        input_file = '../data/donne.json'
        if len(sys.argv) > 1:
            input_file = sys.argv[1]

        logger.info(f"Lecture du fichier: {input_file}")
        
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs('rune_exports', exist_ok=True)
        output_file = f'rune_exports/rune_inserts_{timestamp}.sql'

        create_rune_inserts(data, output_file)

    except FileNotFoundError:
        logger.error(f"Erreur: Le fichier {input_file} n'a pas été trouvé")
    except json.JSONDecodeError:
        logger.error("Erreur: Le fichier n'est pas un JSON valide")
    except Exception as e:
        logger.error(f"Erreur inattendue: {str(e)}")
    finally:
        logger.info("Fin du traitement")

if __name__ == "__main__":
    main()