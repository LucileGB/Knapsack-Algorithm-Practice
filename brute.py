import csv
import os.path
import time

MAX_AMOUNT = 500


def brute_force():
    start = time.time()

    csv_file = Process_CSV.get_csv()
    data = Process_CSV.fetch_data(csv_file)
    print(data)
    print("Starting process...")
    length = len(data)
    Data_handling.add_interests(data)
    brute = Data_handling()
    brute_result = brute.combination_brute(data, 0, length - 1)
#NOTE : to use if we print everything    sorted_result = Data_handling.sort_profit(brute_result)

    print("The most advantageous combination is the following :")
    Utilities.print_results(brute.best)
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
            if exists == False:
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

        return data

    @staticmethod
    def process_row(dict_row):
        """Transform the relevant dictionary fields into floats"""
        dict_row["cost"] = float(dict_row["cost"])
        dict_row["interests"] = float(dict_row["interests"])

class Data_handling:
    def __init__(self, best={"actions": [], "final_worth": 0}):
        self.best = best

    def combination_brute(self, data, start, end):
        """"Print permutations of a list. Takes three parameters:
        the list, the starting index, the ending index of the list."""
        if start == end:
            to_compare = {}
            to_compare.update({"actions": Data_handling.keep_below(data, MAX_AMOUNT)})
            Data_handling.total_earned(to_compare)
            if to_compare["final_worth"] > self.best["final_worth"]:
                self.best = to_compare

        else:
            for i in range(start, end + 1):
                data[start], data[i] = data[i], data[start]
                self.combination_brute(data, start + 1, end)
                data[start], data[i] = data[i], data[start]

    @staticmethod
    def add_interests(action):
        """Adds an interests field to each 'action' dictionary."""
        for dictionary in action:
            interests = Data_handling.interests(dictionary["cost"], dictionary["interests"])
            dictionary.update({"interests": interests})

    @staticmethod
    def interests(amount, rate):
        """Calculates the final amount earned by buying one action."""
        mult = rate/100
        interests = round(amount*mult, 2)
#        result = amount + interests
        return interests

    @staticmethod
    def keep_below(data_list, maximum):
        """Take a list of action and returns only values whose sum is below MAX_AMOUNT"""
        sum_list = 0
        new_list = []
        for element in data_list:
            if sum_list <= maximum:
                new_list.append(element)
                sum_list += element["cost"]
                if sum_list == maximum:
                    return new_list
            else:
                return new_list[:-1]

    @staticmethod
    def sort_profit(data):
        #NOTE : To use if we decide to show the result of each combination
        """Update each combination with its results, then sort them by profit."""
        for combination in data:
            Data_handling.add_interests(combination["actions"])
            Data_handling.total_earned(combination)

        return sorted(data, key=lambda item: item["final_worth"])

    @staticmethod
    def total_earned(combination):
        """Updates each combination dictionary with its final worth."""
        total = 0
        for dictionary in combination["actions"]:
            total = total + dictionary["interests"]
        combination.update({"final_worth": total})

class Utilities:
    open_error = """A problem occured. Please check the following:
-  If different from the script's folder, there is no mistake in the file's path;
-  You included the file's suffix (.xls, .ods, etc.);
-  No typo in the file's name."""
    @staticmethod
    def print_results(result_dict):
        names_list = []
        for action in result_dict["actions"]:
            names_list.append(action["name"])
        for name in names_list:
            print(name)
        print(f"\nThe final worth of this combination is {round(result_dict['final_worth'], 2)} euros.")

brute_force()
