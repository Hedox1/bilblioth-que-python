import tkinter
from tkinter import *
from tkinter.ttk import *

from EditPopup import EditPopup


class DataTable(Frame):
    def __init__(self, master=None, columns=(), table_name=None, *args,
                 **kwargs):
        super().__init__(master, *args, **kwargs)
        self.columns = columns
        self.table_name = table_name
        self.create_ui()

    def create_ui(self):
        tv = Treeview(self, columns=self.columns, show="headings", selectmode="browse")

        for col in self.columns:
            tv.heading(col, text=col)
            tv.column(col, anchor='center', width=100)

        tv.grid(sticky=(tkinter.N, tkinter.S, tkinter.W, tkinter.E))
        self.treeview = tv
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def add_data(self, data: dict[str, any], search_name: str = None, search_value: str = None):
        if (search_name is not None and len(search_name) > 0
                and search_value is not None and len(search_value) > 0
                and data[str.lower(search_name)] != search_value):
            return

        values = [data[str.lower(column)] for column in self.columns]
        self.treeview.insert("", "end", values=values)
        print(values)

    def clear(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

    def get_selection(self):
        item = self.treeview.selection()[0]
        values = self.treeview.item(item, "values")
        return values

    def delete_selection(self):
        self.treeview.delete(self.treeview.selection()[0])

