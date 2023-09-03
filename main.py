from tkinter import Tk, Label, Entry, Button, Canvas, PhotoImage, END, messagebox
from random import choice, randint, shuffle
import pyperclip
import json

def generate_password():
    """Generate a random password and populate the password entry field."""
    characters = {
        'letters': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'numbers': '0123456789',
        'symbols': '!#$%&()*+'
    }

    password = (
        [choice(characters['letters']) for _ in range(randint(8, 10))] +
        [choice(characters['symbols']) for _ in range(randint(2, 4))] +
        [choice(characters['numbers']) for _ in range(randint(2, 4))]
    )

    shuffle(password)
    final_password = ''.join(password)

    password_entry.delete(0, END)
    password_entry.insert(0, final_password)
    pyperclip.copy(final_password)


def save_password():
    """Save the website, email, and password information to a JSON file."""
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if not website or not password:
        messagebox.showinfo("Oops", "Please fill in all fields.")
        return

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        data = {}

    data.update(new_data)

    with open("data.json", "w") as data_file:
        json.dump(data, data_file, indent=4)

    website_entry.delete(0, END)
    password_entry.delete(0, END)


def find_password():
    """Find and display the password for the given website."""
    website = website_entry.get()
    
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo("Error", "No Data File Found.")
        return

    if website in data:
        email = data[website]['email']
        password = data[website]['password']
        messagebox.showinfo(website, f"Email: {email}\nPassword: {password}")
    else:
        messagebox.showinfo("Error", f"No details for {website} exists.")


# Initialize Tkinter window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Create Labels
Label(text="Website:").grid(row=1, column=0)
Label(text="Email/Username:").grid(row=2, column=0)
Label(text="Password:").grid(row=3, column=0)

# Create Entry fields
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "example@gmail.com")

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)

# Create Buttons
Button(text="Search", width=13, command=find_password).grid(row=1, column=2)
Button(text="Generate Password", command=generate_password).grid(row=3, column=2)
Button(text="Add", width=36, command=save_password).grid(row=4, column=1, columnspan=2)

window.mainloop()
