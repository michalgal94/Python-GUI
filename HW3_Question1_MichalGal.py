import datetime
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


def time_decorator(transaction_func):
    def inner_func(*args):
        time = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        account_id = transaction_func(*args)
        if account_id is None:
            print("Transaction failed.")
        else:
            print(str(transaction_func.__name__.replace('_', ' ').capitalize()) + " executed at: " + str(time) +
                  " by account number: " + str(account_id))
    return inner_func


class Bank:

    def __init__(self, name, accounts=[]):
        self.name = name
        self.accounts = accounts
        self.current_account = None

    def add_account_to_bank(self, account):
        for acc in self.accounts:
            if account.account_id == acc.account_id:
                # account already exist in system.
                return False
        self.accounts.append(account)
        return True

    def get_account_by_id(self, id):
        for acc in self.accounts:
            if acc.account_id == id:
                return acc
        return False

    def print_all_accounts(self):
        for acc in self.accounts:
            print(acc)

    def is_id_exist(self, id):
        for acc in self.accounts:
            if id == acc.account_id:
                return True
        return False

    def balance_generator(self):
        for acc in self.accounts:
            yield acc.balance


class BankGui:

    def __init__(self, main_window, bank):
        self.bank = bank
        self.main_window = main_window

        # setting connection entries to save values
        self.name_entry = None
        self.id_entry = None
        self.connect = None
        self.connect_button = None
        self.deposit_window = None
        self.withdraw_window = None
        self.transfer_window = None

        # setting new account entries to save values
        self.new_account_window = None
        self.new_name_entry = None
        self.new_id_entry = None
        self.new_balance_entry = None
        self.new_credit_entry = None

        # setting transactions entries
        self.deposit_amount_entry = None
        self.withdraw_amount_entry = None
        self.transfer_amount_entry = None
        self.to_name_entry = None
        self.to_id_entry = None
        self.selected_account = None

        # vars for StringVar() label changes
        self.acc_name = StringVar()
        self.acc_name.set("None")
        self.acc_id = StringVar()
        self.acc_id.set("None")
        self.acc_balance = StringVar()
        self.acc_balance.set("None")
        self.acc_credit = StringVar()
        self.acc_credit.set("None")

        # main window
        self.main_window.title("Bank Menu")
        self.main_window.geometry("450x350")

        # title of bank at the top
        title_label = Label(self.main_window, text=self.bank.name, width=60, font=("Impact", 20))
        title_label.pack(side=TOP)

        # hold center of bank (account details and login frames)
        self.bank_frame = Frame(self.main_window)
        self.bank_frame.pack()

        # account details frame
        self.show_acc_final = ttk.LabelFrame(self.bank_frame, borderwidth=20, text="Account Details ")
        self.show_acc_final.pack(padx=10, pady=15)

        # create details labels and fields, set fields to "None"
        # right side details
        name_label = Label(self.show_acc_final, text="Name:")
        name_label.grid(row=0, sticky=E)
        show_name_label = Label(self.show_acc_final, textvariable=self.acc_name)
        show_name_label.grid(row=0, column=1, padx=(0, 70))
        id_label = Label(self.show_acc_final, text="ID:")
        id_label.grid(row=1, sticky=E)
        show_id_label = Label(self.show_acc_final, textvariable=self.acc_id)
        show_id_label.grid(row=1, column=1, padx=(0, 70))

        # left side details
        balance_label = Label(self.show_acc_final, text="Balance:")
        balance_label.grid(row=0, column=2, sticky=E)
        show_balance_label = Label(self.show_acc_final, textvariable=self.acc_balance)
        show_balance_label.grid(row=0, column=3, padx=(0, 30))
        credit_label = Label(self.show_acc_final, text="Line of credit:")
        credit_label.grid(row=1, column=2, sticky=E)
        show_credit_label = Label(self.show_acc_final, textvariable=self.acc_credit)
        show_credit_label.grid(row=1, column=3, padx=(0, 30))

        # create login frame
        self.login_frame = Frame(self.bank_frame)
        self.login_frame.pack()

        # create login buttons and add to login frame
        self.log_button_text = StringVar()
        self.log_button_text.set("Login")
        login_button = Button(self.login_frame, textvariable=self.log_button_text, font=20, width=10, command=self.open_connect_window)
        login_button.pack(side=LEFT, padx=10)
        create_account_button = Button(self.login_frame, text="Create new account", font=20, command=self.create_new_account)
        create_account_button.pack(side=RIGHT, padx=10)

        gen_frame = Frame(self.bank_frame)
        gen_frame.pack()
        show_gen_button = Button(gen_frame, text="Start generator\n(print in console)", command=self.print_gen)
        show_gen_button.pack(side=BOTTOM, pady=20)

        # create bottom frame with buttons and add to main frame
        self.transaction_buttons_frame = Frame(self.main_window)
        self.transaction_buttons_frame.pack(side=BOTTOM)
        self.deposit_button = Button(self.transaction_buttons_frame, text="Deposit", state=DISABLED, pady=8, padx=8, command=self.open_deposit_window)
        self.deposit_button.pack(side=LEFT, pady=10, padx=10)
        self.withdraw_button = Button(self.transaction_buttons_frame, text="Withdraw", state=DISABLED, pady=8, padx=8, command=self.open_withdraw_window)
        self.withdraw_button.pack(side=LEFT, pady=10, padx=10)
        self.transfer_button = Button(self.transaction_buttons_frame, text="Transfer", state=DISABLED, pady=8, padx=8, command=self.open_transfer_window)
        self.transfer_button.pack(side=LEFT, pady=10, padx=10)

    def print_gen(self):
        print("All clients balance from generator function:\n")
        for bal, client in zip(self.bank.balance_generator(), self.bank.accounts):
            print(str(client) + ", Balance: " + str(bal))
        print("\n")

    def open_connect_window(self):
        if self.log_button_text.get() == "Login":
            if not self.connect:
                self.connect = Tk()

                self.connect.title("Connect")
                self.connect.geometry("215x200")
                connect_frame = Frame(self.connect)
                connect_frame.pack()

                title_label = Label(connect_frame, text="Connect", width=20, font=("Impact", 20))
                title_label.pack(side=TOP)

                login_frame = Frame(connect_frame)
                login_frame.pack()

                login_label = Label(login_frame, text="login", font=14)
                login_label.grid(row=0, sticky=W)

                name_label = Label(login_frame, text="Name:")
                name_label.grid(row=1, pady=5, padx=5)
                self.name_entry = Entry(login_frame)
                self.name_entry.insert(0, "nir")
                self.name_entry.grid(row=1, column=1, pady=5, padx=5)

                id_label = Label(login_frame, text="ID:")
                id_label.grid(row=2, sticky=E, pady=5, padx=5)
                self.id_entry = Entry(login_frame)
                self.id_entry.insert(0, "123")
                self.id_entry.grid(row=2, column=1, pady=5, padx=5)

                self.connect_button = Button(login_frame, text="Connect", command=self.connect_account)
                self.connect_button.grid(row=3, column=1, sticky=E)
                quit_button = Button(login_frame, text="Back", command=self.connect.destroy)
                quit_button.grid(row=4, sticky=W, pady=8)

                self.connect.attributes('-topmost', True)
                self.connect.bind("<Destroy>", self.on_closing_connect)
                self.connect.mainloop()
        elif self.log_button_text.get() == "Logout":
            self.logout()

    def on_closing_connect(self, event):
        self.connect = None

    def connect_account(self):
        acc_name = self.name_entry.get()
        acc_id = self.id_entry.get()

        for acc in self.bank.accounts:
            if acc.name == str(acc_name):
                if acc.account_id == int(acc_id):
                    self.bank.current_account = acc
                    self.connect_button.config(state="disabled")
                    messagebox.showinfo("Login", "Logged in successfully")
                    if self.connect:
                        self.connect.destroy()
                    self.log_button_text.set("Logout")
                    self.deposit_button.config(state="normal")
                    self.withdraw_button.config(state="normal")
                    self.transfer_button.config(state="normal")
                    self.show_account()
                    return
                else:
                    print("wrong id.")
                    return
        print("no account by the name " + acc_name)

    def show_account(self):
        self.acc_name.set(self.bank.current_account.name)
        self.acc_id.set(self.bank.current_account.account_id)
        self.acc_balance.set(self.bank.current_account.balance)
        self.acc_credit.set(self.bank.current_account.limit)

    def logout(self):
        self.bank.current_account = None
        messagebox.showinfo("Logout", "Logged out successfully")
        self.acc_name.set("None")
        self.acc_id.set("None")
        self.acc_balance.set("None")
        self.acc_credit.set("None")
        self.deposit_button.config(state="disabled")
        self.withdraw_button.config(state="disabled")
        self.transfer_button.config(state="disabled")
        self.log_button_text.set("Login")

    def create_new_account(self):
        if not self.new_account_window:
            self.new_account_window = Tk()

            self.new_account_window.title("New Account")
            self.new_account_window.geometry("275x300")

            new_account_label = Label(self.new_account_window, text="New Account", width=20, font=("Impact", 20))
            new_account_label.pack()

            # frame to hold all labels and entries to add account
            inner_frame = Frame(self.new_account_window)
            inner_frame.pack()

            # labels and entries to add new account
            new_name_label = Label(inner_frame, text="Name:")
            new_name_label.grid(row=0, sticky=E, pady=5, padx=5)
            self.new_name_entry = Entry(inner_frame)
            self.new_name_entry.grid(row=0, column=1, pady=5, padx=5)

            new_id_label = Label(inner_frame, text="ID:")
            new_id_label.grid(row=1, sticky=E, pady=5, padx=5)
            self.new_id_entry = Entry(inner_frame)
            self.new_id_entry.grid(row=1, column=1, pady=5, padx=5)

            new_balance_label = Label(inner_frame, text="Balance:")
            new_balance_label.grid(row=2, sticky=E, pady=5, padx=5)
            self.new_balance_entry = Entry(inner_frame)
            self.new_balance_entry.grid(row=2, column=1, pady=5, padx=5)

            new_credit_label = Label(inner_frame, text="Line of credit:")
            new_credit_label.grid(row=3, sticky=E, pady=5, padx=5)
            self.new_credit_entry = Entry(inner_frame)
            self.new_credit_entry.grid(row=3, column=1, pady=5, padx=5)

            # Button
            create_button = Button(inner_frame, text="Create", font=20, width=10, command=self.create_account_from_entry)
            create_button.grid(row=4, column=1, sticky=E, pady=5)
            quit_button = Button(inner_frame, text="Back", font=20, width=10, command=self.new_account_window.destroy)
            quit_button.grid(row=5, column=0, sticky=W, pady=20)

            self.new_account_window.attributes('-topmost', True)
            self.new_account_window.bind("<Destroy>", self.on_closing_create)
            self.new_account_window.mainloop()

    def on_closing_create(self, event):
        self.new_account_window = None

    def create_account_from_entry(self):
        ok_flag = True
        new_name = self.new_name_entry.get()
        new_id = self.new_id_entry.get()
        new_balance = self.new_balance_entry.get()
        new_credit = self.new_credit_entry.get()

        error_string = ""
        if new_name == "":
            error_string += "Invalid name.\n"
            ok_flag = False
        else:
            try:
                float(new_name)
                ok_flag = False
                error_string += "Invalid name.\n"
            except:
                pass
        try:
            new_id = int(new_id)
        except:
            error_string += "Invalid id.\n"
            ok_flag = False
        try:
            new_balance = int(new_balance)
        except:
            try:
                float(new_balance)
            except:
                error_string += "Invalid balance.\n"
                ok_flag = False
        if new_credit == "":
            new_credit = 1500
        else:
            try:
                new_credit = int(new_credit)
            except:
                try:
                    float(new_credit)
                except:
                    error_string += "Invalid line of credit.\n"
                    ok_flag = False

        if ok_flag is False:
            messagebox.showerror("Invalid Input", error_string + "\nPlease make sure that name is a string.\n"
                                                                 "ID is an integer, Balance and Credit are numbers."
                                                                 "\nCredit is optional (1500 default)")
            return

        new_account = Account(new_name, new_id, new_balance, new_credit)

        if self.bank.is_id_exist(new_account.account_id) is False:
            self.bank.add_account_to_bank(new_account)
            messagebox.showinfo("Success", "Account created successfully")
            self.new_account_window.destroy()
        else:
            messagebox.showerror("Error", "ID number: " + str(new_id) + " already exist in bank.\nPlease try again.")

    def open_deposit_window(self):
        if not self.deposit_window:
            self.deposit_window = Tk()
            self.deposit_window.title("Deposit")
            self.deposit_window.geometry("300x125")

            deposit_label = Label(self.deposit_window, text="Deposit", width=20, font=("Impact", 20))
            deposit_label.pack()

            inner_deposit = Frame(self.deposit_window)
            inner_deposit.pack()

            amount_label = Label(inner_deposit, text="Amount:")
            amount_label.grid(row=0, sticky=E, pady=5, padx=5)
            self.deposit_amount_entry = Entry(inner_deposit)
            self.deposit_amount_entry.grid(row=0, column=1, pady=5, padx=5)
            execute_button = Button(inner_deposit, text="Execute", command=self.exec_deposit)
            execute_button.grid(row=0, column=2, pady=5, padx=5)
            quit_button = Button(inner_deposit, text="Back", command=self.deposit_window.destroy)
            quit_button.grid(row=1, column=1, pady=5, padx=5)

            self.deposit_window.attributes('-topmost', True)
            self.deposit_window.bind("<Destroy>", self.on_closing_deposit)
            self.deposit_window.mainloop()

    def on_closing_deposit(self, event):
        self.deposit_window = None

    def exec_deposit(self):
        amount = self.deposit_amount_entry.get()
        ok_flag = True
        try:
            amount = int(amount)
        except:
            try:
                amount = float(amount)
            except:
                ok_flag = False
                print("invalid amount. please insert a number.")
        if ok_flag is True:
            result = messagebox.askyesno("Confirm", "Are you sure?")
            if result is True:
                self.bank.current_account.deposit(amount)
                self.acc_balance.set(self.bank.current_account.balance)

    def open_withdraw_window(self):
        if not self.withdraw_window:
            self.withdraw_window = Tk()
            self.withdraw_window.title("Withdraw")
            self.withdraw_window.geometry("300x125")

            withdraw_label = Label(self.withdraw_window, text="Withdraw", width=20, font=("Impact", 20))
            withdraw_label.pack()

            inner_withdraw = Frame(self.withdraw_window)
            inner_withdraw.pack()

            amount_label = Label(inner_withdraw, text="Amount:")
            amount_label.grid(row=0, sticky=E, pady=5, padx=5)
            self.withdraw_amount_entry = Entry(inner_withdraw)
            self.withdraw_amount_entry.grid(row=0, column=1, pady=5, padx=5)
            execute_withdraw_button = Button(inner_withdraw, text="Execute", command=self.exec_withdraw)
            execute_withdraw_button.grid(row=0, column=2, pady=5, padx=5)
            quit_button = Button(inner_withdraw, text="Back", command=self.withdraw_window.destroy)
            quit_button.grid(row=1, column=1, pady=5, padx=5)

            self.withdraw_window.attributes('-topmost', True)
            self.withdraw_window.bind("<Destroy>", self.on_closing_withdraw)
            self.withdraw_window.mainloop()

    def on_closing_withdraw(self, event):
        self.withdraw_window = None

    def exec_withdraw(self):
        amount = self.withdraw_amount_entry.get()
        ok_flag = True
        try:
            amount = int(amount)
        except:
            try:
                amount = float(amount)
            except:
                ok_flag = False
                print("invalid amount. please insert a number.")
        if ok_flag is True:
            result = messagebox.askyesno("Confirm", "Are you sure?")
            if result is True:
                self.bank.current_account.withdraw(amount)
                self.acc_balance.set(self.bank.current_account.balance)

    def open_transfer_window(self):
        if not self.transfer_window:
            self.transfer_window = Tk()
            self.transfer_window.title("Transfer")
            self.transfer_window.geometry("300x275")

            transfer_label = Label(self.transfer_window, text="Transfer", width=20, font=("Impact", 20))
            transfer_label.pack()

            inner_transfer = Frame(self.transfer_window)
            inner_transfer.pack()

            amount_label = Label(inner_transfer, text="Amount:")
            amount_label.grid(row=0, sticky=E, pady=5, padx=5)
            self.transfer_amount_entry = Entry(inner_transfer)
            self.transfer_amount_entry.grid(row=0, column=1, pady=5, padx=5)
            to_account_label = Label(inner_transfer, text="Transfer to:")
            to_account_label.grid(row=1, sticky=E, pady=5, padx=5)
            name_label = Label(inner_transfer, text="Name:")
            name_label.grid(row=2, sticky=E, pady=5, padx=5)
            self.to_name_entry = Entry(inner_transfer)
            self.to_name_entry.grid(row=2, column=1, pady=5, padx=5)
            id_label = Label(inner_transfer, text="ID:")
            id_label.grid(row=3, sticky=E, pady=5, padx=5)
            self.to_id_entry = Entry(inner_transfer)
            self.to_id_entry.grid(row=3, column=1, pady=5, padx=5)
            execute_transfer_button = Button(inner_transfer, text="Execute", command=self.exec_transfer)
            execute_transfer_button.grid(row=4, column=1, sticky=E, pady=5, padx=5)
            quit_button = Button(inner_transfer, text="Back", command=self.transfer_window.destroy)
            quit_button.grid(row=5, column=0, sticky=W, pady=5, padx=5)

            acc_names_list = list()
            acc_names_list.append("Select account")
            for acc in self.bank.accounts:
                acc_names_list.append(acc.account_id)

            self.selected_account = StringVar(inner_transfer)
            self.selected_account.set(acc_names_list[0])  # default value

            account_drop_list = OptionMenu(inner_transfer, self.selected_account, *acc_names_list)
            account_drop_list.grid(row=1, column=1, pady=5, padx=5)

            select_button = Button(inner_transfer, text="Select", command=self.select_account)
            select_button.grid(row=1, column=2, sticky=E, pady=5, padx=5)

            self.transfer_window.attributes('-topmost', True)
            self.transfer_window.bind("<Destroy>", self.on_closing_transfer)
            self.transfer_window.mainloop()

    def on_closing_transfer(self, event):
        self.transfer_window = None

    def select_account(self):
        if self.selected_account.get() == "Select account":
            self.to_name_entry.delete(0, END)
            self.to_id_entry.delete(0, END)
            return
        for acc in self.bank.accounts:
            if acc.account_id == int(self.selected_account.get()):
                if self.to_name_entry.get() is not "":
                    self.to_name_entry.delete(0, END)
                    self.to_id_entry.delete(0, END)
                self.to_name_entry.insert(0, acc.name)
                self.to_id_entry.insert(0, acc.account_id)

    def exec_transfer(self):
        amount = self.transfer_amount_entry.get()
        ok_flag = True
        try:
            amount = int(amount)
        except:
            try:
                amount = float(amount)
            except:
                ok_flag = False
                print("Invalid amount. Please enter a number.")
        id = self.to_id_entry.get()
        try:
            id = int(id)
        except:
            ok_flag = False
            print("Invalid id. Please enter an integer.")
        name = self.to_name_entry.get()
        try:
            float(name)
            ok_flag = False
            print("Invalid name. Please enter a string")
        except:
            pass
        if ok_flag is True:
            account = self.bank.get_account_by_id(id)
            if account is False:
                print("Could not find an account by this id.")
                return
            if account.name != name:
                print("Wrong name. Can't execute transaction.")
                return
            result = messagebox.askyesno("Confirm", "Are you sure?")
            if result is True:
                self.bank.current_account.transfer_to(account, amount)
                self.acc_balance.set(self.bank.current_account.balance)


