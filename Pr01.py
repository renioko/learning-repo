import sys
import click
import pickle
from typing import List
from csv import DictReader
from logging import exception

EXPENSES = 'Projects\\expenses.db'

class Expense:
    def __init__(self, id:int, amount:float, desc:str) -> None:
        self.id = id
        self.amount = amount
        self.desc = desc
        self.check_amount()


    def __str__(self) -> str:
        return f'{self.id:4} {self.amount:8}  {self.desc}'
    def __repr__(self) -> str:
        return f"Expense(id:{self.id!r}, {self.amount!r}, {self.desc!r}"
    
    def check_amount(self):
        if self.amount < 0:
            raise ValueError('Error - you enetred a negative number')


# Helper functions

def generate_id(expenses: List[Expense]) -> int:
    ids = {exp.id for exp in expenses} # warto uzyc set
    id = 1
    while id in ids:
        id += 1
    return id

def check_big(amount: float) -> bool:
    return True if amount >= 1000 else False

def calculate_total(expenses: List[Expense]) -> float:
    amounts = [e.amount for e in expenses]
    return sum(amounts)


def add_expense(expenses: List[Expense], amount: float, desc: str) -> List:
    try:
        id = generate_id(expenses)
        expense = Expense(id, amount, desc)
        expenses.append(expense)
    except ValueError as e:
        print(e)
    return expenses


# File handling

def save_expenses(content): 
    try:
        with open(EXPENSES, 'wb') as stream:
            pickle.dump(content, stream)

    except FileNotFoundError:
        with open(EXPENSES, 'xb') as stream:
            pickle.dump(content, stream)
    print('data saved')

def load_expenses() -> List[Expense]:
    try:
        with open(EXPENSES, 'rb') as stream:
            expenses = pickle.load(stream)
    except FileNotFoundError:
            expenses = []
    return expenses

# Raport

def print_raport(expenses: List[Expense]) -> None:
    print('-ID- -BIG?- -AMOUNT- --DESCRIPTION-')
    print('---- ------ -------- --------------')

    for e in expenses:
        big = check_big(e.amount)
        if big:
            big = 'v'
        else:
            big = ''

        print(f'{e.id:4}  {big:^6} {e.amount:7}  {e.desc}')
    total = calculate_total(expenses)
    print('---------------------')
    print(f'TOTAL: {total}')

# Click commands

@click.group()
def cli():
    pass

@cli.command()
@click.argument('amount', type=float, required=1)
@click.argument('desc', required=1)
def add(amount: str, desc:str) -> None:
    amount = float(amount)
    expenses = load_expenses()
    expenses = add_expense(expenses, amount, desc)
    save_expenses(expenses)
    print('expense added')

@cli.command()
@click.argument("desc", required=1)
def remove(desc:str) -> None:
    expenses = load_expenses()
    for e in expenses:
        if e.desc == desc:
            expenses.remove(e)
    save_expenses(expenses)
    print('expense removed')

@cli.command()
def raport():
    expenses = load_expenses()
    print_raport(expenses)

@cli.command()
def export_python():
    expenses = load_expenses()
    print(expenses)

@cli.command()
@click.argument('csv_file', required=1)
def import_csv(csv_file:str) -> List[Expense]:
    expenses = load_expenses()
    try:
        with open(csv_file, 'r') as stream:
            reader = DictReader(stream)
            for row in reader:
                amount = float(row['amount'])
                desc = row['description']
                expenses = add_expense(expenses, amount, desc)
    except FileNotFoundError:
        print('error, file does not exist')
        sys.exit(1)
    save_expenses(expenses)
    print('csv file loaded')
   
if __name__ == '__main__':

    cli()



