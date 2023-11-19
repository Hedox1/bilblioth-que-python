import tkinter

import dbManager

from dataTable import DataTable
from tkinter import *
from tkinter.ttk import *

from EditPopup import EditPopup


class MainWindow(Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.db_manager = dbManager.DbManager()
        self.utilisateurs_table_name = "utilisateurs"
        self.livres_table_name = "livres"
        self.emprunts_table_name = "emprunts"
        self.utilisateurs_columns = ('Prenom', 'Nom', 'Categorie')
        self.livres_columns = ('Titre', 'Auteur', 'Genre', 'ISBN')
        self.emprunts_columns = ('emprunt_id', 'Nom', 'Prenom', 'Titre', 'Auteur', 'Debut', 'Fin')
        self.livres = ()
        self.utilisateurs = ()
        self.emprunts = ()

        self.emprunts_table = None
        self.emprunts_tab = None
        self.livre_table = None
        self.livres_tab = None
        self.utilisateurs_table = None
        self.tabControl = None
        self.utilisateurs_tab = None
        self.search_utilisateurs_entry = None
        self.search_livres_combobox = None
        self.search_utilisateurs_entry = None
        self.search_utilisateurs_combobox = None
        self.search_emprunts_combobox = None
        self.search_emprunts_entry = None

        try:
            self.fetch_utilisateurs()
            self.fetch_livres()
            self.fetch_emprunts()
        except:
            print("Fail to load from data")

        self.createUI()

    def createUI(self):
        label = Label(window, text="Gérer la bibliothèque", font=("Arial Bold", 30))
        label.pack()

        self.tabControl = Notebook(window)

        # UsersTab
        self.utilisateurs_tab = Frame(self.tabControl)
        self.tabControl.add(self.utilisateurs_tab, text='Utilisateurs')

        self.utilisateurs_table = DataTable(self.utilisateurs_tab,
                                            columns=self.utilisateurs_columns,
                                            table_name=self.utilisateurs_table_name)

        add_user_button = Button(self.utilisateurs_tab, text="Ajouter utilisateur", command=self.add_user_command)
        add_user_button.pack()

        edit_user_button = Button(self.utilisateurs_tab, text="Editer utilisateur", command=self.edit_user_command)
        edit_user_button.pack()

        delete_user_button = Button(self.utilisateurs_tab, text="Supprimer utilisateur",
                                    command=self.delete_user_command)
        delete_user_button.pack()

        search_user_frame = Frame(self.utilisateurs_tab)

        search_label_user = Label(search_user_frame, text="Rechercher Par")
        search_label_user.grid(row=0, column=0, padx=5, pady=5)

        self.search_utilisateurs_combobox = Combobox(search_user_frame, values=self.utilisateurs_columns)
        self.search_utilisateurs_combobox.grid(row=0, column=1, padx=5, pady=5)

        self.search_utilisateurs_entry = Entry(search_user_frame, width=30)
        self.search_utilisateurs_entry.grid(row=0, column=2, padx=5, pady=5)

        search_user_button = Button(search_user_frame, text="Rechercher", command=self.search_user)
        search_user_button.grid(row=0, column=3, padx=5, pady=5)

        search_user_frame.pack()

        self.utilisateurs_table.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)

        self.refresh_users()

        # BookTab
        self.livres_tab = Frame(self.tabControl)
        self.tabControl.add(self.livres_tab, text='Livres')

        self.livre_table = DataTable(self.livres_tab, columns=self.livres_columns, table_name=self.livres_table_name)

        add_book_button = Button(self.livres_tab, text="Ajout livre", command=self.add_book_command)
        add_book_button.pack()

        edit_book_button = Button(self.livres_tab, text="Editer livre", command=self.edit_book_command)
        edit_book_button.pack()

        delete_book_button = Button(self.livres_tab, text="Supprimer livre", command=self.delete_book_command)
        delete_book_button.pack()

        search_book_frame = Frame(self.livres_tab)

        search_label_book = Label(search_book_frame, text="Rechercher Par")
        search_label_book.grid(row=0, column=0, padx=5, pady=5)

        self.search_livres_combobox = Combobox(search_book_frame, values=self.livres_columns)
        self.search_livres_combobox.grid(row=0, column=1, padx=5, pady=5)

        self.search_utilisateurs_entry = Entry(search_book_frame, width=30)
        self.search_utilisateurs_entry.grid(row=0, column=2, padx=5, pady=5)

        search_book_button = Button(search_book_frame, text="Rechercher", command=self.search_book)
        search_book_button.grid(row=0, column=3, padx=5, pady=5)

        search_book_frame.pack()

        self.livre_table.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)

        self.refresh_books()

        # BorrowTab
        self.emprunts_tab = Frame(self.tabControl)
        self.tabControl.add(self.emprunts_tab, text='Emprunts')

        self.emprunts_table = DataTable(self.emprunts_tab, columns=self.emprunts_columns,
                                        table_name=self.emprunts_table_name)

        add_borrow_button = Button(self.emprunts_tab, text="Ajouter emprunts", command=self.add_borrow_command)
        add_borrow_button.pack()

        edit_borrow_button = Button(self.emprunts_tab, text="Editer emprunts", command=self.edit_borrow_command)
        edit_borrow_button.pack()

        delete_borrow_button = Button(self.emprunts_tab, text="Supprimer emprunts", command=self.delete_borrow_command)
        delete_borrow_button.pack()

        search_borrow_frame = Frame(self.emprunts_tab)

        search_borrow_book = Label(search_borrow_frame, text="Rechercher Par")
        search_borrow_book.grid(row=0, column=0, padx=5, pady=5)

        self.search_emprunts_combobox = Combobox(search_borrow_frame, values=self.emprunts_columns)
        self.search_emprunts_combobox.grid(row=0, column=1, padx=5, pady=5)

        self.search_emprunts_entry = Entry(search_borrow_frame, width=30)
        self.search_emprunts_entry.grid(row=0, column=2, padx=5, pady=5)

        search_borrow_button = Button(search_borrow_frame, text="Rechercher", command=self.search_borrow)
        search_borrow_button.grid(row=0, column=3, padx=5, pady=5)

        search_borrow_frame.pack()

        self.emprunts_table.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)

        self.refresh_borrows()

        self.tabControl.pack(expand=True, fill=tkinter.BOTH)

    def fetch_utilisateurs(self):
        print("fetch_users")
        utilisateur_data = self.db_manager.get_data(table_name=self.utilisateurs_table_name)
        self.utilisateurs = [{'nom': nom, 'prenom': prenom, 'categorie': categorie, "utilisateur_id": utilisateur_id}
                             for
                             nom, prenom, categorie, utilisateur_id in utilisateur_data]
        print(self.utilisateurs)

    def refresh_users(self, search_name: str = None, search_value: str = None):
        print("refresh users")
        self.utilisateurs_table.clear()
        for user in self.utilisateurs:
            self.utilisateurs_table.add_data(user, search_name=search_name, search_value=search_value)

    def fetch_livres(self):
        print("fetch_books")
        livres_data = self.db_manager.get_data(table_name=self.livres_table_name)
        self.livres = [{'titre': titre, 'auteur': auteur, 'genre': genre, 'isbn': isbn, "livre_id": livre_id} for
                       titre, auteur, genre, isbn, livre_id in livres_data]
        print(self.livres)

    def refresh_books(self, search_name: str = None, search_value: str = None):
        print("refresh books")
        self.livre_table.clear()
        for livre in self.livres:
            self.livre_table.add_data(data=livre, search_name=search_name, search_value=search_value)

    def fetch_emprunts(self):
        print("fetch_borrows")
        emprunt_data = self.db_manager.get_data(table_name=self.emprunts_table_name,
                                                fields=["emprunts.emprunt_id",
                                                        "utilisateurs.nom",
                                                        "utilisateurs.prenom",
                                                        "livres.titre",
                                                        "livres.auteur",
                                                        "emprunts.debut", "emprunts.fin"],
                                                join=["livres ON emprunts.livre_id = livres.livre_id",
                                                      "utilisateurs on emprunts.utilisateur_id = utilisateurs.utilisateur_id"])

        self.emprunts = [{'emprunt_id': emprunt_id, 'nom': nom, 'prenom': prenom, 'titre': titre, "auteur": auteur,
                          "debut": debut, "fin": fin}
                         for emprunt_id, nom, prenom, titre, auteur, debut, fin in emprunt_data]
        print(self.emprunts)

    def refresh_borrows(self, search_name: str = None, search_value: str = None):
        print("refresh borrows")
        self.emprunts_table.clear()
        for borrow in self.emprunts:
            self.emprunts_table.add_data(borrow, search_name=search_name, search_value=search_value)

    def add_user_command(self):
        print("add user")
        popup = EditPopup(window, table_name=self.utilisateurs_table_name,
                          fields=self.utilisateurs_table.columns,
                          action="add",
                          db_manager=self.db_manager,
                          on_close=self.fetch_refresh_users)

    def add_book_command(self):
        print("add book")
        popup = EditPopup(window, table_name=self.livres_table_name,
                          fields=self.livre_table.columns,
                          action="add",
                          db_manager=self.db_manager,
                          on_close=self.fetch_refresh_books)

    def add_borrow_command(self):
        print("add borrow")
        popup = EditPopup(window, table_name=self.emprunts_table_name,
                          fields=["startDate", "endDate", "user_id", "book_id"],
                          action="add",
                          db_manager=self.db_manager,
                          on_close=self.fetch_refresh_borrows)

    def edit_user_command(self):
        print("edit user")
        popup = EditPopup(window, table_name=self.utilisateurs_table_name,
                          fields=self.utilisateurs_table.columns,
                          default_values=self.utilisateurs_table.get_selection(),
                          action="update",
                          db_manager=self.db_manager,
                          on_close=self.fetch_refresh_users)

    def edit_book_command(self):
        print("edit book")
        popup = EditPopup(window, table_name=self.livres_table_name,
                          fields=self.livre_table.columns,
                          default_values=self.livre_table.get_selection(),
                          action="update",
                          db_manager=self.db_manager,
                          on_close=self.fetch_refresh_books)

    def edit_borrow_command(self):
        print("edit borrow")
        values = self.emprunts_table.get_selection()
        values_dict = dict(zip([string.lower() for string in self.utilisateurs_table.columns], values))

        print(values_dict)
        popup = EditPopup(window, table_name=self.emprunts_table_name,
                          fields=["startDate", "endDate", "user_id", "book_id"],
                          default_values=self.emprunts_table.get_selection(),
                          action="update",
                          db_manager=self.db_manager,
                          on_close=self.refresh_borrows)

    def build_condition(self, values, columns):
        values_dict = dict(zip([string.lower() for string in columns], values))
        conditions = [f"{str.lower(key)} = \'{value}\'" for key, value in values_dict.items()]
        where = " AND ".join(conditions)
        return where

    def delete_user_command(self):
        print("delete user")
        values = self.utilisateurs_table.get_selection()
        where = self.build_condition(values, self.utilisateurs_table.columns)
        self.db_manager.delete_data(table_name=self.utilisateurs_table_name, where=where)
        self.fetch_refresh_users()

    def delete_book_command(self):
        print("delete book")
        values = self.livre_table.get_selection()
        where = self.build_condition(values, self.livre_table.columns)
        self.db_manager.delete_data(table_name=self.livres_table_name, where=where)
        self.fetch_refresh_books()

    def delete_borrow_command(self):
        print("delete borrow")
        values = self.emprunts_table.get_selection()
        self.db_manager.delete_data(table_name=self.emprunts_table_name, where=f'borrow_id={values[0]}')
        self.fetch_refresh_borrows()

    def search_user(self):
        print("search user")
        self.refresh_users(search_name=self.search_utilisateurs_combobox.get(),
                           search_value=self.search_utilisateurs_entry.get())

    def search_book(self):
        print("search user")
        self.refresh_books(search_name=self.search_livres_combobox.get(),
                           search_value=self.search_utilisateurs_entry.get())

    def search_borrow(self):
        print("search borrow")
        self.refresh_borrows()

    def fetch_refresh_users(self):
        self.fetch_utilisateurs()
        self.search_user()

    def fetch_refresh_books(self):
        self.fetch_livres()
        self.search_book()

    def fetch_refresh_borrows(self):
        self.fetch_emprunts()
        self.search_borrow()


window = Tk()
window.title("Bibliothèque")
window.geometry('800x600')

mainWindow = MainWindow(window)
mainWindow.pack()

window.mainloop()
