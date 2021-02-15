import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        if date is None:
            td = dt.datetime.now()
            self.date = td.date()
        else:
            date_format = '%d.%m.%Y'
            moment = dt.datetime.strptime(date, date_format)
            self.date = moment.date()
        self.comment = comment


class Calculator:
    TD = dt.datetime.now()

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)
        return self.records

    def get_today_stats(self):
        count_1 = 0
        for record in self.records:
            if record.date == self.TD.date():
                count_1 += record.amount
        return count_1

    def get_week_stats(self):
        lastweek = []
        for i in range(7):
            lastweek.append(self.TD.date() - dt.timedelta(days=i))
        count_2 = 0
        for record in self.records:
            if record.date in lastweek:
                count_2 += record.amount
        return count_2


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        remainder = self.limit - self.get_today_stats()
        if remainder > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {remainder} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def get_today_cash_remained(self, currency):
        currency_dt = {'rub': 'руб', 'usd': 'USD', 'eur': 'Euro'}
        currency_rate = {'rub': 1, 'usd': self.USD_RATE, 'eur': self.EURO_RATE}
        remainder = self.limit - self.get_today_stats()
        if remainder > 0:
            left = round((remainder / currency_rate[currency]), 2)
            return f'На сегодня осталось {left} {currency_dt[currency]}'
        elif remainder == 0:
            return 'Денег нет, держись'
        else:
            left = round((-remainder / currency_rate[currency]), 2)
            return (f'Денег нет, держись: твой долг - '
                    f'{left} {currency_dt[currency]}')
