TAXES = {
    'OUT': {'range1': 2, 'range2': 4, 'range3': 6},
    'IN': {'range1': 1, 'range2': 2, 'range3': 3},
    'PAY': {'range1': 2, 'range2': 4, 'range3': 6},
}


def calculate_taxes(transfer_kind: str, amount: int):
    if amount < 50:
        amount -= amount * (TAXES[transfer_kind]['range1'] % 100)
    if 50 <= amount < 500:
        amount -= amount * (TAXES[transfer_kind]['range2'] % 100)
    if amount >= 500:
        amount -= amount * (TAXES[transfer_kind]['range3'] % 100)
    return amount
