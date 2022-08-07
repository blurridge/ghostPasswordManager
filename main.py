# Main

# Improvements to be made:
# 1. Add tabs
# 2. Add tab where user can edit, and view csv data
# 3. Find a way to encrypt passwords, open it with a password, then instantly copy to clipboard
# 4. Allow authentication via Mac Touch ID
# 5. Recovery phrase / Password for authentication

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
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
        show_details()

# PASSWORD GENERATOR

def create_password():
    password_entry.delete(0, END)
    new_password = ''.join([random.choice(CHARS) for _ in range(10)])
    password_entry.insert(0, new_password)

# SHOW DETAILS

def clear_data():
    details_view.delete(*details_view.get_children())

def show_details():
    path = Path("./user_details.csv")
    if path.exists():
        df = pd.read_csv("user_details.csv")
        clear_data()
        details_view["column"] = list(df.columns)
        details_view["show"] = "headings"

        for column in details_view["column"]:
            details_view.heading(column, text=column)
            col_width = 250 if column == "Email" else 150
            details_view.column(column=column, minwidth=0, width=col_width, stretch=False)

        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            details_view.insert("", "end", values=row)

# GUI SETUP

root = Tk()
root.title("Ghost by blurridge")
root.geometry("700x400")
root.resizable(False, False)

tab_control = ttk.Notebook(root)
home = ttk.Frame(tab_control)
view = ttk.Frame(tab_control)
tab_control.add(home, text="Home")
tab_control.add(view, text="View")
tab_control.pack(expand=1, fill="both")
home_widget_frame = Frame(home, width=700, height=400)
home_widget_frame.pack()

# HOME

canvas = Canvas(home_widget_frame, width=200, height=200, highlightthickness=0)
ghost_img = PhotoImage(file="ghost_logo.png")
canvas.create_image(120, 100, image=ghost_img)
canvas.grid(column=1, row=0)

website_label = Label(home_widget_frame, text="Website:",font=FONT)
website_label.grid(column=0, row=1)
email_label = Label(home_widget_frame, text="Email/Username:", font=FONT)
email_label.grid(column=0, row=2)
password_label = Label(home_widget_frame, text="Password:",font=FONT)
password_label.grid(column=0, row=3)

website_entry = Entry(home_widget_frame, width=36, bg="white", fg="black", insertbackground="black")
website_entry.grid(column=1, row=1, columnspan=2, sticky="w")
website_entry.focus()
email_entry = Entry(home_widget_frame, width=36, bg="white", fg="black", insertbackground="black")
email_entry.grid(column=1, row=2, columnspan=2, sticky="w")
password_entry = Entry(home_widget_frame, width=21, bg="white", fg="black", insertbackground="black")
password_entry.grid(column=1, row=3, sticky="w")

generate_btn = Button(home_widget_frame, text="Generate Password", width=11, bg="white", fg="black", command=create_password)
generate_btn.grid(column=2, row=3, sticky="w")
add_btn = Button(home_widget_frame, text="Add", width=33, command=save_details)
add_btn.grid(column=1, row=4, columnspan=2, sticky="w")

# VIEW 

details_view = ttk.Treeview(view)
scrolly = ttk.Scrollbar(view, orient="vertical", command=details_view.yview)
details_view.configure(yscrollcommand=scrolly.set)
details_view.pack()
scrolly.pack(side="right", fill="y")
show_details()

root.mainloop()