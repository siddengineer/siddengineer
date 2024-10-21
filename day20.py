import random
from tabulate import tabulate
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

# Step 1: Define the AngryBird class
class AngryBird:
    def __init__(self, name, power, speed, ability):
        self.name = name
        self.power = power
        self.speed = speed
        self.ability = ability
        self.skills = []

    # Step 2: Method to display bird stats using Tabulate
    def display_stats(self):
        stats = [
            ["Character", self.name],
            ["Power", self.power],
            ["Speed", self.speed],
            ["Special Ability", self.ability],
            ["Skills", ", ".join(self.skills) if self.skills else 'None']
        ]
        print(Fore.BLUE + tabulate(stats, headers=["Attribute", "Value"], tablefmt="fancy_grid"))

    # Step 3: Method to power up (random increase in power and speed)
    def power_up(self):
        power_increase = random.randint(5, 15)
        speed_increase = random.randint(5, 10)
        self.power += power_increase
        self.speed += speed_increase
        print(f"\n{Fore.GREEN}{self.name} powered up! {Fore.YELLOW}Power increased by {power_increase} {Fore.CYAN}and speed increased by {speed_increase}.")

    # Step 4: Method to learn a random skill
    def learn_random_skill(self):
        skills = ['High Jump', 'Sonic Boom', 'Explosive Strike', 'Mega Speed', 'Sharp Beak']
        new_skill = random.choice(skills)
        self.skills.append(new_skill)
        print(f"\n{Fore.MAGENTA}{self.name} learned a new skill: {Fore.LIGHTRED_EX}{new_skill}.")

# Step 5: Function to display a simple menu
def game_menu():
    print("\n" + Fore.LIGHTYELLOW_EX + "--- Angry Birds Character Management ---")
    print(Fore.LIGHTGREEN_EX + "1. Display Character Stats")
    print(Fore.LIGHTGREEN_EX + "2. Power Up")
    print(Fore.LIGHTGREEN_EX + "3. Learn New Skill")
    print(Fore.LIGHTGREEN_EX + "4. Exit")

# Main function to manage the game characters
def main():
    # Predefined Angry Birds characters
    birds = {
        "Red": AngryBird("Red", power=50, speed=30, ability="Angry Shout"),
        "Chuck": AngryBird("Chuck", power=40, speed=90, ability="Speed Burst"),
        "Bomb": AngryBird("Bomb", power=80, speed=20, ability="Explosive Blast")
    }

    print(Fore.LIGHTCYAN_EX + "Choose your Angry Bird character (Red, Chuck, Bomb): ")
    char_name = input("Enter your choice: ").capitalize()

    if char_name in birds:
        player = birds[char_name]
    else:
        print(f"{Fore.RED}Invalid choice! Defaulting to Red.")
        player = birds["Red"]

    while True:
        game_menu()
        choice = input(Fore.LIGHTCYAN_EX + "Choose an option: ")

        if choice == '1':
            player.display_stats()
        elif choice == '2':
            player.power_up()
        elif choice == '3':
            player.learn_random_skill()
        elif choice == '4':
            print(Fore.LIGHTBLUE_EX + "\nExiting game...")
            break
        else:
            print(Fore.RED + "Invalid choice, please try again.")

# Run the game
if __name__ == "__main__":
    main()
