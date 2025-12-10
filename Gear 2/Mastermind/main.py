import random

class Mastermind:
    def intro(self):
        print("Welcome to Mastermind!")
        print("R=Red, Y=Yellow, G=Green.")
        print("You have 10 attempts to guess the set of 5.")
        print("Like this>> R Y G G Y")
    
    def mind(self):
        guesses = 10
        colors = ["R", "Y", "G"]
        box = random.choices(colors, k=5)

        while guesses > 0:
            user_input = input(f"You have {guesses} attempts remaining.\nYour input: ")
            user_box = user_input.split()

            if len(user_box) != 5:
                print("The input contain only 5 characters!")
                continue

            correct = 0
            for index, color in enumerate(box):
                if color == user_box[index]:
                    correct += 1
            
            if user_box == box:
                print(f"BINGO!>>>{user_box}")
                return
            
            print(f"{correct} positions are correct!")
            guesses -= 1
        
        print(f"You have run out of your attempts.\nThe correct answer was>>{box}")

m = Mastermind()
m.intro()
m.mind()

