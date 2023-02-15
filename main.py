from tkinter import *
import random
from tkinter import messagebox
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

def generate_password():
  nr_letters = random.randint(8, 10)
  nr_symbols = random.randint(2, 4)
  nr_numbers = random.randint(2, 4)
  
  password_list = [random.choice(letters) for _ in range(nr_letters)]
  password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
  password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
  
  combined_password = password_list + password_symbols + password_numbers
  random.shuffle(combined_password)
  
  password = "".join(combined_password)
  
  password_entry.insert(0, password)
  pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
  website = website_entry.get()
  username = username_entry.get()
  password = password_entry.get()
  new_dict = {
    website: {
      "email": username,
      "password": password
    }
  }
  
  if len(website) == 0 or len(password) == 0 or len(username) == 0:
    messagebox.showinfo(title="Oops", message="Please make sure you fill out every details.")
  else:
    is_okay = messagebox.askokcancel(title=website, message=f"These are the details entered: \n"
                                                  f"Email: {username}\n"
                                                  f"Password: {password}\n"
                                                  f"Is it okay to save?")
    if is_okay:
      try:
        with open("data.json", "r") as file:
          data = json.load(file)
      except FileNotFoundError:
        with open('data.json', 'w') as file:
          json.dump(new_dict, file, indent=4)
      else:
        data.update(new_dict)
        with open('data.json', 'w') as file:
          json.dump(data, file, indent=4)
      finally:
        website_entry.delete(0, END)
        password_entry.delete(0, END)
        
def search():
  website = website_entry.get()
  try:
    with open("data.json", 'r') as file:
      data = json.load(file)
  except FileNotFoundError:
    messagebox.showinfo(title="Error", message="No File Found.")
  else:
      if website in data:
        messagebox.showinfo(title=website, message=f"Email: {data[website]['email']}\n"
                                                f"Password: {data[website]['password']}")
      else:
        messagebox.showinfo(title="Error", message="No such Website found.")
   
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=20, padx=20)


photo = PhotoImage(file="logo.png")
canvas = Canvas(height=200, width=200, highlightthickness=0)
canvas.create_image(100, 100, image=photo)
canvas.grid(column=2, row=1)

website_label = Label(text="Website:")
website_label.grid(column=1, row=2)

username_label = Label(text="Email/Username:")
username_label.grid(column=1, row=3)

password_label = Label(text="Password")
password_label.grid(column=1, row=4)

website_entry = Entry(width=25)
website_entry.grid(row=2, column=2, columnspan=1)
website_entry.focus()

username_entry = Entry(width=40)
username_entry.grid(row=3, columnspan=2, column=2)
username_entry.insert(0, "hin@gmail.com")

password_entry = Entry(width=25)
password_entry.grid(row=4, column=2)

generate_button = Button(text="Generate Password", command=generate_password, width=15)
generate_button.grid(column=3, row=4)

add_button = Button(text='Add', width=35, command=save_data)
add_button.grid(column=2, row=5, columnspan=2)

search_button = Button(text="Search", width=15, command=search)
search_button.grid(column=3, row=2)

window.mainloop()
