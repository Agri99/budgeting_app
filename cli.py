from budget.budgeting_app import Category
import sys


def find_category(categories, name):
    '''
        Return Category object or None (case-sensitive).
    '''
    return categories.get(name)


def print_menu():
    print('\n==Budget App==')
    print('1) Create Ledger')
    print('2) Deposit')
    print('3) Withdrawal')
    print('4) Transfer')
    print('5) Ledger / Balance')
    print('0) Exit\n')


def safe_float(prompt):
    try:
        return float(input(prompt))
    except ValueError:
        print('Invalid number.')
        return None


def main():
    categories = {} # mapping name -> Category

    while True:
        print_menu()
        choice = input('Select an option:')

        if choice == '1':
            name = input('\nEnter category name: ').strip()
            if not name:
                print('Name cannot be empty.')
                continue
            if name in categories:
                print(f'Category "{name}" already exist.')
            else:
                categories[name] = Category(name)
                print(f'Created category "{name}".')

        elif choice == '2':
            name = input('Category name: ').strip()
            cat = find_category(categories, name)
            if not cat:
                print('Category not found.')
                continue
            amount = safe_float('Enter deposit amount: ')
            if amount is None:
                continue
            desc = input('Enter description (optional): ')
            cat.deposit(amount, desc)
            print(f'\n~~Deposited {amount:.2f} to {name}.~~')

        elif choice == '3':
            name = input('\nCategory name: ')
            cat = find_category(categpries, name)
            if not cat:
                print('Category not found.')
                continue
            amount = safe_float('Enter withdraw amount: ')
            if amount is None:
                continue
            desc = input('Enter description (optional): ')
            ok = cat.withdraw(amount, desc)
            if ok:
                print(f'\n~~Withdraw {amount:.2f} from {name}~~')
            else:
                print('Insufficient funds.')

        elif choice == '4':
            src = input('\nSource category: ').strip()
            dst = input('Destination category: ').strip()
            if src not in categories or dst not in categories:
                print('Source or Destination not available.')
                continue
            amount = safe_float('Enter transfer amount: ')
            if amount is None:
                continue
            ok = categories[src].transfer(amount, categories[dst])
            if ok:
                print(f'\n~~Transferred {amount:.2f} from {src} to {dst}.~~')
            else:
                print(f'\nTransfer failed: insufficient funds.')

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
                    print('Category not found.')
                else:
                    print(cat)

        elif choice == '0':
            print('\n\n~~Goodbye!~~')
            exit()
        
        else:
            print('[!] Invalid Option.')


if __name__ == '__main__':
    main()
