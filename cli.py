import sys
import json
import os
from budget.budgeting_app import Category
from budget.exceptions import InsufficientFundsError


Data_File = 'data.json'


def normalize_name(name:str) -> str:
    """
    Sanitize and Normalize name into lowercase
    """
    return name.strip().lower()


def find_category(categories, name) -> dict:
    """
    Find if categories name exists
    """
    if not name:
        return None

    # Normalize everything to lowercase
    return categories.get(normalize_name(name))


def print_menu() -> None:
    """
    CLI Menu
    """
    print('\n==Budget App==')
    print('1) Create Ledger')
    print('2) Deposit')
    print('3) Withdrawal')
    print('4) Transfer')
    print('5) Ledger / Balance')
    print('0) Exit\n')


def safe_float(prompt) -> float:
    """
    Check if the input is number and convert it into float
    """
    try:
        return float(input(prompt))
    except ValueError:
        print('Invalid number.')
        return None


def load_categories() -> dict:
    """
    Load categories ledger if exists
    """
    if not os.path.exists(Data_File):
        return {}

    try:
        with open(Data_File, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        return {}

    categories = {}
    for name, cat_data in data.items():
        categories[name] = Category.from_dict(cat_data)
    return categories


def save_categories(categories) -> None:
    """
    Save new ledger into JSON file and backup the old one
    """
    data = {name: cat.to_dict() for name, cat in categories.items()}
    if os.path.exists(Data_File):
        os.replace(Data_File, Data_File + '.bak') # Create backup

    with open(Data_File, 'w') as f:
        json.dump(data, f, indent=2)


def main():
    categories = load_categories() # load from file if exists

    while True:
        print_menu()
        choice = input('Select an option:')

        if choice == '1':
            name = input('\nEnter category name: ').strip()
            if not name:
                print('Name cannot be empty.')
                continue

            key = normalize_name(name)

            if key in categories:
                print(f'Category "{name}" already exist.')
            else:
                categories[name.lower()] = Category(name)
                print(f'Created category "{name}".')

        elif choice == '2':
            name = input('Category name: ').strip()
            cat = find_category(categories, name)
            if not cat:
                print('Category not found. Available: ', [c.name for c in categories.values()])
                continue
            amount = safe_float('Enter deposit amount: ')
            if amount is None:
                continue
            desc = input('Enter description (optional): ')
            cat.deposit(amount, desc)
            print(f'\n~~Deposited {amount:.2f} to {name}.~~')

        elif choice == '3':
            name = input('\nCategory name: ')
            cat = find_category(categories, name)

            if not cat:
                print('Category not found. Available: ', [c.name for c in categories.values()])
                continue
            amount = safe_float('Enter withdraw amount: ')
            if amount is None:
                continue
            desc = input('Enter description (optional): ')
            try:
                cat.withdraw(amount, desc)
                print(f'\n~~Withdraw {amount:.2f} from {name}~~')
            except InsufficientFundsError as e:
                print(f'[ERROR] {e}')

        elif choice == '4':
            src = input('\nSource category: ').strip()
            dst = input('Destination category: ').strip()
            if not src:
                print(f'Source category "{src}" not found. Available: {list(category.keys())}')
                continue
            if not dst:
                print(f'Destination category "{dst}" not found. Available: {list(category.keys())}')
                continue
            if src not in categories or dst not in categories:
                print('Source or Destination not available.')
                continue
            amount = safe_float('Enter transfer amount: ')
            if amount is None:
                continue
            try:
                categories[src].transfer(amount, categories[dst])
                print(f'\n~~Transferred {amount:.2f} from {src} to {dst}.~~')
            except InsufficientFundsError as e:
                print(f'[ERROR] {e}')

        elif choice == '5':
            name = input('\nCategory name (or "all"): ').strip()
            if name.lower() == 'all':
                if not categories:
                    print('No categories created yet.')
                for cat in categories.values():
                    print(cat)
                    print('-' * 40)
            else:
                cat = categories.get(name)
                if not cat:
                    print('Category not found. Available: ', [c.name for c in categories.values()])
                else:
                    print(cat)

        elif choice == '0':
            save_categories(categories)
            print('\n\n~~Goodbye!~~')
            exit()
        
        else:
            print('[!] Invalid Option.')

        input('Press ENTER to continue...')


if __name__ == '__main__':
    main()
