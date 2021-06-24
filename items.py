class Item:
    name = 'Item'
    description = '"Default item"'
    amount = 1

    def __init__(self, amount):
        self.amount = amount

    def activate(self, entity):
        self.amount -= 1
        self.use(entity)

    def use(self, entity):
        print("test item")

class Healer(Item):
    heal = 1

    def use(self, entity):
        entity.health += self.heal
        if entity.health == entity.healthmax:
            print('You have maxed your hp, your hp is now', entity.health)
        else:
            print('You have healed', self.heal, 'hp, you are now on', entity.health,
                  'hp')

class Bandage(Healer):
    name = 'Bandage'
    heal = 10
    description = '"Heals 10 hp"'

class Medkit(Healer):
    name = 'Medkit'
    heal = 25
    description = '"Heals 25 hp, can stop bleeding and heal fractures"'


class Adrenaline(Item):
    name = 'Adrenaline'
    description = '"Maxes out your hp and double the mana income for this fight"'

    def use(self, entity):
        entity.health = entity.healthmax
        entity.manaincome *= 2
