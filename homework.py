import datetime as dt


class Calculator:
    def __init__(self, limit: int):
        self.limit = limit
        self.records = []

    def add_record(self, recordObj):
        self.records.append(recordObj)

    def get_today_stats(self):
        dateTmp = dt.datetime.today().date()
        summDay = 0
        for row in self.records:
            if row.date == dateTmp:
                summDay = summDay+row.amount
        return int(summDay)

    def get_week_stats(self):
        dateTmpEnd = dt.datetime.today().date()
        dateTmpBegin = dateTmpEnd-dt.timedelta(days=7)
        summDay = 0
        for row in self.records:
            if row.date > dateTmpBegin and row.date <= dateTmpEnd:
                summDay = summDay+row.amount
        return int(summDay)


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        balans = self.limit - self.get_today_stats()
        if balans < self.limit and balans >= 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {balans} кКал'
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 72.3
    EURO_RATE = 79.2

    def get_today_cash_remained(self, currency):
        balans = self.limit-self.get_today_stats()
        if currency == 'rub':
            balans = balans
            currencyName = 'руб'
        elif currency == 'usd':
            balans = round(balans / self.USD_RATE, 2)
            currencyName = 'USD'
        elif currency == 'eur':
            balans = round(balans / self.EURO_RATE, 2)
            currencyName = 'Euro'

        if balans > 0:
            result = f'На сегодня осталось {balans} {currencyName}'
        elif balans == 0:
            result = 'Денег нет, держись'
        else:
            balans = abs(balans)
            result = f'Денег нет, держись: твой долг - {balans} {currencyName}'

        return result


class Record:
    def __init__(self, amount: int, comment: str, date=None):
        self.amount = amount
        self.comment = comment
        try:
            date = dt.datetime.strptime(str(date), '%d.%m.%Y').date()
        except:
            date = dt.datetime.now().date()
        self.date = date
