# by Shriya Sateesh
# Finished 4/24/2023
# Banking system with tkinter GUI for Code2College Elite 102 Course
# Utilizes users and accounts tables in MySQL
# Written originally on VSCode

import mysql.connector
import datetime
import tkinter as tk
from tkinter import messagebox

# connection with database
def connect_to_db():
    return mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password='codecottage21',
        database='banking_c2c'
    )

# function for creating accounts with value from gui
def create_account(firstname, lastname, birthday, address, initial_balance, pin):
    connection = connect_to_db()
    cursor = connection.cursor()

    sql = "INSERT INTO users (firstname, lastname, birthday, address) VALUES (%s, %s, %s, %s)"
    values = (firstname, lastname, birthday, address)
    cursor.execute(sql, values)

    user_id = cursor.lastrowid

    sql = "INSERT INTO accounts (user_id, balance, pin) VALUES (%s, %s, %s)"
    values = (user_id, initial_balance, pin)
    cursor.execute(sql, values)

    connection.commit()

    messagebox.showinfo("Congratulations!", f"An account has been created  for {firstname} {lastname} with ID {user_id}.")

    cursor.close()
    connection.close()

# pops up after pressing create button in menu, input suggested values
def create_account_gui():
    def submit_account():
        firstname = firstname_entry.get()
        lastname = lastname_entry.get()
        birthday = birthday_entry.get()
        address = address_entry.get()
        initial_balance = float(balance_entry.get())
        pin = pin_entry.get()
        create_account(firstname, lastname, birthday, address, initial_balance, pin)

    
    root = tk.Tk()
    root.title('Create Account')

    firstname_label = tk.Label(root, text='First Name:')
    firstname_label.pack()

    firstname_entry = tk.Entry(root)
    firstname_entry.pack()

    lastname_label = tk.Label(root, text='Last Name:')
    lastname_label.pack()

    lastname_entry = tk.Entry(root)
    lastname_entry.pack()

    birthday_label = tk.Label(root, text='Birthday (YYYY-MM-DD):')
    birthday_label.pack()

    birthday_entry = tk.Entry(root)
    birthday_entry.pack()

    address_label = tk.Label(root, text='Address:')
    address_label.pack()

    address_entry = tk.Entry(root)
    address_entry.pack()

    balance_label = tk.Label(root, text='Initial Balance (in $)')
    balance_label.pack()

    balance_entry = tk.Entry(root)
    balance_entry.pack()

    pin_label = tk.Label(root, text='PIN (4-digits):')
    pin_label.pack()

    pin_entry = tk.Entry(root, show='*')
    pin_entry.pack()

    submit_button = tk.Button(root, text='Submit', command=submit_account)
    submit_button.pack()

    root.mainloop()

