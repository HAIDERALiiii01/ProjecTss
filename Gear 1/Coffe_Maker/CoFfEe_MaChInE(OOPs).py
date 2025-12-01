import pygame
from art import coffee_art, coffee_maker_letter_art

print(coffee_maker_letter_art)

class CoffeeMaker():
    def __init__(self):
        self.resources = {
        "report":{
            "ingredients": {
                "water": 1000,
                "coffee": 500,
                "milk": 800,
            },
            "cost": 0,
        },
        "espresso":{
            "ingredients": {
                "water": 50,
                "coffee": 18,
            },
            "cost": 400,
        },
        "latte":{
            "ingredients": {
                "water": 200,
                "milk": 150,
                "coffee": 24,
            },
            "cost": 800,
        },
        "cappuccino":{
            "ingredients": {
                "water": 250,
                "milk": 100,
                "coffee": 24,
            },
            "cost": 1000,
        }

    }

    def fun(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("chai.mpeg")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            continue  

    def dict_update(self, user_report):
        water = self.resources["report"]["ingredients"]["water"] - self.resources[user_report]["ingredients"]["water"]
        coffee = self.resources["report"]["ingredients"]["coffee"] - self.resources[user_report]["ingredients"]["coffee"]
        milk = self.resources["report"]["ingredients"]["milk"] - self.resources[user_report]["ingredients"].get("milk", 0)
        total_cost = self.resources["report"]["cost"] + self.resources[user_report]["cost"]

        self.resources["report"]["ingredients"]["water"] = water
        self.resources["report"]["ingredients"]["milk"] = milk
        self.resources["report"]["ingredients"]["coffee"] = coffee
        self.resources["report"]["cost"] = total_cost

    def change_calculator(self, user_choice):
        user_paid = 0
        cost = self.resources[user_choice]["cost"]
        print(f"It would be {cost} PKR.")

        
        rupees = [1000, 500, 100, 50]

        for r in rupees:
            if user_paid >= cost:
                break
            try:
                note = int(input(f"Insert {r} rupees note here: "))
                user_paid += note
            except ValueError:
                print("Invalid input! Please insert numbers only.")

        if user_paid < cost:
            print(f"Not enough money!\nMoney refunded: {user_paid} PKR")
            return False
        else:
            change = user_paid - cost
            print(f"Here is your change: {change} PKR")
            return True

            
    def Serving(self, user_demand):
            print(coffee_art)
            print(f"Here is your '{user_demand}'☕😎")
            self.fun()  


    def run(self):
        menu = {1: "espresso", 2: "latte", 3: "cappuccino", 4: "report"}
        run_machine = True
        while run_machine: 
            if self.resources["report"]["ingredients"]["water"] < 50 or self.resources["report"]["ingredients"]["milk"] < 100 or self.resources["report"]["ingredients"]["coffee"] < 18:
                print("Sorry, stock is finished!")
                self.fun()
                run_machine = False
            else:
                run_machine = True    
                try:
                    user_input = int(input(
                        "(espresso/latte/cappuccino/report/exit): \n"
                        "Press 1️⃣   for espresso\n"
                        "Press 2️⃣   for latte\n"
                        "Press 3️⃣   for cappuccino\n"
                        "Press 4️⃣   for report\n"
                        "Press 5️⃣   to exit\n"
                        "What would you like?:"
                    ))
                except ValueError:
                    print("\nInvalid input! Please enter a number from 1 to 5.\n")
                    continue
                
                if user_input == 5:
                    print("Thanks for using our precious machine!")
                    self.fun()
                    break

                elif user_input not in menu:
                    print("Please select from 1-5")
                    continue

                choice = menu[user_input]

                if choice == "report":
                    print(f"\nWater {self.resources["report"]["ingredients"]["water"]}ml") 
                    print(f"Coffee {self.resources["report"]["ingredients"]["coffee"]}gm") 
                    print(f"Milk {self.resources["report"]["ingredients"]["milk"]}ml") 
                    print(f"Earned {self.resources["report"]["cost"]} PKR\n") 
                    continue

                else:
                    if self.change_calculator(choice):
                        self.dict_update(choice)
                        self.Serving(choice)
                    else:
                        continue


cm = CoffeeMaker()
cm.run()

