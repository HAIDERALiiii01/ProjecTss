import time
from pathlib import Path
import random
import pyttsx3
import os
import shutil  

engine = pyttsx3.init()
engine.setProperty("rate", 150)  
engine.setProperty("volume", 1)  

def speak(text):
    print(text)  
    engine.say(text)
    engine.runAndWait()

speak("Welcome to the game of 'ROCK', 'PAPER' & SCISSOR.")
time.sleep(0.5)
speak("If you have not yet heard about this game then.... ")
time.sleep(0.5)
speak("Just close the video and go to sleep.")
time.sleep(0.5)
speak("Okay then....")
time.sleep(0.5)
speak("We will ask you to choose from ROCK, PAPER, or SCISSOR.")
time.sleep(0.5)
speak("Let's start this stupid game.")

dic = {1: "ROCK", 2: "PAPER", 3: "SCISSOR"}

user_score = 0
computer_score = 0

while True:
    speak("\nChoose 1 for 'ROCK'\nChoose 2 for 'PAPER'\nChoose 3 for 'SCISSOR'")
    speak("Type 'exit' if you want to quit the game.")

    user_input = input("YOUR CHOICE: ")

    if user_input.lower() == "exit":
        speak(f"Final Score - You: {user_score}, Computer: {computer_score}")
        speak(f"YOU WILL GET {user_score}$")

        
        desktop = Path.home() / "Desktop"
        folder_name = desktop / "HERE_COMES_THE_MONEY"
        os.makedirs(folder_name, exist_ok=True)  

        
        source_audio = "KYU.mp3"
        destination_audio = os.path.join(folder_name, "money.mp3")

        # Copy the MP3 file
        if os.path.exists(source_audio):
            shutil.copy(source_audio, destination_audio)
            speak("The amount is transferred.")
            speak("A folder has been created on your desktop." )
            speak("Go to your desktop and open the folder named HERE COMES THE MONEY.")
            speak("There is an audio file.")
            speak("It will tell you how you can withdraw you winning amount.")
        else:
            speak("Oops! The audio file was not found. Please check the path.")

        speak("CONGRATULATIONS BUDDY.")
        speak("Thanks for playing this game! Goodbye!")
        break  

    if not user_input.isdigit():
        speak("Invalid input! Please enter a number (1, 2, or 3).")
        continue  

    what_user_choose = int(user_input)

    if what_user_choose not in dic:
        speak("Invalid choice! Please enter 1, 2, or 3.")
        continue  

    random_key = random.randint(1, 3)
    what_computer_choose = dic[random_key]
    user_choice_name = dic[what_user_choose]

    speak(f"\nUser chose: {user_choice_name} ({what_user_choose})")
    speak(f"Computer chose: {what_computer_choose} ({random_key})")

    if what_user_choose == random_key:
        speak("DRAW")
    elif (what_user_choose == 1 and random_key == 3) or \
         (what_user_choose == 2 and random_key == 1) or \
         (what_user_choose == 3 and random_key == 2):
        speak("YOU WIN")
        user_score += 1000
    else:
        speak("YOU LOSE")
        computer_score += 1000  

    speak(f"Current Score - You: {user_score}, Computer: {computer_score}")
    
    time.sleep(2)

