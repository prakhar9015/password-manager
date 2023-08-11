from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def new_random_password():
    """ Putting this functionality in function makes sure, that it returns  NEW password each time it is called"""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    #  will only output passwords of length 20, each time
    nr_letters = random.randint(7, 7)
    nr_symbols = random.randint(7, 7)
    nr_numbers = random.randint(6, 6)

    # using list comprehension
    password_list = [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    password_list = [char for char in password_list]
    password = "".join(password_list)  # .join() -> concatenates the list items and removes the "" among them

    print(len(password))
    print(password)
    return password


def create_password():
    """ It will prevent adding the password in a whole length, if password_generator is clicked more than once, rather
    will clear the previous one and then display the new one"""

    password_entry.delete(0, END)
    password_entry.insert(0, new_random_password())


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    """ It will save the password, email and website name of users, when Add btn is clicked, but before saving
    will check for data, if already present and can catch exceptions  """

    website_name = website_entry.get().title()
    email_address = email_entry.get()
    password_value = password_entry.get()

    # Json data format
    new_data = {
        website_name: {
            "email": email_address,
            "password": password_value
        }
    }

    if len(website_name) == 0 or len(password_value) == 0:
        messagebox.showinfo(title="Oops!", message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website_name,
                                       message=f"These are the details entered: \n\n Email:  {email_address} \n"
                                               f"Password:  {password_value} \n\n Is it okay to save? ")

        if is_ok:  # messagebox(askokcancel) -> returns boolean
            try:  # try to open the file and read the data
                with open("data.json", mode="r") as data_file:
                    # Reading old data
                    data = json.load(data_file)

                    # if data already exists in database, then inform the user and ask consent
                    try:
                        data_already_exists = data[website_name]

                        update = messagebox.askyesnocancel(title="Uh-oh!",
                                                           message=f"Data ALREADY exists for {website_name} \n\n "
                                                                   f"Email:{data_already_exists['email']} \n Password: "
                                                                   f"{data_already_exists['password']} \n\n Do you wanna"
                                                                   f" update the entry? ")

                        if update:  # Update the EXISTING data
                            data.update(new_data)  # Updating old data with new data -> above json format

                            with open("data.json", mode="w") as updated_data_file:
                                json.dump(data, updated_data_file, indent=4)
                                refresh_and_copy_pass()
                        else:
                            pass  # else don't update the data

                    except KeyError:  # if no existing data found then, save the NEW entry
                        data.update(new_data)  # # Updating old data with new data  -> above json format
                        with open("data.json", mode="w") as database:
                            json.dump(data, database, indent=4)
                            refresh_and_copy_pass()

            except FileNotFoundError:  # if no, data file is found, then Create a new one with given data
                with open("data.json", mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4)
                    refresh_and_copy_pass()


def refresh_and_copy_pass():
    """ it will clear the website and password field after ADD btn is clicked and also copies the password
    to clipboard """
    pyperclip.copy(password_entry.get())
    website_entry.delete(0, END)
    password_entry.delete(0, END)


# ------------ SEARCH DATA -----------------


def search_data():
    """ When search btn is clicked, it will look for asked website name in database, and display it, if it is found
    or not, ALSO, if search btn is clicked and no file exists, then will catch the exception"""
    asked_website = website_entry.get().title()

    if len(asked_website) == 0:
        messagebox.showerror(title="Error", message="cannot search for empty field")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="No database found ")
        else:
            try:
                found_email = data[asked_website]["email"]
                found_password = data[asked_website]["password"]

                messagebox.showinfo(title=asked_website,
                                    message=f"Email: {found_email}\n Password: {found_password}")
                pyperclip.copy(found_password)
            except KeyError:
                messagebox.showinfo(title="Not Found", message=f" No details found for {asked_website}")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=52, pady=52)

canvas = Canvas(width=200, height=200, highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# -------------------- Widgets creation ----------------------

website_label = Label(text="Website: ", font=("Ariel", 11, "normal"), padx=2, pady=3)
website_label.grid(column=0, row=1)

website_entry = Entry(width=40)
website_entry.focus()
website_entry.grid(column=1, row=1)

search_btn = Button(text="Search", width=14, command=search_data)
search_btn.grid(column=2, row=1)

# -------------------------

email_label = Label(text="Email/Username: ", font=("Ariel", 11, "normal"), padx=2, pady=3)
email_label.grid(column=0, row=2)

email_entry = Entry(width=60)
email_entry.insert(0, string="prakhar@gmail.com")
email_entry.grid(column=1, columnspan=2, row=2)

# -------------------------

password_label = Label(text="Password: ", font=("Ariel", 11, "normal"), padx=2, pady=3)
password_label.grid(column=0, row=3)

password_entry = Entry(width=40)  # 33
password_entry.grid(column=1, row=3)

# -------------------------

generate_password = Button(text="Generate Password", command=create_password)
generate_password.grid(column=2, row=3)

add = Button(text="Add", width=50, command=save)
add.grid(column=1, columnspan=2, row=4)

window.mainloop()
