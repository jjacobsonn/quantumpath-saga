import random


class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = {"Health Potions": 2, "Shield": False}  # Start without a shield
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 250  # XP needed to reach the next level
        self.gold = 50  # Player starts with 50 gold
        self.weapon = {"name": "Basic Sword", "damage": (5, 10)}  # Default weapon
        self.armor = {"name": "None", "defense": 0}  # No armor by default

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
        reduced_damage = amount - self.armor["defense"]
        if self.inventory["Shield"]:
            reduced_damage = max(0, reduced_damage // 2)  # Shield halves the damage
            print(f"{self.name} blocks with their shield! Damage reduced by half.")
        reduced_damage = max(0, reduced_damage)  # Ensure damage doesn't go below 0
        self.health -= reduced_damage
        print(f"{self.name} takes {reduced_damage} points of damage after armor. Health is now {self.health}.")

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

    def buy_weapon(self, weapon_name, damage_range, price):
        if self.gold >= price:
            self.gold -= price
            self.weapon = {"name": weapon_name, "damage": damage_range}
            print(f"{self.name} bought a new weapon: {weapon_name} for {price} gold!")
        else:
            print("Not enough gold!")

    def buy_armor(self, armor_name, defense, price):
        if self.gold >= price:
            self.gold -= price
            self.armor = {"name": armor_name, "defense": defense}
            print(f"{self.name} bought new armor: {armor_name} with {defense} defense for {price} gold!")
        else:
            print("Not enough gold!")

    def buy_shield(self, price):
        if self.gold >= price:
            self.gold -= price
            self.inventory["Shield"] = True
            print(f"{self.name} bought a shield for {price} gold!")
        else:
            print("Not enough gold!")

    def gain_experience(self, amount):
        """Adds experience to the player and handles leveling up."""
        self.experience += amount
        print(f"{self.name} gains {amount} XP!")
        if self.experience >= self.experience_to_next_level:
            self.level_up()

        # Show progress toward next level
        print(f"XP: {self.experience}/{self.experience_to_next_level}")

    def level_up(self):
        """Increases the player's level, experience requirements, and unlocks new monsters and items."""
        self.level += 1
        self.experience = 0
        self.experience_to_next_level += 250  # Increase XP required for the next level
        self.health = 100 + (self.level * 10)  # Increase max health with level
        print(f"{self.name} leveled up! Now level {self.level} with {self.health} max health.")

        # Unlock better weapons and enemies at certain levels
        if self.level == 3:
            print("New weapons and enemies unlocked!")
        elif self.level == 5:
            print("More powerful weapons and stronger enemies unlocked!")


class Enemy:
    def __init__(self, name, health):
        self.name = name
        self.health = health

    def attack(self, player):
        damage = random.randint(5, 15)  # Enemy damage between 5 and 15
        print(f"{self.name} attacks {player.name} for {damage} points of damage!")
        return damage


def create_enemy(player_level):
    """Creates a new enemy based on player's level."""
    enemies = [
        Enemy("Goblin", 50),
        Enemy("Troll", 75)
    ]
    if player_level >= 3:
        enemies.append(Enemy("Dragon", 120))
    if player_level >= 5:
        enemies.append(Enemy("Ogre", 150))
    return random.choice(enemies)


def visit_shop(player):
    while True:
        print(f"\n{player.name} has {player.gold} gold.")
        print("\nWelcome to the shop!")
        print("1. Buy Health Potion (10 gold each)")
        print("2. Buy Steel Sword (damage: 10-20, 30 gold)")
        print("3. Buy Leather Armor (defense: 3, 20 gold)")
        print("4. Buy Iron Armor (defense: 5, 40 gold)")
        print("5. Buy Shield (50 gold)")

        # Add higher-level weapons depending on the player's level
        if player.level >= 3:
            print("6. Buy Magic Staff (damage: 15-25, 50 gold)")
        if player.level >= 5:
            print("7. Buy Legendary Sword (damage: 25-35, 100 gold)")

        print("8. Leave shop")

        choice = input("What would you like to buy? (Enter the number or '8' to exit): ")

        if choice == "1":
            quantity = int(input("How many health potions would you like to buy? "))
            player.buy_item("Health Potions", 10, quantity)
        elif choice == "2":
            player.buy_weapon("Steel Sword", (10, 20), 30)
        elif choice == "3":
            player.buy_armor("Leather Armor", 3, 20)
        elif choice == "4":
            player.buy_armor("Iron Armor", 5, 40)
        elif choice == "5":
            player.buy_shield(50)
        elif choice == "6" and player.level >= 3:
            player.buy_weapon("Magic Staff", (15, 25), 50)
        elif choice == "7" and player.level >= 5:
            player.buy_weapon("Legendary Sword", (25, 35), 100)
        elif choice == "8":
            print("You left the shop.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

        # Ask to continue shopping
        continue_shopping = input("Do you want to buy something else? (yes/no): ").lower()
        if continue_shopping != "yes":
            print("You left the shop.")
            break


def play_game():
    player_name = input("Enter your player's name: ")
    player = Player(player_name)
    print(f"\nWelcome, {player.name}! Your adventure begins.")
    print(f"You start with {player.gold} gold.")
    print("-" * 40)

    continue_game = True
    while player.health > 0 and continue_game:
        # Create a new enemy for each battle based on player's level
        enemy = create_enemy(player.level)
        print(f"\nA wild {enemy.name} appears with {enemy.health} health!")

        # Battle loop
        while player.health > 0 and enemy.health > 0:
            print("\nWhat will you do?")
            print("1. Attack")
            print("2. Use Health Potion")
            if player.inventory["Shield"]:
                print("3. Block with Shield")
            print("4. Run away")

            choice = input("Enter the number of your action: ")
            print()

            if choice == "1":
                damage = player.attack(enemy.name)
                enemy.health -= damage

                if enemy.health > 0:
                    damage = enemy.attack(player)
                    player.take_damage(damage)
                else:
                    print(f"You have defeated the {enemy.name}!")
                    player.gain_experience(random.randint(50, 100))  # More XP for tougher enemies
                    player.gold += random.randint(10, 20)  # Gain random gold
                    print(f"{player.name} now has {player.gold} gold!")

                    # Chance to find an item
                    if random.random() < 0.3:  # 30% chance to find an item
                        item = random.choice(["Health Potion", "Sword", "Shield"])
                        player.add_item(item)

                    break

            elif choice == "2":
                player.use_health_potion()

            elif choice == "3" and player.inventory["Shield"]:
                print(f"{player.name} blocks with their shield!")
                damage = enemy.attack(player)
                player.take_damage(damage // 2)  # Blocking halves the damage

            elif choice == "4":
                print(f"{player.name} runs away from the {enemy.name}!")
                break

            else:
                print("Invalid choice, try again.")

            if player.health <= 0:
                print(f"{player.name} has been defeated!")
                break

        if player.health <= 0:
            print("Game over!")
            break

        print("-" * 40)
        visit_shop_choice = input("Do you want to visit the shop? (yes/no): ").lower()
        if visit_shop_choice == "yes":
            visit_shop(player)

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