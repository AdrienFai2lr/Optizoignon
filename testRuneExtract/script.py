import json
from datetime import datetime
import sys
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_equipped_status(rune_data):
    """Retourne un commentaire sur l'état d'équipement de la rune"""
    if rune_data.get('occupied_type') == 1:
        return f"Équipée sur le monstre {rune_data.get('occupied_id')}"
    elif rune_data.get('occupied_type') == 2:
        return "Dans le stockage"
    return "État inconnu"

def get_rune_quality(rank):
    """Détermine la qualité de la rune basée sur son rang"""
    quality_mapping = {
        1: 'rare',
        2: 'rare',
        3: 'rare',
        4: 'heroic',
        5: 'legendary'
    }
    return quality_mapping.get(rank, 'rare')

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

def validate_rune_data(rune_data):
    """Valide les données de base d'une rune"""
    required_fields = ['rune_id', 'wizard_id', 'slot_no', 'rank', 'class', 'set_id', 'pri_eff']
    return all(field in rune_data for field in required_fields)

def is_ancient_rune(rune):
    """Détermine si une rune est ancienne basée sur son rank"""
    return rune.get('rank') == 15 and rune.get('class') == 16

def validate_rune_data(rune_data):
    """Valide les données de base d'une rune"""
    required_fields = ['rune_id', 'wizard_id', 'slot_no', 'rank', 'class', 'set_id', 'pri_eff']
    return all(field in rune_data for field in required_fields)

def extract_runes_from_monsters(data):
    """Extrait toutes les runes équipées sur les monstres"""
    all_runes = []
    monster_count = 0
    runes_per_monster = {}
    normal_runes_count = 0
    ancient_runes_count = 0
    monsters_with_ancient = []
    
    if 'unit_list' not in data:
        logger.warning("Aucune liste de monstres trouvée dans les données")
        return all_runes
        
    for monster in data.get('unit_list', []):
        monster_count += 1
        monster_id = monster.get('unit_id')
        monster_name = monster.get('unit_master_id', 'Unknown')
        runes = monster.get('runes', [])
        normal_count = 0
        ancient_count = 0
        
        for rune in runes:
            if validate_rune_data(rune):
                if is_ancient_rune(rune):
                    ancient_count += 1
                    ancient_runes_count += 1
                else:
                    normal_count += 1
                    normal_runes_count += 1
                all_runes.append(rune)
            else:
                logger.warning(f"Rune invalide trouvée sur le monstre {monster_id}")
        
        if ancient_count > 0:
            monsters_with_ancient.append((monster_name, monster_id, ancient_count))
        
        runes_per_monster[monster_id] = normal_count + ancient_count
    
    logger.info(f"Nombre total de monstres analysés: {monster_count}")
    logger.info(f"Runes normales équipées: {normal_runes_count}")
    logger.info(f"Runes anciennes équipées: {ancient_runes_count}")
    
    if monsters_with_ancient:
        logger.info("\nMonstres avec des runes anciennes:")
        for monster_name, monster_id, count in monsters_with_ancient:
            logger.info(f"- Monstre {monster_name} (ID: {monster_id}): {count} runes anciennes")
    
    logger.info("\nTop 5 des monstres avec le plus de runes:")
    for monster_id, count in sorted(runes_per_monster.items(), key=lambda x: x[1], reverse=True)[:5]:
        logger.info(f"- Monstre {monster_id}: {count} runes")
                
    return all_runes

def generate_sql_queries(rune_data):
    """Génère les requêtes SQL pour une rune et ses sous-stats"""
    try:
        # Normalisation des valeurs avec validation
        normalized_rank = min(max(1, rune_data.get('rank', 5)), 5)
        normalized_class = min(max(1, rune_data.get('class', 6)), 6)
        quality = get_rune_quality(normalized_rank)
        grade = get_rune_grade(normalized_rank)
        
        # Gestion explicite de occupied_type et occupied_id avec valeurs par défaut
        occupied_type = rune_data.get('occupied_type', 0)
        occupied_id = rune_data.get('occupied_id', 0)
        
        equipped_status = get_equipped_status(rune_data)
        
        rune_query = f"""-- État: {equipped_status}
INSERT INTO runes 
        (rune_id, wizard_id, occupied_type, occupied_id, slot_no, 
         `rank`, `class`, set_id, upgrade_limit, upgrade_curr,
         base_value, sell_value, pri_eff_type, pri_eff_value,
         prefix_eff_type, prefix_eff_value, quality,
         level, original_grade, current_grade, original_quality, locked)
    VALUES 
        ({rune_data['rune_id']}, 
         {rune_data['wizard_id']}, 
         {occupied_type}, 
         {occupied_id}, 
         {rune_data['slot_no']},
         {normalized_rank}, 
         {normalized_class}, 
         {rune_data['set_id']}, 
         {rune_data.get('upgrade_limit', 15)}, 
         {rune_data.get('upgrade_curr', 0)},
         {rune_data.get('base_value', 0)}, 
         {rune_data.get('sell_value', 0)}, 
         {rune_data['pri_eff'][0]}, 
         {rune_data['pri_eff'][1]},
         {rune_data.get('prefix_eff', [0, 0])[0]}, 
         {rune_data.get('prefix_eff', [0, 0])[1]}, 
         '{quality}',
         {rune_data.get('upgrade_curr', 0)},
         '{grade}',
         '{grade}',
         {normalized_rank},
         {rune_data.get('locked', 0)});"""
        
        get_id_query = "SET @last_rune_id = LAST_INSERT_ID();\n"
        
        substat_queries = []
        for substat in rune_data.get('sec_eff', []):
            if len(substat) >= 2:  # Validation minimale des sous-stats
                initial_value = substat[1] - (substat[3] if len(substat) > 3 else 0)
                substat_query = f"""INSERT INTO rune_substats 
                    (rune_id, stat_type, stat_value, upgrade_count, initial_value)
                VALUES 
                    (@last_rune_id, 
                     {substat[0]}, 
                     {substat[1]}, 
                     {substat[2] if len(substat) > 2 else 0}, 
                     {initial_value});"""
                substat_queries.append(substat_query)
        
        return rune_query, get_id_query, substat_queries
    except Exception as e:
        logger.error(f"Erreur lors de la génération des requêtes SQL pour la rune {rune_data.get('rune_id')}: {str(e)}")
        return None, None, []

