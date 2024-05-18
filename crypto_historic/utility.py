import os
from os import path
import time
import datetime
# import numpy as np
# from matplotlib import pyplot as plt


def unix_ts_now(milli=True):
    """
    Get UNIX now in the Binance API format
    """
    if milli:
        return int(time.time() * 1000)
    else:
        return int(time.time())


def unix_ts(
    year="2023", month="01", day="01", hour="00", minute="00", second="00", milli=True
):
    """
    Get UNIX for anytime
    """
    txt1 = "{year}-{month}-{day} {hour}:{minute}:{second}".format(
        year=year, month=month, day=day, hour=hour, minute=minute, second=second
    )
    if milli:
        return int(
            time.mktime(
                datetime.datetime.strptime(txt1, "%Y-%m-%d %H:%M:%S").timetuple()
            )
            * 1000
        )
    else:
        return int(
            time.mktime(
                datetime.datetime.strptime(txt1, "%Y-%m-%d %H:%M:%S").timetuple()
            )
        )


def unix_ts_from_string(date, milli=True):
    """
    Get UNIX from a string
    """
    if milli:
        return int(
            time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple()) * 1000
        )
    else:
        return int(
            time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())
        )


def unix_ts_to_date(unix, milli=True):
    """
    Get a date from a UNIX timestamp
    """
    if milli:
        return datetime.datetime.fromtimestamp(unix / 1000).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    else:
        return datetime.datetime.fromtimestamp(unix).strftime("%Y-%m-%d %H:%M:%S")


def unix_relative_now(unix):
    """
    Get the relative time from now
    """
    return str(round((unix_ts_now() - unix) / 3600000, 1)) + " hours ago"


def parent_dir():
    """
    Get the parent folder of the proj
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    return parent_dir
    # return path.dirname(path.dirname(__file__))


def simple_bernouli(
    daily_trades=20,
    n_trades=550,
    transaction_cost=0.01,
    avg_loss=0.08,
    avg_profit=0.08,
    p_success=0.58,
    trade_size=100,
    experiments=1000,
):
    profit_experiments = []
    for i in range(experiments):
        # Simulate the trading outcomes
        trades = np.random.binomial(n=1, p=p_success, size=n_trades)
        profits = np.where(
            trades == 1,
            -transaction_cost * trade_size + trade_size * avg_profit,
            -transaction_cost * trade_size - avg_loss * trade_size,
        )

        # Calculate the total profit or loss
        total_profit = np.sum(profits)
        profit_experiments.append(total_profit)
        # Calculate the Sharpe ratio
        sharpe_ratio = np.sqrt(n_trades) * np.mean(profits) / np.std(profits)

        # Print the results
        # print(f"Total profit: {total_profit}")
        # print(f"Sharpe ratio: {sharpe_ratio:.2f}")
    profit_experiments = np.array(profit_experiments)
    print("Total profit %: {:.2f}".format(np.mean(profit_experiments) / trade_size))
    DailyProf = (np.mean(profit_experiments) / trade_size) / (n_trades / daily_trades)
    print(f"Daily profit %: {DailyProf}")
    # draw histogram
    plt.hist(profit_experiments, bins=100)
    plt.show()

    #
    # monthly trades
    monthly_profit = (1 + DailyProf) ** 20 - 1
    print("Monthly profit %: {:.2f}".format(monthly_profit))
    print(
        "Average Revenue per month: {:.2f} with {:.2f} trade size".format(
            monthly_profit * trade_size - trade_size, trade_size
        )
    )


def bernouli_with_changing_portfoweight(
    daily_trades=20,
    n_trades=550,
    transaction_cost=0.01,
    avg_loss=0.08,
    avg_profit=0.08,
    p_success=0.58,
    trade_size=100,
    experiments=1000,
    portfo=100,
    correctionAfterLose=0.5,
    correctionAfterWin=1.5,
):
    profit_experiments = []
    for i in range(experiments):
        portfolio_value = portfo

        # Initialize the trade sizes and profits
        trade_sizes = np.zeros(n_trades)
        profits = np.zeros(n_trades)
        # Loop over each trade
        for i in range(n_trades):
            # Calculate the trade size based on the current portfolio value and Kelly fraction
            trade_size = 0.1 * portfolio_value

            # Adjust the trade size based on the success or failure of the last trade
            if i > 0:
                if profits[i - 1] > 0:
                    trade_size *= correctionAfterWin  # Increase trade size by 50% after a winning trade
                else:
                    trade_size *= correctionAfterLose  # Decrease trade size by 50% after a losing trade

            # Make the trade and calculate the profit or loss
            trades = np.random.binomial(n=1, p=p_success, size=n_trades)
            trade_profit = np.where(
                trades == 1,
                -transaction_cost * trade_size + trade_size * avg_profit,
                -transaction_cost * trade_size - avg_loss * trade_size,
            )

            portfolio_value += trade_profit[0]  # Update the portfolio value

            # Save the trade size and profit
            trade_sizes[i] = trade_size
            profits[i] = trade_profit[0]
        total_profit = np.sum(profits)
        sharpe_ratio = np.sqrt(n_trades) * np.mean(profits) / np.std(profits)
        profit_experiments.append(total_profit)

    # histogram of the profit_experiments
    plt.hist(profit_experiments, bins=100)
    plt.show()
    profit_experiments = np.array(profit_experiments)
    print("Total profit %: {:.2f}".format(np.mean(profit_experiments) / trade_size))
    DailyProf = (np.mean(profit_experiments) / portfolio_value) / (
        n_trades / daily_trades
    )
    print(f"Daily profit %: {DailyProf}")
    # monthly trades
    monthly_profit = (1 + DailyProf) ** 20 - 1
    print("Monthly profit %: {:.2f}".format(monthly_profit))
    print(
        "Average Revenue per month: {:.2f} with {:.2f} trade size".format(
            monthly_profit * trade_size - trade_size, trade_size
        )
    )


def inverse_pct_change(np_array, first_value):
    t = np.empty(len(np_array) + 1)
    t[0] = first_value
    for i in range(1, len(np_array)):
        t[i] = t[i - 1] * (1 + np_array[i])
    return t[1:]


def product_changes(arr):
    p=1
    for i in arr:
        p*=(i+1)
    return p
def get_prediction(lag,target,arr):
    multiplier=product_changes(arr[:lag].reshape(-1,1))
    return (multiplier*target)[0]
