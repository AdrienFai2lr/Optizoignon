class Skill:
    def __init__(self, data):
        self.id = data[0]
        self.name = data[1]
        self.description = data[2]
        self.cooldown = data[3]
        self.hits = data[4]
        self.aoe = bool(data[5])
        self.passive = bool(data[6])
        self.icon_filename = data[7]
        self.level_progress_description = data[8]