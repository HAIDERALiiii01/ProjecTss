import tkinter as tk
import pandas

BACKGROUND_COLOR = "#B1DDC6"

window = tk.Tk()
window.title("Project Flashcard")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

# Load images
img1 = tk.PhotoImage(file=r"images\card_front.png")
img2 = tk.PhotoImage(file=r"images\card_back.png")
right_img = tk.PhotoImage(file=r"images\right.png")
left_img = tk.PhotoImage(file=r"images\wrong.png")

# Canvas
canvas = tk.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_bg = canvas.create_image(400, 263, image=img1)
title_text = canvas.create_text(400, 150, text="", fill="black", font=("Arial", 40, "bold"))
word_text = canvas.create_text(400, 263, text="", fill="black", font=("Arial", 30, "italic"))
canvas.grid(row=0, column=0, columnspan=2)

# Data
data = pandas.read_csv(r"data\japanese_words.csv")
j_list = data["Japanese"].to_list()
e_list = data["English"].to_list()

index = 0
points = 0

def show_japanese(i):
    canvas.itemconfig(card_bg, image=img1)
    canvas.itemconfig(title_text, text="Japanese", fill="black")
    canvas.itemconfig(word_text, text=j_list[i], fill="black")
    set_buttons("disabled")  # Disable buttons during Japanese
    
def show_english(i):
    canvas.itemconfig(card_bg, image=img2)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=e_list[i], fill="white")
    set_buttons("normal")  # Enable buttons after showing English

def show_score():
    canvas.itemconfig(card_bg, image=img1)
    canvas.itemconfig(title_text, text="Score", fill="black")
    canvas.itemconfig(word_text, text=f"You got {points} correct!", fill="black")

def right_answer():
    global points
    points += 1
    next_card()

def wrong_answer():
    next_card()

def next_card():
    global index
    if index < len(j_list):
        current_index = index  # Lock the current index
        show_japanese(current_index)
        window.after(3000, lambda: show_english(current_index))
        index += 1  # Move to next for future use
    else:
        show_score()


# Buttons
wrong_button = tk.Button(image=left_img, borderwidth=0, highlightthickness=0, command=wrong_answer)
wrong_button.grid(row=1, column=0)

right_button = tk.Button(image=right_img, borderwidth=0, highlightthickness=0, command=right_answer)
right_button.grid(row=1, column=1)

def set_buttons(state):
    right_button.config(state=state)
    wrong_button.config(state=state)


next_card()  # Start the first card

window.mainloop()
