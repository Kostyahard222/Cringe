from entities.entity import *
from items import *

class Player(Entity):
    name = ["You", "Yours"]
    immune = []
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
        Entity.__init__(self, 999, 999, 9, 12, 12)
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
