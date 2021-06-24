import math
from random import randint
from enum import IntEnum


# prints stats of the fight(e.x Enemy Attacks!)
def printstats(entity1, entity2):
    if entity2.move == 'attack':
        print(entity2.name[Namecase.obj], 'attacked with', entity2.damage, 'damage!', end=' ')
        if entity1.move == 'block':
            print(entity1.name[Namecase.obj], 'blocked', str(entity1.defense), 'damage.', end=' ')

    print(entity1.name[Namecase.obj], 'has', entity1.health, 'hp')


# enum for cases of names
class Namecase(IntEnum):
    obj = 0  # objective case
    poss = 1  # possesive case


# class for base entities(enemy, player, etc)
class Entity:
    name = ["Entity", "Entity's"]  # name in subjective and possessive cases
    damage = 0  # overall damage in this turn
    defense = 0  # overall defense in this turn
    move = ""  # name of move you did in this turn
    breakpercentage = 0  # percentage of enemy's defense to be broken (ex. if it's 0.5 enemy's defense is halved)
    blockpercentage = 0  # percentage of damage to be blocked in this turn (adds up to defense)
    _mana = 0
    manaincome = 1
    isdead = False

    def __init__(self, health, healthmax, attackmin, attackmax, attackcrit, blockmin=5, blockdelta=0.2, manamax=10):
        self.healthmax = healthmax
        self.health = health
        self.attackmin = min(attackmax, attackmin)  # prevent min attack from being higher than max attack
        self.attackmax = max(attackmax, self.attackmin)  # prevent max attack from being lower than min attack
        self.attackcrit = attackcrit
        self.blockmin = blockmin
        self.blockdelta = blockdelta
        self.manamax = manamax
        self.initmovedict()

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = max(min(value, self.healthmax), 0)

    @health.deleter
    def health(self):
        del self._health

    @property
    def mana(self):
        return self._mana

    @mana.setter
    def mana(self, value):
        self._mana = max(min(value, self.manamax), 0)

    @mana.deleter
    def mana(self):
        del self._mana

    # initializes movedict
    def initmovedict(self):
        self.movedict = {
            "attack": self.attack,
            "block": self.block
        }

    # activates move from movedict
    def activatemove(self, move):
        for i in self.movedict:
            if move == i:
                self.move = move
                self.movedict[i]()  # execute move

    def attack(self):
        attack = randint(self.attackmin, self.attackmax)
        if attack == self.attackcrit:
            self.breakpercentage = 0.5
        self.damage += attack

    def block(self):
        self.blockpercentage = max((randint(0, 10) - 5) * self.blockdelta, 0)

    # called at start of every turn
    def update(self):
        self.defense = 0
        self.damage = 0
        self.blockpercentage = 0
        self.breakpercentage = 0
        self.move = ""
        self.mana = min(self.manamax, self.mana + self.manaincome)

    # apples certain things, like damage, defense, etc. called right after all moves activation
    def applymoves(self, enemy):
        self.defense += enemy.damage * self.blockpercentage
        self.defense *= (1 - enemy.breakpercentage)
        self.defense = int(self.defense)
        self.health -= max(enemy.damage - self.defense, 0)
        if self.health == 0:
            self.isdead = True
            self.deathrattle()

    # subtracts certain amount of mana. if there's not enough mana retruns -1, else returns 0
    def paymana(self, cost):
        if (self.mana < cost):
            return -1
        else:
            return 0

    def deathrattle(self):
        print('Entity has died')


# item helper functions
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


class Player(Entity):
    name = ["You", "Yours"]

    invArr = []

    def initmovedict(self):
        self.movedict = {
            "attack": self.attack,
            "block": self.block,
            "item": self.getitem
        }

    def initinventory(self):
        self.invArr = []
        self.invArr.append(Bandage(4))
        self.invArr.append(Medkit(1))
        self.invArr.append(Adrenaline(2))

    def __init__(self):
        Entity.__init__(self, 50, 50, 9, 12, 12)
        self.initinventory()

    def deathrattle(self):
        print('You died, fucking cringe')

    def getitem(self):
        print('Your items are:')
        for item in self.invArr:
            print(item.name, item.amount, end=' ', sep=' - ')

        print('\nType the name of the item you want to use')
        itemname = input().upper()

        for item in self.invArr:
            if item.name.upper() == itemname:
                print('You want to use', item.name)
                print(item.description)
                print('Are you sure? Y/N')
                confirm = input().upper()
                while confirm != 'Y' and confirm != 'N':
                    confirm = input().upper()
                if confirm == 'Y':
                    item.use(self)
                break
        else:
            print("This item doesn't exist or you don't have it in your inventory")


class TestEnemy(Entity):
    name = ["Enemy", "Enemy's"]

    def __init__(self):
        Entity.__init__(self, 50, 50, 8, 11, 11)

    def deathrattle(self):
        print('Enemy is ded')
        print('You won a fight, but not a war')


player = Player()
enemy = TestEnemy()

while True:
    player.update()
    enemy.update()
    player.activatemove(input())
    enemy.activatemove("attack")
    player.applymoves(enemy)
    enemy.applymoves(player)
    if not (player.isdead or enemy.isdead):
        printstats(player, enemy)
        printstats(enemy, player)
    else:
        break
