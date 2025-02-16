class Monster:
    def __init__(self, data):
        self.id = data[0]
        self.name = data[1]
        self.stars = data[2]
        self.hp = data[3]
        self.attack = data[4]
        self.defense = data[5]
        self.speed = data[6]
        self.crit_rate = data[7]
        self.crit_damage = data[8]
        self.element = data[9]
        self.image_filename = data[10]
        self.resistance = data[11]
        self.accuracy = data[12]
        self.skills = []  # Liste qui contiendra les skills
    
    def set_skills(self, skills):
        self.skills = skills
        print(f"✅ Monster {self.name} now has {len(self.skills)} skills: {self.skills}")  # Ajout debug

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