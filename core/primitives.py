from datetime import timedelta
from re import search, UNICODE
from django.utils.timezone import now


class PrimitiveComputer:
    def compute(self, key):
        match = search('(?P<primitive>\w*(?=\(.*\)))', key, UNICODE)
        if not match:
            return key

        primitive_label = match.group('primitive')
        primitive = PRIMITIVES.get(primitive_label)
        expression = key.replace(primitive_label, primitive)

        return eval(expression)


def previous_month():
    today = now().date()

    month = today.month

    if month != 1:
        return month - 1

    return 12


def previous_month_year():
    today = now().date()

    month = today.month

    if month != 1:
        return today.year

    return today.year - 1


def today(days=0, fmt="%d/%m/%Y"):
    today = now().date()

    if days != 0:
        today = today + timedelta(days=days)

    return today.strftime(fmt)


PRIMITIVES = {u'mes_anterior': 'previous_month', u'a\xf1o_mes_anterior': 'previous_month_year', u'hoy': 'today'}
