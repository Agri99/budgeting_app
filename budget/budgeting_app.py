class Category:
    def __init__(self, name: str) -> None:
        self.name = name
        self.balance = 0
        self.ledger = []


    def deposit(self, amount: float, description: str) -> None:
        self.ledger.append({
                    'amount': amount,
                    'description': description
                    })
        self.balance += amount


    def withdraw(self, amount: float, description: str) -> bool:
        if self.check_funds(amount):
            self.ledger.append({
                        'amount': -amount,
                        'description': description
                        })
            self.balance -= amount
            return True
        return False


    def get_balance(self) -> float:
        return self.balance


    def transfer(self, amount: float, other_categories) -> bool:
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {other_categories.name}')
            other_categories.deposit(amount, f'Transfer from {self.name}')
            return True
        return False


    def check_funds(self, amount: float) -> bool:
        return self.balance >= amount


    def __str__(self):
        title = f'\n\n{self.name:*^30}\n'
        items = ''
        for i, string in enumerate(self.ledger):
            description = f'{string["description"]}'[:23].ljust(23)
            amount = f'{string["amount"]:.2f}\n'.rjust(8)
            items += ''.join(description + amount)
        total = 'Total Balance: '.ljust(23) + f'{self.balance}'.rjust(7)
        return title + items + total


