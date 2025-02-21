class Rune:
    def __init__(self, data):
        self.id = data[0]
        self.rune_id = data[1]
        self.wizard_id = data[2]
        self.slot_no = data[3]
        self.rank = data[4]
        self.class_ = data[5]
        self.set_id = data[6]
        self.upgrade_limit = data[7]
        self.upgrade_curr = data[8]
        self.base_value = data[9]
        self.sell_value = data[10]
        self.pri_eff_type = data[11]
        self.pri_eff_value = data[12]
        self.prefix_eff_type = data[13]
        self.prefix_eff_value = data[14]
        self.quality = data[15]
        self.locked = data[16]
        self.level = data[17]
        self.original_grade = data[18]
        self.current_grade = data[19]
        self.original_quality = data[20]
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
            24: "seal",  # Nouveau set
            25: "intangible"  # Nouveau set
        }
        return rune_sets.get(self.set_id, "unknown")

    def to_table_row(self):
        """Convert rune data to a table row format"""
        return [
            self.get_set_name(),  # Nom du set au lieu de "Set X"
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
        return self.rank == 15 and self.class_ == 16

    def get_main_stat_display(self):
        return f"{self.get_stat_type_name(self.pri_eff_type)}: {self.pri_eff_value}"

    def get_prefix_stat_display(self):
        if self.prefix_eff_type and self.prefix_eff_value:
            return f"{self.get_stat_type_name(self.prefix_eff_type)}: {self.prefix_eff_value}"
        return ""

    def get_substats_display(self):
        return "\n".join([f"{sub.stat_type}: {sub.stat_value}" for sub in self.substats])

    @staticmethod
    def get_stat_type_name(stat_type_id):
        # This should be replaced with actual stat type names from the database
        stat_types = {
            12: "HP",           # HP_FLAT
            13: "HP%",          # HP_PCT
            14: "ATK",          # ATK_FLAT
            15: "ATK%",         # ATK_PCT
            16: "DEF",          # DEF_FLAT
            17: "DEF%",         # DEF_PCT
            18: "SPD",          # SPD
            19: "Taux\nCritique",  # CRIT_RATE
            20: "Dégâts\nCritiques", # CRIT_DMG
            21: "Résistance",    # RES
            22: "Précision"      # ACC
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

    @property
    def stat_type(self):
        return Rune.get_stat_type_name(self.stat_type_id)