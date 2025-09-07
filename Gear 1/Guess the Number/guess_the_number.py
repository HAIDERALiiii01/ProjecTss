import random
import pyttsx3
import time

engine = pyttsx3.init()
voices = engine.getProperty('voices')  
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate", 150)
engine.setProperty('volume', 1.0)


def speak_and_print(text):
    print(text)
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.5)

speak_and_print("WELCOME TO ANOTHER INTERESTING GAME!")
speak_and_print("SO FIRST, LET'S UNDERSTAND HOW THIS GAME WORKS")
speak_and_print("YOU HAVE TO CHOOSE ONE NUMBER FROM 1 TO 100")
speak_and_print("THE SYSTEM WILL ALSO CHOOSE A NUMBER FROM 1 TO 100")
speak_and_print("THE GOAL IS TO MATCH YOUR CHOICE WITH THE SYSTEM'S CHOICE!")
speak_and_print("WE WILL TELL YOU IF YOU ARE NEAR OR FAR FROM THE SYSTEM'S CHOICE")
speak_and_print("SO LET'S GET STARTED!")

n = random.randint(1, 100)

guesses = 0
a = -1

while a != n:
    guesses += 1
    try:
        a = int(input("Enter a number between 1 to 100: "))
    except ValueError:
        speak_and_print("Invalid input! Please enter a valid number.")
        continue  

    if a > n:
        random_word1 = random.choice(["LOWER THE NUMBER MAN", "I SAID LOWER THE NUMBER", "MORE LOWER", "LOWER"])
        speak_and_print(random_word1)
    elif a < n:
        random_word2 = random.choice(["HIGHER THE NUMBER MAN", "I SAID HIGHER THE NUMBER", "MORE HIGHER", "HIGHER"])
        speak_and_print(random_word2)


speak_and_print(f"You have guessed the number {n} in {guesses} attempts.")
