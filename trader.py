from random import uniform
import json
from argparse import ArgumentParser


# setting up CLI (Command Line Interface)
args = ArgumentParser()
args.add_argument('arg_1', type=str)
args.add_argument("arg_2", nargs='?')
args = vars(args.parse_args())

# set up for directory config
config_location = "config.json"
state_location = "state.json"


def read_config():
    with open(config_location, 'r') as file:
        return json.load(file)


def read_state():
    with open(state_location, 'r') as file:
        return json.load(file)


def get_available():
    print(f'AVAILABLE BALANCE: {round(read_state()["UAH"], 2)} UAH; {round(read_state()["USD"], 2)} USD')
    pass


def restart():
    with open(state_location, 'w') as f:
        json.dump({"rate": "", "UAH": "", "USD": ""}, f)


def _create_state_file():
    if read_state()["rate"] != "":
        pass
    else:
        restart()


error_negative_value = 'The input should be larger then 0'


class Person:
    def __init__(self):
        if read_state()["UAH"] == "":
            self.uah_balance = read_config()["UAH"]
        else:
            self.uah_balance = read_state()["UAH"]
        if read_state()["USD"] == "":
            self.usd_balance = read_config()["USD"]
        else:
            self.usd_balance = read_state()["USD"]
        _create_state_file()

    def _state_update(self, current_rate):
        with open(state_location, 'w') as f:
            json.dump({"rate": current_rate, "UAH": self.uah_balance, "USD": self.usd_balance}, f)
        pass

    def get_next(self):
        current_rate = read_config()["rate"] + round(uniform(- read_config()["delta"], read_config()["delta"]), 2)
        self._state_update(current_rate)
        return current_rate

    def get_rate(self):
        if read_state()["rate"] != "":
            return read_state()["rate"]
        else:
            return self.get_next()

    def buy_usd(self, usd):
        if usd <= 0:
            print(error_negative_value)
        elif usd > (self.uah_balance / self.get_rate()):
            print(f"UNAVAILABLE, REQUIRED BALANCE {round((usd * self.get_rate()), 2)} UAH, \
AVAILABLE {self.uah_balance} UAH")
        else:
            self.usd_balance += usd
            self.uah_balance -= usd * self.get_rate()
            print(f'TRANSACTION COMPLETED. {round((usd * self.get_rate()), 2)} UAH EXCHANGED TO {round(usd, 2)} USD')
            self._state_update(self.get_rate())

    def sell_usd(self, usd):
        if usd <= 0:
            print(error_negative_value)
        elif usd > self.usd_balance:
            print(f"UNAVAILABLE, REQUIRED BALANCE {usd} UAH, AVAILABLE {self.usd_balance}")
        else:
            self.uah_balance += usd * self.get_rate()
            self.usd_balance -= usd
            print(f'TRANSACTION COMPLETED: {usd} USD EXCHANGED TO {round((usd * self.get_rate()), 2)} UAH')
            self._state_update(self.get_rate())

    def sell_usd_all(self):
        print(f'TRANSACTION COMPLETED: {round(self.usd_balance, 2)} USD EXCHANGED TO \
{round((self.usd_balance * self.get_rate()), 2)} UAH')
        self.uah_balance += self.usd_balance * self.get_rate()
        self.usd_balance = 0
        self._state_update(self.get_rate())

    def buy_usd_all(self):
        print(f'TRANSACTION COMPLETED: {round(self.uah_balance, 2)} UAH EXCHANGED TO\
{round((self.uah_balance / self.get_rate()), 2)} USD')
        self.usd_balance += self.uah_balance / self.get_rate()
        self.uah_balance = 0
        self._state_update(self.get_rate())


# setting up arguments in CLI
user = Person()

if args['arg_1'] == 'RATE':
    print(user.get_rate())
elif args['arg_1'] == 'NEXT':
    print(user.get_next())
elif args['arg_1'] == 'AVAILABLE':
    get_available()
elif args['arg_1'] == 'BUY' and args['arg_2'] == 'ALL':
    user.buy_usd_all()
elif args['arg_1'] == 'SELL' and args['arg_2'] == 'ALL':
    user.sell_usd_all()
elif args['arg_1'] == 'BUY':
    user.buy_usd(float(args['arg_2']))
elif args['arg_1'] == 'SELL':
    user.sell_usd(float(args['arg_2']))
elif args['arg_1'] == 'RESTART':
    restart()
