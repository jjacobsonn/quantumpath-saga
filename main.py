class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = []

    def attack(self, target):
        print(f"{self.name} attacks {target}!")

    def heal(self, amount):
        self.health += amount
        print(f"{self.name} heals for {amount} points! Health is now {self.health}.")

if __name__ == "__main__":
    player_name = input("Enter your player's name: ")
    player = Player(player_name)
    print(f"Welcome, {player.name}! Your adventure begins.")