# function for modify accounts with value from gui
def modify_account(firstname, lastname, birthday, address, balance, pin, user_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    sql = "UPDATE users SET firstname = %s, lastname = %s, birthday = %s, address = %s WHERE id = %s"
    values = (firstname, lastname, birthday, address, user_id)
    cursor.execute(sql, values)

    user_id = cursor.lastrowid

    sql = "UPDATE accounts SET balance = %s, pin = %s WHERE user_id = %s"
    values = (balance, pin, user_id)
    cursor.execute(sql, values)

    connection.commit()

    messagebox.showinfo("Congratulations!", f"Your account has been modified: {firstname} {lastname} with ID {user_id}.")

    cursor.close()
    connection.close()

# pops up after pressing modify button in open account menu, input suggested values
def modify_account_gui(balance, user_id):
    def submit_modify():
        firstname = firstname_entry.get()
        lastname = lastname_entry.get()
        birthday = birthday_entry.get()
        address = address_entry.get()
        pin = pin_entry.get()
        modify_account(firstname, lastname, birthday, address, balance, pin, user_id)

    
    root = tk.Tk()
    root.title('Modify Account: Please re-enter all information')

    firstname_label = tk.Label(root, text='First Name:')
    firstname_label.pack()

    firstname_entry = tk.Entry(root)
    firstname_entry.pack()

    lastname_label = tk.Label(root, text='Last Name:')
    lastname_label.pack()

    lastname_entry = tk.Entry(root)
    lastname_entry.pack()

    birthday_label = tk.Label(root, text='Birthday (YYYY-MM-DD):')
    birthday_label.pack()

    birthday_entry = tk.Entry(root)
    birthday_entry.pack()

    address_label = tk.Label(root, text='Address:')
    address_label.pack()

    address_entry = tk.Entry(root)
    address_entry.pack()

    pin_label = tk.Label(root, text='PIN (4-digits):')
    pin_label.pack()

    pin_entry = tk.Entry(root, show='*')
    pin_entry.pack()

    submit_button = tk.Button(root, text='Submit', command=submit_modify)
    submit_button.pack()

    root.mainloop()

# called by delete_gui, deletes account from accounts tablen and users table (apparently needs two sql statements cause of referential integrity)
def delete_account(user_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    sql = "DELETE FROM accounts WHERE user_id = %s"
    values = (user_id,)
    cursor.execute(sql, values)
    connection.commit()

    sql = "DELETE FROM users WHERE id = %s"
    values = (user_id,)
    cursor.execute(sql, values)
    connection.commit()

    messagebox.showinfo("UPDATE", f"You have deleted the account with the id {user_id}.")

    cursor.close()
    connection.close()

## gui to delete account (just click DELETE button)
def delete_gui(user_id):
    def submit_delete():
        delete_account(user_id)

    root = tk.Tk()
    root.title('Delete Account?')

    submit_button = tk.Button(root, text='DELETE', command=submit_delete)
    submit_button.pack()

    root.mainloop()

# gui for opening account (enter pin and user id and get options - withdraw, deposit, delete)
def open_account_gui():
    def submit_account():
        user_id = user_id_entry.get()
        pin = pin_entry.get()
        
        connection = connect_to_db()
        cursor = connection.cursor()
        
        sql = "SELECT users.firstname, users.lastname, users.birthday, users.address, accounts.user_id, accounts.balance, accounts.pin FROM accounts JOIN users ON accounts.user_id = users.id WHERE accounts.user_id = %s AND accounts.pin = %s"
        values = (user_id, pin)
        cursor.execute(sql, values)
        
        result = cursor.fetchone()
        if result:
            firstname, lastname, birthday, address, user_id, balance, pin = result
            show_info_label = tk.Label(root, text = f"\nName: {firstname} {lastname}\n Birthday: {birthday}\n Address: {address}\n User ID: {user_id}\n Balance: {balance}\n")
            show_info_label.pack()

            withdraw_button = tk.Button(root, text='Withdraw', command=lambda: withdraw_gui(user_id, pin))
            withdraw_button.pack()
            deposit_button = tk.Button(root, text='Deposit', command=lambda: deposit_gui(user_id, pin))
            deposit_button.pack()
            deposit_button = tk.Button(root, text='Modify', command=lambda: modify_account_gui(balance, user_id))
            deposit_button.pack()
            delete_button = tk.Button(root, text='Delete', command=lambda: delete_gui(user_id))
            delete_button.pack()

        else:
            error_label = tk.Label(root, text = "Invalid user ID or PIN.")
            error_label.pack()
        
        cursor.close()
        connection.close()
    
    root = tk.Tk()
    root.title('Open Account')

    user_id_label = tk.Label(root, text='User ID')
    user_id_label.pack()

    user_id_entry = tk.Entry(root)
    user_id_entry.pack()

    pin_label = tk.Label(root, text='PIN')
    pin_label.pack()

    pin_entry = tk.Entry(root, show='*')
    pin_entry.pack()

    submit_button = tk.Button(root, text='Submit', command=submit_account)
    submit_button.pack()

    root.mainloop()


# function for adding money to balance column in accounts
def deposit(id, pin, amount):
    connection = connect_to_db()
    cursor = connection.cursor()

    sql = "UPDATE accounts SET balance = balance + %s WHERE user_id = %s AND pin = %s"
    values = (amount, id, pin)
    cursor.execute(sql, values)
    connection.commit()

    messagebox.showinfo("Deposited", f"You have deposited ${amount:.2f} to account {id}.")

    cursor.close()
    connection.close()

# window that comes from button in open account (after) to deposit money
def deposit_gui(user_id, pin):
    def submit_deposit():
        amount = amount_entry.get()
        deposit(user_id, pin, float(amount))

    root = tk.Tk()
    root.title('Deposit')

    amount_label = tk.Label(root, text='Amount:')
    amount_label.pack()

    amount_entry = tk.Entry(root)
    amount_entry.pack()

    submit_button = tk.Button(root, text='Deposit', command=submit_deposit)
    submit_button.pack()

    root.mainloop()

# function that subtracts amount ($) from balance in accounts table
def withdraw(id, pin, amount):
    connection = connect_to_db()
    cursor = connection.cursor()

    sql = "UPDATE accounts SET balance = balance - %s WHERE user_id = %s AND pin = %s"
    values = (amount, id, pin)
    cursor.execute(sql, values)
    connection.commit()

    messagebox.showinfo("Withdrawn", f"You have removed ${amount:.2f} from account {id}.")

    cursor.close()
    connection.close()

# window pops up after clicking withdraw button, input amount to be removed
def withdraw_gui(user_id, pin):
    def submit_withdraw():
        amount = amount_entry.get()
        withdraw(user_id, pin, float(amount))

    root = tk.Tk()
    root.title('Withdraw')

    amount_label = tk.Label(root, text='Amount:')
    amount_label.pack()

    amount_entry = tk.Entry(root)
    amount_entry.pack()

    submit_button = tk.Button(root, text='Withdraw', command=submit_withdraw)
    submit_button.pack()

    root.mainloop()


# opens main menu with gui and gives create and open accounts options
def main_menu():
    def open_create_account():
        create_account_gui()

    def open_open_account():
        open_account_gui()

    root = tk.Tk()
    root.title('Banking App')

    create_account_button = tk.Button(root, text='Create Account', command=open_create_account)
    create_account_button.pack()

    open_account_button = tk.Button(root, text='Open Account', command=open_open_account)
    open_account_button.pack()

    root.mainloop()

main_menu()