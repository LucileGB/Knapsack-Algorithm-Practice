import csv
import itertools
import os.path
import time

MAX_AMOUNT = 500


def brute_force():
    csv_file = Process_CSV.get_csv()
    start = time.time()
    data = Process_CSV.fetch_data(csv_file)
    print("Starting process...")
    combinations = Data_handling.combination_brute(data)
    best_combination = Data_handling.best_profit(combinations)
    Utilities.print_results(best_combination)
    duration = time.time() - start
    print(f"This entire process has taken {round(duration, 2)} second.")


class Process_CSV:
    @staticmethod
    def get_csv():
        """Checks whether the file exists at the given address. If so, returns it."""
        csv_file = ""
        exists = os.path.exists(csv_file)

        while exists == False:
            csv_file = input("Please enter the name of the file to analyse, suffix included.\n")
            exists = os.path.exists(csv_file)
            if exists is False:
                print(Utilities.open_error)
            else:
                return csv_file

    @staticmethod
    def fetch_data(file):
        """Check whether a row contains the three informations we need (name, price, interests),
        then add it to the result list and return it."""
        data = []
        with open(file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=["name", "cost", "interests"])
            for row in reader:
                complete = True
                for value in row.values():
                    if not value:
                        complete = False
                        break
                    else:
                        try:
                            is_valid = (float(value))
                            if is_valid <= 0:
                                complete = False
                                break
                        except Exception as e:
                            continue
                if complete:
                    try:
                        Process_CSV.process_row(row)
                    except Exception as e:
                        continue
                    data.append(row)

        return data

    @staticmethod
    def process_row(dict_row):
        """Transform the relevant dictionary fields into floats"""
        dict_row["cost"] = float(dict_row["cost"])
        dict_row["interests"] = float(dict_row["interests"])


class Data_handling:
    @staticmethod
    def combination_brute(actions):
        combinations_list = itertools.permutations(actions)
        to_sort = []
        for combination in combinations_list:
            under_max = Data_handling.keep_below(combination, MAX_AMOUNT)
            if len(under_max) > 0:
                formatted = Data_handling.format_actions(under_max)
                to_sort.append(formatted)

        return to_sort

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
        profit = round(amount*mult, 2)
        return profit

    @staticmethod
    def keep_below(data_list, maximum):
        """Take a list of action and returns only values whose sum is below MAX_AMOUNT"""
        sum_list = 0
        new_list = []
        length = len(data_list)
        for element in data_list:
            if sum_list <= maximum:
                if sum_list == maximum:
                    return new_list
                new_list.append(element)
                sum_list += element["cost"]
                if len(new_list) == length:
                    return new_list
            else:
                return new_list[:-1]

    @staticmethod
    def best_profit(combinaisons):
        result = list(reversed(sorted(combinaisons, key=lambda item: item["final_worth"])))

        return result[0]

    @staticmethod
    def total_earned(combination):
        """Updates each combination dictionary with its final worth."""
        total = 0
        for dictionary in combination["actions"]:
            total = total + dictionary["interests"]
        combination.update({"final_worth": total})

    @staticmethod
    def format_actions(actions_dict):
        Data_handling.add_profit(actions_dict)
        result = {}
        result.update({"actions": actions_dict})
        result.update({"final_worth": sum(int(dic["profit"]) for dic in actions_dict)})

        return result


class Utilities:
    open_error = """A problem occured. Please check the following:
-  If different the file isn't in the script's folder, there is no mistake in the file's path;
-  You included the file's suffix (.xls, .ods, etc.);
-  No typo in the file's name."""

    @staticmethod
    def print_results(result_dict):
        total_cost = sum(int(dic["cost"]) for dic in result_dict["actions"])
        print("The best combination is the following:")
        for action in result_dict["actions"]:
            print(f"{action['name']}, for {action['cost']};")
        print(f"The final profit of this combination is {round(result_dict['final_worth'], 2)} euros, for a total cost of {total_cost} euros.")


brute_force()
