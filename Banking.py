import tkinter as tk
from tkinter import messagebox

class BankAccount:
    def __init__(self, name, account_number, password, balance):
        self.name = name
        self.account_number = account_number
        self.balance = balance
        self.password = password
        
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("Deposit amount must be positive")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
        else:
            raise ValueError("Invalid withdrawal amount")
    
    def get_balance(self):
        return self.balance

    def get_name(self):
        return self.name

    def get_account(self):
        return self.account_number

    def get_password(self):
        return self.password

    def get_account_type(self):
        return type(self).__name__

    def get_file_info(self):
        with open("accountinfo.txt", "r") as file_obj:
            display = file_obj.read()
            return display

    def save(self):
        content = f"{self.name},{self.account_number},{self.password},{self.balance},{self.get_account_type()}" 
        with open("accountinfo.txt", "w") as file_obj:
            file_obj.write(content)
        
# Subclass for Savings Account
class Savings(BankAccount):
    def __init__(self, name, account_number, password, balance=0): #if balance is not provided, its 0 by default
        super().__init__(name, account_number, password, balance)

# Subclass for Checking Account
class Checking(BankAccount):
    def __init__(self, name, account_number, password, balance=0): #if balance is not provided, its 0 by default
        super().__init__(name, account_number, password, balance)

# Subclass for TFSA Account
class TFSA(BankAccount):
    def __init__(self, name, account_number, password, balance=0): #if balance is not provided, its 0 by default
        super().__init__(name, account_number, password, balance)
        

#GUI Class
class BankApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.title("Banking Simulator")

        header = tk.Label(self, text="🏦 Banking Simulator", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white", pady=10)
        header.pack(fill="x")
 
        self.account = self.load_account_from_file()

        self.create_gui()

    def load_account_from_file(self):
        try:
            with open("accountinfo.txt", "r") as file_obj:
                data = file_obj.read().strip().split(",") #splitting arguments by comma
                if len(data) != 5:
                    raise ValueError("Invalid account info format")

                name, account_number, password, balance, account_type = data
                account_number = int(account_number) #changing str to int
                balance = float(balance)

                # Create the correct account type based on the file data
                if account_type == "Savings":
                    return Savings(name, account_number, password, balance)
                elif account_type == "Checking":
                    return Checking(name, account_number, password, balance)
                elif account_type == "TFSA":
                    return TFSA(name, account_number, password, balance)
                else:
                    raise ValueError("Invalid account type")

        except FileNotFoundError:
            messagebox.showerror("Error", "Account file not found.")
            self.quit()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load account: {e}")
            self.quit()
            
    
    def create_gui(self):
        
        #Label to show Name
        self.Name_label = tk.Label(self, text=f"Account Owner: {self.account.get_name()}")
        self.Name_label.pack(pady=5)
        
        #Label to show Account Nunber
        self.AccountNum_label = tk.Label(self, text=f"Account Number: {self.account.get_account()}")
        self.AccountNum_label.pack(pady=5)

        #Label to show Account Type
        self.type_label = tk.Label(self, text=f"Account Type: {self.account.get_account_type()}")
        self.type_label.pack(pady=5)
        
        #Label to show balance
        self.balance_label = tk.Label(self, text=f"Balance: ${self.account.get_balance()}")
        self.balance_label.pack(pady=5)

        self.ammount_label = tk.Label(self, text=f"Enter amount:")
        self.ammount_label.pack(pady=5)
    
        # Entry for amount
        self.amount_entry = tk.Entry(self)
        self.amount_entry.pack(pady=5)

        #Label for password
        self.password_label = tk.Label(self, text=f"Enter Password:")
        self.password_label.pack(pady=5)
    
        # Entry for password
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)
    
        # Deposit button
        deposit_btn = tk.Button(self, text="Deposit", command=self.deposit)
        deposit_btn.pack(pady=2)
    
        # Withdraw button
        withdraw_btn = tk.Button(self, text="Withdraw", command=self.withdraw)
        withdraw_btn.pack(pady=2)

        # Save data button
        save_btn = tk.Button(self, text="Save info", command=self.save)
        save_btn.pack(pady=2)

        # End program button
        end_btn = tk.Button(self, text = "End program", command = self.destroy)
        end_btn.pack(pady=30)
    

    def deposit(self):
        entered_password = str(self.password_entry.get())
        if entered_password == self.account.get_password():
            try:
                amount = float(self.amount_entry.get())
                self.account.deposit(amount)
                self.update_balance()
                messagebox.showinfo("Successful Transaction", f"${self.amount_entry.get()} Has Been Deposited To Your Account")

            except ValueError as e:
                messagebox.showinfo("Input Error", f"Invalid Amount ({self.amount_entry.get()})")

        else:
             messagebox.showinfo("Input Error", f"Invalid Password")

    def withdraw(self):
        entered_password = str(self.password_entry.get())
        if entered_password == self.account.get_password():
            amount = float(self.amount_entry.get())
            if amount > self.account.get_balance():
                messagebox.showinfo("Input Error", "Insufficient Funds")
            else:
                try:
                    self.account.withdraw(amount)
                    self.update_balance()
                    messagebox.showinfo("Successful Transaction", f"${self.amount_entry.get()} Has Been Withdrawn From Your Account")
                except ValueError:
                    messagebox.showinfo("Input Error", f"Invalid Amount ({self.amount_entry.get()})")

        else:
            messagebox.showinfo("Input Error", f"Invalid Password")
            

    def update_balance(self):
        self.balance_label.config(text=f"Balance: ${self.account.get_balance()}")

    def save(self):
        self.account.save()
        messagebox.showinfo("Data Saved Successfully", "Saved To: accountinfo.txt")

        
app = BankApp()
app.mainloop()