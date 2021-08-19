import csv
import os.path
import time

MAX_AMOUNT = 500


def optimized_algorithm():
    start = time.time()

    csv_file = Process_CSV.get_csv()
    data = Process_CSV.fetch_data(csv_file)

    print("Starting process...")
    length = len(data)
    max_price = MAX_AMOUNT*100
    optimize = Data_handling(max_price-1, length-1)
    optimize.add_profit(data)
    best = optimize.optimized_algorithm(data)
    components_best = optimize.items_in_optimal(data)

    Utilities.print_results(components_best, best)
    duration = time.time() - start
    print(f"This entire process has taken {round(duration, 2)} second.")


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
        """Check whether a row contains the three informations we need (name, price, interests),
        then add it to the result list and return it."""
        data = []
        i = 0

        with open(file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=["name", "cost", "interests"])
            for row in reader:
                complete = True
                for value in row.values():
                    #NOTE : is it a good way of dealing with it or should I print "bad" rows with an error message?
                    if not value:
                        complete = False
                        break
                    else:
                        try:
                            is_valid = (float(value))
                            if is_valid <= 0:
                                complete = False
                                break
                        except:
                            continue
                if complete:
                    try:
                        Process_CSV.process_row(row)
                    except:
                        continue
                    data.append(row)
# Allows control of sample size for test purposes
                if i == 15:
                    return data

        return data

    @staticmethod
    def process_row(dict_row):
        """Transform the relevant dictionary fields into integers or floats"""
        dict_row["cost"] = int(float(dict_row["cost"])*100)
        dict_row["interests"] = float(dict_row["interests"])

class Data_handling:
    def __init__(self, max_price, amount, table=None):
        self.max_price = max_price
        self.amount = amount
        self.table = self.generate_table()

    def generate_table(self):
#A ETE TIME
        start = time.time()
        """Generate the table we will use for our algorithm."""
        table = []
        max_price = self.max_price
        amount = self.amount

        for i in range(amount + 1):
            price_range = []
            for j in range(max_price + 1):
                price_range.append(0)
            table.append(price_range)
        end = time.time() - start
        print(end)
        return table

    def optimized_algorithm(self, actions):
# MESURE AUSSI
        cost = self.table
        max_price = self.max_price
        amount = self.amount
        for i in range(1, amount+1):
            for price in range(1, max_price+1):
                if (actions[i]["cost"] > price):
                    cost[i][price] = cost[i-1][price]

                else:
                    if ((actions[i]["profit"] + cost[i-1][price-actions[i]["cost"]]) > cost[i-1][price]):
                        cost[i][price] = actions[i]["profit"] + cost[i-1][price-actions[i]["cost"]]

                    else:
                        cost[i][price] = cost[i-1][price]

        return cost[amount][max_price]

    def items_in_optimal(self, actions):
        cost = self.table
        i = self.amount
        j = self.max_price
        items = []

        while (i > 0 and j > 0):
            if(cost[i][j] != cost[i-1][j]):
                items.append(actions[i])
                j = j-actions[i]["cost"]
                i = i-1
            else:
                i = i-1

        return items

    @staticmethod
    def add_profit(action):
        """Adds a profit field to each 'action' dictionary."""
        for dictionary in action:
            profit = Data_handling.profit(dictionary["cost"], dictionary["interests"])
            dictionary.update({"profit": profit})

    @staticmethod
    def profit(amount, interest):
        """Calculates the amount earned by buying one action."""
        mult = interest/100
        profit = int(round(amount*mult, 2))
#        result = amount + profit
        return profit



class Utilities:
    open_error = """A problem occured. Please check the following:
-  If different from the script's folder, there is no mistake in the file's path;
-  You included the file's suffix (.xls, .ods, etc.);
-  No typo in the file's name."""
    @staticmethod
    def print_results(result_dict, final_value):
        total_cost = sum(int(dic["cost"]) for dic in result_dict)

        print("The most advantageous combination is the following:\n")
        for action in result_dict:
            print(f"{action['name']}, bringing a profit of {round(float(action['profit'])/100, 2)} euros;")
        print(f"\nThe final profit of this combination is {float(final_value)/100} euros, for a total cost of {float(total_cost)/100} euros.")

optimized_algorithm()
