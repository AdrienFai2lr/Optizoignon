class Rune:
    def __init__(self, data):
        # Champs d'identification
        self.id = data[0]
        self.rune_id = data[1]
        self.wizard_id = data[2]
        
        # Caractéristiques de base
        self.slot_no = data[3]
        self.set_id = data[4]
        self.quality = data[5]
        self.level = data[6]
        self.is_ancient = bool(data[7])
        
        # Statistique principale
        self.main_stat_type = data[8]
        self.main_stat_value = data[9]
        
        # Statistique préfixe
        self.prefix_stat_type = data[10]
        self.prefix_stat_value = data[11]
        self.prefix_grind_value = data[12]
        self.prefix_is_gemmed = bool(data[13])
        
        # Sous-statistiques
        self.substats = []
        for i in range(4):
            base_idx = 14 + (i * 4)
            stat_type = data[base_idx]
            if stat_type:  # Seulement si la sous-stat existe
                self.substats.append({
                    'type': stat_type,
                    'value': data[base_idx + 1],
                    'grind_value': data[base_idx + 2],
                    'is_gemmed': bool(data[base_idx + 3]),
                    'original_type': data[base_idx + 4]
                })
        
        # Référence au monstre équipé
        self.equipped_monster_id = data[30]

    def get_set_name(self):
        """Retourne le nom du set de runes"""
        rune_sets = {
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
        return rune_sets.get(self.set_id, "Unknown")

    def get_main_stat_display(self):
        """Affiche la statistique principale avec sa valeur"""
        return f"{self.main_stat_type}: {self.main_stat_value}"

    def get_prefix_stat_display(self):
        """Affiche la statistique préfixe avec sa valeur et le bonus de grind"""
        if not self.prefix_stat_type:
            return ""
        
        display = f"{self.prefix_stat_type}: {self.prefix_stat_value}"
        if self.prefix_grind_value > 0:
            display += f" (+{self.prefix_grind_value})"
        if self.prefix_is_gemmed:
            display += " [Gemme]"
        return display

    def get_substats_display(self):
        """Retourne l'affichage formaté des sous-statistiques"""
        return "\n".join([
            self._format_substat(substat)
            for substat in self.substats
        ])

    def _format_substat(self, substat):
        """Formate une sous-statistique pour l'affichage"""
        display = f"{substat['type']}: {substat['value']}"
        
        if substat['grind_value'] > 0:
            display += f" (+{substat['grind_value']})"
            
        if substat['is_gemmed']:
            display += f" [Gemme: {substat['original_type']}]"
            
        return display

    def to_table_row(self):
        """Convertit les données de la rune en format ligne de tableau"""
        return [
            self.get_set_name(),
            f"+{self.level}",
            str(self.slot_no),
            self.quality.capitalize(),
            self.get_main_stat_display(),
            self.get_prefix_stat_display(),
            self.get_substats_display()
        ]