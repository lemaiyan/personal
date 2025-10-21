#!/usr/bin/env python3
"""
Main expense processing script for Mother-in-Law House construction project.

This script orchestrates the expense tracking by:
1. Loading expense data from data modules
2. Processing expenses and calculating fees
3. Generating summary reports
4. Exporting data for dashboards
"""

from calculations import (
    calculate_category_summary,
    calculate_pending_amounts,
    calculate_project_totals,
    calculate_summary_stats,
    process_expenses,
)
from data import get_expenses_data, get_outstanding_balances, get_pending_purchases
from reports import export_dashboard_data, print_summary_report


def main():
    """Main function to process expenses and generate reports."""
    # Load data
    expenses_data = get_expenses_data()
    outstanding_balances = get_outstanding_balances()
    pending_purchases = get_pending_purchases()

    # Process expenses
    df = process_expenses(expenses_data)

    # Calculate summaries
    summary_stats = calculate_summary_stats(df)
    category_summary = calculate_category_summary(summary_stats["paid_df"])
    pending_amounts = calculate_pending_amounts(
        df, outstanding_balances, pending_purchases
    )
    project_totals = calculate_project_totals(summary_stats, pending_amounts)

    # Print reports
    print_summary_report(
        summary_stats,
        pending_amounts,
        project_totals,
        category_summary,
        outstanding_balances,
    )

    # Export dashboard data
    output_path = "/Users/lemaiyan/dev/all/personal/mum-in-law-house/expense_data.json"
    num_transactions = export_dashboard_data(
        df,
        summary_stats,
        pending_amounts,
        project_totals,
        category_summary,
        outstanding_balances,
        output_path,
    )

    print(
        f"\nData exported for HTML dashboard: {num_transactions} transactions processed"
    )
    print(f"JSON file created: expense_data.json")


if __name__ == "__main__":
    main()
