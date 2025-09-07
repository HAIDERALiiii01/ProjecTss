import time

HANGMAN_PICS = ['''
   +---+
       |
       |
       |
      ===''', '''
   +---+
   O   |
  /|\  |
  / \  |
      ===''']

print("Welcome TO THE GAME OF HANGMAN")
time.sleep(2)
print("YOUR FRIEND IS HANGED!")
time.sleep(2)
print("WE WILL ASK YOU QUESTIONS")
time.sleep(2)
print("TOTAL OF SIX QUESTIONS WILL BE ASKED.")
time.sleep(2)
print("ATLEAST 3 OF THEM SHOULD BE CORRECT TO SAVE YOUR FRIEND")
time.sleep(2)
print("IF YOU GIVE MORE THAN TWO ANSWERS WRONG... THEN YOUR FRIEND WILL BE HANGED!")
time.sleep(2)
print(HANGMAN_PICS[-1])
time.sleep(2)
print("YOUR FRIEND IS HANGED SO HURRY UP")
time.sleep(2)
print("GOOD LUCK!")
time.sleep(4)

questions = [
    {
        "q": "Who is the 'King of Curses'?",
        "options": {1: "Gojo", 2: "Sung-Jin-woo", 3: "Tera bhai", 4: "Sukuna"},
        "correct": 4
    },
    {
        "q": "How many goals does 'Messi' scored in 'World Cup Final 2022?",
        "options": {1: "0", 2: "Messi khela hi nhi tha", 3: "1", 4: "2"},
        "correct": 4
    },
    {
        "q": "Who won the 'Euro cup 2024'?",
        "options": {1: "Kolkata-Qalandars", 2: "Lyari-Dolphins", 3: "Spain", 4: "Germany"},
        "correct": 3
    },
    {
        "q": "Who has lifted 'Mjölnir'(Thor ka hammer) other than Thanos and Vision?",
        "options": {1: "Spiderman", 2: "Captain America", 3: "Loki", 4: "Hawkeye"},
        "correct": 2
    },
    {
        "q": "How many people does the 'Snap' in 'Infinity-War' and 'Endgame'?",
        "options": {1: "3", 2: "Aik to tera bhai tha", 3: "1", 4: "4"},
        "correct": 1
    },
    {
        "q": "Parhai kb shuru kr rha ha tu bhai???",
        "options": {1: "Aik din pehle", 2: "Parhai kya hota", 3: "Khana k baad", 4: "kl se"},
        "correct": 2
    }
]

wrong_answers = 0
MAX_WRONG = 3

print("HERE ARE THE QUESTIONS")
time.sleep(3)

question_number = 1
for question in questions:
    print(f"\nQ{question_number}: {question['q']}")
    time.sleep(2)
    for num, option in question['options'].items():
        print(f"{num}. {option}")
        time.sleep(1)

    try:
        answer = int(input("Your answer: "))
    except ValueError:
        print("❌ Invalid input! Please enter a number between 1 and 4.")
        continue

    if answer == question['correct']:
        print("✅ Correct!")
    
    else:
        wrong_answers += 1
        print("❌ Wrong!")
        

    question_number += 1
    time.sleep(2)

if wrong_answers <= MAX_WRONG:
    print("🎉 Mubarak ho! Tera manhoos dost bach gya.")
    print(HANGMAN_PICS[0])
elif wrong_answers > MAX_WRONG:
    print("Areyy..rey..rey..Marwana diya na becharey ko.")
    print(HANGMAN_PICS[-1])  
    