import tkinter as tk
from tkinter import Label, Button, StringVar, Entry, Radiobutton, Frame
from PIL import Image, ImageTk
import random





def bribe_condition(player):
    """Bribe success chance based on player power and reputation."""
    if player.power >= 80 and player.reputation >= 70:
        return True
    return False





MILESTONES = {
    1: "empire_crumbles.png",  # Example milestone at day 10 (for example purposes)
    4: "voucher_wars.png",     # Another milestone at day 50
    10: "business_or_bullet.png",      # Mid 1990s
    12: "ruble_meltdown.png",          # 2000s
    14: "new_rules_new_risks.png",    # Current day
}



class Player:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.money, self.reputation, self.health, self.power = self.set_starting_stats()
        self.inventory = {}
        self.day = 0
        self.event_chance = 0.01  # Daily chance of a random event
        self.alive = True

    def set_starting_stats(self):
        roles = {
            "Oil Baron (+5M RUB, +40 Reputation, +60 Health)": (5_000_000, 40, 60, 50),
            "Tech Baron (+3M RUB, +60 Reputation, +80 Health)": (3_000_000, 60, 80, 40),
            "Military General (+1M RUB, +80 Reputation, +90 Health)": (1_000_000, 80, 90, 30),
            "Wealthy Heir (+10M RUB, +30 Reputation, +80 Health)": (10_000_000, 30, 80, 80),
            "KGB Agent (+500K RUB, +40 Reputation, +90 Health)": (500_000, 40, 90, 100)
        }
        return roles[self.role]

    def apply_event(self, event):
        self.money += event.money_change
        self.reputation = max(0, min(100, self.reputation + event.reputation_change))
        self.health = max(0, min(100, self.health + event.health_change))
        self.power = max(0, min(100, self.power + event.power_change))

        # Check for health-based death
        if self.health <= 0:
            self.alive = False

        # Check for bankruptcy
        if self.money < 0:
            self.alive = False



    def attempt_bribe(self):
        success = self.stat_weighted_success([("power", 0.6), ("reputation", 0.4)], difficulty=50)
        if success:
            self.money -= 20000
            self.reputation += 5
            self.power += 2
            return True, "Bribe successful. Your influence grows."
        else:
            self.money -= 20000
            self.reputation -= 10
            self.power -= 5
            return False, "Bribe failed. You’ve attracted unwanted attention."

    def update_message(self, title, description):
        # You can use this function to display messages on the screen.
        print(f"{title}: {description}")


class GameEvent:
    def __init__(self, name, money_change=0, reputation_change=0, health_change=0, power_change=0, description="", condition=None, outcomes=None):
        self.name = name
        self.money_change = money_change
        self.reputation_change = reputation_change
        self.health_change = health_change
        self.power_change = power_change
        self.description = description
        self.condition = condition  # Optional function that returns True/False
        self.outcomes = outcomes  # Optional list of possible outcomes (dicts)

    def apply_random_outcome(self, player):
        if self.outcomes:
            outcome = random.choice(self.outcomes)
            player.money += outcome.get('money_change', 0)
            player.reputation += outcome.get('reputation_change', 0)
            player.health += outcome.get('health_change', 0)
            player.power += outcome.get('power_change', 0)

            # Clamp stats
            player.reputation = max(0, min(100, player.reputation))
            player.health = max(0, min(100, player.health))
            player.power = max(0, min(100, player.power))

            return outcome.get('description', "")
        else:
            # Apply default values and clamp
            player.money += self.money_change
            player.reputation = max(0, min(100, player.reputation + self.reputation_change))
            player.health = max(0, min(100, player.health + self.health_change))
            player.power = max(0, min(100, player.power + self.power_change))
            return self.description

