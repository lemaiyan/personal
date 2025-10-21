# Mother-in-Law House Expense Tracking System

A modular Python application for tracking construction expenses, calculating M-Pesa fees, managing outstanding balances, and generating comprehensive financial reports.

## Project Structure

```
mum-in-law-house/
├── config.py                      # Project constants and M-Pesa fee calculator
├── calculations.py                # Financial calculations and data processing
├── reports.py                     # Report generation and export functions
├── data/                          # Data modules
│   ├── __init__.py               # Package initialization
│   ├── expenses.py               # All expense transactions (471 entries)
│   └── pending_items.py          # Outstanding balances & pending purchases
├── process_expenses_new.py       # Main entry point (NEW - modular version)
├── process_expenses.py           # Original monolithic version (DEPRECATED)
├── create_excel.py               # Excel report generator
├── expense_data.json             # Generated dashboard data (git-ignored)
└── Mother-In-Law-House-Expenses.xlsx  # Generated Excel report
```

## Module Overview

### `config.py`

- **Purpose**: Central configuration and constants
- **Contents**:
  - `TOTAL_BUDGET`: Project budget (KES 1,000,000)
  - `PROJECT_START`: Project start date
  - `calculate_mpesa_fee()`: M-Pesa fee calculation function

### `data/` Package

Contains all project data separated by type:

#### `data/expenses.py`

- **Function**: `get_expenses_data()`
- **Returns**: List of 471 expense transactions
- **Structure**: Each expense has:
  - `date`: Transaction date (DD/MM/YYYY)
  - `category`: Main category (e.g., "Building Materials", "Labor Costs")
  - `subcategory`: Detailed category
  - `description`: Expense description
  - `amount`: Amount in KES
  - `vendor`: Vendor/supplier name

#### `data/pending_items.py`

- **Function**: `get_outstanding_balances()`
  - Returns 6 outstanding specialist balances (total: KES 91,300)
- **Function**: `get_pending_purchases()`
  - Returns 11 pending purchases (base: KES 147,500)
  - Note: 15% contingency calculated dynamically

### `calculations.py`

Core financial calculation functions:

- **`process_expenses(expenses_data)`**
  - Adds M-Pesa fees and payment status to each expense
  - Returns processed DataFrame
- **`calculate_summary_stats(df)`**
  - Calculates total spent, fees, balance, budget percentage
  - Returns dictionary with summary statistics
- **`calculate_category_summary(paid_df)`**
  - Groups expenses by category with totals
  - Sorts by budget percentage
- **`calculate_pending_amounts(df, outstanding_balances, pending_purchases)`**
  - Calculates unpaid labor, outstanding balances
  - Adds 15% contingency to pending purchases
  - Returns comprehensive pending amounts
- **`calculate_project_totals(summary_stats, pending_amounts)`**
  - Calculates total project cost and additional funds needed
  - Returns overall project financial analysis

### `reports.py`

Report generation and export functions:

- **`print_summary_report(...)`**
  - Prints formatted console report with all financial details
- **`export_dashboard_data(...)`**
  - Exports JSON data for HTML dashboard
  - Returns number of transactions processed

### `process_expenses_new.py`

**Main entry point** - orchestrates the entire process:

1. Loads data from data modules
2. Processes expenses and calculates fees
3. Generates summary reports
4. Exports dashboard data

## Usage

### Running the Expense Processor

```bash
cd /Users/lemaiyan/dev/all/personal/mum-in-law-house
python process_expenses_new.py
```

### Output

- Console report with comprehensive financial summary
- `expense_data.json`: JSON export for dashboards (git-ignored)

### Generating Excel Report

```bash
python create_excel.py
```

Generates `Mother-In-Law-House-Expenses.xlsx` with 7 sheets:

1. Home Summary
2. Daily Expenses
3. Category Analysis
4. M-Pesa Fees
5. Outstanding Balances
6. Unpaid Labor
7. Pending Purchases

## Adding New Expenses

To add new expenses, edit `data/expenses.py`:

```python
# In get_expenses_data() function, add to the return list:
{
    "date": "22/10/2025",
    "category": "Labor Costs",
    "subcategory": "Daily Labor",
    "description": "Jack - UNPAID",  # Add "UNPAID" for unpaid expenses
    "amount": 1500,
    "vendor": "Worker",
},
```

**Important**:

- Add "UNPAID" in description for unpaid labor
- Use consistent date format (DD/MM/YYYY)
- Choose appropriate category/subcategory

## Updating Outstanding Balances

Edit `data/pending_items.py`:

### For outstanding balances:

```python
# In get_outstanding_balances() function:
{
    "vendor": "Vendor Name",
    "description": "Work description",
    "amount": 5000,
    "due_date": "To be scheduled",
},
```

### For pending purchases:

```python
# In get_pending_purchases() function:
{
    "category": "Category Name",
    "description": "Item description",
    "amount": 10000,
},
```

## Financial Summary (As of Oct 21, 2025)

- **Original Budget**: KES 1,000,000
- **Total Spent (Paid)**: KES 1,473,573.50 (147.36%)
- **Outstanding Balances**: KES 91,300
- **Unpaid Labor**: KES 15,900
- **Pending Purchases**: KES 185,705 (includes 15% contingency)
- **Total Pending**: KES 292,905
- **Additional Funds Needed**: KES 766,478.50 (76.65% over budget)
- **Total Project Cost**: KES 1,766,478.50

## Benefits of Modular Structure

### Before (Monolithic)

- ❌ Single 4,181-line file
- ❌ Difficult to navigate and maintain
- ❌ Hard to reuse components
- ❌ Risk of breaking changes

### After (Modular)

- ✅ Organized into logical modules (~100-200 lines each)
- ✅ Easy to find and update specific data
- ✅ Reusable calculation functions
- ✅ Clear separation of concerns
- ✅ Easy to test individual components
- ✅ Better Git diffs when making changes

## Migration Notes

The original `process_expenses.py` (4,181 lines) has been refactored into:

- `config.py`: 44 lines
- `calculations.py`: 170 lines
- `reports.py`: 166 lines
- `data/expenses.py`: ~3,840 lines (pure data)
- `data/pending_items.py`: 106 lines
- `process_expenses_new.py`: 64 lines (main orchestrator)

**Old file**: `process_expenses.py` (can be removed after verification)  
**New entry point**: `process_expenses_new.py`

## Development Workflow

1. **Add daily expenses**: Edit `data/expenses.py`
2. **Update balances**: Edit `data/pending_items.py`
3. **Run processor**: `python process_expenses_new.py`
4. **Generate Excel**: `python create_excel.py`
5. **Commit changes**: `git add -A && git commit -m "Update expenses"`

## Dependencies

- Python 3.13+
- pandas
- numpy
- openpyxl (for Excel generation)

Install via:

```bash
pip install pandas numpy openpyxl
```
