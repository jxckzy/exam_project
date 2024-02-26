import random
from PIL import Image

result = 0
enemies_count = 0


class Character:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.hp_max = hp

        self.weapon = Fists()

    def attack(self, target):
        target.hp -= self.weapon.dmg
        target.hp = max(target.hp, 0)
        print(f"{self.name} has dealt {self.weapon.dmg} to {target.name} with {self.weapon.name}")


class Hero(Character):
    def __init__(self, name, hp):
        super().__init__(name=name, hp=hp)
        self.default_weapon = Fists()
        self.reset_weapon()

    def reset_weapon(self):
        self.weapon = random.choice([Gun(), Sword()])

    def equip(self):
        self.reset_weapon()
        print(f"\n{self.name} has been equipped with {self.weapon.name}")
        input("Press Enter if you want to continue the fight! \n")

    def drop(self):
        if self.weapon.usages == 0:
            self.reset_weapon()
            return input(f"Oh no, your weapon has been broken! You can buy a new weapon for 10 HP "
                         f"by typing E or continue with Fists by clicking Enter  ")
        return ""


class Enemy(Character):
    def __init__(self, name, hp):
        super().__init__(name=name, hp=hp)
        self.weapon = random.choice([Fists(), Stick()])


class Weapon:
    def __init__(self, name, dmg, usages):
        self.name = name
        self.dmg = dmg
        self.usages = usages


class Gun(Weapon):
    def __init__(self):
        super().__init__(name="Gun", dmg=10, usages=3)


class Sword(Weapon):
    def __init__(self):
        super().__init__(name="Sword", dmg=5, usages=5)


class Stick(Weapon):
    def __init__(self):
        super().__init__(name="Stick", dmg=3, usages=100)


class Fists(Weapon):
    def __init__(self):
        super().__init__(name="Fists", dmg=2, usages=150)


def log_iterator(result):
    with open("game_results.txt", "w") as file:
        file.write("Game Results:\n")
        file.write(f"Total Rounds: {result}\n")
        file.write(f"Total Enemy kill count: {enemies_count}\n")
        file.write(f"Health left of the last Enemy: {enemy.hp-2}\n")
        file.write("Game Over: Your character is dead.\n")


class PhotoIterator:
    def __init__(self, image_path):
        self.fight = image_path

    def show_photo(self):
        img = Image.open(self.fight)
        img.show()


hero = Hero(name="Hero", hp=100)
enemy = Enemy(name="Enemy", hp=100)

fight_image_path = "fight.png"
scene = PhotoIterator(fight_image_path)

while True:
    log_iterator(result)
    hero.attack(enemy)
    enemy.attack(hero)

    hero.weapon.usages -= 1
    result += 1

    print(f"Health of {hero.name}: {hero.hp}")
    print(f"Health of {enemy.name}: {enemy.hp}")

    input("Press Enter if you want to continue the fight! \n")

    if hero.weapon.usages == 0:
        choice = hero.drop()
        if choice == "E" or choice == "e":
            hero.equip()
            hero.hp -= 10
        else:
            hero.weapon = Fists()

    if enemy.hp == 0:
        print("A new enemy has been spawned!")
        enemy.hp = 100
        enemies_count += 1
        input("Press Enter if you want to continue the fight! \n")
    elif hero.hp == 0:
        print("Your character is dead and the game is over. See the results in game_results.txt")
        scene.show_photo()
        break
