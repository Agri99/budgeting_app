from .exceptions import InsufficientFundsError, CategoryExistsError

class Category:

    def __init__(self, name: str) -> None:
        self.name = name
        self.balance = 0
        self.ledger = []


    def deposit(self, amount: float, description: str) -> None:
        """
        Add money to the category ledger

        Args:
            amount (float): The amount to deposit
            description (str): Optional description of the deposit
        """
        self.ledger.append({
                    'amount': amount,
                    'description': description
                    })
        self.balance += amount


    def withdraw(self, amount: float, description: str) -> bool:
        """
        Withdraw money from category ledger

        Args:
            amount (float): The amount to withdraw
            description (str): Optional description of withdrawing
        """
        if self.check_funds(amount):
            self.ledger.append({
                        'amount': -amount,
                        'description': description
                        })
            self.balance -= amount
            return True
        raise InsufficientFundsError(
            f'Cannot withdraw {amount:.2f}, balance is only {self.balance:.2f}'
        )


    def get_balance(self) -> float:
        """
        Check total balance from category ledger
        """
        return self.balance


    def transfer(self, amount: float, other_categories) -> bool:
        """
        Transfer amount of balance from one category to another

        Args:
            amount (float): The amount to transfer
            other_categories: The destination category
        """
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {other_categories.name}')
            other_categories.deposit(amount, f'Transfer from {self.name}')
            return True
        return False


    def check_funds(self, amount: float) -> bool:
        """
        Check if the balance is enough to be withdraw / transfer
        """
        return self.balance >= amount


    def to_dict(self):
        '''
            Convert Category into serializable dict.
        '''
        return {
            'name': self.name,
            'balance': self.balance,
            'ledger': self.ledger
                }


    @classmethod
    def from_dict(cls, data):
        '''
            Rebuild Category from saved dict.
        '''
        cat = cls(data['name'])
        cat.balance = data['balance']
        cat.ledger = data['ledger']
        return cat


    def __str__(self):
        title = f'\n\n{self.name:*^30}\n'
        items = ''
        for i, string in enumerate(self.ledger):
            description = f'{string["description"]}'[:23].ljust(23)
            amount = f'{string["amount"]:.2f}\n'.rjust(8)
            items += ''.join(description + amount)
        total = 'Total Balance: '.ljust(23) + f'{self.balance}'.rjust(7)
        return title + items + total


