import mysql.connector
import datetime

def connect_to_db():
    return mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password='your_password',
        database='banking_c2c'
    )

def create_account_table():
    connection = connect_to_db()
    cursor = connection.cursor()

    sql = "CREATE TABLE IF NOT EXISTS accounts (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT NOT NULL, balance FLOAT(10,2) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    cursor.execute(sql)

    cursor.close()
    connection.close()

def check_balance(account_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    sql = "SELECT balance FROM accounts WHERE id = %s"
    values = (account_id,)
    cursor.execute(sql, values)

    balance = cursor.fetchone()[0]
    print(f"Current balance: ${balance:.2f}")

    cursor.close()
    connection.close()

def deposit(account_id, amount):
    connection = connect_to_db()
    cursor = connection.cursor()

    sql = "UPDATE accounts SET balance = balance + %s WHERE id = %s"
    values = (amount, account_id)
    cursor.execute(sql, values)
    connection.commit()

    print(f"Deposited ${amount:.2f} to account {account_id}.")

    cursor.close()
    connection.close()

def withdraw(account_id, amount):
    connection = connect_to_db()
    cursor = connection.cursor()

    sql = "SELECT balance FROM accounts WHERE id = %s"
    values = (account_id,)
    cursor.execute(sql, values)

    balance = cursor.fetchone()[0]

    if balance >= amount:
        sql = "UPDATE accounts SET balance = balance - %s WHERE id = %s"
        values = (amount, account_id)
        cursor.execute(sql, values)
        connection.commit()

        print(f"Withdrew ${amount:.2f} from account {account_id}.")
    else:
        print("Insufficient funds.")

    cursor.close()
    connection.close()

def create_account(firstname, lastname, birthday, address, initial_balance):
    connection = connect_to_db()
    cursor = connection.cursor()

    sql = "INSERT INTO users (firstname, lastname, birthday, address) VALUES (%s, %s, %s, %s)"
    values = (firstname, lastname, birthday, address)
    cursor.execute(sql, values)

    user_id = cursor.lastrowid

    sql = "INSERT INTO accounts (user_id, balance) VALUES (%s, %s)"
    values = (user_id, initial_balance)
    cursor.execute(sql, values)

    connection.commit()

    print(f"Created account for {firstname} {lastname} with ID {user_id}.")

    cursor.close()
    connection.close()

def delete_account(account_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    sql = "DELETE FROM accounts WHERE id = %s"
    values = (account_id,)
    cursor.execute(sql, values)
    connection.commit()

    print(f"Deleted account {account_id}.")

    cursor.close()
    connection.close()

def modify_account(account_id, field, new_value):
    connection = connect_to_db()
    cursor = connection.cursor()

    if field == "firstname":
        sql = "UPDATE users SET firstname = %s WHERE id"
        
