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
        try:
            # Sous-stat 1
            if data[14]:  # Vérifiez si le type existe
                self.substats.append({
                    'type': data[14],
                    'value': data[15],
                    'grind_value': data[16],
                    'is_gemmed': bool(data[17]),
                    'original_type': data[18]
                })
            
            # Sous-stat 2
            if data[19]:  # Vérifiez si le type existe
                self.substats.append({
                    'type': data[19],
                    'value': data[20],
                    'grind_value': data[21],
                    'is_gemmed': bool(data[22]),
                    'original_type': data[23]
                })
            
            # Sous-stat 3
            if data[24]:  # Vérifiez si le type existe
                self.substats.append({
                    'type': data[24],
                    'value': data[25],
                    'grind_value': data[26],
                    'is_gemmed': bool(data[27]),
                    'original_type': data[28]
                })
            
            # Sous-stat 4
            if data[29]:  # Vérifiez si le type existe
                self.substats.append({
                    'type': data[29],
                    'value': data[30],
                    'grind_value': data[31],
                    'is_gemmed': bool(data[32]),
                    'original_type': data[33]
                })
        except IndexError:
            # En cas d'erreur d'indexation, on continue avec les substats déjà traités
            pass
        
        # Référence au monstre équipé (ajustement d'index si nécessaire)
        try:
            self.equipped_monster_id = data[34] if len(data) > 34 else None
        except IndexError:
            self.equipped_monster_id = None

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
        if not self.main_stat_type:
            return "N/A"
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
        if not self.substats:
            return ""
        return "\n".join([
            self._format_substat(substat)
            for substat in self.substats
        ])

    def _format_substat(self, substat):
        """Formate une sous-statistique pour l'affichage"""
        if not substat or 'type' not in substat:
            return ""
            
        display = f"{substat['type']}: {substat['value']}"
        
        if substat.get('grind_value', 0) > 0:
            display += f" (+{substat['grind_value']})"
            
        if substat.get('is_gemmed', False):
            original = substat.get('original_type', 'Unknown')
            display += f" [Gemme: {original}]"
            
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