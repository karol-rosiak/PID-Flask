#sterownik=>zbiornik=>sterownik
class ZBIORNIK:

    def __init__(self):
        self.doplyw = 30
        self.poziom = 20
        self.maxpojemnosc = 50
        self.odplyw = 7

    def open(self, x):
        self.poziom=self.poziom + self.doplyw*(x/100) - self.odplyw
