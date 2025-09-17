import json
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# Create comprehensive expense tracking system for Mother-in-Law House

# Project constants
TOTAL_BUDGET = 1_000_000  # KES
PROJECT_START = datetime(2025, 9, 15)


# M-Pesa fee structure (KES)
def calculate_mpesa_fee(amount):
    """Calculate M-Pesa transaction fee based on amount"""
    if amount <= 49:
        return 0
    elif amount <= 100:
        return 1
    elif amount <= 500:
        return 5
    elif amount <= 1000:
        return 10
    elif amount <= 1500:
        return 15
    elif amount <= 3000:
        return 25
    elif amount <= 5000:
        return 40
    elif amount <= 7500:
        return 75
    elif amount <= 10000:
        return 96
    elif amount <= 15000:
        return 156
    elif amount <= 20000:
        return 171.5
    elif amount <= 35000:
        return 355
    elif amount <= 50000:
        return 455
    else:
        return 455  # Max fee for amounts above 50K


# September 15, 2025 expenses
expenses_data = [
    # Transport & Logistics
    {
        "date": "15/09/2025",
        "category": "Transport & Logistics",
        "subcategory": "Worker Transport",
        "description": "Transport for the Workers",
        "amount": 2000,
        "vendor": "Local Transport",
    },
    {
        "date": "15/09/2025",
        "category": "Transport & Logistics",
        "subcategory": "Material Transport",
        "description": "Transport ballast",
        "amount": 2500,
        "vendor": "Transport Company",
    },
    {
        "date": "15/09/2025",
        "category": "Transport & Logistics",
        "subcategory": "Material Transport",
        "description": "Transport blocks",
        "amount": 2500,
        "vendor": "Transport Company",
    },
    # Workers Accommodation
    {
        "date": "15/09/2025",
        "category": "Workers Accommodation",
        "subcategory": "Accommodation",
        "description": "Accommodation for the workers",
        "amount": 2000,
        "vendor": "Local Lodge",
    },
    {
        "date": "15/09/2025",
        "category": "Workers Accommodation",
        "subcategory": "Housing",
        "description": "House rented for the workers (monthly)",
        "amount": 4000,
        "vendor": "Property Owner",
    },
    {
        "date": "15/09/2025",
        "category": "Workers Accommodation",
        "subcategory": "Bedding",
        "description": "3 mattresses @2500 each",
        "amount": 7500,
        "vendor": "Furniture Store",
    },
    # Building Materials
    {
        "date": "15/09/2025",
        "category": "Building Materials",
        "subcategory": "Sand",
        "description": "Sand - 14 tonnes",
        "amount": 9600,
        "vendor": "Sand Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Building Materials",
        "subcategory": "Ballast",
        "description": "Ballast 7 tonnes",
        "amount": 17150,
        "vendor": "Ballast Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Building Materials",
        "subcategory": "Blocks",
        "description": "Blocks 300@52",
        "amount": 15600,
        "vendor": "Block Manufacturer",
    },
    {
        "date": "15/09/2025",
        "category": "Building Materials",
        "subcategory": "Cement",
        "description": "Simba cement 710 @50 bags",
        "amount": 35500,
        "vendor": "Cement Dealer",
    },
    # Hardware Items
    {
        "date": "15/09/2025",
        "category": "Hardware Items",
        "subcategory": "Sealants",
        "description": "Calafiator 1 ltr @1800",
        "amount": 1800,
        "vendor": "Hardware Store",
    },
    {
        "date": "15/09/2025",
        "category": "Hardware Items",
        "subcategory": "Tools",
        "description": "Metal spades 550 @ 2",
        "amount": 1100,
        "vendor": "Hardware Store",
    },
    {
        "date": "15/09/2025",
        "category": "Hardware Items",
        "subcategory": "Protective",
        "description": "Polythene Papers rolls 2300 @ 2",
        "amount": 4600,
        "vendor": "Hardware Store",
    },
    {
        "date": "15/09/2025",
        "category": "Hardware Items",
        "subcategory": "Reinforcement",
        "description": "Hoop Iron 200 #4kg",
        "amount": 800,
        "vendor": "Hardware Store",
    },
    {
        "date": "15/09/2025",
        "category": "Hardware Items",
        "subcategory": "Fasteners",
        "description": 'Nails 4" 200 @ 5kg',
        "amount": 1000,
        "vendor": "Hardware Store",
    },
    {
        "date": "15/09/2025",
        "category": "Hardware Items",
        "subcategory": "Fasteners",
        "description": 'Nails 3" 200 @ 3kg',
        "amount": 600,
        "vendor": "Hardware Store",
    },
    {
        "date": "15/09/2025",
        "category": "Hardware Items",
        "subcategory": "Fasteners",
        "description": 'Nails 2.5" 200 @3kg',
        "amount": 600,
        "vendor": "Hardware Store",
    },
    {
        "date": "15/09/2025",
        "category": "Hardware Items",
        "subcategory": "Roofing",
        "description": 'Roofing poles 3" 250 @ 8',
        "amount": 2000,
        "vendor": "Hardware Store",
    },
    {
        "date": "15/09/2025",
        "category": "Hardware Items",
        "subcategory": "Fasteners",
        "description": "Roofing Nails 300 @ 3kg",
        "amount": 900,
        "vendor": "Hardware Store",
    },
    {
        "date": "15/09/2025",
        "category": "Hardware Items",
        "subcategory": "Sealing",
        "description": "Rubber maroon 200 @ 3pckts",
        "amount": 600,
        "vendor": "Hardware Store",
    },
    {
        "date": "15/09/2025",
        "category": "Hardware Items",
        "subcategory": "Plumbing",
        "description": "Horse Pipe clear 0.5 X60ft @ 1400",
        "amount": 1400,
        "vendor": "Hardware Store",
    },
    # Metal & Steel
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Welding",
        "description": "Welding rods 650 @ 2 packets",
        "amount": 1300,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Structure",
        "description": "Squaretube 1.5 X 1.5 900 @ 23 pcs",
        "amount": 20700,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Structure",
        "description": "Squaretubes 1.5 X 1 800@ 16 pcs",
        "amount": 12800,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Structure",
        "description": "Squaretubes 0.75 X 0.75 500 @17pcs",
        "amount": 8500,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Structure",
        "description": "Zed 0.75 850 @10pcs",
        "amount": 8500,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Structure",
        "description": "Squaretubes 1 X 1 600@4pcs",
        "amount": 2400,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Sheets",
        "description": "Blacksheet (18g) 3pcs 2400@3pcs",
        "amount": 7200,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Bars",
        "description": "Flatbar 0.5 X 0.125 850 @ 1pc",
        "amount": 850,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Bars",
        "description": "Flatbar 0.75 X 0.125 450 @ 10pcs",
        "amount": 4500,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Accessories",
        "description": "Chappy 250 @ 3pcs",
        "amount": 750,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Bars",
        "description": "Round 16 100 @ 5ft",
        "amount": 500,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Bars",
        "description": 'Flat busy 0.75 " 120 @ 26 pcs',
        "amount": 3120,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Structure",
        "description": "T-bar 0.75 850 @ 1pc",
        "amount": 850,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Accessories",
        "description": "Down stopper 120 @12pcs",
        "amount": 1440,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Finishing",
        "description": "Sand Paper p36 100 @3ms",
        "amount": 300,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Tools",
        "description": "Cutting disk 250 @5pcs",
        "amount": 1250,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Tools",
        "description": "Grinding disk 250 @ 2pcs",
        "amount": 500,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Paint",
        "description": "Undercoat paint 5 ltrs 1050 @ 1pc",
        "amount": 1050,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Paint",
        "description": "Thinner 5ltrs 1450 @ 1pc",
        "amount": 1450,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Tools",
        "description": 'Brush 2" 150 @2pcs',
        "amount": 300,
        "vendor": "Metal Supplier",
    },
    {
        "date": "15/09/2025",
        "category": "Metal & Steel",
        "subcategory": "Accessories",
        "description": "Chappy Normal (complete) 650 @ 1pc",
        "amount": 650,
        "vendor": "Metal Supplier",
    },
    # Labor
    {
        "date": "15/09/2025",
        "category": "Labor Costs",
        "subcategory": "Daily Labor",
        "description": "Jack",
        "amount": 2000,
        "vendor": "Worker",
    },
    {
        "date": "15/09/2025",
        "category": "Labor Costs",
        "subcategory": "Daily Labor",
        "description": "Fundi 1",
        "amount": 1300,
        "vendor": "Worker",
    },
    # Miscellaneous
    {
        "date": "15/09/2025",
        "category": "Miscellaneous",
        "subcategory": "Lost Payment",
        "description": "Overpayment not refunded",
        "amount": 1000,
        "vendor": "Unknown",
    },
    # September 16, 2025 expenses
    {
        "date": "16/09/2025",
        "category": "Labor Costs",
        "subcategory": "Specialist Labor",
        "description": "Welder deposit",
        "amount": 12000,
        "vendor": "Welder",
    },
    {
        "date": "16/09/2025",
        "category": "Hardware Items",
        "subcategory": "Tools",
        "description": "Wheelbarrow",
        "amount": 4350,
        "vendor": "Hardware Store",
    },
    {
        "date": "16/09/2025",
        "category": "Hardware Items",
        "subcategory": "Plumbing",
        "description": 'Tap 1/2"',
        "amount": 550,
        "vendor": "Hardware Store",
    },
    {
        "date": "16/09/2025",
        "category": "Hardware Items",
        "subcategory": "Storage",
        "description": "Blue drum",
        "amount": 2600,
        "vendor": "Hardware Store",
    },
    {
        "date": "16/09/2025",
        "category": "Hardware Items",
        "subcategory": "Tools",
        "description": 'Hacksaw 14"',
        "amount": 280,
        "vendor": "Hardware Store",
    },
    {
        "date": "16/09/2025",
        "category": "Building Materials",
        "subcategory": "Doors & Windows",
        "description": "Door Frames 6 @ 1200",
        "amount": 7200,
        "vendor": "Carpenter",
    },
    {
        "date": "16/09/2025",
        "category": "Transport & Logistics",
        "subcategory": "Worker Transport",
        "description": "Transport for two electricians to voi",
        "amount": 2700,
        "vendor": "Transport Service",
    },
    # Paid labor for 16/09/2025
    {
        "date": "16/09/2025",
        "category": "Labor Costs",
        "subcategory": "Daily Labor",
        "description": "Jack - Daily Labor",
        "amount": 2000,
        "vendor": "Worker",
    },
    {
        "date": "16/09/2025",
        "category": "Labor Costs",
        "subcategory": "Daily Labor",
        "description": "Fundi 1 - Daily Labor",
        "amount": 1300,
        "vendor": "Worker",
    },
    {
        "date": "16/09/2025",
        "category": "Labor Costs",
        "subcategory": "Daily Labor",
        "description": "Helper 1 - Daily Labor",
        "amount": 600,
        "vendor": "Worker",
    },
    {
        "date": "16/09/2025",
        "category": "Labor Costs",
        "subcategory": "Daily Labor",
        "description": "Helper 2 - Daily Labor",
        "amount": 600,
        "vendor": "Worker",
    },
    # September 17, 2025 expenses
    {
        "date": "17/09/2025",
        "category": "Labor Costs",
        "subcategory": "Specialist Labor",
        "description": "Electrician Labor for fixing wiring pipes and boxes",
        "amount": 10000,
        "vendor": "Electrician",
    },
    {
        "date": "17/09/2025",
        "category": "Transport & Logistics",
        "subcategory": "Worker Transport",
        "description": "Transport back to Nairobi",
        "amount": 2200,
        "vendor": "Transport Service",
    },
    {
        "date": "17/09/2025",
        "category": "Hardware Items",
        "subcategory": "Electrical",
        "description": '15"X15" meterbox 1pc',
        "amount": 2300,
        "vendor": "Electrical Supplier",
    },
    {
        "date": "17/09/2025",
        "category": "Hardware Items",
        "subcategory": "Electrical",
        "description": "8-way ccu 1pc",
        "amount": 3500,
        "vendor": "Electrical Supplier",
    },
    {
        "date": "17/09/2025",
        "category": "Hardware Items",
        "subcategory": "Electrical",
        "description": "16pcs twin boxes",
        "amount": 800,
        "vendor": "Electrical Supplier",
    },
    {
        "date": "17/09/2025",
        "category": "Hardware Items",
        "subcategory": "Electrical",
        "description": "13pcs single boxes",
        "amount": 450,
        "vendor": "Electrical Supplier",
    },
    {
        "date": "17/09/2025",
        "category": "Hardware Items",
        "subcategory": "Electrical",
        "description": "60pcs 20mm conduits",
        "amount": 5400,
        "vendor": "Electrical Supplier",
    },
    {
        "date": "17/09/2025",
        "category": "Hardware Items",
        "subcategory": "Electrical",
        "description": "3pcs 25mm conduits",
        "amount": 600,
        "vendor": "Electrical Supplier",
    },
    {
        "date": "17/09/2025",
        "category": "Hardware Items",
        "subcategory": "Electrical",
        "description": "2pcs 32mm conduits",
        "amount": 520,
        "vendor": "Electrical Supplier",
    },
    {
        "date": "17/09/2025",
        "category": "Hardware Items",
        "subcategory": "Electrical",
        "description": "80pcs 20mm couplers",
        "amount": 400,
        "vendor": "Electrical Supplier",
    },
    {
        "date": "17/09/2025",
        "category": "Hardware Items",
        "subcategory": "Electrical",
        "description": "10pcs 25mm couplers",
        "amount": 200,
        "vendor": "Electrical Supplier",
    },
    {
        "date": "17/09/2025",
        "category": "Hardware Items",
        "subcategory": "Electrical",
        "description": "3pcs 32mm couplers",
        "amount": 105,
        "vendor": "Electrical Supplier",
    },
    {
        "date": "17/09/2025",
        "category": "Hardware Items",
        "subcategory": "Electrical",
        "description": "3pcs 32mm bends",
        "amount": 150,
        "vendor": "Electrical Supplier",
    },
    {
        "date": "17/09/2025",
        "category": "Hardware Items",
        "subcategory": "Electrical",
        "description": "1pc masking tape",
        "amount": 250,
        "vendor": "Electrical Supplier",
    },
    {
        "date": "17/09/2025",
        "category": "Labor Costs",
        "subcategory": "Daily Labor",
        "description": "Jack",
        "amount": 1500,
        "vendor": "Worker",
    },
    {
        "date": "17/09/2025",
        "category": "Labor Costs",
        "subcategory": "Daily Labor",
        "description": "Fundi 1",
        "amount": 1300,
        "vendor": "Worker",
    },
    {
        "date": "17/09/2025",
        "category": "Labor Costs",
        "subcategory": "Daily Labor",
        "description": "Helper 1",
        "amount": 600,
        "vendor": "Worker",
    },
    {
        "date": "17/09/2025",
        "category": "Labor Costs",
        "subcategory": "Daily Labor",
        "description": "Helper 2",
        "amount": 600,
        "vendor": "Worker",
    },
    {
        "date": "17/09/2025",
        "category": "Labor Costs",
        "subcategory": "Daily Labor",
        "description": "Helper 3",
        "amount": 600,
        "vendor": "Worker",
    },
    {
        "date": "17/09/2025",
        "category": "Labor Costs",
        "subcategory": "Daily Labor",
        "description": "Helper 4",
        "amount": 600,
        "vendor": "Worker",
    },
    {
        "date": "17/09/2025",
        "category": "Workers Accommodation",
        "subcategory": "Food",
        "description": "Food for the workers",
        "amount": 3260,
        "vendor": "Local Vendor",
    },
]

