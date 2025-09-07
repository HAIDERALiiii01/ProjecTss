import tkinter
import math
import pygame
import time




# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
loop = None

# ---------------------------- Break_time_sound ------------------------------- #
def sound():
    pygame.mixer.init()
    pygame.mixer.music.load('alarm.mp3')
    pygame.mixer.music.play()

# ---------------------------- PoP_Up ------------------------------- #
def bring_window_to_front():
    window.deiconify()       # Restore the window if it was minimized
    window.lift()            # Bring it to the top of the stacking order

 
# ---------------------------- TIMER RESET ------------------------------- # 
def reset_button_work():
    global reps, loop
    if loop is not None:
        window.after_cancel(loop)
        loop = None  # Reset loop ID to prevent double cancel
    reps = 0
    canvas.itemconfig(time_text, text="00:00")
    text_label.config(text="Timer", font=(FONT_NAME, 50, "bold"), bg=YELLOW, fg=GREEN)
    check_text_label.config(text="")

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 2 == 0:
        count_down(short_break_sec)
        text_label.config(text="Break", font=(FONT_NAME, 50, "bold"), bg=YELLOW, fg=GREEN)
        sound()
        time.sleep(3)
        bring_window_to_front()
    elif reps % 8 == 0:
        count_down(long_break_sec)
        text_label.config(text="Break", font=(FONT_NAME, 50, "bold"), bg=YELLOW, fg=GREEN)
        sound()
        time.sleep(3)
        bring_window_to_front()
    else:
        count_down(work_sec)
        text_label.config(text="Timer", font=(FONT_NAME, 50, "bold"), bg=YELLOW, fg=GREEN)



# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = math.floor(count % 60)
    if count_sec < 10:
        count_sec = f"0{count_sec}"    

    canvas.itemconfig(time_text, text=f"{count_min}:{count_sec}")

    if count > 0:
        global loop
        loop = window.after(1000, count_down, count - 1)
    else:
        timer()
        mark = ""
        work_session = math.floor(reps/2)
        for _ in range(work_session):
            mark += "✔"
        check_text_label.config(text=mark,font=(FONT_NAME, 24, "bold"), bg=YELLOW, fg=GREEN)

# ---------------------------- UI SETUP ------------------------------- #

window = tkinter.Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)
#Canvas
canvas = tkinter.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
img = tkinter.PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image = img)
time_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

#Timer_text
text_label = tkinter.Label(text="Timer", font=(FONT_NAME, 50, "bold"), bg=YELLOW, fg=GREEN)
text_label.grid(column=1, row=0)

#Check_text
check_text_label = tkinter.Label(font=(FONT_NAME, 24, "bold"), bg=YELLOW, fg=GREEN)
check_text_label.grid(column=1, row=3)

#Start_button
start = tkinter.Button(text="Start",command= timer, highlightthickness=0)
start.grid(column=0, row=2)
#Reset_button
reset_button = tkinter.Button(text="Reset", command=reset_button_work, highlightthickness=0)
reset_button.grid(column=2, row=2)


window.mainloop()