def main():
    try:
        # Lecture du fichier JSON avec gestion explicite du chemin
        input_file = '../data/donne.json'
        if len(sys.argv) > 1:
            input_file = sys.argv[1]
            
        logger.info(f"Lecture du fichier: {input_file}")
        
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        # Collecter toutes les runes (stockage + équipées)
        all_runes = []
        
        # Ajouter les runes normales du stockage
        if 'runes' in data:
            logger.info(f"Nombre de runes normales trouvées dans le stockage: {len(data['runes'])}")
            all_runes.extend(data['runes'])
        else:
            logger.warning("Aucune rune normale trouvée dans le stockage (clé 'runes' absente)")
            
        # Ajouter les runes anciennes du stockage
        if 'ancient_runes' in data:
            logger.info(f"Nombre de runes anciennes trouvées dans le stockage: {len(data.get('ancient_runes', []))}")
            all_runes.extend(data['ancient_runes'])
        else:
            logger.warning("Aucune rune ancienne trouvée dans le stockage (clé 'ancient_runes' absente)")

        # Structure des données pour debug
        logger.info("Clés disponibles dans les données:")
        for key in data.keys():
            logger.info(f"- {key}")
            
        # Ajouter les runes équipées sur les monstres
        equipped_runes = extract_runes_from_monsters(data)
        all_runes.extend(equipped_runes)
        
        if not all_runes:
            logger.error("Aucune rune trouvée dans le fichier JSON")
            return
            
        # Création du fichier SQL
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sql_filename = f'runes_import_{timestamp}.sql'
        
        # Compteurs pour les statistiques
        equipped_count = 0
        storage_count = 0
        error_count = 0
        
        with open(sql_filename, 'w', encoding='utf-8') as sql_file:
            sql_file.write("START TRANSACTION;\n\n")
            
            for rune in all_runes:
                try:
                    if not validate_rune_data(rune):
                        logger.warning(f"Rune invalide ignorée: {rune.get('rune_id')}")
                        error_count += 1
                        continue
                        
                    # Mise à jour des compteurs
                    if rune.get('occupied_type') == 1:
                        equipped_count += 1
                    elif rune.get('occupied_type') == 2:
                        storage_count += 1
                        
                    rune_query, get_id_query, substat_queries = generate_sql_queries(rune)
                    
                    if rune_query:
                        sql_file.write(f"-- Rune ID: {rune['rune_id']}\n")
                        sql_file.write(rune_query + "\n")
                        sql_file.write(get_id_query + "\n")
                        
                        if substat_queries:
                            sql_file.write("-- Sous-stats pour la rune\n")
                            for query in substat_queries:
                                sql_file.write(query + "\n")
                            sql_file.write("\n")
                    
                except Exception as e:
                    logger.error(f"Erreur lors du traitement de la rune {rune.get('rune_id')}: {str(e)}")
                    error_count += 1
                    continue
            
            sql_file.write("COMMIT;\n")
            
        logger.info(f"Fichier SQL généré avec succès : {sql_filename}")
        logger.info("\nStatistiques détaillées:")
        logger.info(f"- Runes équipées: {equipped_count}")
        logger.info(f"- Runes en stockage: {storage_count}")
        logger.info(f"- Erreurs: {error_count}")
        logger.info(f"- Total: {equipped_count + storage_count}")
        
        # Statistiques sur les slots
        slot_stats = {}
        quality_stats = {}
        set_stats = {}
        for rune in all_runes:
            slot_stats[rune.get('slot_no', 0)] = slot_stats.get(rune.get('slot_no', 0), 0) + 1
            quality_stats[get_rune_quality(rune.get('rank', 1))] = quality_stats.get(get_rune_quality(rune.get('rank', 1)), 0) + 1
            set_stats[rune.get('set_id', 0)] = set_stats.get(rune.get('set_id', 0), 0) + 1
        
        logger.info("\nDistribution par slot:")
        for slot in sorted(slot_stats.keys()):
            logger.info(f"- Slot {slot}: {slot_stats[slot]} runes")
            
        logger.info("\nDistribution par qualité:")
        for quality in ['legendary', 'heroic', 'rare']:
            logger.info(f"- {quality.capitalize()}: {quality_stats.get(quality, 0)} runes")
            
        logger.info("\nTop 5 des sets de runes:")
        for set_id, count in sorted(set_stats.items(), key=lambda x: x[1], reverse=True)[:5]:
            logger.info(f"- Set {set_id}: {count} runes")
        
    except FileNotFoundError:
        logger.error(f"Erreur: Le fichier {input_file} n'a pas été trouvé")
    except json.JSONDecodeError:
        logger.error("Erreur: Le fichier n'est pas un JSON valide")
    except Exception as e:
        logger.error(f"Erreur inattendue: {str(e)}")

if __name__ == "__main__":
    main()