# Calculate M-Pesa fees for each expense
for expense in expenses_data:
    # For unpaid expenses, set M-Pesa fee to 0 and mark as unpaid
    if "UNPAID" in expense["description"]:
        expense["mpesa_fee"] = 0.0
        expense["total_cost"] = 0.0  # Don't count in spending until paid
        expense["status"] = "unpaid"
    else:
        expense["mpesa_fee"] = calculate_mpesa_fee(expense["amount"])
        expense["total_cost"] = expense["amount"] + expense["mpesa_fee"]
        expense["status"] = "paid"

# Create DataFrame
df = pd.DataFrame(expenses_data)

# Calculate summary statistics (only paid expenses)
paid_df = df[df["status"] == "paid"]
total_spent = paid_df["amount"].sum()
total_mpesa_fees = paid_df["mpesa_fee"].sum()
total_cost = paid_df["total_cost"].sum()
balance_remaining = TOTAL_BUDGET - total_cost
percentage_used = (total_cost / TOTAL_BUDGET) * 100

# Category summary (only paid expenses)
category_summary = (
    paid_df.groupby("category")
    .agg({"amount": "sum", "mpesa_fee": "sum", "total_cost": "sum"})
    .reset_index()
)

# Calculate budget percentage and sort by it (descending)
category_summary["budget_percentage"] = (
    category_summary["total_cost"] / TOTAL_BUDGET
) * 100
category_summary = category_summary.sort_values(
    "budget_percentage", ascending=False
).reset_index(drop=True)

