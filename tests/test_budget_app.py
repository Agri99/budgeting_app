import pytest
from budget.budgeting_app import Category
from budget.exceptions import InsufficientFundsError

def test_deposit_and_balance():
    food = Category('Food')
    food.deposit(100, 'Salary')
    assert food.get_balance() == 100


def test_withdraw():
    food = Category('Food')
    food.deposit(100, 'Deposit')
    assert food.withdraw(30, 'Groceries')
    assert food.get_balance() == 70


def test_withdraw_insufficient_funds():
    food = Category('Food')
    food.deposit(10, 'Deposit')
    with pytest.raises(InsufficientFundsError):
        food.withdraw(50, 'Big purchase')
