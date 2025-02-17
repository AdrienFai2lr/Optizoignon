class Skill:
    def __init__(self, data):
        self.id = data[0]
        self.name = data[1]
        self.description = data[2]
        self.cooldown = data[3]
        self.hits = data[4]
        self.multiplier_formula = data[5]
        self.aoe = data[6]
        self.passive = data[7]
        self.icon_filename = data[8]
        self.level_progress_description = data[9]
        
    def __str__(self):
        return f"{self.name} (ID: {self.id})"