import sys, csv, os, re, datetime

ledger = []

now = datetime.datetime.now()
formatted_date = now.strftime("%Y-%m-%d")


class Transaction:
    def __init__(self, date, description, amount: float):
        self.date = date
        self.description = description
        self.amount = amount

    def __str__(self):
        return (
            f"Date: {self.date}, Description: {self.description}, Amount: {self.amount}"
        )

    def to_dict(self):
        return {
            "date": self.date,
            "description": self.description.title(),
            "amount": self.amount if self.amount != 0 else "",
        }


def initialize_ledger(filename=None):
    """Initialize the ledger from a file or create a new one"""
    global ledger
    ledger = []

    if filename:
        if os.path.exists(filename):
            with open(filename, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        row["amount"] = float(row["amount"])
                    except ValueError:
                        row["amount"] = 0.0
                    trans = Transaction(row["date"], row["description"], row["amount"])
                    ledger.append(trans)
        else:
            fieldnames = ["date", "description", "amount"]
            with open(filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames)
                writer.writeheader()

    log_transaction = Transaction(formatted_date, "---Ledger Opened---", 0)
    ledger.append(log_transaction)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit("Indicate ledger filename!")

    filename = sys.argv[1]

    root, ext = os.path.splitext(filename)
    if not ext == ".csv":
        sys.exit("Ledger must be a csv file!")

    initialize_ledger(filename)


def main():
    while True:
        action = (
            input(
                "\n\t\t\t||Select an action||\n1. [L]ist all transactions\n2. [V]iew balance\n3. [A]dd transaction\n4. [R]eport by category\n5. [E]dit transaction\n6. [D]elete transaction\n7. [Q]uit "
            )
            .lower()
            .strip()
        )
        if action == "1" or action == "l" or action == "list":
            transact = list_transactions()
            if len(transact) == 0:
                print("\n\t\t\t\tNO TRANSACTIONS")
            else:
                print("\t\t\t----------TRANSACTIONS----------\n")
                print("-" * 80)
                print(
                    f"{'ID':^3}|| {'Date':^10} || {'Description':^40} || {'Amount (₦)':^14} ||"
                )
                print("-" * 80)
                i = 1
                for item in transact:
                    print(
                        f"{i}. || {item.date:<10} || {item.description:<40} || {item.amount:>14,.2f} ||"
                    )
                    i += 1
                print("-" * 80)

        elif action == "2" or action == "v" or action == "view":
            inc_bal, exp_bal, tot_bal = view_balance()
            print(
                f"Total Income: ₦ {inc_bal:,.2f}\nTotal Expenditure: ₦ {exp_bal:,.2f}\nYour net balance is ₦ {tot_bal:,.2f}"
            )

        elif action == "3" or action == "a" or action == "add":
            while True:
                typ = input("Income or Expenditure (I or E)").lower()
                if typ == "i":
                    income = add_income()
                    print(
                        f"Income of ₦ {income.amount:,.2f} has been succesfully added."
                    )
                    break

                elif typ == "e":
                    exp = add_expenditure()
                    print(
                        f"Expenditure of ₦ {exp.amount:,.2f} has been succesfully added."
                    )
                    break

                else:
                    print("Invalid transcation type!")
                    break

        elif action == "4" or action == "r" or action == "report":
            while True:
                typ = input("By [i]ncome or by [e]xpenditure? ").lower().strip()
                if typ == "i" or typ == "income":
                    income, total_income = income_report()
                    if len(income) == 0:
                        print("\n\t\t\tNO INCOME")
                        break
                    else:
                        print("\n\t\t\t----------INCOME REPORT----------")
                        print("-" * 80)
                        print(
                            f"| {'i':^2} | {'Date':^10} | {'Description':^40} | {'Amount (₦)':^14} |"
                        )
                        print("-" * 80)
                        for i, trans in enumerate(income):
                            print(
                                f"| {i+1:<2} | {trans.date:<10} | {trans.description:<40} | {trans.amount:>14,.2f} |"
                            )
                        print("-" * 80)
                        print(f"\nTotal Income = ₦ {total_income:,.2f}")
                        break

                elif typ == "expenditure" or typ == "e":
                    expenses, total_expenses = expenses_report()
                    if len(expenses) == 0:
                        print("\n\t\t\tNO EXPENDITURE")
                        break
                    else:
                        print("\n\t\t\t----------EXPENDITURE REPORT----------")
                        print("-" * 80)
                        print(
                            f"| {'i':^2} | {'Date':^10} | {'Description':^40} | {'Amount (₦)':^14} |"
                        )
                        print("-" * 80)
                        for i, trans in enumerate(expenses):
                            print(
                                f"| {i+1:<2} | {trans.date:<10} | {trans.description:<40} | {trans.amount:>14,.2f} |"
                            )
                        print("-" * 80)
                        print(f"\nTotal Expenditure = ₦ {total_expenses:,.2f}")
                        break

                else:
                    break

        elif action == "5" or action == "e" or action == "edit":
            transactions = list_transactions()
            if len(transactions) == 0:
                print("\n\t\t\tNO TRANSACTIONS")
            else:
                print("\t\t\t----------TRANSACTIONS----------\n")
                print("-" * 80)
                print(
                    f"{'ID':^3}|| {'Date':^10} || {'Description':^40} || {'Amount (₦)':^14} ||"
                )
                print("-" * 80)
                i = 1
                for item in transactions:
                    print(
                        f"{i}. || {item.date:<10} || {item.description:<40} || {item.amount:>14,.2f} ||"
                    )
                    i += 1
                print("-" * 80)
                while True:
                    try:
                        id = int(input("Choose transaction to edit by ID: ")) - 1
                        if id in range(0, i-1):
                            date, desc, amount = edit_transaction(id, transactions)
                            print(
                                f"Task with\nDate: {date}, Description: {desc} and Amount: ₦ {amount:,.2f}\nHas been updated!"
                            )
                            save_ledger()
                            break
                        else:
                            print("Invalid ID!")
                            continue
                    except ValueError:
                        print("Invalid ID!")
                        continue

        elif action == "6" or action == "d" or action == "delete":
            transactions = list_transactions()
            if len(transactions) == 0:
                print("\n\t\t\tNO TRANSACTIONS")
            else:
                print("\t\t\t----------TRANSACTIONS----------\n")
                print("-" * 80)
                print(
                    f"{'ID':^3}|| {'Date':^10} || {'Description':^40} || {'Amount (₦)':^14} ||"
                )
                print("-" * 80)
                i = 1
                for item in transactions:
                    print(
                        f"{i}. || {item.date:<10} || {item.description:<40} || {item.amount:>14,.2f} ||"
                    )
                    i += 1
                print("-" * 80)
                while True:
                    try:
                        id = int(input("Choose transaction to delete by ID: ")) - 1
                        if id in range(0, i-1):
                            break
                        else:
                            print("Invalid ID!")
                            continue
                    except ValueError:
                        print("Invalid ID!")
                        continue
                print(
                    f"Confirm you want to delete transaction:\nDate: {item.date} Description: {item.description} Amount: ₦ {item.amount:,.2f}"
                )
                ans = input("[Y]es or [N]o: ").lower().strip()
                if ans == "yes" or ans == "y":
                    deleted = delete_transaction(id, transactions)
                    print(f"Transaction\n{deleted}\nHas been deleted!")
                    save_ledger()
                elif ans == "no" or ans == "n":
                    break
                else:
                    break

        elif action == "7" or action == "q" or action == "quit":
            save_ledger()
            print("Ledger succesfully saved!")
            break

        else:
            print("Invalid option!")
            continue


def list_transactions():
    transactions = [trans for trans in ledger if trans.amount != 0]
    return transactions


def edit_transaction(id, transactions):
    for i, trans in enumerate(ledger):
        if trans is transactions[id]:
            print(
                f"Date: {trans.date} Description: {trans.description} Amount: {trans.amount}"
            )
            desc = ""
            if trans.description.endswith("(Income)"):
                desc = "(Income)"
            elif trans.description.endswith("(Expenditure)"):
                desc = "(Expenditure)"

            while True:
                date = input("Date (YYYY-MM-DD): ")
                check = validate_date(date)

                if check == False:
                    print("Wrong date format!")
                    continue
                else:
                    trans.date = date
                    break

            while True:
                description = input("Description (Not more than 40 characters): ").title()
                if len(description) > 40:
                    print("Too many characters!")
                    continue
                trans.description = description + desc
                break

            while True:
                try:
                    amount = float(input("Amount: "))
                    if desc == "(Expenditure)":
                        trans.amount = -amount
                    else:
                        trans.amount = amount
                    break
                except ValueError:
                    print("Invalid amount!")
                    continue
                

            return (trans.date, trans.description, trans.amount)


def delete_transaction(id, transactions):
    for i, trans in enumerate(ledger):
        if trans is transactions[id]:
            deleted = ledger.pop(i)
            return deleted


def view_balance():
    income, income_total = income_report()
    expense, expense_total = expenses_report()
    total = 0
    for trans in ledger:
        total += trans.amount
    return income_total, expense_total, total


def add_income():
    while True:
        date = input("Date (YYYY-MM-DD): ")
        check = validate_date(date)

        if check == False:
            print("Wrong date format!")
            continue
        else:
            break
    while True:
        description = input("Description (Not more than 40 characters): ").title()
        if len(description) > 40:
            print("Too many characters!")
            continue
        description = description + "(Income)"
        break

    while True:
        try:
            amount = float(input("Amount: "))
        except ValueError:
            print("Invalid amount!")
            continue
        break
    trans = Transaction(date, description, amount)
    ledger.append(trans)
    save_ledger()
    return trans


def add_expenditure():
    while True:
        date = input("Date (YYYY-MM-DD): ")
        check = validate_date(date)

        if check == False:
            print("Wrong date format!")
            continue
        else:
            break
    while True:
        description = input("Description (Not more than 40 characters): ").title()
        if len(description) > 40:
            print("Too many characters!")
            continue
        description = description + "(Expenditure)"
        break

    while True:
        try:
            amount = float(input("Amount: "))
            amount = -amount
        except ValueError:
            print("Invalid amount!")
            continue
        break
    trans = Transaction(date, description, amount)
    ledger.append(trans)
    save_ledger()
    return trans


def validate_date(date):
    if not re.search(r"^\d{4}-(\d{2})-(\d{2})$", date):
        return False
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def income_report():
    income = []
    total = 0
    for trans in ledger:
        if trans.amount > 0:
            income.append(trans)
            total += trans.amount
    return income, total


def expenses_report():
    expenses = []
    total = 0
    for trans in ledger:
        if trans.amount < 0:
            expenses.append(trans)
            total += abs(trans.amount)
    return expenses, total


def save_ledger():
    to_save = [t.to_dict() for t in ledger]
    fieldnames = ["date", "description", "amount"]
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(to_save)


if __name__ == "__main__":
    main()