class Account:

    def __init__(self, name, account_id, balance, limit=1500):
        self.name = name
        self.account_id = int(account_id)
        self.balance = balance
        self.limit = limit

    def __str__(self):
        return "Name: " + self.name + ". Account ID: " + str(self.account_id)

    @time_decorator
    def deposit(self, amount):
        if type(amount) is not str:
            self.balance += amount
            return self.account_id
        else:
            print("Can only deposit numeric values.")

    @time_decorator
    def withdraw(self, amount):
        if type(amount) is not str:
            if self.balance - amount >= self.limit*(-1):
                self.balance -= amount
                return self.account_id
            else:
                print("Can't withdraw amount of " + str(amount) + " because limit passed")
        else:
            print("Can only withdraw numeric values.")

    def get_balance(self):
        return self.balance

    @time_decorator
    def transfer_to(self, account, amount):
        if isinstance(account, Account):
            if type(amount) is not str:
                if abs(self.balance - amount) <= self.limit:
                    self.balance -= amount
                    account.balance += amount
                else:
                    print("Can't transfer amount of " + str(amount) + " because limit passed")
                    return None
            else:
                print("Can only transfer numeric values.")
            return self.account_id


if __name__ == '__main__':
    # ------Question #1------
    bank = Bank("Sgt. Pepper's Lonely Hearts Club Bank")

    n = Account("nir", 123, 100)
    m = Account("michal", 121, 1000)
    g = Account("geula", 122, 700, 1000)
    sh = Account("shimi", 125, 2000, 2000)
    bank.add_account_to_bank(n)
    bank.add_account_to_bank(m)
    bank.add_account_to_bank(g)
    bank.add_account_to_bank(sh)

    root = Tk()
    bank_gui = BankGui(root, bank)
    root.mainloop()
