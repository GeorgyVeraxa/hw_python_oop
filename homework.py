import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        if date is None:
            td = dt.datetime.now()
        else:
            date_format = '%d.%m.%Y'
            td = dt.datetime.strptime(date, date_format)
        self.date = td.date()
        self.comment = comment


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)
        return self.records

    def get_today_stats(self):
        td = dt.datetime.now()
        return (sum([record.amount for record in self.records
                     if record.date == td.date()]))

    def get_week_stats(self):
        td = dt.datetime.now()
        week_beg = td - dt.timedelta(days=7)
        return (sum([record.amount for record in self.records
                     if week_beg.date() < record.date <= td.date()]))

    def today_remained(self):
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        if self.today_remained() > 0:
            today_remained = self.today_remained()
            return ('Сегодня можно съесть что-нибудь ещё, но с общей'
                    f' калорийностью не более {today_remained} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def get_today_cash_remained(self, currency):
        currency_dict = {'rub': ('руб', 1),
                         'usd': ('USD', self.USD_RATE),
                         'eur': ('Euro', self.EURO_RATE)}
        left = round((self.today_remained() / currency_dict[currency][1]), 2)
        currency_label = currency_dict[currency][0]
        if self.today_remained() > 0:
            return f'На сегодня осталось {left} {currency_label}'
        elif self.today_remained() == 0:
            return 'Денег нет, держись'
        else:
            left_minus = abs(left)
            return ('Денег нет, держись: твой долг - '
                    f'{left_minus} {currency_label}')
