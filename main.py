import csv
import os.path
import time

MAX_AMOUNT = 500


def brute_force():
    start = time.time()
    csv_file = Process_CSV.get_csv()
    data = Process_CSV.fetch_data(csv_file)
    brute_result = Data_handling.combination_brute(data, MAX_AMOUNT)
    sorted_result = Data_handling.sort_profit(brute_result)

    print("The most advantageous combination is the following :")
    Utilities.print_results(sorted_result[0])
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
                print(Utilies.open_error)
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

        #We return the data while skipping the header line.
        return data[1:]

    @staticmethod
    def process_row(dict_row):
        """Transform the relevant dictionary fields into floats"""
        dict_row["cost"] = float(dict_row["cost"])
        dict_row["interests"] = float(dict_row["interests"])

class Data_handling:
    @staticmethod
    def combination_brute(data, max_amount):
        """Trying all possible combinations under the max_amount value."""
        result = []
        i = 0
        for num in data:
            combination = [num]
            total = [num["cost"]]

            for other_num in data:
                if sum(total) < max_amount and data.index(num) != data.index(other_num) :
                    combination.append(other_num)
                    total.append(other_num["cost"])

            if sum(total) > max_amount:
                combination = combination[:-1]
            result.append({"actions":combination})
            i += 1

        return result

    @staticmethod
    def final_amount(amount, rate):
        """Calculates the final amount earned by buying one action."""
        mult = rate/100
        interests = amount*mult
        total = amount + interests
        return total

    @staticmethod
    def add_interests(dict_list):
        """Adds an interest field to each 'action' dictionary."""
        for dictionary in dict_list:
            interests = Data_handling.final_amount(dictionary["cost"], dictionary["interests"])
            dictionary.update({"interests": interests})

    @staticmethod
    def total_earned(combination):
        """Updates each combination dictionary with its final worth."""
        total = 0
        for dictionary in combination["actions"]:
            total = total + dictionary["interests"]
        combination.update({"final_worth": total})

    @staticmethod
    def sort_profit(data):
        """Update each combination with its results, then sort them by profit."""
        for combination in data:
            Data_handling.add_interests(combination["actions"])
            Data_handling.total_earned(combination)

        return sorted(data, key=lambda item: item["final_worth"])

class Utilities:
    open_error = """Une erreur est survenue. Veuillez vérifier les points suivants :
-  Le chemin d'accès est bien conforme ;
-  Le nom du fichier se termine bien par le suffixe approprivé (.xls, .ods, etc.) ;
-  Aucune faute de frappe dans le nom du fichier."""

    @staticmethod
    def print_results(result_dict):
        names_list = []
        for action in result_dict["actions"]:
            names_list.append(action["name"])
        for name in names_list:
            print(name)
        print(f"\nThe final worth of this combination is {round(result_dict['final_worth'], 2)} euros.")

brute_force()
