import json
from datetime import datetime

import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

# Load the processed data
with open("/Users/lemaiyan/dev/personal/mum-in-law-house/expense_data.json", "r") as f:
    data = json.load(f)

# Create Excel workbook
wb = Workbook()

# Remove default sheet and create custom sheets
wb.remove(wb.active)

# Create sheets
summary_sheet = wb.create_sheet("Home Summary")
daily_sheet = wb.create_sheet("Daily Expenses")
category_sheet = wb.create_sheet("Category Analysis")
mpesa_sheet = wb.create_sheet("M-Pesa Fees")

# Define styles
header_font = Font(bold=True, size=12, color="FFFFFF")
header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
title_font = Font(bold=True, size=14, color="2C5F2D")
currency_font = Font(size=11)
border = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin"),
)

# === HOME SUMMARY SHEET ===
ws = summary_sheet

# Project header
ws["A1"] = "MOTHER-IN-LAW HOUSE - EXPENSE TRACKER"
ws["A1"].font = Font(bold=True, size=16, color="2C5F2D")
ws.merge_cells("A1:E1")

# Key metrics
ws["A3"] = "Project Overview"
ws["A3"].font = title_font

project_info = data["project_info"]
ws["A4"] = "Total Budget:"
ws["B4"] = f"KES {project_info['total_budget']:,}"
ws["A5"] = "Total Spent:"
ws["B5"] = f"KES {project_info['total_cost']:,}"
ws["A6"] = "Balance Remaining:"
ws["B6"] = f"KES {project_info['balance_remaining']:,}"
ws["A7"] = "Budget Used:"
ws["B7"] = f"{project_info['percentage_used']}%"
ws["A8"] = "M-Pesa Fees:"
ws["B8"] = f"KES {project_info['total_mpesa_fees']:,}"

# Category summary
ws["A10"] = "Category Breakdown"
ws["A10"].font = title_font

# Headers
headers = ["Category", "Amount Spent", "M-Pesa Fees", "Total Cost", "Budget %"]
for col, header in enumerate(headers, 1):
    cell = ws.cell(row=11, column=col, value=header)
    cell.font = header_font
    cell.fill = header_fill
    cell.border = border

# Category data
for row, category in enumerate(data["category_summary"], 12):
    ws.cell(row=row, column=1, value=category["category"]).border = border
    ws.cell(row=row, column=2, value=category["amount"]).border = border
    ws.cell(row=row, column=3, value=category["mpesa_fee"]).border = border
    ws.cell(row=row, column=4, value=category["total_cost"]).border = border
    percentage = (category["total_cost"] / project_info["total_budget"]) * 100
    ws.cell(row=row, column=5, value=f"{percentage:.2f}%").border = border

# Adjust column widths
ws.column_dimensions["A"].width = 25
ws.column_dimensions["B"].width = 15
ws.column_dimensions["C"].width = 15
ws.column_dimensions["D"].width = 15
ws.column_dimensions["E"].width = 12

# === DAILY EXPENSES SHEET ===
ws = daily_sheet

# Headers
expense_headers = [
    "Date",
    "Category",
    "Subcategory",
    "Description",
    "Amount",
    "M-Pesa Fee",
    "Total Cost",
    "Vendor",
]
for col, header in enumerate(expense_headers, 1):
    cell = ws.cell(row=1, column=col, value=header)
    cell.font = header_font
    cell.fill = header_fill
    cell.border = border

# Expense data
for row, expense in enumerate(data["daily_expenses"], 2):
    ws.cell(row=row, column=1, value=expense["date"]).border = border
    ws.cell(row=row, column=2, value=expense["category"]).border = border
    ws.cell(row=row, column=3, value=expense["subcategory"]).border = border
    ws.cell(row=row, column=4, value=expense["description"]).border = border
    ws.cell(row=row, column=5, value=expense["amount"]).border = border
    ws.cell(row=row, column=6, value=expense["mpesa_fee"]).border = border
    ws.cell(row=row, column=7, value=expense["total_cost"]).border = border
    ws.cell(row=row, column=8, value=expense["vendor"]).border = border

# Adjust column widths
for col in ["A", "B", "C", "D", "E", "F", "G", "H"]:
    ws.column_dimensions[col].width = 18

# === M-PESA FEES SHEET ===
ws = mpesa_sheet

ws["A1"] = "M-Pesa Fee Analysis"
ws["A1"].font = title_font

# Fee structure table
ws["A3"] = "Fee Structure"
ws["A3"].font = Font(bold=True)

fee_headers = ["Amount Range", "Fee (KES)", "Transactions", "Total Fees"]
for col, header in enumerate(fee_headers, 1):
    cell = ws.cell(row=4, column=col, value=header)
    cell.font = header_font
    cell.fill = header_fill

# Calculate fee analysis from expenses
fee_analysis = {}
for expense in data["daily_expenses"]:
    amount = expense["amount"]
    fee = expense["mpesa_fee"]

    # Determine fee bracket
    if amount <= 49:
        bracket = "0-49"
    elif amount <= 100:
        bracket = "50-100"
    elif amount <= 500:
        bracket = "101-500"
    elif amount <= 1000:
        bracket = "501-1000"
    elif amount <= 1500:
        bracket = "1001-1500"
    elif amount <= 3000:
        bracket = "1501-3000"
    elif amount <= 5000:
        bracket = "3001-5000"
    elif amount <= 7500:
        bracket = "5001-7500"
    elif amount <= 10000:
        bracket = "7501-10000"
    elif amount <= 15000:
        bracket = "10001-15000"
    elif amount <= 20000:
        bracket = "15001-20000"
    elif amount <= 35000:
        bracket = "20001-35000"
    else:
        bracket = "35001+"

    if bracket not in fee_analysis:
        fee_analysis[bracket] = {"count": 0, "total_fees": 0, "fee_rate": fee}
    fee_analysis[bracket]["count"] += 1
    fee_analysis[bracket]["total_fees"] += fee

# Add fee analysis to sheet
row = 5
for bracket, analysis in fee_analysis.items():
    ws.cell(row=row, column=1, value=bracket)
    ws.cell(row=row, column=2, value=analysis["fee_rate"])
    ws.cell(row=row, column=3, value=analysis["count"])
    ws.cell(row=row, column=4, value=analysis["total_fees"])
    row += 1

# Summary
ws[f"A{row+2}"] = "Total M-Pesa Fees:"
ws[f"B{row+2}"] = f"KES {project_info['total_mpesa_fees']:,}"
ws[f"B{row+2}"].font = Font(bold=True)

# Save the Excel file
wb.save(
    "/Users/lemaiyan/dev/personal/mum-in-law-house/Mother-In-Law-House-Expenses.xlsx"
)
print("Excel file created: Mother-In-Law-House-Expenses.xlsx")
print("Sheets created: Home Summary, Daily Expenses, Category Analysis, M-Pesa Fees")
