from random import uniform


class Bleeding:
    damage = 2
    duration = 0


    def __init__(self, duration):
        self.duration = duration

    def apply(self,Entity):
        if self.duration != 0 and ("Bleeding" not in Entity.immune):
            Entity.health -= self.damage
            print(Entity.name[0], "is bleeding!", Entity.name[0], "got 2 damage!", Entity.name[0], "is on", Entity.health, "hp now.", self.duration, "moves until expiration")
            self.duration -= 1
        else:
            del self
