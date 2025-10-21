"""Configuration and constants for Mother-in-Law House expense tracking."""

from datetime import datetime

# Project constants
TOTAL_BUDGET = (
    1_000_000  # KES - Original budget (to show true picture of budget overrun)
)
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
