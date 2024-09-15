import random

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = {"Health Potions": 2}
        self.level = 1
        self.experience = 0
        self.gold = 50  # Player starts with 50 gold
        self.weapon = {"name": "Basic Sword", "damage": (5, 10)}  # Default weapon

    def attack(self, target):
        damage = random.randint(self.weapon["damage"][0], self.weapon["damage"][1])  # Damage based on weapon
        critical_hit = random.random() < 0.1  # 10% chance for a critical hit
        if critical_hit:
            damage *= 2
            print(f"**Critical hit!** {self.name} attacks {target} with {self.weapon['name']} for {damage} points of damage!")
        else:
            print(f"{self.name} attacks {target} with {self.weapon['name']} for {damage} points of damage!")
        return damage

    def heal(self, amount):
        self.health += amount
        if self.health > 100 + (self.level * 10):  # Cap health at max health
            self.health = 100 + (self.level * 10)
        print(f"{self.name} heals for {amount} points! Health is now {self.health}.")

    def use_health_potion(self):
        if self.inventory["Health Potions"] > 0:
            self.inventory["Health Potions"] -= 1
            self.heal(30)  # Potions heal 30 points
            print(f"{self.name} used a Health Potion. Potions left: {self.inventory['Health Potions']}")
        else:
            print("No Health Potions left!")

    def take_damage(self, amount):
        self.health -= amount
        print(f"{self.name} takes {amount} points of damage! Health is now {self.health}.")

    def add_item(self, item, quantity=1):
        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity
        print(f"{self.name} found {quantity} {item}!")

    def buy_item(self, item, price, quantity=1):
        total_cost = price * quantity
        if self.gold >= total_cost:
            self.gold -= total_cost
            self.add_item(item, quantity)
            print(f"{self.name} bought {quantity} {item}(s) for {total_cost} gold.")
        else:
            print("Not enough gold!")

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

    def buy_weapon(self, weapon_name, damage_range, price):
        if self.gold >= price:
            self.gold -= price
            self.weapon = {"name": weapon_name, "damage": damage_range}
            print(f"{self.name} bought a new weapon: {weapon_name} for {price} gold!")
        else:
            print("Not enough gold!")

class Enemy:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def attack(self, player):
        damage = random.randint(5, 15)  # Enemy damage between 5 and 15
        print(f"{self.name} attacks {player.name} for {damage} points of damage!")
        return damage

def create_enemy():
    """Creates a new enemy from the list with default health."""
    enemies = [
        Enemy("Goblin", 50),
        Enemy("Troll", 75),
        Enemy("Dragon", 120)
    ]
    return random.choice(enemies)

def visit_shop(player):
    print("\nWelcome to the shop!")
    print("1. Buy Health Potion (10 gold each)")
    print("2. Buy Steel Sword (damage: 10-20, 30 gold)")
    print("3. Buy Magic Staff (damage: 15-25, 50 gold)")
    print("4. Leave shop")

    choice = input("What would you like to buy? (Enter the number): ")

    if choice == "1":
        quantity = int(input("How many health potions would you like to buy? "))
        player.buy_item("Health Potions", 10, quantity)
    elif choice == "2":
        player.buy_weapon("Steel Sword", (10, 20), 30)
    elif choice == "3":
        player.buy_weapon("Magic Staff", (15, 25), 50)
    elif choice == "4":
        print("You left the shop.")
    else:
        print("Invalid choice.")

def play_game():
    player_name = input("Enter your player's name: ")
    player = Player(player_name)
    print(f"\nWelcome, {player.name}! Your adventure begins.")
    print(f"You start with {player.gold} gold.")
    print("-" * 40)

    # Main game loop
    continue_game = True
    while player.health > 0 and continue_game:
        # Create a new enemy for each battle
        enemy = create_enemy()
        print(f"\nA wild {enemy.name} appears with {enemy.health} health!")

        # Battle loop
        while player.health > 0 and enemy.health > 0:
            print("\nWhat will you do?")
            print("1. Attack")
            print("2. Use Health Potion")
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
                    player.gold += random.randint(10, 20)  # Gain random gold
                    print(f"{player.name} now has {player.gold} gold!")

                    # Chance to find an item
                    if random.random() < 0.3:  # 30% chance to find an item
                        item = random.choice(["Health Potion", "Sword", "Shield"])
                        player.add_item(item)

                    break

            elif choice == "2":
                # Player uses a health potion
                player.use_health_potion()

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

        # After battle, allow the player to visit the shop
        print("-" * 40)
        visit_shop_choice = input("Do you want to visit the shop? (yes/no): ").lower()
        if visit_shop_choice == "yes":
            visit_shop(player)

        # Ask if the player wants to continue after defeating an enemy or running away
        print("-" * 40)
        next_action = input("Do you want to continue your adventure? (yes/no): ").lower()
        if next_action != "yes":
            continue_game = False
            print(f"{player.name} decides to rest. Adventure ends here.")

    print("\nGame over.")

if __name__ == "__main__":
    while True:
        play_game()
        play_again = input("\nDo you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            print("Thanks for playing! Goodbye.")
            break