"""Report generation and output formatting."""

import json

from config import PROJECT_START, TOTAL_BUDGET


def print_summary_report(
    summary_stats,
    pending_amounts,
    project_totals,
    category_summary,
    outstanding_balances,
):
    """
    Print comprehensive expense summary report to console.

    Args:
        summary_stats: Dictionary from calculate_summary_stats
        pending_amounts: Dictionary from calculate_pending_amounts
        project_totals: Dictionary from calculate_project_totals
        category_summary: DataFrame with category breakdown
        outstanding_balances: List of outstanding balance items
    """
    # Main summary
    print("=== MOTHER-IN-LAW HOUSE EXPENSE SUMMARY ===")
    print(f"Date: {PROJECT_START.strftime('%d/%m/%Y')}")
    print(f"Total Budget: KES {TOTAL_BUDGET:,}")
    print(f"Total Spent (Paid): KES {summary_stats['total_spent']:,}")
    print(f"M-Pesa Fees: KES {summary_stats['total_mpesa_fees']:,}")
    print(f"Total Cost (inc. fees): KES {summary_stats['total_cost']:,}")
    print(f"Balance Remaining: KES {summary_stats['balance_remaining']:,}")
    print(f"Budget Used (Paid Only): {summary_stats['percentage_used']:.2f}%")
    print()

    # Outstanding amounts
    print("=== OUTSTANDING AMOUNTS ===")
    print(f"Outstanding Balances: KES {pending_amounts['total_outstanding']:,}")
    print(f"Unpaid Labor: KES {pending_amounts['total_unpaid_labor']:,}")
    print(f"Total Pending: KES {pending_amounts['total_pending']:,}")
    print(
        f"Total Committed (Paid + Pending): KES {project_totals['total_committed']:,}"
    )
    print(
        f"Budget Used (Inclusive): {project_totals['percentage_used_inclusive']:.2f}%"
    )
    print(f"Effective Balance: KES {project_totals['effective_balance']:,}")
    print()

    # Category breakdown
    print("=== CATEGORY BREAKDOWN ===")
    for _, row in category_summary.iterrows():
        print(
            f"{row['category']}: KES {row['total_cost']:,} "
            f"(Amount: {row['amount']:,} + Fees: {row['mpesa_fee']:,})"
        )
    print()

    # Pending purchases
    print("=== PENDING PURCHASES (Not Yet Procured) ===")
    for item in pending_amounts["pending_purchases_with_contingency"]:
        print(f"{item['category']}: {item['description']} - KES {item['amount']:,}")
    print(
        f"\nTotal Pending Purchases: KES {pending_amounts['total_pending_purchases_with_contingency']:,}"
    )
    print()

    # Pending items summary
    print("=== PENDING ITEMS (Not Yet Paid/Bought) ===")
    print(
        f"Outstanding Balances (Specialist Work):  KES {pending_amounts['total_outstanding']:,}"
    )
    print(
        f"Unpaid Labor (Daily Workers):            KES {pending_amounts['total_unpaid_labor']:,}"
    )
    print(
        f"Pending Purchases (Items to Buy):        KES {pending_amounts['total_pending_purchases_with_contingency']:,}"
    )
    print(f"{'─'*50}")
    print(
        f"TOTAL PENDING (Not Yet Paid/Bought):     KES {project_totals['total_not_yet_paid']:,}"
    )
    print()

    # Project completion estimate
    print("=== PROJECT COMPLETION ESTIMATE ===")
    print(f"1. Already Spent (Paid): KES {summary_stats['total_cost']:,}")
    print(f"2. Outstanding Balances: KES {pending_amounts['total_outstanding']:,}")
    print(f"3. Unpaid Labor: KES {pending_amounts['total_unpaid_labor']:,}")
    print(
        f"4. Pending Purchases: KES {pending_amounts['total_pending_purchases_with_contingency']:,}"
    )
    print(f"   - Items to buy: KES {pending_amounts['total_pending_purchases']:,}")
    print(f"   - Contingency (15%): KES {pending_amounts['miscellaneous_estimate']:,}")
    print(f"\n{'='*50}")
    print(f"TOTAL ESTIMATED PROJECT COST: KES {project_totals['total_project_cost']:,}")
    print(f"Current Budget: KES {TOTAL_BUDGET:,}")
    print(
        f"Already Over Budget (Spent): KES {summary_stats['total_cost'] - TOTAL_BUDGET:,}"
    )
    print()
    print(f"ADDITIONAL FUNDS NEEDED: KES {project_totals['additional_funds_needed']:,}")
    print(f"  Breakdown:")
    print(f"  • Outstanding Balances:     KES {pending_amounts['total_outstanding']:,}")
    print(
        f"  • Unpaid Labor:             KES {pending_amounts['total_unpaid_labor']:,}"
    )
    print(
        f"  • Pending Purchases:        KES {pending_amounts['total_pending_purchases_with_contingency']:,}"
    )
    print(f"  ─────────────────────────────────────────────")
    print(f"  Total Breakdown:            KES {project_totals['total_not_yet_paid']:,}")
    print()
    print(
        f"Total Over Budget: {((project_totals['additional_funds_needed'] / TOTAL_BUDGET) * 100):.2f}%"
    )
    print(f"{'='*50}")


def export_dashboard_data(
    df,
    summary_stats,
    pending_amounts,
    project_totals,
    category_summary,
    outstanding_balances,
    output_path,
):
    """
    Export data to JSON for HTML dashboard.

    Args:
        df: Complete DataFrame with all expenses
        summary_stats: Dictionary from calculate_summary_stats
        pending_amounts: Dictionary from calculate_pending_amounts
        project_totals: Dictionary from calculate_project_totals
        category_summary: DataFrame with category breakdown
        outstanding_balances: List of outstanding balance items
        output_path: Path to save JSON file

    Returns:
        Number of transactions processed
    """
    dashboard_data = {
        "project_info": {
            "name": "Mother-in-Law House Completion",
            "start_date": "15/09/2025",
            "total_budget": TOTAL_BUDGET,
            "total_spent": int(summary_stats["total_spent"]),
            "total_mpesa_fees": int(summary_stats["total_mpesa_fees"]),
            "total_cost": int(summary_stats["total_cost"]),
            "balance_remaining": int(summary_stats["balance_remaining"]),
            "percentage_used": round(summary_stats["percentage_used"], 2),
            "percentage_used_inclusive": round(
                project_totals["percentage_used_inclusive"], 2
            ),
            "total_outstanding": int(pending_amounts["total_outstanding"]),
            "total_unpaid_labor": int(pending_amounts["total_unpaid_labor"]),
            "total_pending": int(pending_amounts["total_pending"]),
            "total_committed": int(project_totals["total_committed"]),
            "effective_balance": int(project_totals["effective_balance"]),
            "total_pending_purchases": int(
                pending_amounts["total_pending_purchases_with_contingency"]
            ),
            "total_not_yet_paid": int(project_totals["total_not_yet_paid"]),
            "total_project_cost": int(project_totals["total_project_cost"]),
            "additional_funds_needed": int(project_totals["additional_funds_needed"]),
        },
        "category_summary": category_summary.to_dict("records"),
        "daily_expenses": df.to_dict("records"),
        "outstanding_balances": outstanding_balances,
        "unpaid_expenses": pending_amounts["unpaid_expenses"],
        "pending_purchases": pending_amounts["pending_purchases_with_contingency"],
        "last_updated": "24/09/2025 12:00:00",
    }

    # Save data for HTML dashboard
    with open(output_path, "w") as f:
        json.dump(dashboard_data, f, indent=2)

    return len(df)
