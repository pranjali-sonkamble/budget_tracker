import tkinter as tk
from tkinter import messagebox, ttk
from budget import Category, create_spend_chart
from storage import save_data, load_data


class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        self.root.geometry("520x420")

        self.categories = load_data()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Budget Tracker", font=("Arial", 16, "bold")).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        tk.Label(frame, text="Category").grid(row=0, column=0, padx=5)
        self.category_entry = tk.Entry(frame)
        self.category_entry.grid(row=0, column=1)

        tk.Button(frame, text="Add Category", command=self.add_category).grid(row=0, column=2, padx=5)

        tk.Label(frame, text="Amount").grid(row=1, column=0, padx=5)
        self.amount_entry = tk.Entry(frame)
        self.amount_entry.grid(row=1, column=1)

        tk.Label(frame, text="Description").grid(row=2, column=0, padx=5)
        self.desc_entry = tk.Entry(frame)
        self.desc_entry.grid(row=2, column=1)

        tk.Button(frame, text="Deposit", width=12, command=self.deposit).grid(row=3, column=0, pady=5)
        tk.Button(frame, text="Withdraw", width=12, command=self.withdraw).grid(row=3, column=1, pady=5)

        transfer_frame = tk.Frame(self.root)
        transfer_frame.pack(pady=5)

        tk.Label(transfer_frame, text="From").grid(row=0, column=0)
        tk.Label(transfer_frame, text="To").grid(row=0, column=2)

        self.from_combo = ttk.Combobox(transfer_frame, values=self.get_category_names())
        self.from_combo.grid(row=0, column=1, padx=5)

        self.to_combo = ttk.Combobox(transfer_frame, values=self.get_category_names())
        self.to_combo.grid(row=0, column=3, padx=5)

        tk.Button(transfer_frame, text="Transfer", command=self.transfer).grid(row=0, column=4, padx=5)

        tk.Button(self.root, text="View Balances", command=self.view_balances).pack(pady=5)
        tk.Button(self.root, text="View Spending Chart", command=self.view_chart).pack(pady=5)
        tk.Button(self.root, text="Save & Exit", command=self.save_and_exit).pack(pady=10)

    def get_category_names(self):
        return list(self.categories.keys())

    def refresh_dropdowns(self):
        values = self.get_category_names()
        self.from_combo["values"] = values
        self.to_combo["values"] = values

    def add_category(self):
        name = self.category_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Category name required")
            return
        if name in self.categories:
            messagebox.showerror("Error", "Category already exists")
            return
        self.categories[name] = Category(name)
        self.refresh_dropdowns()
        messagebox.showinfo("Success", "Category added")

    def deposit(self):
        self.transaction(is_withdraw=False)

    def withdraw(self):
        self.transaction(is_withdraw=True)

    def transaction(self, is_withdraw):
        name = self.category_entry.get().strip()
        if name not in self.categories:
            messagebox.showerror("Error", "Invalid category")
            return
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
            return

        desc = self.desc_entry.get()
        cat = self.categories[name]

        if is_withdraw:
            if not cat.withdraw(amount, desc):
                messagebox.showerror("Error", "Insufficient funds")
                return
        else:
            cat.deposit(amount, desc)

        messagebox.showinfo("Success", "Transaction successful")

    def transfer(self):
        from_cat = self.from_combo.get()
        to_cat = self.to_combo.get()

        if from_cat not in self.categories or to_cat not in self.categories:
            messagebox.showerror("Error", "Invalid categories")
            return

        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
            return

        if not self.categories[from_cat].transfer(amount, self.categories[to_cat]):
            messagebox.showerror("Error", "Insufficient funds")
            return

        messagebox.showinfo("Success", "Transfer completed")

    def view_balances(self):
        text = ""
        for cat in self.categories.values():
            text += str(cat) + "\n\n"
        messagebox.showinfo("Balances", text if text else "No data")

    def view_chart(self):
        chart = create_spend_chart(self.categories.values())
        messagebox.showinfo("Spending Chart", chart)

    def save_and_exit(self):
        save_data(self.categories)
        self.root.destroy()
