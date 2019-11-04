from tkinter import *
import tkinter.scrolledtext as tkscrolled
import matplotlib.pyplot as plt


FILE_NAME = "words.txt"


class WordsGui:

    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.title("Words Analyzer")
        self.main_window.geometry("425x350")

        self.letter_entry = None
        self.include_state = None

        title_label = Label(self.main_window, text="The Word", font=("Impact", 35))
        title_label.pack(side=TOP, pady=10)

        self.body_frame = Frame(self.main_window)
        self.body_frame.pack()

        self.scrolled_words_box = tkscrolled.ScrolledText(self.body_frame, height=15, width=23, wrap='word', state="normal")
        self.scrolled_words_box.pack(side=RIGHT, padx=(5,15))

        control_frame = Frame(self.body_frame)
        control_frame.pack(side=LEFT, padx=15)
        letter_label = Label(control_frame, text="Letter:")
        letter_label.grid(row=0, sticky=E, pady=10)
        self.letter_entry = Entry(control_frame)
        self.letter_entry.grid(row=0, column=1, sticky=E, pady=10)

        self.radio_value = IntVar()
        self.radio_value.set(0)
        radio_frame = Frame(control_frame)
        radio_frame.grid(row=1, column=1, pady=(0, 10))
        include_radio = Radiobutton(radio_frame, text="Include", variable=self.radio_value, value=1, command=self.set_state)
        include_radio.pack(side=LEFT, anchor=E)
        exclude_radio = Radiobutton(radio_frame, text="Exclude", variable=self.radio_value, value=2, command=self.set_state)
        exclude_radio.pack(side=LEFT, anchor=E)

        print_words_button = Button(control_frame, text="Print Words", command=self.print_words, height=2, width=9)
        print_words_button.grid(row=2, column=1)
        show_graph_button = Button(control_frame, text="Show Graph", command=self.show_graph, height=2, width=9)
        show_graph_button.grid(row=3, column=1, pady=10)

    def print_words(self):
        if self.radio_value.get() == 0:
            print("Please select an option.")
            return
        self.scrolled_words_box.delete(1.0, END)
        input = self.letter_entry.get()

        if input.isalpha():  # input is string from a-Z.
            if len(input) == 1:  # input is a single char
                if self.include_state:
                    self.scrolled_words_box.insert(1.0, "Mode: Include " + input.lower() + "\n\n")
                else:
                    self.scrolled_words_box.insert(1.0, "Mode: Exclude " + input.lower() + "\n\n")

                self.letter_entry.delete(0)
                for word in self.words_generator(input, include=self.include_state):
                    self.scrolled_words_box.insert(END, word + "\n")
            else:
                print("Enter only 1 character.")
        else:
            print("Enter letters only.")

    def set_state(self):
        if self.radio_value.get() == 1:
            self.include_state = True
        elif self.radio_value.get() == 2:
            self.include_state = False

    def create_words_list(self):
        with open(FILE_NAME, "r") as f:
            data = f.readlines()

        lines_dic = {}
        i = 0
        for line in data:
            lines_dic[i] = line.split(",")
            i += 1

        all_words = list()
        for line in lines_dic:
            for word in lines_dic[line]:
                word = word.replace("\n", "")
                # add the new words to an updated list of all words
                all_words.append(word)

        return all_words

    def words_generator(self, letter, include):
        all_words = self.create_words_list()

        if include:
            for word in all_words:
                if letter.lower() in word.lower():
                    yield word
        elif not include:
            for word in all_words:
                if letter.lower() not in word.lower():
                    yield word
        else:
            print("include= can get values: True for include, False for exclude")

    # ----------Graph----------
    def show_graph(self):
        graph_dict = self.prepare_graph_data()
        plt.bar(graph_dict["letters"], graph_dict["num of appearance"])
        plt.title('Count letters', fontsize=14)
        plt.xlabel('Letters', fontsize=14)
        plt.ylabel('Number of appearances', fontsize=14)
        for amount, letter in zip(graph_dict["num of appearance"], range(10)):
            plt.annotate(str(amount), (letter, amount))
        plt.show()

    def prepare_graph_data(self):
        i = 97  # 'a' ASCII
        graph_dict = {}
        graph_dict["letters"] = []
        graph_dict["num of appearance"] = []
        for letter in range(10):
            graph_dict["letters"].append(chr(i))
            graph_dict["num of appearance"].append(0)
            i += 1

        i = 97
        all_words = self.create_words_list()
        for letter in range(10):
            for word in all_words:
                if chr(i) in word:
                    graph_dict["num of appearance"][letter] += word.count(chr(i))
            i += 1

        return graph_dict


if __name__ == '__main__':
    words_root = Tk()
    words_gui = WordsGui(words_root)
    words_root.mainloop()
