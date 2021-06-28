from random import randint


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

    @property
    def mana(self):
        return self._mana

    @mana.setter
    def mana(self, value):
        self._mana = max(min(value, self.manamax), 0)

    # initializes movedict
    def initmovedict(self):
        self.movedict = {
            "attack": self.attack,
            "block": self.block
        }

    # activates move from movedict
    def activatemove(self, move):
        move = move.lower()
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
        self.mana += self.manaincome

    # apples certain things, like damage, defense, etc. called right after all moves activation
    def applymoves(self, enemy):
        self.defense += enemy.damage * self.blockpercentage
        self.defense *= (1 - enemy.breakpercentage)
        self.defense = int(self.defense)
        self.health -= max(enemy.damage - self.defense, 0)
        if self.health == 0:
            self.isdead = True
            self.deathrattle()

    # subtracts certain amount of mana. if there's not enough mana retruns -1, else returns 1
    def paymana(self, cost):
        if self.mana < cost:
            return -1
        else:
            return 1

    def deathrattle(self):
        print('Entity has died')
