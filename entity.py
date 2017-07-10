
class Entity:
#On crée une classe pour tout les "objets"
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        # Move the entity by a given amount d veut dire difference
        self.x += dx
        self.y += dy

class Adventurer(Entity):

    def __init__(self, x, y, char, color):
        Entity.__init__(self, x, y, char, color)
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.HP = 10
