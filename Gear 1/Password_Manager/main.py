# ---------------------------- IMPORTS ------------------------------- #
import tkinter
import tkinter.messagebox
import random
import pyperclip
import json

# ---------------------------- Window_Setup ------------------------------- #
window = tkinter.Tk()
window.title("Password Generator")
window.config(padx=100, pady=40)

# ---------------------------- Canvas_Setup ------------------------------- #
canvas = tkinter.Canvas(width=200, height=200)
img = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = entry_for_website.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            if website in data:
                copied_email = data[website]["email"]
                copied_password = data[website]["password"]

                entry_for_eu.delete(0, tkinter.END)
                entry_for_eu.insert(0, copied_email)

                entry_for_password.delete(0, tkinter.END)
                entry_for_password.insert(0, copied_password)
            else:
                tkinter.messagebox.showerror(
                    title="No Data Found",
                    message="No such data exists."
                )
    except FileNotFoundError:
        tkinter.messagebox.showerror(
            title="File not found",
            message="No data file exists."
        )

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = entry_for_website.get()
    email_username = entry_for_eu.get()
    password = entry_for_password.get()

    new_data = {
        website: {
            "email": email_username,
            "password": password,
        }
    }

    if website == "" or email_username == "" or password == "":
        tkinter.messagebox.showerror(
            title="Error",
            message="Please fill out all fields. Type something in each box."
        )
        return

    is_ok = tkinter.messagebox.askokcancel(
        title="Confirmation",
        message=f"These are the details you entered:\nWebsite: {website}\nEmail: {email_username}\nPassword: {password}"
    )

    if is_ok:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            entry_for_website.delete(0, tkinter.END)
            entry_for_password.delete(0, tkinter.END)
            entry_for_website.focus()
            tkinter.messagebox.showinfo("Success", "Data saved")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    numbers = list("0123456789")
    symbols = list("!#$%&()*+")

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    pyperclip.copy(password)

    entry_for_password.delete(0, tkinter.END)
    entry_for_password.insert(0, password)

# ---------------------------- UI SETUP ------------------------------- #
ENTRY_WIDTH = 36

# Website Label + Entry
website_label = tkinter.Label(text="Website:", font=("Arial", 10), fg="black")
website_label.grid(column=0, row=1)

entry_for_website = tkinter.Entry(width=ENTRY_WIDTH)
entry_for_website.grid(column=1, row=1, columnspan=2)
entry_for_website.focus()

# Email/Username Label + Entry
eu_label = tkinter.Label(text="Email/Username:", font=("Arial", 10), fg="black")
eu_label.grid(column=0, row=2)

entry_for_eu = tkinter.Entry(width=ENTRY_WIDTH)
entry_for_eu.grid(column=1, row=2, columnspan=2)
entry_for_eu.insert(0, "zoro@gmail.com")

# Password Label + Entry
password_label = tkinter.Label(text="Password:", font=("Arial", 10), fg="black")
password_label.grid(column=0, row=3)

entry_for_password = tkinter.Entry(width=ENTRY_WIDTH)
entry_for_password.grid(column=1, row=3, columnspan=2)

# Buttons
generate_password = tkinter.Button(text="Generate Password", width=18, highlightthickness=0, borderwidth=1, command=password_generator)
generate_password.grid(column=1, row=4)

add = tkinter.Button(text="Add", width=18, highlightthickness=0, borderwidth=1, command=save)
add.grid(column=1, row=5)

search = tkinter.Button(text="Search", width=18, highlightthickness=0, borderwidth=1, command=find_password)
search.grid(column=1, row=6)

window.mainloop()
