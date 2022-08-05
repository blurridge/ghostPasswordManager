# Main

# Improvements to be made:
# 1. Add tabs
# 2. Add tab where user can edit, and view csv data
# 3. Find a way to encrypt passwords, open it with a password, then instantly copy to clipboard
# 4. Allow authentication via Mac Touch ID
# 5. Recovery phrase / Password for authentication

from tkinter import *
from tkinter import messagebox
from pathlib import Path
import pandas as pd
import random
import string

FONT = ("SF Pro", 14, "normal")
CHARS = [*string.ascii_letters, *string.punctuation, *string.digits]

# FILE HANDLING

def save_details():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Warning", message="Please do not leave any fields empty.")
    else:
        data = {
            "Website": [website],
            "Email": [email],
            "Password": [password],
        }
        df = pd.DataFrame(data)
        path = Path("./user_details.csv")
        is_ok = messagebox.askokcancel(title=website, message=f"Are you sure you want to save:\nEmail: {email}\n Password:{password}")
        if is_ok:
            if path.exists():
                df.to_csv("./user_details.csv", mode='a', index=False, header=False)
            else:
                df.to_csv("./user_details.csv", index=False)
        website_entry.delete(0, END)
        email_entry.delete(0, END)
        password_entry.delete(0, END)

# PASSWORD GENERATOR

def create_password():
    password_entry.delete(0, END)
    new_password = ''.join([random.choice(CHARS) for _ in range(10)])
    password_entry.insert(0, new_password)

# GUI

root = Tk()
root.title("Ghost by blurridge")
root.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200, highlightthickness=0)
ghost_img = PhotoImage(file="ghost_logo.png")
canvas.create_image(120, 100, image=ghost_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:",font=FONT)
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:", font=FONT)
email_label.grid(column=0, row=2)
password_label = Label(text="Password:",font=FONT)
password_label.grid(column=0, row=3)

website_entry = Entry(width=36, bg="white", fg="black", insertbackground="black")
website_entry.grid(column=1, row=1, columnspan=2, sticky="w")
website_entry.focus()
email_entry = Entry(width=36, bg="white", fg="black", insertbackground="black")
email_entry.grid(column=1, row=2, columnspan=2, sticky="w")
password_entry = Entry(width=21, bg="white", fg="black", insertbackground="black")
password_entry.grid(column=1, row=3, sticky="w")

generate_btn = Button(text="Generate Password", width=11, bg="white", fg="black", command=create_password)
generate_btn.grid(column=2, row=3, sticky="w")
add_btn = Button(text="Add", width=33, command=save_details)
add_btn.grid(column=1, row=4, columnspan=2, sticky="w")

root.mainloop()