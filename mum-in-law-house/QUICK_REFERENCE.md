# Quick Reference Guide

## Daily Workflow

### 1. Add New Expenses
Edit: `data/expenses.py`

```python
# At the end of the list in get_expenses_data():
{
    "date": "22/10/2025",
    "category": "Labor Costs",
    "subcategory": "Daily Labor", 
    "description": "Jack - UNPAID",  # Add "UNPAID" for unpaid labor
    "amount": 1500,
    "vendor": "Worker",
},
```

**Categories**: Building Materials, Labor Costs, Hardware Items, Metal & Steel, Utilities, Transport & Logistics, Workers Accommodation, Miscellaneous, Furniture & Fixtures

### 2. Update Outstanding Balances
Edit: `data/pending_items.py` → `get_outstanding_balances()`

```python
{
    "vendor": "Electrician",
    "description": "Remaining balance for electrical work",
    "amount": 5000,  # Update amount
    "due_date": "To be scheduled",
},
```

### 3. Add/Update Pending Purchases
Edit: `data/pending_items.py` → `get_pending_purchases()`

```python
{
    "category": "Paint",
    "description": "20 ltrs silk Ivory",
    "amount": 14700,
},
```

### 4. Run Reports
```bash
cd /Users/lemaiyan/dev/all/personal/mum-in-law-house

# Generate console report + JSON
python process_expenses.py

# Generate Excel report  
python create_excel.py
```

### 5. Commit Changes
```bash
git add -A
git commit -m "Add Oct 22 expenses: labor and materials"
git push
```

## Common Tasks

### Mark Labor as Paid
Remove "- UNPAID" from description in `data/expenses.py`:
```python
# Before:
"description": "Jack - UNPAID",

# After:
"description": "Jack (paid 22/10)",
```

### Add Material Purchase
```python
{
    "date": "22/10/2025",
    "category": "Building Materials",
    "subcategory": "Cement & Aggregates",
    "description": "10 bags cement @ 750",
    "amount": 7500,
    "vendor": "Hardware Store",
},
```

### Update Budget (if needed)
Edit: `config.py`
```python
TOTAL_BUDGET = 1_500_000  # Update if budget increases
```

### Change Contingency Percentage
Edit: `calculations.py` → `calculate_pending_amounts()`
```python
# Line ~116
miscellaneous_estimate = int(contingency_base * 0.20)  # Changed from 0.15
```

## File Locations Quick Reference

| Task | File | Function |
|------|------|----------|
| Add expense | `data/expenses.py` | `get_expenses_data()` |
| Update outstanding | `data/pending_items.py` | `get_outstanding_balances()` |
| Update pending | `data/pending_items.py` | `get_pending_purchases()` |
| Change budget | `config.py` | `TOTAL_BUDGET` |
| Modify M-Pesa | `config.py` | `calculate_mpesa_fee()` |
| Change calculations | `calculations.py` | Various functions |
| Modify reports | `reports.py` | `print_summary_report()` |

## Output Files

| File | Purpose | Git Status |
|------|---------|------------|
| `expense_data.json` | Dashboard data | Ignored |
| `Mother-In-Law-House-Expenses.xlsx` | Excel report | Tracked |
| `process_expenses_old.py` | Old backup | Ignored |

## Tips

1. **Always test after changes**: Run `python process_expenses.py`
2. **Add descriptive commit messages**: Include amounts and what changed
3. **Mark unpaid items clearly**: Use "UNPAID" in description
4. **Use consistent dates**: DD/MM/YYYY format
5. **Group related expenses**: Use comments like `# Tuesday 22/10/2025`

## Troubleshooting

### Import Error
```bash
# Make sure you're in the right directory
cd /Users/lemaiyan/dev/all/personal/mum-in-law-house

# Check Python environment
which python
# Should show: /Users/lemaiyan/dev/all/personal/.venv/bin/python
```

### Wrong Totals
1. Check for duplicate entries in `data/expenses.py`
2. Verify "UNPAID" flag is correct
3. Run script and review console output

### Excel Generation Fails
1. Ensure `process_expenses.py` ran successfully first
2. Check that `expense_data.json` exists
3. Verify no file permission issues

## Quick Stats (Current)

- **Budget**: KES 1,000,000
- **Spent**: KES 1,473,573.50 (147.36%)
- **Unpaid Labor**: KES 15,900
- **Outstanding**: KES 91,300
- **Pending Purchases**: KES 185,705
- **Total Needed**: KES 766,478.50 more (76.65% over budget)
- **Transactions**: 471

---

**Last Updated**: October 21, 2025  
**Version**: 2.0 (Modular)
