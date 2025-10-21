"""Financial calculations for expense tracking."""

import pandas as pd
from config import TOTAL_BUDGET, calculate_mpesa_fee


def process_expenses(expenses_data):
    """
    Process expenses data and calculate M-Pesa fees.

    Args:
        expenses_data: List of expense dictionaries

    Returns:
        DataFrame with processed expenses including fees and status
    """
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

    return pd.DataFrame(expenses_data)


def calculate_summary_stats(df):
    """
    Calculate summary statistics from expense DataFrame.

    Args:
        df: DataFrame with processed expenses

    Returns:
        Dictionary with summary statistics
    """
    # Calculate summary statistics (only paid expenses)
    paid_df = df[df["status"] == "paid"]
    total_spent = paid_df["amount"].sum()
    total_mpesa_fees = paid_df["mpesa_fee"].sum()
    total_cost = paid_df["total_cost"].sum()
    balance_remaining = TOTAL_BUDGET - total_cost
    percentage_used = (total_cost / TOTAL_BUDGET) * 100

    return {
        "paid_df": paid_df,
        "total_spent": total_spent,
        "total_mpesa_fees": total_mpesa_fees,
        "total_cost": total_cost,
        "balance_remaining": balance_remaining,
        "percentage_used": percentage_used,
    }


def calculate_category_summary(paid_df):
    """
    Calculate category-wise expense breakdown.

    Args:
        paid_df: DataFrame with paid expenses only

    Returns:
        DataFrame with category summary sorted by budget percentage
    """
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

    return category_summary


def calculate_pending_amounts(df, outstanding_balances, pending_purchases):
    """
    Calculate all pending amounts including unpaid labor and purchases.

    Args:
        df: DataFrame with all expenses
        outstanding_balances: List of outstanding balance items
        pending_purchases: List of pending purchase items (without contingency)

    Returns:
        Dictionary with pending amount calculations
    """
    # Unpaid labor expenses
    unpaid_df = df[df["status"] == "unpaid"]
    unpaid_expenses = unpaid_df.to_dict("records")

    total_outstanding = sum(balance["amount"] for balance in outstanding_balances)
    total_unpaid_labor = sum(expense["amount"] for expense in unpaid_expenses)
    total_pending = total_outstanding + total_unpaid_labor

    # Calculate total pending purchases (base items only)
    total_pending_purchases = sum(item["amount"] for item in pending_purchases)

    # Calculate miscellaneous contingency (15% of pending purchases + outstanding balances)
    # Based on project history: ~6% has been miscellaneous/unexpected costs
    # For safety, recommend 15% contingency for remaining work
    contingency_base = total_pending_purchases + total_outstanding + total_unpaid_labor
    miscellaneous_estimate = int(contingency_base * 0.15)

    # Add contingency to pending purchases
    pending_purchases_with_contingency = pending_purchases.copy()
    pending_purchases_with_contingency.append(
        {
            "category": "Miscellaneous & Contingency",
            "description": "Estimated miscellaneous costs (15% of remaining work) - includes transport, food, accommodation, unexpected items",
            "amount": miscellaneous_estimate,
        }
    )

    # Recalculate with contingency
    total_pending_purchases_with_contingency = (
        total_pending_purchases + miscellaneous_estimate
    )

    return {
        "unpaid_expenses": unpaid_expenses,
        "total_outstanding": total_outstanding,
        "total_unpaid_labor": total_unpaid_labor,
        "total_pending": total_pending,
        "total_pending_purchases": total_pending_purchases,
        "miscellaneous_estimate": miscellaneous_estimate,
        "pending_purchases_with_contingency": pending_purchases_with_contingency,
        "total_pending_purchases_with_contingency": total_pending_purchases_with_contingency,
    }


def calculate_project_totals(summary_stats, pending_amounts):
    """
    Calculate overall project totals and budget analysis.

    Args:
        summary_stats: Dictionary from calculate_summary_stats
        pending_amounts: Dictionary from calculate_pending_amounts

    Returns:
        Dictionary with project totals
    """
    total_cost = summary_stats["total_cost"]
    total_pending = pending_amounts["total_pending"]
    total_pending_purchases = pending_amounts[
        "total_pending_purchases_with_contingency"
    ]

    # Calculate inclusive budget percentages
    total_committed = total_cost + total_pending  # All spent + all outstanding/unpaid
    percentage_used_inclusive = (total_committed / TOTAL_BUDGET) * 100
    effective_balance = TOTAL_BUDGET - total_committed

    # Calculate project completion estimates
    total_project_cost = total_cost + total_pending + total_pending_purchases
    additional_funds_needed = total_project_cost - TOTAL_BUDGET
    total_not_yet_paid = total_pending + total_pending_purchases

    return {
        "total_committed": total_committed,
        "percentage_used_inclusive": percentage_used_inclusive,
        "effective_balance": effective_balance,
        "total_project_cost": total_project_cost,
        "additional_funds_needed": additional_funds_needed,
        "total_not_yet_paid": total_not_yet_paid,
    }
