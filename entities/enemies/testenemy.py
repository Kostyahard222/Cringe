from entities.entity import *

class TestEnemy(Entity):
    name = ["Enemy", "Enemy's"]

    def __init__(self):
        Entity.__init__(self, 50, 50, 8, 11, 11)

    def deathrattle(self):
        print('Enemy is ded')
        print('You won a fight, but not a war')
