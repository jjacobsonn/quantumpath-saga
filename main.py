import random

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = []

    def attack(self, target):
        damage = random.randint(5, 20)  # Random damage between 5 and 20
        print(f"{self.name} attacks {target} for {damage} points of damage!")
        return damage

    def heal(self, amount):
        self.health += amount
        print(f"{self.name} heals for {amount} points! Health is now {self.health}.")

    def take_damage(self, amount):
        self.health -= amount
        print(f"{self.name} takes {amount} points of damage! Health is now {self.health}.")

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
    print(f"Welcome, {player.name}! Your adventure begins.")

    # Initialize an enemy for the player to fight
    enemy = Enemy("Goblin", 50)
    print(f"A wild {enemy.name} appears!")

    # Main game loop
    while player.health > 0 and enemy.health > 0:
        print("\nWhat will you do?")
        print("1. Attack")
        print("2. Heal")
        print("3. Run away")

        choice = input("Enter the number of your action: ")

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

    print("Game over.")