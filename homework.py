import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record_object):
        self.records.append(record_object)

    def get_today_stats(self):
        today = dt.date.today()
        amounts = [
            record.amount
            for record in self.records
            if record.date == today
        ]
        return sum(amounts)

    def get_today_remained(self):
        balance = self.limit - self.get_today_stats()
        return balance

    def get_week_stats(self):
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)
        amounts = [
            record.amount
            for record in self.records
            if week_ago <= record.date <= today
        ]
        return sum(amounts)


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        today_remained = self.get_today_remained()
        if today_remained > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {today_remained} кКал'
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = float(72.3)
    EURO_RATE = float(79.2)
    RUB_RATE = float(1)

    def get_today_cash_remained(self, currency):
        balance = round(self.get_today_remained(), 4)
        if balance == 0:
            result = 'Денег нет, держись'
        else:
            currencies = {
                'eur': ('Euro', self.EURO_RATE),
                'usd': ('USD', self.USD_RATE),
                'rub': ('руб', self.RUB_RATE),
            }
            currency_name, currency_rate = currencies[currency]
            remained = round(balance/currency_rate, 2)
            if balance > 0:
                result = f'На сегодня осталось {remained} {currency_name}'
            elif balance < 0:
                remained = abs(round(balance/currency_rate, 2))
                result = f'Денег нет, держись: твой долг - {remained} {currency_name}'
        return result


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(str(date), '%d.%m.%Y').date()
        else:
            self.date = dt.date.today()
