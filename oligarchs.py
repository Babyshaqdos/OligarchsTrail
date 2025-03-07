import random
import time

class Oligarch:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.money, self.reputation, self.health, self.power = self.set_starting_stats()
        self.inventory = {}
        self.day = 1
        self.alive = True
        self.football_fixes = 0
        self.rivals = 3
        self.passive_income = 0
        self.crackdown_chance = 5
        self.jail_chance = 2
        self.crackdown_severity = 1

    def set_starting_stats(self):
        roles = {
            "Oil Baron": (5_000_000, 30, 70, 60),
            "Tech Baron": (3_000_000, 50, 80, 40),
            "Military General": (1_000_000, 80, 90, 30),
            "Wealthy Heir": (10_000_000, 20, 90, 80),
            "KGB Agent": (500_000, 40, 90, 100)
        }
        return roles[self.role]

    def daily_decision(self):
        options = ["Bribe Government Official (-20k RUB)", "Invest in Shell Company (-500K RUB)", "Start Crypto Ponzi Scheme (-200K RUB)", "Buy Football Club (-10M RUB)",
                    "Disappear a Journalist (-100k RUB)", "Blackmail Rival (-100k RUB)", "Luxury Spa Visit (-50k RUB)", "Bribe Doctor (-100k RUB)", "Offshore Investment (50% chance of doubling money or losing 1/2)",]
        
        # Unlock dynamic options based on inventory
        if "Shell Company" in self.inventory:
            options.extend(["Launder Money", "Sell Shell Company"])

        if "Football Club" in self.inventory:
            options.extend(["Fix Matches", "Sell Football Club"])

        if "Crypto Ponzi Scheme" in self.inventory:
            options.append("Pump & Dump Crypto")

        print(f"Day {self.day}: What will you do, {self.name} the {self.role}?")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        choice = int(input("Choose: ")) - 1
        self.resolve_decision(options[choice])

    def resolve_decision(self, choice):
        if choice == "Bribe Government Official (-20k RUB)":
            if self.money < 20_000:
                print("You don't have enough money to bribe anyone.")
                return
            self.money -= 20_000
            success_chance = 35 if self.role != "KGB Agent" else 90
            success_chance += self.power
            if random.randint(1, 100) <= success_chance:
                print("Bribe successful! (+200K RUB, +20 Reputation)")
                self.money += 200_000
                self.reputation += 20
                self.power += 10
            else:
                print("Bribe failed (-20K RUB, -20 Reputation).")
                self.reputation -= 20
                self.power -= 30

        elif choice == "Invest in Shell Company (-500K RUB)":
            if self.money < 500_000:
                print("You don't have enough money to invest in a shell company.")
                return
            self.inventory["Shell Company"] = True
            self.money -= 500_000
            self.passive_income += 10_000
            print("You invested in a shell company. (-500K RUB, +10K RUB/day)")
            self.power += 5

        elif choice == "Start Crypto Ponzi Scheme (-200K RUB)":
            if self.money < 200_000:
                print("You don't have enough money to start a crypto ponzi scheme.")
                return
            self.inventory["Crypto Ponzi Scheme"] = True
            print("You started a crypto ponzi scheme. (-200K RUB, +10 Reputation, +2K RUB/day)")
            self.money -= 200_000
            self.passive_income += 2_000
            self.reputation += 10
            self.power -= 5

        elif choice == "Buy Football Club (-10M RUB)":
            if self.money < 10_000_000 or "Football Club" in self.inventory:
                print("You don't have enough money or you already own a football club.")
                return
            if self.power + self.reputation < 100:
                print("Your 'peers' mock your feeble bid for a club. (-500k RUB, -50 Reputation)")
                self.reputation -= 50
                self.money -= 500_000
            else:
                print("You bought a football club, potentially generating passive income. (-10M RUB, +15K RUB/day, +20 Reputation)")
                self.money -= 10_000_000
                self.passive_income += 5_000
                self.inventory["Football Club"] = True
                self.reputation += 20
                self.power += 5

        elif choice == "Launder Money":
            if random.randint(1, 100) <= self.power:
                print("You laundered money through your shell company. (+200K RUB)")
                self.money += 200_000
                self.power += 10
            else:
                print("Your shell company was discovered. (-10K RUB, -20 Reputation)")
                self.money -= 100_000
                self.reputation -= 20
                self.power -= 10

        elif choice == "Fix Matches":
            if self.power < 50:
                print("You get caught fixing matches. (-100K RUB, -20 Reputation)")
                self.money -= 100_000
                self.reputation -= 20
                self.football_fixes += 1
            else:                 
                print("You fixed matches for your football club. (+100K RUB, +20 Reputation)")
                self.money += 100_000
                self.reputation += 20
                self.power += 10
  

        elif choice == "Pump & Dump Crypto":
            if self.reputation + self.power > 100:
                print("You executed a pump & dump scheme. (+300K RUB, +10 Reputation)")
                self.money += 300_000
                self.reputation += 10
            else:
                print("Your pump & dump scheme failed. (-100K RUB, -20 Reputation)")
                self.money -= 100_000
                self.reputation -= 20
                if self.role == "Tech Baron":
                    print("But you are a Tech Baron, so you just call it a memecoin and the rubes eat it up! (+300K RUB, +10 Reputation)")
                    self.money += 400_000  
                    self.reputation += 30

        elif choice == "Disappear a Journalist (-100k RUB)":
            success_chance = 5 if self.role != "KGB Agent" else 90
            success_chance += self.power
            self.money -= 100_000
            if random.randint(1, 100) <= success_chance:
                print("You disappeared a journalist. (+30 Reputation, -1 Rivals)")
                self.reputation += 30
                self.power += 30
                self.rivals -= 1
            else:
                print("You failed to disappear a journalist, who in turn wrote a widely published account of your misdeeds. (-20 Reputation)")
                self.reputation -= 20

        elif choice == "Luxury Spa Visit (-50k RUB)":
            print("You enjoyed a luxury spa visit. (-50K RUB, +10 Health)")
            self.health += 10
            self.money -= 50_000
            self.power -= 5

        elif choice == "Bribe Doctor (-100k RUB)":
            print("You bribed a doctor to give you experimental treatments. (-100K RUB, +20 Health)")
            self.health += 20
            self.money -= 100_000
            if random.randint(1, 100) <= 10:
                print("The experimental treatments did not translate into humans. Your last thoughts are if your rival was responsible for this (-1000 Health)")
                self.health -= 1000

        elif choice == "Offshore Investment (50% chance of doubling money or losing 1/2)":
            print("You attempted an offshore investment. (50% chance of doubling money, 50% chance of halving money)")
            if random.randint(1, 2) == 1:
                self.money *= 2
                print("Your offshore investment paid off!")
            else:
                self.money //= 2
                print("Your offshore investment failed.")

        elif choice == "Blackmail Rival (-100k RUB)":
            success_chance = 10 if self.role != "KGB Agent" else 90
            success_chance += self.power
            if random.randint(1, 100) <= success_chance:
                print("You blackmailed a rival oligarch. (+500K RUB, -30 Reputation)")
                self.money += 500_000
                self.reputation -= 30
                self.power += 20
                if random.randint(1, 100) <= 10:
                    print("With this incriminating evidence you may never have to worry about this rival again (-1 Rival)")
                    self.rivals -= 1
                    self.power += 10
            else:
                print("You failed to blackmail a rival. (-100k RUB, -10 Reputation)")
                self.reputation -= 10
                self.money -= 100_000

        elif choice == "Sell Shell Company":
            if random.randint(1, 100) <= 70 or self.role == "Oil Baron":
                print("You sold your shell company for a profit. (+2M RUB)")
                self.money += 2_000_000
                del self.inventory["Shell Company"]
            else:
                print("Your shell company was seized by the authorities due to ongoing sanctions. (-500k RUB, -20 Reputation)")
                self.money -= 500_000
                self.reputation -= 20
                del self.inventory["Shell Company"]

        elif choice == "Sell Football Club":
            print("You sold your football club. (+5M RUB)")
            self.money += 5_000_000
            del self.inventory["Football Club"]

        self.check_health()

    def check_health(self):
        if self.health <= 0:
            print(f"{self.name} has died.")
            self.alive = False

    def check_rivals(self):
        if self.rivals <= 0:
            print("You have eliminated all your rivals and are the supreme oligarch!")
            self.alive = False

    def next_day(self):
        if self.alive:
            self.day += 1
            self.health -= random.randint(1, 5)
            self.money += self.passive_income
            self.random_crackdown()
            print(f"Day {self.day} ends. Health: {self.health}, Money: {self.money:,}, Reputation: {self.reputation}, Rivals Left: {self.rivals}")
            if self.day % 5 == 0:
                self.crackdown_chance += 3
                self.jail_chance += 2
                self.crackdown_severity += 1
        else:
            print("Game Over.")

    def random_crackdown(self):
        if random.randint(1, 100) <= self.crackdown_chance:
            print("Government crackdown! Some assets have been seized.")
            seizeable_assets = [k for k in self.inventory.keys() if k not in ["Football Club"]]
            severity = random.randint(1, self.crackdown_severity)
            for _ in range(severity):
                if seizeable_assets:
                    seized = random.choice(seizeable_assets)
                    print(f"{seized} has been seized.")
                    del self.inventory[seized]
                    self.passive_income -= 100_000
        if random.randint(1, 100) <= self.jail_chance:
            print("You have been sent to jail. All assets have been seized.")
            self.inventory = {}
            self.money = 100_000
            self.passive_income = 0

    def check_endings(self):
        if self.money >= 50_000_000:
            print("You retire to a private island with billions in offshore accounts. Congratulations!")
            self.alive = False
        elif self.reputation >= 100:
            print("You ascend to political power and become president for life!")
            self.alive = False
        elif self.health <= 0:
            print("Your reckless lifestyle has caught up with you. You die under mysterious circumstances.")
            self.alive = False


def start_game():
    name = input("Enter your Oligarch's name: ")
    print("Choose your background:")

    roles = ["Oil Baron", "Tech Baron", "Military General", "Wealthy Heir", "KGB Agent"]
    # Stats descriptions for each role
    role_descriptions = [
        "(+5M RUB, +40 Reputation, +70 Health)",
        "(+3M RUB, +60 Reputation, +80 Health)",
        "(+1M RUB, +80 Reputation, +90 Health)",
        "(+10M RUB, +30 Reputation, +90 Health)",
        "(+500K RUB, +40 Reputation, +90 Health)"
    ]

    for i, (role, description) in enumerate(zip(roles, role_descriptions), 1):
        print(f"{i}. {role} {description}")

    
    role_choice = int(input("Choose: ")) - 1
    player = Oligarch(name, roles[role_choice])

    while player.alive:
        player.daily_decision()
        player.next_day()
        time.sleep(3)

if __name__ == "__main__":
    start_game()
