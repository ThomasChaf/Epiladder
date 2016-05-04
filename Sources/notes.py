class Notes():
    def __init__(self, arg, mods):
        self.notes = arg
        self.coefs = mods

    def init(self):
        for x in self.notes:
            for y in self.notes[x]:
                self.notes[x][y] = 0

    def add_note(self, note):
        module_name = note['codemodule']
        if module_name in self.notes and note['title'] in self.notes[module_name]:
            self.notes[note['codemodule']][note['title']] = note['final_note'] * self.coefs[module_name]

    def moyenne(self):
        total = 0
        coef = 0
        for module_name in self.notes:
            total += sum(self.notes[module_name].values())
            coef += self.coefs[module_name] * len(self.notes[module_name])
        return round(total / coef, 2)
