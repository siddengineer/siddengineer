import time
import random
import sys
from colorama import Fore, Style, init
import pyfiglet

# Initialize colorama for colored text
init()

# Countdown timer function
def countdown(seconds):
    while seconds > 0:
        print(Fore.RED + f"\nTime remaining: {seconds} seconds" + Style.RESET_ALL)
        time.sleep(1)
        seconds -= 1
        if seconds == 0:
            print(Fore.RED + "BOOM! The bomb explodes. Mission Failed!" + Style.RESET_ALL)
            sys.exit()

# ASCII Art for Titles (pyfiglet)
def mission_title():
    ascii_banner = pyfiglet.figlet_format("Operation Cobra")
    print(Fore.GREEN + ascii_banner + Style.RESET_ALL)

# Bomb defusal logic
def defuse_bomb():
    print(Fore.YELLOW + "\nYou have found a bomb!" + Style.RESET_ALL)
    countdown(30)  # Start 30 second timer for defusal
    wire_to_cut = random.choice(['red', 'blue', 'green'])
    
    print(Fore.CYAN + "There are three wires: red, blue, and green." + Style.RESET_ALL)
    choice = input("Which wire will you cut? (red, blue, green): ")
    
    if choice == wire_to_cut:
        print(Fore.GREEN + "Success! You defused the bomb!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Wrong wire! The bomb explodes." + Style.RESET_ALL)
        sys.exit()

# Encounter with enemy
def encounter_enemy():
    print(Fore.RED + "\nAn enemy appears!" + Style.RESET_ALL)
    action = input("Do you want to (1) fight, (2) use stealth, or (3) flee? Enter 1, 2, or 3: ")

    if action == "1":
        if random.choice([True, False]):
            print(Fore.GREEN + "You defeated the enemy in hand-to-hand combat!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "The enemy overpowers you. Mission Failed!" + Style.RESET_ALL)
            sys.exit()

    elif action == "2":
        if random.choice([True, False]):
            print(Fore.GREEN + "You silently take down the enemy." + Style.RESET_ALL)
        else:
            print(Fore.RED + "You failed to sneak past the enemy. Mission Failed!" + Style.RESET_ALL)
            sys.exit()

    elif action == "3":
        print(Fore.YELLOW + "You fled from the enemy. The bomb is still active." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Invalid choice. The enemy attacks you. Mission Failed!" + Style.RESET_ALL)
        sys.exit()

# Story progression
def mission_briefing():
    print(Fore.YELLOW + "\nYou are Agent Cobra, on a mission to save Mumbai from a terrorist attack." + Style.RESET_ALL)
    print("Your mission is to infiltrate the enemy hideout, disable enemies, and defuse the bombs.")
    
    # Random scenario: enemy or bomb
    scenario = random.choice(['enemy', 'bomb'])
    if scenario == 'enemy':
        encounter_enemy()
    else:
        defuse_bomb()

# Game start
def start_game():
    mission_title()
    mission_briefing()
    
    # Continue the game loop
    while True:
        continue_mission = input("\nContinue to the next location? (yes/no): ").lower()
        if continue_mission == "yes":
            mission_briefing()
        else:
            print(Fore.YELLOW + "Mission aborted. Exiting..." + Style.RESET_ALL)
            sys.exit()

# Run the game
start_game()