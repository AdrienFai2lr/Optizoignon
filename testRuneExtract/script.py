import json
from datetime import datetime
import sys
import logging
import os

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_rune_quality(rank):
    """Détermine la qualité de la rune basée sur son rang"""
    quality_mapping = {
        1: 'normal',
        2: 'magique',
        3: 'rare',
        4: 'heroic',
        5: 'legendary'
    }
    return quality_mapping.get(rank, 'normal')

def get_rune_grade(rank):
    """Détermine le grade de la rune basée sur son rang"""
    grade_mapping = {
        1: 'normal',
        2: 'magic',
        3: 'rare',
        4: 'heroic',
        5: 'legendary'
    }
    return grade_mapping.get(rank, 'normal')

def get_stat_code(stat_id):
    """Retourne le code de stat basé sur l'ID"""
    stat_type_mapping = {
        1: 'HP_FLAT',
        2: 'HP_PCT',
        3: 'ATK_FLAT',
        4: 'ATK_PCT',
        5: 'DEF_FLAT',
        6: 'DEF_PCT',
        7: 'SPD',
        8: 'CRIT_RATE',
        9: 'CRIT_DMG',
        10: 'RES',
        11: 'ACC'
    }
    return stat_type_mapping.get(stat_id, 'HP_FLAT')

def validate_rune_data(rune_data):
    """Valide les données de base d'une rune"""
    required_fields = ['rune_id', 'wizard_id', 'slot_no', 'rank', 'class', 'set_id', 'pri_eff']
    return all(field in rune_data for field in required_fields)

def generate_rune_upgrades(rune_data, upgrade_count, is_ancient):
    """Génère les enregistrements d'upgrade pour une rune"""
    upgrades = []
    if upgrade_count > 0:
        for substat in rune_data.get('sec_eff', []):
            if len(substat) > 3 and substat[2] > 0:  # Si la stat a été améliorée
                upgrade_count = substat[2]
                initial_value = substat[1] - substat[3]  # Valeur initiale
                value_per_upgrade = substat[3] / upgrade_count

                for i in range(upgrade_count):
                    level = (i + 1) * 3  # Niveaux 3, 6, 9, 12
                    old_value = initial_value + (i * value_per_upgrade)
                    new_value = initial_value + ((i + 1) * value_per_upgrade)
                    
                    upgrade_query = f"""
INSERT INTO rune_upgrades 
(rune_id, level_reached, stat_type_id, old_value, new_value, upgrade_date)
SELECT 
    @last_rune_id,
    {level},
    (SELECT id FROM stat_types WHERE code = '{get_stat_code(substat[0])}'),
    {old_value},
    {new_value},
    NOW();"""
                    upgrades.append(upgrade_query)
    return upgrades

