import datetime as dt
from random import randint


def _value() -> str:
    value = "{}.{}".format(
        "".join((str(randint(0, 9)) for v in range(3))),
        "".join((str(randint(0, 9)) for v in range(2))),
    )

    return f"{float(value):,.2f}"


def _ref() -> str:
    return "{}-00{}".format(
        "".join((str(randint(0, 9)) for v in range(9))), str(randint(0, 3))
    )


def _vencimento() -> str:
    if randint(0, 1):
        return (dt.datetime.today() - dt.timedelta(randint(1, 30))).strftime("%d/%m/%y")

    return (dt.datetime.today() + dt.timedelta(randint(1, 30))).strftime("%d/%m/%y")


def _item() -> str:

    return str(randint(1, 3))


def create_debit(quant: int):
    debits = []

    for i in range(quant):
        debits.append(
            {
                "ref": _ref(),
                "value": _value(),
                "vencimento": _vencimento(),
                "item": _item(),
            }
        )

    return debits


def convert_money(value: str | float):
    if isinstance(value, str):
        value = float(value)

    return f"{value:,.2f}".replace(".", "b").replace(",", ".").replace("b", ",")
