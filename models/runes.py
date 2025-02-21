class Rune:
    def __init__(self, data):
        self.id = data[0]
        self.rune_id = data[1]
        self.wizard_id = data[2]
        self.occupied_type = data[3]
        self.occupied_id = data[4]
        self.slot_no = data[5]
        self.rank = data[6]
        self.class_ = data[7]
        self.set_id = data[8]
        self.upgrade_limit = data[9]
        self.upgrade_curr = data[10]
        self.base_value = data[11]
        self.sell_value = data[12]
        self.pri_eff_type = data[13]
        self.pri_eff_value = data[14]
        self.prefix_eff_type = data[15]
        self.prefix_eff_value = data[16]
        self.quality = data[17]
        self.locked = data[18]
        self.level = data[19]
        self.original_grade = data[20]
        self.current_grade = data[21]
        self.original_quality = data[22]
        
        # Ajout des noms de stats depuis la base de données
        self.pri_stat_name = data[23] if len(data) > 23 else None
        self.prefix_stat_name = data[24] if len(data) > 24 else None
        
        self.substats = []

    def get_set_name(self):
        """Retourne le nom du set de runes"""
        rune_sets = {
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
            23: "tolerance",
            24: "seal",
            25: "intangible"
        }
        return rune_sets.get(self.set_id, "unknown")

    def to_table_row(self):
        """Convert rune data to a table row format"""
        return [
            self.get_set_name(),
            f"+{self.level}",
            str(self.slot_no),
            self.quality,
            self.get_main_stat_display(),
            self.get_prefix_stat_display() if self.prefix_eff_type else "",
            self.get_substats_display()
        ]

    def set_substats(self, substats):
        self.substats = substats

    @property
    def is_ancient(self):
        """Détermine si la rune est une rune ancienne"""
        return self.rank == 15 and self.class_ == 16

    def get_main_stat_display(self):
        """Retourne l'affichage de la statistique principale"""
        stat_name = self.pri_stat_name or self.get_stat_type_name(self.pri_eff_type)
        return f"{stat_name}: {self.pri_eff_value}"

    def get_prefix_stat_display(self):
        """Retourne l'affichage de la statistique préfixe"""
        if self.prefix_eff_type and self.prefix_eff_value:
            stat_name = self.prefix_stat_name or self.get_stat_type_name(self.prefix_eff_type)
            return f"{stat_name}: {self.prefix_eff_value}"
        return ""

    def get_substats_display(self):
        """Retourne l'affichage des sous-statistiques"""
        return "\n".join([f"{sub.stat_type}: {sub.stat_value}" for sub in self.substats])

    @staticmethod
    def get_stat_type_name(stat_type_id):
        """Retourne le nom du type de statistique basé sur son ID"""
        stat_types = {
            12: "HP",           # HP_FLAT
            13: "HP%",          # HP_PCT
            14: "ATK",          # ATK_FLAT
            15: "ATK%",         # ATK_PCT
            16: "DEF",          # DEF_FLAT
            17: "DEF%",         # DEF_PCT
            18: "SPD",          # SPD
            19: "TCC",          # CRIT_RATE
            20: "DCC",          # CRIT_DMG
            21: "Res",          # RES
            22: "Acc"           # ACC
        }
        return stat_types.get(stat_type_id, f"Unknown({stat_type_id})")


class RuneSubstat:
    def __init__(self, data):
        self.id = data[0]
        self.rune_id = data[1]
        self.stat_type_id = data[2]
        self.stat_value = data[3]
        self.upgrade_count = data[4]
        self.initial_value = data[5]
        self.stat_code = data[7] if len(data) > 7 else None
        self.stat_name = data[8] if len(data) > 8 else None

    @property
    def stat_type(self):
        """Retourne le type de statistique"""
        return self.stat_name or Rune.get_stat_type_name(self.stat_type_id)