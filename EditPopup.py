import dbManager
import tkinter
from tkinter import *
from tkinter.ttk import *


class EditPopup(Frame):
    def __init__(self, master=None, fields=(), default_values=(), table_name="", action="add", db_manager=None,
                 on_close=None,
                 *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.popup = None
        self.fields = fields
        self.default_values = default_values
        self.table_name = table_name
        self.action = action
        self.on_close = on_close
        self.db_manager = db_manager
        self.entry_widgets = []
        if self.db_manager is None:
            self.db_manager = dbManager.DbManager()

        self.create_ui()

    def create_ui(self):
        self.popup = Toplevel(self)
        self.popup.title(f'{self.action} in {self.table_name}')
        self.popup.geometry(f'200x{(1 + len(self.fields)) * 40}')

        fields_grid = Frame(self.popup)

        values_dict = dict(zip(self.fields, self.default_values)) if self.default_values else {col: "" for col in
                                                                                               self.fields}
        print(values_dict)

        index = 0
        for key, val in values_dict.items():
            label = Label(fields_grid, text=key)
            label.grid(row=index, column=0, padx=5, pady=5)
            input_field = Entry(fields_grid, width=10)
            input_field.grid(row=index, column=1, padx=5, pady=5)
            input_field.insert(0, str(val))
            self.entry_widgets.append(input_field)
            index += 1

        fields_grid.pack()

        button_ok = Button(self.popup, text="Ok", command=self.execute_action)
        button_ok.pack()

    def execute_action(self):

        values = [f'\'{entry.get()}\'' if len(entry.get()) > 0 else None for entry in self.entry_widgets]

        values_dict = dict(zip([string.lower() for string in self.fields], values))
        values_dict = {key: value for key, value in values_dict.items() if value is not None}

        print(values_dict)

        if self.action == "add":
            self.db_manager.insert_data(table_name=self.table_name, values=values_dict)
            pass
        elif self.action == "update":
            default_values_dict = dict(zip(self.fields, self.default_values))
            conditions = [f"{str.lower(key)} = \'{value}\'" for key, value in default_values_dict.items()]
            where = " AND ".join(conditions)
            self.db_manager.update_data(table_name=self.table_name, values=values_dict, where=where)
            pass

        if self.on_close is not None:
            self.on_close()

        self.popup.destroy()
