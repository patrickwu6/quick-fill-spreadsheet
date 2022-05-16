import csv
import math
from tkinter import *
from tkinter import ttk

class Quick_Spreadsheet:
    def __init__(self, master):
        self.categories = []
        self.data = None
        self.filepath = None
        self.master = master
        frame = ttk.Frame(master, padding=10)
        frame.grid()
        self.file_label = ttk.Label(frame, text="No file open.")
        self.file_label.grid(column=0, row=0)
        ttk.Button(frame, text="Create category", command=self.create_category_button).grid(column=1, row=0)
        ttk.Button(frame, text="Open CSV", command=self.open_csv_button).grid(column=0, row=1)
        ttk.Button(frame, text="Save to file", command=self.save_csv).grid(column=1, row=1)
        ttk.Button(frame, text="Start filling spreadsheet", command=self.create_build_spreadsheet_ui).grid(column=2, row=0)
        ttk.Button(frame, text="Get statistics", command=self.get_statistics).grid(column=2, row=1)
        master.bind("c", lambda x: self.create_category_button())
        master.bind("o", lambda x: self.open_csv_button())
        master.bind("s", lambda x: self.save_csv())
        master.bind("f", lambda x: self.create_build_spreadsheet_ui())
        master.bind("g", lambda x: self.get_statistics())

    def add_data_to_csv(self, p, c, v):
        p.destroy()
        self.data.append([c,v])
        print(self.data)

    def get_data_for_csv(self, c):
        get_data = Toplevel(self.master)
        get_data_label = Label(get_data, text=f"Enter data (Category {c}:")
        get_data_entry = Entry(get_data)
        get_data_confirm = Button(get_data, text="Confirm", command=lambda:self.add_data_to_csv(get_data, c, get_data_entry.get()))
        get_data_quit = Button(get_data, text="Quit", command=get_data.destroy)
        get_data_entry.focus()
        get_data.bind("<Return>", lambda x: self.add_data_to_csv(get_data, c, get_data_entry.get()))
        get_data.bind("<Escape>", lambda x: get_data.destroy())
        get_data_label.grid(column=0,row=0)
        get_data_entry.grid(column=0, row=1)
        get_data_confirm.grid(column=0, row=2)
        get_data_quit.grid(column=1, row=2)
        
    def get_statistics(self):
        if not self.filepath:
            get_statistics = Toplevel(self.master)
            get_statistics_label = Label(get_statistics, text="Open a CSV first.")
            get_statistics_quit = Button(get_statistics, text="Ok", command=get_statistics.destroy)
            get_statistics_label.grid(column=0, row=0)
            get_statistics_quit.grid(column=0, row=1)
            get_statistics_quit.focus()
            get_statistics.bind("<Return>", lambda x: get_statistics.destroy())
            return
        sorted_data = {}
        for c in self.categories:
            sorted_data[c] = 0
        for d in self.data:
            sorted_data[d[0]] += int(d[1])
        get_statistics = Toplevel(self.master)
        label_text = ""
        for k, v  in sorted_data.items():
            label_text += f"Total value of {k}: {v}\n"
        label_text += f"\nOverall total: {sum(sorted_data.values())}"
        get_statistics_text = Text(get_statistics, height=len(sorted_data.keys()) + 2)
        get_statistics_text.insert(1.0, label_text)
        get_statistics_text.configure(bg=get_statistics.cget("bg"), relief="flat", state="disabled")
        get_statistics_quit = Button(get_statistics, text="Ok", command=get_statistics.destroy)
        get_statistics_text.grid(column=0, row=0)
        get_statistics_quit.grid(column=0, row=1)
        get_statistics_quit.focus()
        get_statistics.bind("<Return>", lambda x: get_statistics.destroy())

    def create_build_spreadsheet_ui(self):
        build_sheet_ui = Toplevel(self.master)
        button_list = []
        for i in self.categories:
            button_list.append(ttk.Button(build_sheet_ui, text=i, command=lambda j = i: self.get_data_for_csv(j)))
        tl = math.floor(math.sqrt(len(button_list)))
        for j in range(0, len(button_list)):
            button_list[j].grid(column=j%tl, row=j//tl)
        build_sheet_ui.bind("<Escape>", lambda x: build_sheet_ui.destroy())

    def create_category_button(self):
        create_category = Toplevel(self.master)
        create_category_label = Label(create_category, text="Enter category name:")
        create_category_entry = Entry(create_category)
        create_category_confirm = Button(create_category, text="Confirm", command=lambda: self.create_category(create_category, create_category_entry.get()))
        create_category_quit = Button(create_category, text="Quit", command=create_category.destroy)
        create_category_entry.focus()
        create_category.bind("<Return>", lambda x: self.create_category(create_category, create_category_entry.get()))
        create_category.bind("<Escape>", lambda x: create_category.destroy())
        create_category_label.grid(column=0, row=0)
        create_category_entry.grid(column=0, row=1)
        create_category_confirm.grid(column=0, row=2)
        create_category_quit.grid(column=1, row=2)

    def create_category(self, p, c):
        p.destroy()
        self.categories.append(c)

    def open_csv_button(self):
        open_csv = Toplevel(self.master)
        open_csv_entry = Entry(open_csv)
        open_csv_confirm = Button(open_csv, text="Confirm", command=lambda: self.open_csv(open_csv, open_csv_entry.get()))
        open_csv_quit = Button(open_csv, text="Quit", command=open_csv.destroy)
        open_csv_entry.focus()
        open_csv.bind("<Return>", lambda x: self.open_csv(open_csv, open_csv_entry.get()))
        open_csv.bind("<Escape>", lambda x: open_csv.destroy())
        open_csv_entry.grid(column=1, row=0)
        open_csv_confirm.grid(column=0, row=1)
        open_csv_quit.grid(column=2, row=1)

    def open_csv(self, p, f):
        p.destroy()
        try:
            with open(f"{f}.csv", "r+", newline="") as file:
                self.data = [r for r in csv.reader(file, delimiter= ",", quotechar="|")]
        except FileNotFoundError:
            with open(f"{f}.csv", "w+", newline="") as file:
                self.data = []
        self.filepath = f"{f}.csv"
        self.file_label.configure(text=f"Currently working on {f}.csv.")
        for d in self.data:
            if d[0] not in self.categories:
                self.categories.append(d[0])

    def save_csv(self):
        if not self.filepath:
            save_csv = Toplevel(self.master)
            save_csv_label = Label(save_csv, text="Open a CSV first.")
            save_csv_quit = Button(save_csv, text="Ok", command=save_csv.destroy)
            save_csv_label.grid(column=0, row=0)
            save_csv_quit.grid(column=0, row=1)
            save_csv_quit.focus()
            save_csv.bind("<Return>", lambda x: save_csv.destroy())
            return
        with open(self.filepath, "w+", newline="") as file:
            writer = csv.writer(file, delimiter= ",", quotechar= "|")
            for d in self.data:
                writer.writerow(d)
            save_csv = Toplevel(self.master)
            save_csv_label = Label(save_csv, text=f"Saved to {self.filepath}.")
            save_csv_quit = Button(save_csv, text="Ok", command=save_csv.destroy)
            save_csv_label.grid(column=0, row=0)
            save_csv_quit.grid(column=0, row=1)
            save_csv_quit.focus()
            save_csv.bind("<Return>", lambda x: save_csv.destroy())


categories = []
root = Tk()
root.title("Quick Spreadsheet")
a = Quick_Spreadsheet(root)
root.mainloop()