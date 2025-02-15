class Monster:
    def __init__(self, data):
        self.name = data[0]
        self.stars = data[1]
        self.hp = data[2]
        self.attack = data[3]
        self.defense = data[4]
        self.speed = data[5]
        self.crit_rate = data[6]
        self.crit_damage = data[7]
        self.element = data[8]
        self.image_filename = data[9] if len(data) > 9 else None  # Ajout de l'image_filename
    @property
    def stars_display(self):
        return "★" * self.stars

    @property
    def crit_rate_display(self):
        return f"{self.crit_rate}%"

    @property
    def crit_damage_display(self):
        return f"{self.crit_damage}%"

    def to_table_row(self):
        return [
            self.name,
            self.stars_display,
            str(self.hp),
            str(self.attack),
            str(self.defense),
            str(self.speed),
            self.crit_rate_display,
            self.crit_damage_display,
            self.element
        ]