# Outstanding balances tracking
outstanding_balances = [
    {
        "vendor": "Welder",
        "description": "Remaining balance for welding work",
        "amount": 21000,
        "due_date": "To be scheduled",
    }
]

# Unpaid labor expenses (all labor now paid)
unpaid_expenses = []

# Calculate total outstanding amounts
total_outstanding = sum(balance["amount"] for balance in outstanding_balances)
total_unpaid_labor = sum(expense["amount"] for expense in unpaid_expenses)
total_pending = total_outstanding + total_unpaid_labor

# Print summary for verification
print("=== MOTHER-IN-LAW HOUSE EXPENSE SUMMARY ===")
print(f"Date: {PROJECT_START.strftime('%d/%m/%Y')}")
print(f"Total Budget: KES {TOTAL_BUDGET:,}")
print(f"Total Spent: KES {total_spent:,}")
print(f"M-Pesa Fees: KES {total_mpesa_fees:,}")
print(f"Total Cost (inc. fees): KES {total_cost:,}")
print(f"Balance Remaining: KES {balance_remaining:,}")
print(f"Budget Used: {percentage_used:.2f}%")
print()
print("=== OUTSTANDING AMOUNTS ===")
print(f"Outstanding Balances: KES {total_outstanding:,}")
print(f"Unpaid Labor: KES {total_unpaid_labor:,}")
print(f"Total Pending: KES {total_pending:,}")
print(f"Effective Balance: KES {balance_remaining - total_pending:,}")
print()

