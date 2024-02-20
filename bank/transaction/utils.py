from .models import Commission


def calc_commission(transfer_kind: str, amount: float):
    """
    It returns the calculated commission of a transaction/payment.
    All the comissions are saved in database.
    """
    amount = float(amount)
    comition_rate = Commission.objects.get(kind=transfer_kind)
    if amount < 50:
        comition = amount * (float(comition_rate.range1) / 100)
    if 50 <= amount < 500:
        comition = amount * (float(comition_rate.range2) / 100)
    if amount >= 500:
        comition = amount * (float(comition_rate.range3) / 100)
    return comition
