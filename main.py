import random

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = []
        self.level = 1
        self.experience = 0

    def attack(self, target):
        damage = random.randint(5, 20)  # Random damage between 5 and 20
        critical_hit = random.random() < 0.1  # 10% chance for a critical hit
        if critical_hit:
            damage *= 2
            print(f"**Critical hit!** {self.name} attacks {target} for {damage} points of damage!")
        else:
            print(f"{self.name} attacks {target} for {damage} points of damage!")
        return damage

    def heal(self, amount):
        self.health += amount
        print(f"{self.name} heals for {amount} points! Health is now {self.health}.")

    def take_damage(self, amount):
        self.health -= amount
        print(f"{self.name} takes {amount} points of damage! Health is now {self.health}.")

    def add_item(self, item):
        self.inventory.append(item)
        print(f"{self.name} found a {item}!")

    def gain_experience(self, amount):
        self.experience += amount
        print(f"{self.name} gains {amount} XP!")
        if self.experience >= 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.health = 100 + (self.level * 10)
        print(f"{self.name} leveled up! Level: {self.level}, Health: {self.health}")

class Enemy:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def attack(self, player):
        damage = random.randint(5, 15)  # Enemy damage between 5 and 15
        print(f"{self.name} attacks {player.name} for {damage} points of damage!")
        return damage

if __name__ == "__main__":
    player_name = input("Enter your player's name: ")
    player = Player(player_name)
    print(f"\nWelcome, {player.name}! Your adventure begins.")
    print("-" * 40)

    # Possible enemies list
    enemies = [
        Enemy("Goblin", 50),
        Enemy("Troll", 75),
        Enemy("Dragon", 120)
    ]

    # Main game loop
    while player.health > 0:
        # Randomly choose an enemy
        enemy = random.choice(enemies)
        print(f"\nA wild {enemy.name} appears with {enemy.health} health!")

        # Battle loop
        while player.health > 0 and enemy.health > 0:
            print("\nWhat will you do?")
            print("1. Attack")
            print("2. Heal")
            print("3. Run away")

            choice = input("Enter the number of your action: ")
            print()

            if choice == "1":
                # Player attacks the enemy
                damage = player.attack(enemy.name)
                enemy.health -= damage

                if enemy.health > 0:
                    # Enemy retaliates
                    damage = enemy.attack(player)
                    player.take_damage(damage)
                else:
                    print(f"You have defeated the {enemy.name}!")
                    # Gain XP after winning the battle
                    player.gain_experience(random.randint(20, 50))

                    # Chance to find an item
                    if random.random() < 0.3:  # 30% chance to find an item
                        item = random.choice(["Health Potion", "Sword", "Shield"])
                        player.add_item(item)

                    break

            elif choice == "2":
                # Player heals
                player.heal(10)

            elif choice == "3":
                # Player runs away
                print(f"{player.name} runs away from the {enemy.name}!")
                break

            else:
                print("Invalid choice, try again.")

            # Check if player is still alive
            if player.health <= 0:
                print(f"{player.name} has been defeated!")
                break

        if player.health <= 0:
            print("Game over!")
            break

        # Break between battles
        print("-" * 40)
        next_action = input("Do you want to continue your adventure? (yes/no): ").lower()
        if next_action != "yes":
            print(f"{player.name} decides to rest. Adventure ends here.")
            break

    print("\nGame over.")