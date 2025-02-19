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
        self.substats = []  # Will be populated later

    def set_substats(self, substats):
        self.substats = substats

    @property
    def is_ancient(self):
        return self.rank == 15 and self.class_ == 16

    def to_table_row(self):
        return [
            f"Set {self.set_id}",
            f"+{self.level}",
            str(self.slot_no),
            self.quality,
            self.get_main_stat_display(),
            self.get_prefix_stat_display() if self.prefix_eff_type else "",
            self.get_substats_display()
        ]

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
            1: "HP flat",
            2: "HP%",
            3: "ATK flat",
            4: "ATK%",
            5: "DEF flat",
            6: "DEF%",
            7: "SPD",
            8: "CRIT Rate",
            9: "CRIT DMG",
            10: "RES",
            11: "ACC"
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