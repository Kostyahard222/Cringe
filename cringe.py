from items import *
from entities.entity import *
from namecase import *
from entities.enemies.testenemy import *
from entities.player import *
from random import randint

# prints stats of the fight(e.x Enemy Attacks!)
def printstats(entity1, entity2):
    if entity2.move == 'attack':
        print(entity2.name[Namecase.obj], 'attacked with', entity2.damage, 'damage!', end=' ')
        if entity1.move == 'block':
            print(entity1.name[Namecase.obj], 'blocked', str(entity1.defense), 'damage.', end=' ')

    print(entity1.name[Namecase.obj], 'has', entity1.health, 'hp')



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
