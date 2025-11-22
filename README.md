![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![Platform](https://img.shields.io/badge/Platform-CLI-lightgrey)

# 📊 Personal Ledger Manager (PyLedger)
#### Video Demo:  <https://youtu.be/IwYEI97kR2k>
#### **Description**: 
A command-line personal finance ledger application built with Python that helps you track income and expenditures, generate reports, and maintain your financial records in CSV format.

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Detailed Feature Guide](#detailed-feature-guide)
- [Testing](#testing)
- [Data Format](#data-format)
- [Error Handling](#error-handling)
- [Key Features Explained](#key-features-explained)
- [Known Limitations](#known-limitations)
- [Data Security](#data-security)
- [Author](#author)
- [Support](#support)
- [Acknowledgments](#acknowledgments)

## | Features

- **Transaction Management**
  - View all transactions
  - Add income transactions
  - Add expenditure transactions
  - Edit existing transactions
  - Delete transactions
  
- **Financial Reporting**
  - View overall balance (income, expenses, net balance)
  - Generate income reports
  - Generate expenditure reports
  - Detailed transaction listings
  
- **Data Persistence**
  - Save all transactions to CSV file
  - Load existing ledger from file
  - Automatic session logging
  
- **Input Validation**
  - Date validation (YYYY-MM-DD format)
  - Amount validation (numeric values only)
  - Description length limit (40 characters)
  - Transaction type validation

## | Requirements

- Python 3.6 or higher
- No external dependencies (uses Python standard library)

### Standard Library Modules Used:
- `sys` - Command-line argument handling
- `csv` - CSV file operations
- `os` - File system operations
- `re` - Regular expression for date validation
- `datetime` - Date and time handling

## | Installation

1. **Ensure Python is installed:**
```bash
   python --version
   # or
   python3 --version
```
If not installed, download from [python.org](https://www.python.org)

2. If you are installing from GitHub:
```bash
git clone https://github.com/eboselu2/pyledger.git
```

3. Get the project files:
    - Extract the ZIP file (if received as a compressed file)
    - Or simply copy `project.py` to a folder of your choice

4. **No additional packages to install** - uses only Python standard library!

## | Usage

### Starting the Application

Run the application with a CSV filename as an argument:

```bash
# example
python project.py ledger.csv
```
`ledger.csv` is the name of the csv file for storage of transactions. This file must be specified at command-line and must be a `csv` file.

If the file doesn't exist, it will be created automatically. If it exists, your previous transactions will be loaded.

### Main Menu

After starting, you'll see the main menu:

```
||Select an action||
1. [L]ist all transactions
2. [V]iew balance
3. [A]dd transaction
4. [R]eport by category
5. [E]dit transaction
6. [D]elete transaction
7. [Q]uit
```

You can select options by:
- Entering the number (1-7)
- Entering the letter (l, v, a, r, e, d, q)
- Entering the full word (list, view, add, report, edit, delete, quit)

## | File Structure

```
pyledger/
│
├── project.py           # Main application file
├── test_project.py      # Pytest test suite
├── README.md            # This file
├──requirements.txt      # Requirements file
└── ledger.csv           # Your ledger data (created on first run)
```

## | Detailed Feature Guide

### 1. List all Transactions

Allows the user to view all transactions (both income and expenditure) at once as ordered in the ledger.

```
                   ----------TRANSACTIONS----------

--------------------------------------------------------------------------------
ID ||    Date    ||               Description                ||   Amount (₦)   ||
--------------------------------------------------------------------------------
1. || 2023-09-30 || Paid Job(Income)                         ||     120,000.00 ||
2. || 2023-03-12 || Food(Expenditure)                        ||      50,000.00 ||
--------------------------------------------------------------------------------
```

### 2. View Balance

Displays your financial summary:

```
Total Income: ₦ 150,000.00
Total Expenditure: ₦ 45,000.00
Your net balance is ₦ 105,000.00
```

- Shows total income (all positive amounts)
- Shows total expenditure (absolute value of negative amounts)
- Calculates net balance (income - expenditure)

### 3. Add Transaction

#### Adding Income:

1. Select option `3` (Add transaction)
2. Choose `i` for income
3. Enter date in YYYY-MM-DD format (e.g., `2025-01-15`)
4. Enter description (max 40 characters)
5. Enter amount (positive number)

**Example:**
```
Income or Expenditure (I or E): i
Date (YYYY-MM-DD): 2025-01-15
Description (Not more than 40 characters): Salary payment
Amount: 5000
Income of ₦ 5,000.00 has been successfully added.
```

#### Adding Expenditure:

1. Select option `3` (Add transaction)
2. Choose `e` for expenditure
3. Enter date in YYYY-MM-DD format
4. Enter description (max 40 characters)
5. Enter amount (will be automatically converted to negative)

**Example:**
```
Income or Expenditure (I or E): e
Date (YYYY-MM-DD): 2025-01-16
Description (Not more than 40 characters): Groceries
Amount: 200
Expenditure of ₦ -200.00 has been successfully added.
```

### 4. Generate Reports

#### Income Report:

Select `4` (Report), then `i` (income):

```
                  ----------INCOME REPORT----------
--------------------------------------------------------------------------------
| i  |    Date    |              Description               |  Amount (₦)    |
--------------------------------------------------------------------------------
| 1  | 2025-01-15 | Salary Payment(Income)                 |      5,000.00  |
| 2  | 2025-01-20 | Freelance Work(Income)                 |      1,500.00  |
--------------------------------------------------------------------------------

Total Income = ₦ 6,500.00
```

#### Expenditure Report:

Select `4` (Report), then `e` (expenditure):

```
                  ----------EXPENDITURE REPORT----------
--------------------------------------------------------------------------------
| i  |    Date    |              Description               |  Amount (₦)    |
--------------------------------------------------------------------------------
| 1  | 2025-01-16 | Groceries(Expenditure)                 |        200.00  |
| 2  | 2025-01-18 | Transport(Expenditure)                 |         50.00  |
--------------------------------------------------------------------------------

Total Expenditure = ₦ 250.00
```

### 5. Edit Transaction

1. Select option `5` (Edit)
2. View list of all transactions with IDs
3. Enter the ID number of the transaction to edit
4. Enter new date (or same date)
5. Enter new description
6. Enter new amount

**Example:**
```
                    TRANSACTIONS

--------------------------------------------------------------------------------
ID || Date       || Description                              || Amount (₦)      ||
--------------------------------------------------------------------------------
1. || 2025-01-15 || Salary Payment(Income)                   ||    5,000.00  ||
2. || 2025-01-16 || Groceries(Expenditure)                   ||     -200.00  ||
--------------------------------------------------------------------------------
Choose transaction to edit by ID: 1
Date: 2025-01-15 Description: Salary Payment(Income) Amount: ₦ 5000.0
Date (YYYY-MM-DD): 2025-01-15
Description (Not more than 40 characters): Monthly Salary
Amount: 5500
Task with
Date: 2025-01-15, Description: Monthly Salary and Amount: ₦ 5500.0
Has been updated!
```

### 6. Delete Transaction

1. Select option `6` (Delete)
2. View list of all transactions with IDs
3. Enter the ID number of the transaction to delete
4. Confirm deletion (y/n)

**Example:**
```
Choose transaction to delete by ID: 2
Confirm you want to delete transaction:
Date: 2025-01-16 Description: Groceries(Expenditure) Amount: ₦ -200.0
[Y]es or [N]o: y
Transaction
Date: 2025-01-16, Description: Groceries(Expenditure), Amount: ₦ -200.0
Has been deleted!
```

### 7. Quit

Select option `7` to save and exit:

```
Ledger successfully saved!
```

All transactions are automatically saved to your CSV file.

## | Testing

The project includes a comprehensive pytest test suite.

### Installing pytest:

```bash
pip install pytest
```

### Running Tests:

```bash
# Run all tests
pytest test_project.py -v
```

### Test Coverage:

The test suite covers:
-  Transaction class methods
-  Date validation
-  Ledger initialization
-  Listing all transactions
-  Income/expense reports
-  Balance calculations
-  Adding income/expenditure
-  Editing transactions
-  Deleting transactions
-  Saving/loading from CSV

## | Data Format

### CSV Structure

The ledger is stored in CSV format with three columns:

```csv
date,description,amount
2025-01-15,Salary Payment(Income),5000.0
2025-01-16,Groceries(Expenditure),-200.0
2025-01-17,Freelance Work(Income),1500.0
```

### Transaction Class

Each transaction is represented as a `Transaction` object with:

```python
Transaction(
    date="2025-01-15",           # String in YYYY-MM-DD format
    description="Salary",         # String (max 40 chars recommended)
    amount=5000.0                # Float (positive for income, negative for expense)
)
```

### Special Entries

- **Log Entries**: Zero-amount entries like "---Ledger Opened---" are automatically added
- **Filtered Lists**: Zero-amount entries are excluded from edit/delete listings
- **Title Case**: Descriptions are automatically title-cased when saved

## | Error Handling

The application handles various error scenarios:

### Date Validation
```
Date (YYYY-MM-DD): 2025-13-01
Wrong date format!
Date (YYYY-MM-DD): 2025-01-15  ✓
```

### Description Length
```
Description (Not more than 40 characters): This is a very long description that exceeds the forty character limit
Too many characters!
Description (Not more than 40 characters): Short description  ✓
```

### Amount Validation
```
Amount: not a number
Invalid amount!
Amount: 5000  ✓
```

### File Validation
```bash
python project.py ledger.txt
Ledger must be a csv file!
```

### Missing Filename
```bash
python project.py
Indicate ledger filename!
```

### Invalid Transaction ID
```
Choose transaction to edit by ID: abc
Invalid ID!
Choose transaction to edit by ID: 1  ✓
```

## | Key Features Explained

### Automatic Amount Handling

- **Income**: Positive amounts are stored as-is
- **Expenditure**: Positive input is automatically converted to negative
- **Reports**: Expenditure amounts are displayed as absolute values for readability

### Session Logging

Every time you open the ledger, a log entry is automatically added:
```
Date: 2025-11-11, Description: ---Ledger Opened---, Amount: 0
```

This helps track when the ledger was accessed.

### Auto-Save

Transactions are automatically saved to CSV after:
- Adding income
- Adding expenditure
- Editing a transaction 
- Quitting the application

### Case-Insensitive Input

All menu selections are case-insensitive:
- `V`, `v`, `view` all work for viewing balance
- `I`, `i` both work for income
- `E`, `e` both work for expenditure/expense

## | Known Limitations

1. **No Multi-User Support**: Designed for single-user, local file access
2. **No Categories**: Transactions aren't categorized beyond income/expenditure
3. **No Date Range Filtering**: Reports show all transactions
4. **No Search Function**: Must manually browse transaction lists
5. **No Currency Conversion**: Uses Nigerian Naira (₦) symbol
6. **No Backup**: Manual backups of CSV file recommended

## | Data Security

- All data is stored locally in CSV format
- No internet connection required
- No data sharing or cloud storage
- You have full control over your financial data
- **Recommendation**: Store your CSV file in an encrypted folder or drive


## | Author

Created by Eboselu Ojieabu with ❤️ for personal finance management

## | Support

If you encounter any issues or have questions:
1. Check the [Error Handling](#error-handling) section
2. Review the [Usage](#usage) guide
3. Run the test suite to verify installation

## | Acknowledgments

- Built with Python standard library
- Uses pytest for testing
- Inspired by personal finance management needs

---

**Happy Tracking! 📊💰**
