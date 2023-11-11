# TAXES = {
#     'OUT': {'range1': 2, 'range2': 4, 'range3': 6},
#     'INC': {'range1': 1, 'range2': 2, 'range3': 3},
#     'PAY': {'range1': 2, 'range2': 4, 'range3': 6},
# }

# def calculate_taxes(transfer_kind: str, amount: float):
#     amount = float(amount)
#     if amount < 50:
#         taxe = amount * (TAXES[transfer_kind]['range1'] / 100)
#     if 50 <= amount < 500:
#         taxe = amount * (TAXES[transfer_kind]['range2'] / 100)
#     if amount >= 500:
#         taxe = amount * (TAXES[transfer_kind]['range3'] / 100)
#     return taxe

from .models import Commission

def calculate_taxes(transfer_kind: str, amount: float):
    amount = float(amount)
    comition_rate = Commission.objects.get(kind=transfer_kind)
    if amount < 50:
        comition = amount * (float(comition_rate.range1) / 100)
    if 50 <= amount < 500:
        comition = amount * (float(comition_rate.range2) / 100)
    if amount >= 500:
        comition = amount * (float(comition_rate.range3) / 100)
    return comition
