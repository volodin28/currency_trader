from random import uniform
import json

with open("config.json") as f:
    config_data = json.load(f)

error_negative_value = 'The input should be larger then 0'
rate = 36.00


def get_rate():
    current_rate = config_data["rate"] + round(uniform(- config_data["delta"], config_data["delta"]), 2)
    with open("state.py", 'w') as file:
        file.write('rate = ' + repr(current_rate) + '\n')
    return current_rate


class Person:
    def __init__(self, uah_balance, usd_balance):
        self.uah_balance = uah_balance
        self.usd_balance = usd_balance

    def get_available(self):
        return print(f'AVAILABLE BALANCE: {self.uah_balance} UAH; {self.usd_balance} USD')

    def sell_usd(self, usd):
        if usd <= 0:
            print(error_negative_value)
        elif usd > self.usd_balance:
            print(f"UNAVAILABLE, REQUIRED BALANCE {usd} UAH, AVAILABLE {self.usd_balance}")
        else:
            self.uah_balance += round((usd * rate), 2)
            self.usd_balance -= round(usd, 2)
            print(f'TRANSACTION COMPLETED: {usd} USD EXCHANGED TO {round((usd * rate), 2)} UAH')
            with open("state.py", 'a') as file:
                file.write('UAH = ' + repr(self.uah_balance) + '\n''USD = ' + repr(self.usd_balance) + '\n')
                # file.write('USD = ' + repr(self.usd_balance) + '\n')

    def sell_usd_all(self):
        print(f'TRANSACTION COMPLETED: {self.usd_balance} USD EXCHANGED TO {round((self.usd_balance * rate), 2)} UAH')
        self.uah_balance += round((self.usd_balance * rate), 2)
        self.usd_balance = 0

    def buy_usd_all(self):
        print(f'TRANSACTION COMPLETED: {self.uah_balance} UAH EXCHANGED TO {round((self.uah_balance / rate), 2)} USD')
        self.usd_balance += round((self.uah_balance / rate), 2)
        self.uah_balance = 0

    def buy_usd(self, usd):
        if usd <= 0:
            print(error_negative_value)
        elif usd > round(self.uah_balance / rate, 2):
            print(f"UNAVAILABLE, REQUIRED BALANCE {round((usd * rate), 2)} UAH, AVAILABLE {self.uah_balance} UAH")
        else:
            self.usd_balance += round(usd, 2)
            self.uah_balance -= round((usd * rate), 2)
            print(f'TRANSACTION COMPLETED. {round((usd * rate), 2)} UAH EXCHANGED TO {round(usd, 2)} USD')


slavik = Person(config_data["UAH"], config_data["USD"])
slavik.get_available()
get_rate()
slavik.buy_usd(200.00)
slavik.sell_usd(100)
# slavik.sell_usd_all()
# slavik.get_available()
# slavik.buy_usd_all()
# slavik.get_available()
# slavik.buy_usd(200.00)
# slavik.get_available()
# slavik.sell_usd(100)
# slavik.get_available()


# a = 10000
# b = 200.0005
#
# balance = a - round((b * rate), 2)
# print(round((b * rate), 2))
# print(balance)
