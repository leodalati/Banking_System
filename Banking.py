import tkinter as tk
from tkinter import messagebox, ttk
import os
from datetime import datetime


class BankAccount:
    def __init__(self, name, account_number, password, balance):
        self.name = name
        self.account_number = account_number
        self.balance = balance
        self.password = password

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.log_transaction("Deposit", amount)
        else:
            raise ValueError("Deposit amount must be positive")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.log_transaction("Withdraw", amount)
        else:
            raise ValueError("Invalid withdrawal amount")

    def log_transaction(self, transaction_type, amount):
        file_exists = os.path.isfile("transactions.csv")
        with open("transactions.csv", "a") as f:
            if not file_exists:
                f.write("date,account_number,transaction_type,amount,balance_after\n")
            f.write(
                f"{datetime.now()},{self.account_number},{transaction_type},"
                f"{amount},{self.balance}\n"
            )

    def save(self):
        content = f"{self.name},{self.account_number},{self.password},{self.balance},{type(self).__name__}"
        with open("accountinfo.txt", "w") as f:
            f.write(content)


class Savings(BankAccount): pass
class Checking(BankAccount): pass
class TFSA(BankAccount): pass


class BankApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Banking Simulator")
        self.geometry("900x600")
        self.configure(bg="#f4f6f8")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TButton", padding=8, font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"))
        self.style.configure("Info.TLabel", font=("Segoe UI", 11))

        self.account = self.load_account_from_file()
        self.create_gui()

    def load_account_from_file(self):
        with open("accountinfo.txt", "r") as f:
            name, acc, pw, bal, acc_type = f.read().split(",")
            acc, bal = int(acc), float(bal)
            return {"Savings": Savings,
                    "Checking": Checking,
                    "TFSA": TFSA}[acc_type](name, acc, pw, bal)

    def create_gui(self):
        # ===== Header =====
        header = ttk.Label(self, text="🏦 Banking Simulator", style="Header.TLabel")
        header.pack(pady=20)

        container = ttk.Frame(self, padding=20)
        container.pack(fill="both", expand=True)

        # ===== Account Info Card =====
        info = ttk.Frame(container, padding=20, relief="ridge")
        info.pack(fill="x", pady=10)

        ttk.Label(info, text=f"Account Owner: {self.account.name}", style="Info.TLabel").pack(anchor="w")
        ttk.Label(info, text=f"Account Number: {self.account.account_number}", style="Info.TLabel").pack(anchor="w")
        ttk.Label(info, text=f"Account Type: {type(self.account).__name__}", style="Info.TLabel").pack(anchor="w")

        self.balance_label = ttk.Label(
            info,
            text=f"Balance: ${self.account.balance:,.2f}",
            font=("Segoe UI", 14, "bold")
        )
        self.balance_label.pack(anchor="w", pady=10)

        # ===== Transaction Card =====
        actions = ttk.Frame(container, padding=20, relief="ridge")
        actions.pack(fill="x", pady=10)

        ttk.Label(actions, text="Transaction Amount").grid(row=0, column=0, sticky="w", pady=5)
        self.amount_entry = ttk.Entry(actions)
        self.amount_entry.grid(row=0, column=1, padx=10)

        ttk.Label(actions, text="Password").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(actions, show="*")
        self.password_entry.grid(row=1, column=1, padx=10)

        # ===== Buttons =====
        btn_frame = ttk.Frame(actions)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=15)

        ttk.Button(btn_frame, text="Deposit", command=self.deposit).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Withdraw", command=self.withdraw).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Save", command=self.save).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Exit", command=self.destroy).grid(row=0, column=3, padx=5)

    def deposit(self):
        self._handle_transaction(self.account.deposit, "deposited")

    def withdraw(self):
        self._handle_transaction(self.account.withdraw, "withdrawn")

    def _handle_transaction(self, action, verb):
        if self.password_entry.get() != self.account.password:
            messagebox.showerror("Error", "Invalid password")
            return
        try:
            amount = float(self.amount_entry.get())
            action(amount)
            self.update_balance()
            messagebox.showinfo("Success", f"${amount:.2f} {verb} successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_balance(self):
        self.balance_label.config(text=f"Balance: ${self.account.balance:,.2f}")

    def save(self):
        self.account.save()
        messagebox.showinfo("Saved", "Account information saved successfully.")


if __name__ == "__main__":
    app = BankApp()
    app.mainloop()
