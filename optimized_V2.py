import csv
import numpy as np
import os.path
import pandas as pd
import time

MAX_AMOUNT = 500

class Process_CSV:
    @staticmethod
    def get_csv():
        """Checks whether the file exists at the given address. If so, returns it."""
        csv_file = ""
        exists = os.path.exists(csv_file)

        while exists == False:
            csv_file = input("Veuillez entrer le nom du fichier à analyser, suffixe inclus.\n")
            exists = os.path.exists(csv_file)
            if exists == False:
                print(Utilities.open_error)
            else:
                return csv_file

    @staticmethod
    def fetch_data(file):
        data = pd.read_csv(file, index_col='name')
        data.drop_duplicates(inplace=True)
        data.rename(columns={'profit': 'interest'}, inplace=True)
        data = data[(data['price'] > 0) & (data['interest'] > 0)]
        data['profit'] = Process_CSV.profit(data['price'], data['interest'])
        data['price'] = data['price'].apply(lambda x: int(x*10))
        return data

    @staticmethod
    def profit(amount, interest):
        """Calculates the amount earned by buying one action."""
        mult = interest/100
        profit = round(amount*mult, 2)

        return profit

class Algorithm:
    def __init__(self, actions, max_price=0, nb_actions=0, table=[]):
        self.actions = actions
        self.max_price = MAX_AMOUNT*10
        self.nb_actions = len(actions.axes[0])
        self.table = self.generate_table()

    def generate_table(self):
        table = np.zeros(shape=(self.nb_actions+1, self.max_price+1))

        return table

    def optimized_algorithm(self):
        cost = self.table
        amount = self.nb_actions
        max_price = self.max_price
        prices = self.actions['price'].to_numpy()
        profit = self.actions['profit'].to_numpy()
        prices = np.insert(prices, 0, 0)
        profit = np.insert(profit, 0, 0)

        for i in range(1, amount+1):
            for j in range(1, max_price+1):
                if (prices[i] > j):
                    cost[i][j] = cost[i-1][j]
                else:
                    if ((profit[i] + cost[i-1][j-prices[i]]) > cost[i-1][j]):
                        cost[i][j] = profit[i] + cost[i-1][j-prices[i]]
                    else:
                        cost[i][j] = cost[i-1][j]

#        return cost[amount][max_price]

    def items_in_optimal(self):
        cost = self.table
        i = self.nb_actions
        j = self.max_price
        prices = self.actions['price'].to_numpy()
        prices = np.insert(prices, 0, 0)
        index_items = []

        while (i > 0 and j > 0):
            if(cost[i][j] != cost[i-1][j]):
                index_items.append(i-1)
                j = j-prices[i]
                i = i-1
            else:
                i = i-1

        return index_items

    @staticmethod
    def sum_total(column, column_two):
        return column + column_two

class Utilities:
    open_error = """A problem occured. Please check the following:
-  If different from the script's folder, there is no mistake in the file's path;
-  You included the file's suffix (.xls, .ods, etc.);
-  No typo in the file's name."""

    @staticmethod
    def start_process():
        start = time.time()

        csv_file = Process_CSV.get_csv()
        data = Process_CSV.fetch_data(csv_file)

        print("Starting process...")
        max_price = MAX_AMOUNT*10
        answer = Algorithm(data)
        answer.optimized_algorithm()
        index_results = answer.items_in_optimal()

        Utilities.print_results(index_results, answer.actions)
        duration = time.time() - start
        print(f"This entire process has taken {round(duration, 2)} second.")

    @staticmethod
    def print_results(index_items, actions):
        results = actions.iloc[index_items]
        results['price'] = results['price'].apply(lambda x: float(x)/10)

        print("The most advantageous combination is the following:\n")
        print(results)
        print(f"\nThe final profit of this combination is {round(results['profit'].sum(), 2)} euros, for a total cost of {round(results['price'].sum(), 2)} euros.")

Utilities.start_process()
