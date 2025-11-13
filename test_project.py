import pytest, os, csv, tempfile
from unittest.mock import patch

import project
from project import Transaction, initialize_ledger, view_balance, add_income, add_expenditure, validate_date, income_report, expenses_report, save_ledger, list_transactions, edit_transaction, delete_transaction


@pytest.fixture
def temp_file():
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False)
    name = f.name
    f.close()
    project.filename = name
    yield name
    if os.path.exists(name):
        os.remove(name)
        
@pytest.fixture(autouse=True)
def reset_ledger():
    project.ledger = []
    yield
    project.ledger = []
    
def test_transactions_properties():
    t = Transaction("2025-11-11", "Salary", 3000.0)
    assert t.date == "2025-11-11"
    assert t.description == "Salary"
    assert t.amount == 3000.0
    
def test_to_dict():
    t = Transaction("2025-08-10", "pocket money", 500.0)
    assert t.to_dict()["date"] == "2025-08-10"
    assert t.to_dict()["description"] == "Pocket Money"
    assert t.to_dict()["amount"] == 500.00
    
def test_initialize_ledger(temp_file):
    initialize_ledger(temp_file)
    assert os.path.exists(temp_file)
    assert len(project.ledger) == 1
    assert "---Ledger Opened---" in project.ledger[0].description
    
def test_view_balance():
    project.ledger = [Transaction("2025-08-10", "salary", 1000.0), 
                      Transaction("2025-10-10", "rent", -500.0),
                      Transaction("2025-09-12", "pocket money", 500.0),
                      Transaction("2025-04-20", "food", -300.0),
                    ]
    income_total, expense_total, total = view_balance()
    
    assert income_total == 1500.0
    assert expense_total == 800.0
    assert total == 700.0
    
def test_validate_date():
    assert validate_date("2025-04-20") == True
    assert validate_date("2025-09-40") == False
    
def test_income_report():
    project.ledger = [Transaction("2025-08-10", "salary", 1000.0), 
                      Transaction("2025-10-10", "rent", -500.0),
                      Transaction("2025-09-12", "pocket money", 500.0),
                      Transaction("2025-04-20", "food", -300.0),
                    ]
    income, total = income_report()
    assert len(income) == 2
    assert total == 1500.0
    
def test_expenses_report():
    project.ledger = [Transaction("2025-08-10", "salary", 1000.0), 
                      Transaction("2025-10-10", "rent", -500.0),
                      Transaction("2025-09-12", "pocket money", 500.0),
                      Transaction("2025-04-20", "food", -300.0),
                    ]
    expenses, total = expenses_report()
    assert len(expenses) == 2
    assert total == 800.0
    
def test_save_ledger(temp_file):
    project.ledger = [
        Transaction("2025-08-10", "salary", 1000.0),
        Transaction("2025-10-10", "rent", -500.0)
    ]
    
    save_ledger()
    
    with open(temp_file, "r", newline="") as file:
        rows = list(csv.DictReader(file))
        
    assert len(rows) == 2
    assert rows[0]["date"] == "2025-08-10"
    assert float(rows[0]["amount"]) == 1000.0
    assert rows[1]["date"] == "2025-10-10"
    assert float(rows[1]["amount"]) == -500.0
 
@patch("builtins.input", side_effect = ["2025-11-11", "Pocket Money", "1000"])   
def test_add_income(mock_input, temp_file):
    trans = add_income()
    
    assert trans.date == "2025-11-11"
    assert trans.description == "Pocket Money(Income)"
    assert trans.amount == 1000.0
    assert len(project.ledger) == 1
    assert project.ledger[0] == trans

@patch("builtins.input", side_effect = ["2025-11-11", "Food", "500"])
def test_add_expenditure(mock_input, temp_file):
    trans = add_expenditure()
    
    assert trans.date == "2025-11-11"
    assert trans.description == "Food(Expenditure)"
    assert trans.amount == -500.0
    assert len(project.ledger) == 1
    assert project.ledger[0] == trans

def test_edit_transaction():
    project.ledger = [
        Transaction("2025-01-15", "Salary(Income)", 5000.0),
        Transaction("2025-01-16", "Groceries(Expenditure)", -200.0),
        Transaction("2025-01-17", "Freelance(Income)", 1500.0),
    ]
    
    transactions = list_transactions()

    with patch('builtins.input', side_effect=['2025-01-20', 'Updated Salary', '5500']):
        result = edit_transaction(0, transactions)
    
    assert result == ('2025-01-20', 'Updated Salary(Income)', 5500.0)
    assert project.ledger[0].date == '2025-01-20'
    assert project.ledger[0].description == 'Updated Salary(Income)'
    assert project.ledger[0].amount == 5500.0
    
def test_delete_transaction():
    project.ledger = [
        Transaction("2025-01-15", "Salary", 5000.0),
        Transaction("2025-01-16", "Groceries", -200.0),
        Transaction("2025-01-17", "Freelance", 1500.0),
    ]
    
    transactions = list_transactions()
    initial_length = len(project.ledger)
    
    deleted = delete_transaction(1, transactions)

    assert deleted.description == "Groceries"
    assert deleted.amount == -200.0
    assert len(project.ledger) == initial_length - 1
    assert deleted not in project.ledger
    
def test_list_transactions():
    project.ledger = [
        Transaction("2025-01-15", "Salary", 5000.0),
        Transaction("2025-01-16", "Opening", 0),
        Transaction("2025-01-17", "Groceries", -200.0),
    ]
    
    transactions = list_transactions()
    assert len(transactions) == 2
    assert all(t.amount != 0 for t in transactions)
    