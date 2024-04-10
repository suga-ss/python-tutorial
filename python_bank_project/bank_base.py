##
# @file bank_base.py
# @version 1.0
# @author Shinichiro Suga
# @date 2024/04/09
# @brief Python tutorial.
# @details Learn about functions, class, and more.
# @warning Only the last line in the csv file must be blank.
#          If there are two or more blank lines, line breaks do not work properly when appending.
# @note -

from pathlib import Path
import os
import csv
import random

class BankBase:
    def __init__(self):
        # @var self.data_csv_file_path: csv file path.
        #                               Account number, name, date of birth, address, account balance, PIN.
        # @warning Only the last line in the csv file must be blank.
        #          If there are two or more blank lines, line breaks do not work properly when appending.
        self.data_csv_file_path = str(Path(os.path.abspath(__file__)).resolve().parent) + "/robo_bank_data.csv"
        self.csv_header_list = ["Account_No", "Name", "Birthday", "Address", "Deposit", "PIN"]
        self.csv_header_dict = self.make_csv_header_dict(self.csv_header_list)
        self.cus_identification_dict = self.make_1to1_dict(self.data_csv_file_path, self.csv_header_dict["Account_No"], self.csv_header_dict["Name"])
        self.cus_Pin_val_dict = self.make_1to1_dict(self.data_csv_file_path, self.csv_header_dict["Account_No"], self.csv_header_dict["PIN"])
        self.cus_check_dict = self.make_2to1_dict(self.data_csv_file_path, self.csv_header_dict["Name"], self.csv_header_dict["Birthday"], self.csv_header_dict["Address"])
        # print(self.csv_header_dict)
        # print(self.cus_identification_dict)
        # print(self.cus_Pin_val_dict)
        # print(self.cus_check_dict)
        self.csv_data_num: int = 6
        self.PIN_input_counter: int = 0
        self.PIN_allowable_error_num: int = 3
        self.do_transactions_flag = True
        self.PIN_length: int = 4
        self.PIN_incorrect_flag: bool = True

        self.account_num_set = self.make_account_No_set(self.data_csv_file_path, self.csv_header_dict["Account_No"])
        print(self.account_num_set)
        self.account_num_digit: int = 8

    def make_csv_header_dict(self, csv_header_list):
        csv_header_dict = dict()
        csv_header_dict.clear()
        for i, enum in enumerate(csv_header_list):
            csv_header_dict[enum] = i
        return csv_header_dict

    def make_1to1_dict(self, csv_file_path, dict_key, dict_value):
        made_dict = dict()
        made_dict.clear()
        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                made_dict[row[dict_key]] = row[dict_value]
        return made_dict
    
    def make_2to1_dict(self, csv_file_path, dict_key1, dict_key2, dict_value):
        made_dict = dict()
        made_dict.clear()
        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                made_dict[row[dict_key1] + row[dict_key2]] = row[dict_value]
        return made_dict

    def make_account_No_set(self, csv_file_path, dict_key):
        account_num_set = set()
        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                account_num_set.add(row[dict_key])
        return account_num_set

    def get_cus_data(self, csv_file_path, cus_acc_num):
        target_cus_row = []
        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if cus_acc_num in row:
                    target_cus_row = row
            if len(target_cus_row) != self.csv_data_num:
                print("================================")
                print("Possible system malfunction.")
                print("Call ABC Bank and let them know.")
                print("================================")
            return target_cus_row

    def show_transactions_list(self):
        print("==============================================")
        print("Please enter your preferred transaction number")
        print("1: Deposit")
        print("2: Withdraw")
        print("3: Display only Balance")
        print("4: Display Account data")
        print("5: Exit")
        print("==============================================")

    def deposit(self, balance):
        print("============================")
        print("Please enter deposit amount.")
        print("============================")
        amount = input().rstrip().split()
        amount = int(''.join(amount))
        balance = int(balance)
        if amount > 0:
            balance += amount
            balance = str(balance)
            print("===========================================")
            print("The amount after the deposit is ${balance}.".format(balance=balance))
            print("===========================================")
            return balance

    def withdraw(self, balance):
        print("=============================")
        print("Please enter withdraw amount.")
        print("=============================")
        amount = input().rstrip().split()
        amount = int(''.join(amount))
        balance = int(balance)
        if amount <= balance:
            balance -= amount
            balance = str(balance)
            print("===========================================")
            print("The amount after the withdraw is ${balance}.".format(balance=balance))
            print("===========================================")
            return balance
        else:
            print("===================")
            print("Insufficient funds.")
            print("===================")

    def display_account_data(self, cus_data, cus_name):
        print("Name : {cus_name}".format(cus_name=cus_name))
        print("Account No. : {cus_acc_num}.".format(cus_acc_num = cus_data[0]))
        print("Birthday : {cus_birth}".format(cus_birth = cus_data[2]))
        print("Address : {cus_add}".format(cus_add = cus_data[3]))
        print("Deposits : ${balance}".format(balance=cus_data[4]))
        print("PIN : {Pin}".format(Pin = cus_data[5]))

    def star_deposit_transactions(self, csv_file_path, cus_acc_num, cus_name):
        cus_data = self.get_cus_data(csv_file_path, cus_acc_num)
        while self.do_transactions_flag:
            self.show_transactions_list()
            transactions_num = int(input().strip())
            if transactions_num == 1:
                cus_data[4] = self.deposit(cus_data[4])
            elif transactions_num == 2:
                cus_data[4] = self.withdraw(cus_data[4])
            elif transactions_num == 3:
                print("=========================")
                print("Balance : ${balance}".format(balance=cus_data[4]))
                print("=========================")
            elif transactions_num == 4:
                print("================================")
                print("Display your Account data.")
                self.display_account_data(cus_data, cus_name)
                print("================================")
            elif transactions_num == 5:
                print("=====================================")
                print("Thank you!")
                print("We look forward to serving you again!")
                print("=====================================")
                self.do_transactions_flag = False
            else:
                print("=========================")
                print("Incorrect input detected.")
                print("=========================")
        # Update csv file.
        # @note coming soon!!!!!!!!!!!!!!
        finish_transactions_flag = True
        return finish_transactions_flag

    def generate_account_num(self, digit):
        first_chr = random.choice("123456789")
        remaining_chr = ''.join([random.choice("0123456789") for i in range(digit-1) ])
        return first_chr+remaining_chr

    def make_new_account(self, csv_file_path, cus_name, cus_birth, cus_add, Pin):
        initial_balance = 0
        invalid_account_num_flag = True
        while invalid_account_num_flag:
            account_num = self.generate_account_num(self.account_num_digit)
            if account_num not in self.account_num_set:
                invalid_account_num_flag = False
        with open(csv_file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([account_num, cus_name, cus_birth, cus_add, initial_balance, Pin])
        return [account_num, cus_name, cus_birth, cus_add, initial_balance, Pin]

    def main(self):
        print("===================================================")
        print("               Welcom to ROBO Bank!!               ")
        print("Please enter 1 for deposit transactions.")
        print("Please enter 2 if you wish to open a new account.")
        print("Please enter 3 if you want to close the transaction")
        print("===================================================")
        customer_needs = int(input().strip())
        print("==> I confirm that {customer_needs} has been entered.".format(customer_needs=customer_needs))
        if customer_needs == 1:
            print("================================================================")
            print("Please enter your name and bank account number.")
            print("@warning : Put a comma between name and account number.")
            print("           And the first letter of the name must be capitalized.")
            print("           ex) Albert Einstein, 31415926")
            print("================================================================")
            cus_name, cus_acc_num = map(str, input().rstrip().split(","))
            low_cus_name = cus_name.strip().replace(' ','').lower()
            cus_acc_num = cus_acc_num.strip().replace(' ','')
            if (cus_acc_num, low_cus_name) in self.cus_identification_dict.items():
                print("==================================================================")
                print("Bank account No.{cus_acc_num}, Dear {cus_name}.".format(cus_acc_num=cus_acc_num, cus_name=cus_name))
                print("Please enter your 4-digit PIN")
                print("==================================================================")
                Pin = input().rstrip().split()
                Pin = ''.join(Pin)
                while self.PIN_input_counter <= self.PIN_allowable_error_num:
                    if (cus_acc_num, Pin) in self.cus_Pin_val_dict.items():
                        if self.star_deposit_transactions(self.data_csv_file_path, cus_acc_num, cus_name): return
                    else:
                        self.PIN_input_counter += 1
                        rest_input_times = self.PIN_allowable_error_num - self.PIN_input_counter
                        print("==========================================================")
                        print("PIN is different.")
                        print(" Please enter the correct PIN again.")
                        print(" Enter the number of times that the PIN can input is {rest_input_times}.".format(rest_input_times=rest_input_times))
                        print("==========================================================")
                        Pin = input().rstrip().split()
                        Pin = ''.join(Pin)
                    if (self.PIN_input_counter >= self.PIN_allowable_error_num):
                        print("================================================================")
                        print("The allowable number of PIN incorrect entries has been exceeded.")
                        print("Please start the transaction again from the beginning.")
                        print("================================================================")
                        return
            elif cus_acc_num not in self.cus_identification_dict.keys() and low_cus_name not in self.cus_identification_dict.values():
                print("===========================================")
                print("The account number and name does not exist.")
                print("Please open a new account at ABC Bank.")
                print("===========================================")
                return
            elif cus_acc_num not in self.cus_identification_dict.keys():
                print("==================================")
                print("The account number does not exist.")
                print("==================================")
                return
            elif low_cus_name not in self.cus_identification_dict.values():
                print("================================")
                print("The account name does not exist.")
                print("================================")
                return
        elif customer_needs == 2:
            print("=================================================================")
            print("Thank you for choosing Robo Bank from among many banks.")
            print("Proceed with the account opening procedure.")
            print("Please enter your name, birthday and address.")
            print("@warning : Please follow the format below to enter your birthday.")
            print("           format : yyyymmdd   ex) 20000101")
            print("@warning : Please Put a comma between each item.")
            print("ex) Albert Einstein, 18790314, Germany")
            print("=================================================================")
            cus_name, cus_birth, cus_add = map(str, input().rstrip().split(","))
            lower_cus_name = cus_name.strip().replace(' ','').lower()
            cus_birth = cus_birth.strip().replace(' ','')
            cus_add = cus_add.strip().replace(' ','')
            cus_name_birth_str = lower_cus_name + cus_birth
            if (cus_name_birth_str, cus_add) not in self.cus_check_dict.items():
                print("=============================================================")
                print("Checked against customer data and confirmed no account No.")
                print("Start the registration process.")
                print("Please enter the 4-digit number PIN you wish to register.")
                print("=============================================================")
                Pin = input().rstrip().split()
                Pin = ''.join(Pin)
                while self.PIN_input_counter <= self.PIN_allowable_error_num and self.PIN_incorrect_flag:
                    if len(Pin) == self.PIN_length and Pin.isdecimal():
                        self.PIN_incorrect_flag = False
                    else:
                        self.PIN_input_counter += 1
                        rest_input_times = self.PIN_allowable_error_num - self.PIN_input_counter
                        print("==========================================================")
                        print("The PIN entered is not 4 digits number.")
                        print("Please enter the 4-digit number PIN")
                        print(" Enter the number of times that the PIN can input is {rest_input_times}.".format(rest_input_times=rest_input_times))
                        print("==========================================================")
                        Pin = input().rstrip().split()
                        Pin = ''.join(Pin)
                        print(Pin)
                    if (self.PIN_input_counter >= self.PIN_allowable_error_num):
                        print("================================================================")
                        print("The allowable number of PIN incorrect entries has been exceeded.")
                        print("Please start the transaction again from the beginning.")
                        print("================================================================")
                        return
                cus_data = self.make_new_account(self.data_csv_file_path, lower_cus_name, cus_birth, cus_add, Pin)
                if len(cus_data) == self.csv_data_num:
                    print("=========================================")
                    print("Account successfully registered.")
                    print("Deposits are initialized to $0.")
                    self.display_account_data(cus_data, cus_name)
                    print("")
                    print("Please enter y for deposit transactions.")
                    print("Please enter n to close the transaction")
                    print("=========================================")
                    transaction_flag = input().rstrip().split()
                    transaction_flag = ''.join(transaction_flag)
                    if transaction_flag == "y":
                        if self.star_deposit_transactions(self.data_csv_file_path, cus_data[0], cus_name): return
                    elif transaction_flag == "n":
                        print("===============================")
                        print("Thank you!")
                        print("We look forward to serving you!")
                        print("===============================")
                        return
                    else:
                        print("=========================")
                        print("Incorrect input detected.")
                        print("Close the deal.")
                        print("=========================")
                        return
                else:
                    print("============================")
                    print("Account creation failed.")
                    print("Possible system malfunction.")
                    print("============================")
                    return
            else:
                print("======================================================")
                print("You already have a bank account with ABC Bank.")
                print("Please start the transaction again from the beginning.")
                print("======================================================")
                return
        elif customer_needs == 3:
            print("======================")
            print("Close the transaction.")
            print("Thank you!!")
            print("======================")
            return
        else:
            print("=========================")
            print("Incorrect input detected.")
            print("Close the deal.")
            print("=========================")
            return

if __name__ == "__main__":
    bank_base = BankBase()
    bank_base.main()