def generate_rune_inserts(rune_data, unit_master_id=None):
    """Génère les requêtes SQL pour une rune et ses sous-stats"""
    try:
        # Déterminer si c'est une rune antique
        is_ancient = rune_data.get('rank') == 15 and rune_data.get('class') == 16
        
        # Déterminer la qualité basée sur le rang
        normalized_rank = min(max(1, rune_data.get('rank', 5)), 5)
        if is_ancient:
            normalized_rank = 5  # Les runes antiques sont toujours légendaires
            
        quality = get_rune_quality(normalized_rank)
        grade = get_rune_grade(normalized_rank)
        upgrade_count = rune_data.get('upgrade_curr', 0)

        queries = []
        
        # Vérification des contraintes de slot
        verify_slot_query = f"""
SET @valid_slot = (
    SELECT COUNT(*) 
    FROM slot_stat_constraints 
    WHERE slot_no = {rune_data['slot_no']} 
    AND stat_type_id = (SELECT id FROM stat_types WHERE code = '{get_stat_code(rune_data['pri_eff'][0])}')
);"""
        queries.append(verify_slot_query)

        # INSERT principal pour la rune
        rune_query = f"""
INSERT INTO runes 
(rune_id, wizard_id, occupied_type, occupied_id, slot_no, `rank`, 
 `class`, set_id, upgrade_limit, upgrade_curr, base_value, sell_value, 
 pri_eff_type, pri_eff_value, prefix_eff_type, prefix_eff_value, 
 quality, level, original_grade, current_grade, original_quality, locked)
VALUES 
({rune_data['rune_id']}, 
 {rune_data['wizard_id']}, 
 {rune_data.get('occupied_type', 0)}, 
 {rune_data.get('occupied_id', 0)}, 
 {rune_data['slot_no']},
 {rune_data['rank']}, 
 {rune_data['class']}, 
 {rune_data['set_id']}, 
 {rune_data.get('upgrade_limit', 15)}, 
 {upgrade_count},
 {rune_data.get('base_value', 0)}, 
 {rune_data.get('sell_value', 0)}, 
 (SELECT id FROM stat_types WHERE code = '{get_stat_code(rune_data['pri_eff'][0])}'), 
 {rune_data['pri_eff'][1]},
 (SELECT id FROM stat_types WHERE code = '{get_stat_code(rune_data.get('prefix_eff', [0])[0])}'), 
 {rune_data.get('prefix_eff', [0, 0])[1]}, 
 '{quality}',
 {upgrade_count},
 '{grade}',
 '{grade}',
 {normalized_rank},
 0);

SET @last_rune_id = LAST_INSERT_ID();"""
        queries.append(rune_query)

        # INSERT pour les sous-stats
        for substat in rune_data.get('sec_eff', []):
            if len(substat) >= 2:
                initial_value = substat[1] - (substat[3] if len(substat) > 3 else 0)
                upgrade_count = substat[2] if len(substat) > 2 else 0
                
                substat_query = f"""
INSERT INTO rune_substats 
(rune_id, stat_type_id, stat_value, upgrade_count, initial_value)
SELECT 
    @last_rune_id, 
    (SELECT id FROM stat_types WHERE code = '{get_stat_code(substat[0])}'),
    {substat[1]},
    {upgrade_count},
    {initial_value};

-- Vérification de l'insertion via un SELECT conditionnel
SELECT CONCAT('Erreur: Substat invalide pour la rune ', {rune_data['rune_id']}, 
             ' - Type: ', '{get_stat_code(substat[0])}', 
             ' Valeur: ', {initial_value}) AS warning 
WHERE ROW_COUNT() = 0;
"""
                queries.append(substat_query)

        # Génération des enregistrements d'upgrades
        upgrades = generate_rune_upgrades(rune_data, upgrade_count, is_ancient)
        queries.extend(upgrades)

        # INSERT pour monster_runes si la rune est équipée
        if rune_data.get('occupied_type') == 1 and unit_master_id:
            monster_rune_query = f"""
-- Supprimer toute rune existante dans ce slot pour ce monstre
DELETE FROM monster_runes 
WHERE monster_id = (SELECT id FROM monsters WHERE com2us_id = {unit_master_id})
AND slot_number = {rune_data['slot_no']};

-- Insérer la nouvelle association rune-monstre
INSERT INTO monster_runes (monster_id, rune_id, slot_number)
SELECT 
    (SELECT id FROM monsters WHERE com2us_id = {unit_master_id}), 
    @last_rune_id, 
    {rune_data['slot_no']}
WHERE EXISTS (SELECT 1 FROM monsters WHERE com2us_id = {unit_master_id});"""
            queries.append(monster_rune_query)

        return queries

    except Exception as e:
        logger.error(f"Erreur lors de la génération des requêtes SQL pour la rune {rune_data.get('rune_id')}: {str(e)}")
        return []

def write_sql_file(queries, file_path):
    """Écrit les requêtes SQL dans un fichier"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("START TRANSACTION;\n\n")
        
        # Ajout des DELETE au début du fichier
        f.write("-- Suppression des données existantes\n")
        f.write("DELETE FROM monster_runes;\n")
        f.write("DELETE FROM rune_upgrades;\n")
        f.write("DELETE FROM rune_substats;\n")
        f.write("DELETE FROM runes;\n\n")
        
        for query in queries:
            f.write(query + "\n")
            
        f.write("\nCOMMIT;\n")

def create_single_insert_sql(data_json, output_file):
    """Crée un seul fichier SQL avec tous les INSERT"""
    try:
        # Extraire toutes les runes
        all_runes = []
        
        # 1. Runes non équipées et runes antiques
        all_runes.extend(data_json.get('runes', []))
        all_runes.extend(data_json.get('ancient_runes', []))
        
        # 2. Runes équipées depuis la liste des monstres
        if 'unit_list' in data_json:
            for monster in data_json['unit_list']:
                unit_master_id = monster.get('unit_master_id')
                if monster.get('runes'):
                    for rune in monster.get('runes', []):
                        if validate_rune_data(rune):
                            rune['unit_master_id'] = unit_master_id
                            all_runes.append(rune)

        # Éliminer les doublons potentiels basés sur rune_id
        unique_runes = {rune['rune_id']: rune for rune in all_runes}.values()
        all_runes = list(unique_runes)
        
        file_queries = []
        for rune in all_runes:
            if validate_rune_data(rune):
                file_queries.append(f"-- Rune ID: {rune['rune_id']}")
                queries = generate_rune_inserts(rune, rune.get('unit_master_id'))
                file_queries.extend(queries)
                file_queries.append("")
        
        write_sql_file(file_queries, output_file)
        logger.info(f"Fichier SQL généré : {output_file}")
        logger.info(f"Nombre total de runes traitées : {len(all_runes)}")

    except Exception as e:
        logger.error(f"Erreur lors de la création du fichier SQL : {str(e)}")

def main():
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

        create_single_insert_sql(data, output_file)

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