RANDOM_EVENTS = [
    GameEvent(
        "Stock Market Crash",
        description="The stock market is in free fall.",
        outcomes=[
            {"money_change": -1_000_000, "reputation_change": -5, "description": "You lost a fortune in speculative investments."},
            {"money_change": -500_000, "reputation_change": -2, "description": "You pulled out just in time but still took a hit."},
            {"money_change": 0, "reputation_change": +3, "description": "You shorted the market and emerged smarter than ever."}
        ]
    ),
    GameEvent(
        "Political Scandal", 
        description="A political scandal has rocked the nation.", 
        outcomes=[
            {"money_change": -500_000, "reputation_change": -10, "description": "You were directly implicated!"},
            {"money_change": -100_000, "reputation_change": -5, "description": "You managed to stay out of the spotlight."},
            {"money_change": 0, "reputation_change": +5, "description": "You leaked the scandal and gained clout!"}
        ]
    ),
    GameEvent(
        "Government Crackdown",
        description="The state is flexing its muscle again.",
        outcomes=[
            {"money_change": -1_000_000, "reputation_change": -10, "health_change": -20, "description": "A full investigation and asset freeze struck hard."},
            {"money_change": -500_000, "reputation_change": -5, "health_change": -10, "description": "Some light arrests and fines kept you in line."},
            {"money_change": -100_000, "reputation_change": 0, "health_change": 0, "description": "A warning shot—just enough to rattle you."}
        ]
    ),
    GameEvent(
        "Bribe Attempt",
        condition=bribe_condition,
        description="You tried to grease the right palms.",
        outcomes=[
            {"money_change": -50_000, "reputation_change": -5, "description": "Your offer was rejected and reported."},
            {"money_change": -20_000, "reputation_change": +5, "power_change": +2, "description": "The bribe was accepted—doors are opening."},
            {"money_change": -100_000, "reputation_change": -10, "power_change": -5, "description": "You bribed the wrong person. Oops."}
        ]
    ),
    GameEvent(
        "Business Opportunity",
        description="A shady investment falls in your lap.",
        outcomes=[
            {"money_change": +500_000, "reputation_change": +5, "description": "It actually paid off handsomely!"},
            {"money_change": 0, "reputation_change": 0, "description": "It was a wash, but you didn't lose anything."},
            {"money_change": -250_000, "reputation_change": -5, "description": "Turns out it was a scam all along."}
        ]
    ),
    GameEvent(
        "Assassination Attempt",
        description="Someone wants you dead.",
        outcomes=[
            {"health_change": -50, "description": "A car bomb missed its mark—but you were injured."},
            {"health_change": -25, "description": "A sniper attempt left you shaken and bruised."},
            {"health_change": 0, "description": "You escaped unharmed. Too close for comfort."}
        ]
    ),
    GameEvent(
        "Offshore Windfall",
        description="A foreign account lights up unexpectedly.",
        outcomes=[
            {"money_change": +1_000_000, "description": "An old Cayman account matured. Jackpot!"},
            {"money_change": +500_000, "description": "A forgotten Swiss bond finally cleared."},
            {"money_change": +2_000_000, "description": "Shell company profits poured in unexpectedly."}
        ]
    )
]



