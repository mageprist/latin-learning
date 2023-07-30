#!/usr/bin/env python
import os
import curses

class File():
    def __init__(self):
        self.init_screen()
        self.y = 0
        self.x = 0
        res = []
        for path in os.listdir(f"{os.getcwd()}/lists/"):
            if os.path.isfile(os.path.join(f"{os.getcwd()}/lists/", path)):
                res.append(path)

        res.sort()

        self.print("Choose file:")
        for num, lst in enumerate(res):
            lst = lst.replace("-", " ")
            lst = lst.capitalize()
            self.print(f"({num})" + " " + lst[:-4])

        while True:
            try:
                question = int(self.input(':'))
                break
            except:
                self.print("That's not a valid option!")
                quit()

        self.load_file(res[question])

        self.test()

    def clear(self):
        self.stdscr.clear()
        self.y = 0
        self.stdscr.refresh()

    def clear_line(self, line):
        self.stdscr.addstr(line, 0, " " * (self.width - 1))
        self.stdscr.refresh()

    def print(self, string, end="\n", color=1):
        self.stdscr.attron(curses.color_pair(color))
        self.stdscr.addstr(self.y,
                           self.x,
                           string)

        if end == "\n":
            self.y += 1
            self.x = 0
        else:
            self.x += len(string)
        self.stdscr.attroff(curses.color_pair(color))
        self.stdscr.refresh()


    def word_input(self):
        done = False
        inp = ""
        # self.y += 1
        self.stdscr.addstr(self.height - 1,
                           self.x,
                           inp)
        self.stdscr.refresh()
        while not done:
            k = self.stdscr.getkey()
            if k != " ":

                try:
                    k = str(k)
                except:
                    print("error")

                if k == "-":
                    inp = inp[:-1]
                    self.stdscr.addstr(self.height - 1, self.x + len(inp), " ")
                else:
                    inp += k

                self.stdscr.addstr(self.height - 1, self.x, inp)
                self.stdscr.refresh()
            else:
                done = True

        self.x += len(inp) + 1
        return inp


    def input(self, string):
        done = False
        inp = ""
        self.stdscr.addstr(self.y,
                           0,
                           string)
        # self.y += 1
        self.stdscr.addstr(self.y,
                           len(string),
                           inp)
        self.stdscr.refresh()
        while not done:
            k = self.stdscr.getkey()
            if k != "\n":
                inp += k
                self.stdscr.addstr(self.y, len(string), inp)
                self.stdscr.refresh()
            else:
                done = True
        self.y += 1
        return inp


    def init_screen(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        self.height, self.width = self.stdscr.getmaxyx()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.refresh()

    def test(self):
        self.print("Choose what to study:")
        for num, x in enumerate(self.words):
            self.print(f"({num}) " + x[0][4:-5])

        while True:
            try:
                question = int(self.input(':'))
                break
            except:
                self.print("That's not a valid option!")
                quit()

        done = False
        self.clear()
        for num, glossary in enumerate(self.words[question]):
            if num == 0:
                self.print(glossary)
                continue

            self.print(glossary[0])
            word_num = 0
            while word_num < len(glossary) - 1:
                inp = self.word_input()
                if inp == glossary[word_num + 1]:
                    word_num += 1
                elif inp == "?":
                    for word in glossary[1:]:
                        self.print(word + " ", end='')
                    self.print("")
                    self.y -= 1
                else:
                    self.x = 0
                    self.stdscr.addstr(self.y, 0, " " * (self.width - 1))
                    self.print(f"Incorrect! {glossary[word_num + 1]}", color=2)
                    self.y -= 1
                    self.stdscr.addstr(self.height - 1, 0, " " * (self.width - 1))

                    self.x = 0
                    word_num = 0

            self.print("")
            self.y -= 2
            self.stdscr.addstr(self.height - 1, 0, " " * (self.width - 1))
            self.stdscr.addstr(self.y, 0, " " * (self.width - 1))
            self.stdscr.addstr(self.y + 1, 0, " " * (self.width - 1))

    def load_file(self, file):
        key = []
        words = []
        f = open(f"{os.getcwd()}/lists/" + file, "r", encoding="UTF-8")
        current = -1
        for x in f:
            if "%" in x:
                key = x.split()[1:]
            elif "---" in x:
                current += 1
                words.append([x])
                num_words = 0

            elif ":" in x:
                eng = x.split(":")[0]
                lat = x.split(":")[1].split()
                lat.insert(0, eng)
                words[current].append(lat)

                num_words += 1

        f.close()
        self.words = words
        self.key = key

while 1:
    f = File()




