class Character:

    lvl = 1
    exp = 0

    def __init__(self, character_name, class_name, race):
        self.character_name = character_name
        self.class_name = class_name
        self.race = race

class Mago(Character):
    vigor = 8
    intelligence = 11
    #basic_attack = [*range(1,6)]

class Enemy:
    lvl = 1

    def __init__(self, enemy_name, attack, hp, EXP):
        self.enemy_name = enemy_name
        self.attack = attack
        self.hp = hp
        self.EXP = EXP