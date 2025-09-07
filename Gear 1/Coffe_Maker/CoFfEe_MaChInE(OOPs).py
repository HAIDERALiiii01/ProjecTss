
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

    def change_caclulator(self, user_choice):
        cost = self.resources[user_choice]["cost"]
        print(f"It would be {cost} PKR. ")
        thousand = int(input("Insert 1000 rupees note here: "))   
        five_hundred = int(input("Insert 500 rupees note here: "))   
        hundred = int(input("Insert 100 rupees note here: "))   
        fifty = int(input("Insert 50 rupees note here: "))
        user_paid = thousand + five_hundred + hundred + fifty
        if user_paid < cost:
            print(f"Not enough money!\nMoney refunded: {user_paid} PKR")
            return False
        else:     
            change = user_paid - cost   
            print(f"Here is your change: {change}")  
            return True
            
    def Serving(self, user_demand):
            print(coffee_art)
            print(f"Here is your '{user_demand}'☕😎")
            self.fun()  

    def run(self):
        run_machine = True
        while run_machine: 
            if self.resources["report"]["ingredients"]["water"] < 50 or self.resources["report"]["ingredients"]["milk"] < 100 or self.resources["report"]["ingredients"]["coffee"] < 18:
                print("Sorry, stock is finished!")
                run_machine = False
            else:
                run_machine = True    
                user_input = str(input("What would you like? (espresso/latte/cappuccino/report): "))
                
                if user_input not in ["espresso", "latte", "cappuccino", "report"]:
                    print("Please select from (espresso/latte/cappuccino/report)")
                    continue

                elif user_input == "report":
                    print(f"Water {self.resources["report"]["ingredients"]["water"]}ml") 
                    print(f"Coffee {self.resources["report"]["ingredients"]["coffee"]}gm") 
                    print(f"Milk {self.resources["report"]["ingredients"]["milk"]}ml") 
                    print(f"Earned {self.resources["report"]["cost"]} PKR") 

                else:
                    if self.change_caclulator(user_input):
                        self.dict_update(user_input)
                        self.Serving(user_input)
                    else:
                        continue


cm = CoffeeMaker()
cm.run()