print("=== CATEGORY BREAKDOWN ===")
for _, row in category_summary.iterrows():
    print(
        f"{row['category']}: KES {row['total_cost']:,} (Amount: {row['amount']:,} + Fees: {row['mpesa_fee']:,})"
    )

# Export data for HTML dashboard
dashboard_data = {
    "project_info": {
        "name": "Mother-in-Law House Completion",
        "start_date": "15/09/2025",
        "total_budget": TOTAL_BUDGET,
        "total_spent": int(total_spent),
        "total_mpesa_fees": int(total_mpesa_fees),
        "total_cost": int(total_cost),
        "balance_remaining": int(balance_remaining),
        "percentage_used": round(percentage_used, 2),
        "total_outstanding": int(total_outstanding),
        "total_unpaid_labor": int(total_unpaid_labor),
        "total_pending": int(total_pending),
    },
    "category_summary": category_summary.to_dict("records"),
    "daily_expenses": df.to_dict("records"),
    "outstanding_balances": outstanding_balances,
    "unpaid_expenses": unpaid_expenses,
    "last_updated": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
}

# Save data for HTML dashboard
with open("/Users/lemaiyan/dev/personal/mum-in-law-house/expense_data.json", "w") as f:
    json.dump(dashboard_data, f, indent=2)

print(f"\nData exported for HTML dashboard: {len(df)} transactions processed")
print(f"JSON file created: expense_data.json")
