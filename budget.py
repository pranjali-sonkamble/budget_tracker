import math


class Category:
    def __init__(self, name: str):
        self.name = name
        self.ledger = []

    def deposit(self, amount: float, description: str = ""):
        if not math.isfinite(amount) or amount <= 0:
            raise ValueError("Deposit amount must be a finite number greater than zero.")
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount: float, description: str = "") -> bool:
        if not math.isfinite(amount) or amount <= 0 or not self.check_funds(amount):
            return False
        self.ledger.append({"amount": -amount, "description": description})
        return True

    def transfer(self, amount: float, category) -> bool:
        if not math.isfinite(amount) or amount <= 0 or category is self or not self.check_funds(amount):
            return False
        self.withdraw(amount, f"Transfer to {category.name}")
        category.deposit(amount, f"Transfer from {self.name}")
        return True

    def get_balance(self) -> float:
        return sum(item["amount"] for item in self.ledger)

    def check_funds(self, amount: float) -> bool:
        return math.isfinite(amount) and amount >= 0 and amount <= self.get_balance()

    def total_spent(self) -> float:
        return sum(-item["amount"] for item in self.ledger if item["amount"] < 0)

    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = ""
        for entry in self.ledger:
            desc = entry["description"][:23].ljust(23)
            amt = f"{entry['amount']:.2f}".rjust(7)
            items += f"{desc}{amt}\n"
        return title + items + f"Total: {self.get_balance():.2f}"


def create_spend_chart(categories):
    categories = list(categories)
    if not categories:
        return "No categories available to chart."

    spendings = [cat.total_spent() for cat in categories]
    total = sum(spendings)
    if total <= 0:
        return "No spending recorded yet."

    percentages = [(int((spent / total) * 100) // 10) * 10 for spent in spendings]

    chart = "Percentage spent by category\n"

    for i in range(100, -1, -10):
        chart += f"{str(i).rjust(3)}|"
        for pct in percentages:
            chart += " o " if pct >= i else "   "
        chart += " \n"

    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    max_len = max(len(cat.name) for cat in categories)
    for i in range(max_len):
        chart += "     "
        for cat in categories:
            chart += (cat.name[i] if i < len(cat.name) else " ") + "  "
        if i != max_len - 1:
            chart += "\n"

    return chart