class GameGUI:
    global image_path
    def __init__(self, root):
        self.root = root
        self.player = None
        self.root.geometry("800x600")
        self.root.eval('tk::PlaceWindow . center')
        self.show_welcome_screen()

    def start_game(self):
        name = self.name_entry.get()
        role = self.role_var.get()
        
        if not name or not role:
            Label(self.root, text="Please enter your name and select a role!", fg="red").pack()
            return
        
        self.player = Player(name, role)
        self.show_game_screen()

        
    def generate_random_event(self, player):
        """Generates a random event with a weighted chance based on the player's stats."""
        valid_events = []

        # Filter events based on player stats and conditions
        for event in RANDOM_EVENTS:
            if event.condition is None or event.condition(player):
                valid_events.append(event)

        if valid_events:
            return random.choice(valid_events)
        else:
            return None
    
    
    def check_for_random_event(self):
        """Check if a random event happens based on a daily chance and player's stats."""
        # Base chance of an event
        base_chance = self.player.event_chance

        # Adjust base chance based on stats
        if self.player.power > 75:
            base_chance += 0.05  # 5% more likely if power is high
        if self.player.reputation > 60:
            base_chance += 0.03  # 3% more likely if reputation is high
        if self.player.money > 10_000_000:
            base_chance += 0.02  # More chance if the player is wealthy

        # Check if an event occurs based on adjusted chance
        if random.random() < base_chance:
            event = self.generate_random_event(self.player)
            if event:
                self.trigger_event(event)
            else:
                self.update_game_text("No random event triggered today.")
    
    def trigger_event(self, event: GameEvent):
        message = event.apply_random_outcome(self.player)
        full_message = f"Event: {event.name}\n\n{message}"
        self.update_game_text(full_message)
        self.update_stats_display()

    
    def advance_day(self):
        self.player.day += 1
        self.player.event_chance += 0.01  # Increase the chance slightly every day
        self.check_for_random_event()
        # Check if a milestone has been reached
        if self.player.day in MILESTONES:
            self.root.unbind("<Configure>")
            self.update_image_for_milestone(MILESTONES[self.player.day])
        self.check_win_condition()
        self.check_game_over() 

    def stat_weighted_success(self, relevant_stats, difficulty=50):
        """
        relevant_stats: list of (stat_name, weight) tuples.
        difficulty: threshold for success, 0-100.
        """
        total = 0
        for stat_name, weight in relevant_stats:
            total += getattr(self, stat_name) * weight

        max_total = sum([100 * weight for _, weight in relevant_stats])
        success_chance = total / max_total  # normalize to 0-1
        roll = random.random()
        return roll < success_chance
    
    def check_game_over(self):
        if not self.player.alive:
            if self.player.health <= 0:
                self.update_game_text("💀 You have died. The ruthless climb to power has claimed your life.")
            elif self.player.money < 0:
                self.update_game_text("📉 You’ve gone bankrupt. The wolves have come to collect, and there's nothing left to give.")
            self.disable_game_inputs()


    def update_image_for_milestone(self, image_file):
        """ Change the image based on the milestone reached. """
        try:
            # Load the new image based on the milestone
            new_image = Image.open(image_file)
            global image_path 
            image_path = image_file  # Update the global image path variable
            self.update_image(new_image)
            self.root.bind("<Configure>", lambda event: self.update_image(new_image))
        except FileNotFoundError:
            print(f"Image {image_file} not found.")

    def show_welcome_screen(self):
        self.clear_screen()
        # Load and display the welcome image
        global image_path
        image_path = "oligarch.png" 
        image = Image.open(image_path)   # Replace with your welcome image path
        self.canvas_for_image = tk.Canvas(self.root, bg='gray', highlightthickness=0)
        self.canvas_for_image.pack(fill="both", expand=True)
        self.canvas_for_image.image = ImageTk.PhotoImage(image)
        self.canvas_for_image.create_image(0, 0, image=self.canvas_for_image.image, anchor='nw')
        # Dynamically resize image to fit the available space
        self.update_image(image)
        # Bind resizing event to adjust the image when window size changes
        self.root.bind("<Configure>", lambda event: self.update_image(image))


        Label(self.root, text="Welcome to Oligarchs Trail!", font=("Arial", 24)).pack(pady=20)
        Button(self.root, text="Start", command=self.show_character_selection).pack(pady=10)
        Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def show_character_selection(self):
        self.clear_screen()
        # Load and display the welcome image
        global image_path
        image = Image.open(image_path)   # Replace with your welcome image path
        self.canvas_for_image = tk.Canvas(self.root, bg='gray', highlightthickness=0)
        self.canvas_for_image.pack(fill="both", expand=True)
        self.canvas_for_image.image = ImageTk.PhotoImage(image)
        self.canvas_for_image.create_image(0, 0, image=self.canvas_for_image.image, anchor='nw')
        # Dynamically resize image to fit the available space
        self.update_image(image)
        # Bind resizing event to adjust the image when window size changes
        #self.root.bind("<Configure>", lambda event: self.update_image(image))
        Label(self.root, text="Enter your name:").pack()
        self.name_entry = Entry(self.root)
        self.name_entry.pack()
        Label(self.root, text="Select your role:").pack()
        self.role_var = StringVar()
        roles = [
            "Oil Baron (+5M RUB, +40 Reputation, +60 Health)", 
            "Tech Baron (+3M RUB, +60 Reputation, +80 Health)", 
            "Military General (+1M RUB, +80 Reputation, +90 Health)",
            "Wealthy Heir (+10M RUB, +30 Reputation, +80 Health)", 
            "KGB Agent (+500K RUB, +40 Reputation, +90 Health)"
        ]
        for role in roles:
            Radiobutton(self.root, text=role, variable=self.role_var, value=role).pack()
        Button(self.root, text="Start Game", command=self.start_game).pack()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_game_screen(self):
        self.clear_screen()
        main_frame = Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        #Left Panel for Artwork (Expandable)
        self.art_panel = Frame(main_frame, bg="gray")
        self.art_panel.pack(side="left", fill="both", expand=True)

        #Right Panel for Stats
        self.stats_panel = Frame(main_frame, width=200, bg="lightgray")
        self.stats_panel.pack(side="right", fill="y")

        #Add a label to display messages
        self.message_label = Label(self.stats_panel, text="", wraplength=250, justify="left", bg="lightgray")
        self.message_label.pack(pady=10)

        #Add the Scrollable Text Box for Game Messages
        self.text_frame = Frame(self.root, bg="white")
        self.text_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.text_box = tk.Text(self.text_frame, wrap="word", height=2, bg="white", font=("Arial", 10))
        self.text_box.pack(side="left", fill="both", expand=True)

        self.text_scroll = tk.Scrollbar(self.text_frame, command=self.text_box.yview)
        self.text_scroll.pack(side="right", fill="y")

        self.text_box.config(yscrollcommand=self.text_scroll.set)

        image_path = "empire_crumbles.png"  # Replace with your image path

        #Load and Display Image
        image = Image.open(image_path)  

        self.canvas_for_image = tk.Canvas(self.art_panel, bg='gray', highlightthickness=0)
        self.canvas_for_image.pack(fill="both", expand=True)

        #Dynamically resize image to fit the available space
        self.update_image(image)

        #Bottom Panel for Options
        self.options_panel = Frame(self.root, bg="darkgray")
        self.options_panel.pack(side="bottom", fill="x")

        self.options_menu()

        message = f"Welcome to Oligarchs Trail, {self.player.name}! \n\n" \
                f"The year is 1991, Mikhail Gorbachev has ceded power to Boris Yeltsen. Several Soviet states including Ukraine and Belarus have left the Union.\n" \
                f"The USSR is no more. \n\n"\
                f"But where one ruler falls, more yet may still rise. Your goal in the ensuing chaos is simple: Amass as much wealth and power as you can\n" \
                f"Be wary though, forces are at play that may seek to undermine you... \n\n" \
                f"Your choices will shape your path, and the world around you. \n" \
                f"Will you become a powerful oligarch, or will you fall victim to the very system you seek to exploit?\n\n" \
                f"Choose wisely, and we may see each other again in the year 2020 Tovarishch!"
        #Update the message label with the welcome message

        self.update_game_text(message)

        self.update_stats_display()
        #Bind resizing event to adjust the image when window size changes
        self.root.bind("<Configure>", lambda event: self.update_image(image))

    def update_image(self, image):
        """ Resize and update the image based on the current canvas size """
        canvas_width = self.canvas_for_image.winfo_width()
        canvas_height = self.canvas_for_image.winfo_height()

        if canvas_width > 1 and canvas_height > 1:
            resized_image = image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
            self.canvas_for_image.image = ImageTk.PhotoImage(resized_image)
            self.canvas_for_image.create_image(0, 0, image=self.canvas_for_image.image, anchor='nw')

    def update_stats_display(self):
        for widget in self.stats_panel.winfo_children():
            widget.destroy()
        Label(self.stats_panel, text=f"Money: {self.format_money(self.player.money)}").pack()
        Label(self.stats_panel, text=f"Reputation: {self.player.reputation}").pack()
        Label(self.stats_panel, text=f"Health: {self.player.health}").pack()
        Label(self.stats_panel, text=f"Power: {self.player.power}").pack()

    def update_game_text(self, new_message):
        """Append a new message to the text box and auto-scroll to the bottom."""
        self.text_box.insert("end", new_message + "\n\n")  #Add the new message
        self.text_box.yview_moveto(1.0)  #Auto-scroll to the latest message

    
    def options_menu(self):
        options = [
            ("Bribe Government Official", -20000, 5, 0, 2),
            ("Invest in Shell Company", -500000, 10, 0, 5),
            ("Start Crypto Ponzi Scheme", -200000, 20, 0, 10),
            ("Buy Football Club", -10000000, 50, 0, 15),
            ("Disappear a Journalist", -100000, -10, 0, 5),
            ("Blackmail Rival", -100000, 15, 0, 5),
            ("Luxury Spa Visit", -50000, 0, 10, 0),
            ("Bribe Doctor", -100000, 0, 20, 0),
            ("Offshore Investment", 0, 0, 0, 0)
        ]
        
        rows = 2
        cols = (len(options) + rows - 1) // rows  #Calculate columns dynamically
        for index, option in enumerate(options):
            row = index // cols
            col = index % cols
            event_name, money_change, reputation_change, health_change, power_change = option

            event_data = GameEvent(event_name, money_change, reputation_change, health_change, power_change, "")

            # Check if the player can afford the action (consider money decrease only)
            can_afford = self.player.money + money_change >= 0

            btn = Button(self.options_panel, text=event_name, 
                        command=lambda event=event_data: self.apply_option(event))

            if not can_afford:
                btn.configure(state='disabled')

            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

    def apply_option(self, event):
        if event:  #Check if the event is valid
            #Apply the event to the player's stats
            self.player.apply_event(event)
                
                #Update the stats display
            self.update_stats_display()
            #Update the message label with event description
            message = f"You chose to {event.name}.\n\nEffects: " \
                    f"Money {event.money_change:+}, " \
                    f"Reputation {event.reputation_change:+}, " \
                    f"Health {event.health_change:+}, " \
                    f"Power {event.power_change:+}\n\n{event.description}"

            self.update_game_text(message)  #Append message to text box
            self.advance_day()  #Advance to the next day
            self.options_menu() 

    def check_win_condition(self):
        if self.player.day >= 50:
            if self.player.power >= 100 and self.player.reputation >= 80:
                self.update_game_text("🏛️ Well done Comrade! You have built an empire not even Putin could destroy. Fealty to you Mr(s). President!")
            elif self.player.money >= 20_000_000:
                self.update_game_text("🏆 Economic Victory! You amassed over 20M RUB before 2030. Long live the Oligarchy!")
            elif self.player.health >= 50:
                self.update_game_text("\u2764\uFE0F You didn't make much of a name for yourself, nor did you make much money but you did survive. Congratulations!")
            else:
                self.update_game_text("💀 You failed to rise above the turmoil. A new Russia emerges without you.")
            self.disable_game_inputs()

    def disable_game_inputs(self):
        for widget in self.options_panel.winfo_children():
            widget.configure(state='disabled')

    def format_money(self, amount):
        return f"{amount / 1_000_000:.1f}M RUB" if abs(amount) >= 1_000_000 else f"{amount / 1_000:.1f}K RUB"

if __name__ == "__main__":
    root = tk.Tk()
    game = GameGUI(root)
    root.mainloop()
