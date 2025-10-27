"""Outstanding balances and pending purchases data."""


def get_outstanding_balances():
    """
    Returns list of outstanding balances for specialist work.
    Each balance includes: vendor, description, amount, due_date
    """
    return [
        {
            "vendor": "Electrician",
            "description": "Remaining balance for electrical work (8000 of 28000, paid 10000 on 12/10)",
            "amount": 8000,
            "due_date": "To be scheduled",
        },
        {
            "vendor": "Plumber",
            "description": "Remaining balance for plumbing work (12000 of 27000)",
            "amount": 12000,
            "due_date": "To be scheduled",
        },
        {
            "vendor": "Window Supplier",
            "description": "Window work fully paid (13386 paid on 20/10)",
            "amount": 0,
            "due_date": "Completed",
        },
        {
            "vendor": "Painter",
            "description": "Painting work - 33000, paid 10000 on 23/10 + 7000 on 25/10 = 16000 remaining",
            "amount": 16000,
            "due_date": "To be scheduled",
        },
        {
            "vendor": "Cabinet Specialist",
            "description": "Original work paid (21300 total), additional cabinets added = 7500 remaining",
            "amount": 7500,
            "due_date": "To be scheduled",
        },
        {
            "vendor": "Tile Fixer",
            "description": "Fixing tiles - 30000, paid 14170 on 25/10 = 15830 remaining",
            "amount": 15830,
            "due_date": "To be scheduled",
        },
    ]


def get_pending_purchases():
    """
    Returns list of pending purchases not yet procured.
    Each purchase includes: category, description, amount
    Note: Contingency is calculated dynamically and added in calculations.py
    """
    return [
        {
            "category": "Plumbing & Fixtures",
            "description": "Toilets and mirrors",
            "amount": 25000,
        },
        {
            "category": "Paint",
            "description": "4 ltrs silk Lagoon",
            "amount": 3000,
        },
        {
            "category": "Paint",
            "description": "20 ltrs silk Ivory",
            "amount": 14700,
        },
        {
            "category": "Paint",
            "description": "4 ltrs silk grey",
            "amount": 3000,
        },
        {
            "category": "Paint - Outside",
            "description": "4 ltrs Aquatech white",
            "amount": 3200,
        },
        {
            "category": "Paint - Outside",
            "description": "4 ltrs gloss black",
            "amount": 1200,
        },
        {
            "category": "Paint - Outside",
            "description": "4 ltrs weatherguard ivory",
            "amount": 3200,
        },
        {
            "category": "Paint - Outside",
            "description": "6 @ 4 ltrs weatherguard silicone @ 3200 each",
            "amount": 19200,
        },
        {
            "category": "Construction Work",
            "description": "Veranda works and other pending concrete work",
            "amount": 30000,
        },
    ]
