class Category:
    def __init__(self, name: str):
        self.name = name
        self.ledger = []

    def deposit(self, amount: float, description: str = ""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount: float, description: str = "") -> bool:
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def transfer(self, amount: float, category) -> bool:
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def get_balance(self) -> float:
        return sum(item["amount"] for item in self.ledger)

    def check_funds(self, amount: float) -> bool:
        return amount <= self.get_balance()

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
    spendings = [cat.total_spent() for cat in categories]
    total = sum(spendings)

    percentages = [
        (int((s / total) * 100) // 10) * 10 if total != 0 else 0
        for s in spendings
    ]

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
