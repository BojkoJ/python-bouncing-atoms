import playground
import random

class Atom:

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

        if self.color == "red":
            # Červené atomy budou nejrychlejší a nejmenší
            self.speed_y = random.randint(-100, 100)
            self.speed_x = random.randint(-100, 100)
            self.rad = random.randint(18, 35)
        elif self.color == "blue":
            # Modré atomy budou druhe nejrychlejší a druhé nejmenší
            self.speed_y = random.randint(-80, 80)
            self.speed_x = random.randint(-80, 80)
            self.rad = random.randint(35, 60)
        elif self.color == "green":
            # Zelené atomy budou třetí nejrychlejší a třetí nejmenší
            self.speed_y = random.randint(-45, 45)
            self.speed_x = random.randint(-45, 45)
            self.rad = random.randint(50, 75)
        elif self.color == "yellow":
            # Žluté atomy budou nejpomalejší a nejvetší
            self.speed_y = random.randint(-20, 20)
            self.speed_x = random.randint(-20, 20)
            self.rad = random.randint(70, 95)

    def to_tuple(self):
        # Vrátíme n-tici s informacemi o atomu
        return tuple([self.x, self.y, self.rad, self.color])
    
    # Původní (NEPOUŽÍVANÁ) funkce pro hýbání atomama
    def move(self, width, height):

        # Pohne atomem a zkontroluje, jestli se náhodou nepřesunul mimo hranice
        self.x += self.speed_x
        self.y += self.speed_y

        
        if self.x > width or self.x < 0: # Pokud narazí do krajů

            self.speed_x = (self.speed_x * -1) # Změníme směr rychlosti X tím že ho vynásobíme -1

        elif self.y > height or self.y < 0:  # Nebo pokud narazí do podlahy nebo do stropu

            self.speed_y = (self.speed_y * -1)  # Změníme směr rychlosti Y tím že ho vynásobíme -1


class FallDownAtom(Atom):
    def __init__(self, x, y, color):
        super().__init__(x, y, color) # Volání původního Atom konstruktoru aby jsme to nemuseli implementovat znovu

        self.g = 3.0  # Gravitační síla
        self.damping = 0.8  # Útlum

    # Přetížená metoda move
    def move(self, width, height):
        
        # Působení gravitace na Atom
        self.speed_y += self.g

        # Rychlosti atomu
        self.x += self.speed_x
        self.y += self.speed_y

        # Pokud se atom dotkne podlahy okna
        if self.y > height:
            # Přibrždění atomu pomocí damping:

            # Rychlost y se změní na opačnou a zmenší se o damping
            self.speed_y = (self.speed_y * -self.damping)
            
            # Rychlost x se zmenší o damping
            self.speed_x = (self.speed_x * self.damping)
            
            # Nesmí se dostat pod podlahu okna
            self.y = height

        # Pokud narazí do krajů
        if self.x > width or self.x < 0:
            self.speed_x = (self.speed_x * -1)

        elif self.y < 0: # Nebo pokud narazí na strop
            self.speed_y = (self.speed_y * -1)

class ExampleWorld(object):
    def __init__(self, count, size_x, size_y):
        self.count = count
        self.width = size_x
        self.height = size_y
        self.atoms = []

        # Atom vytvoříme "count" krát
        for num in range(count):
            atom = self.random_atom()
            self.atoms.append(atom)

    # Funkce pro vytvoření náhodného atomu
    def random_atom(self):

        # Náhodně vygenerujeme souřadnice atomu
        # Hranice mezi kterými souřadnice generujeme jsou 0 a šířka/výška okna aby se negenerovaly mimo
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)

        # Náhodně vybereme barvu atomu
        colors = ['blue', 'red', 'green', 'yellow']
        color = random.choice(colors)

        return FallDownAtom(x, y, color)

    def tick(self):

        for atom in self.atoms:
            atom.move(self.width, self.height)

        atom_tuples = []

        for atom in self.atoms:
            atom_tuples.append(atom.to_tuple())

        return atom_tuples


if __name__ == '__main__':
    size_x, size_y = 900, 500

    count = 15

    world = ExampleWorld(count, size_x, size_y)

    playground.run((size_x, size_y), world)