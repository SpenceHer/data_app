from math import exp
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
import utils
import file_handling
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.formula.api as smf
import re
import data_manager
import seaborn as sns
import tkinter.font as tkFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import statsmodels.api as sm


# df = pd.read_excel(r"E:\new\master_8.1.23.xlsx")
df = pd.read_excel(r"C:\Users\smithsp\OneDrive - Oregon Health & Science University\Desktop\data_app\MIS_Open_Data_Coded_Stats_8-13-23.xlsx")
# Create the main window
main_window = tk.Tk()
main_window.title("DataFrame Editor")


main_window.wm_state('zoomed')


editing_content_frame = tk.Frame(main_window, bg="green")
editing_content_frame.pack(side="top", fill=tk.BOTH, expand=True)


regression_button = tk.Button(editing_content_frame, text="Comparison Table", font=("Arial", 36), command=lambda: CreateNewVariableClass(editing_content_frame, df))
regression_button.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)




class CreateNewVariableClass:
    def __init__(self, editing_content_frame, df):
        self.df = df
        self.editing_content_frame = editing_content_frame

        utils.remove_frame_widgets(self.editing_content_frame)

        self.column_selection_frame = tk.Frame(self.editing_content_frame, bg='hotpink')
        self.conditions_frame = tk.Frame(self.editing_content_frame, bg='purple')
        self.finalize_frame = tk.Frame(self.editing_content_frame, bg='red')

        self.create_column_selection_frame()
        self.create_conditions_frame()
        self.create_finalize_frame()

        self.switch_to_column_selection_frame()


    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    def create_column_selection_frame(self):

        self.selected_columns = []

        self.column_choice_frame = tk.Frame(self.column_selection_frame, bg='yellow')
        self.column_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.choose_columns_label = tk.Label(self.column_choice_frame, text="Choose columns to use", font=("Arial", 36))
        self.choose_columns_label.pack(side=tk.TOP, fill=tk.X)

        self.selection_frame = tk.Frame(self.column_choice_frame, bg='blue')
        self.selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



        self.available_columns_frame = tk.Frame(self.selection_frame, bg='green')
        self.available_columns_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
        self.transfer_buttons_frame = tk.Frame(self.selection_frame, bg='red')
        self.transfer_buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.selected_columns_frame = tk.Frame(self.selection_frame, bg='pink')
        self.selected_columns_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)




        # AVAILABLE COLUMNS FRAME
        self.available_column_search_var = tk.StringVar()
        self.available_column_search_var.trace("w", self.update_available_columns_listbox)
        self.search_entry = tk.Entry(self.available_columns_frame, textvariable=self.available_column_search_var, font=("Arial", 24))
        self.search_entry.pack(side=tk.TOP, pady=5)

        self.available_columns_listbox = tk.Listbox(self.available_columns_frame, selectmode=tk.MULTIPLE, font=("Arial", 24))
        self.available_columns_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5, padx=5)

        for column in sorted(self.df.columns, key=str.lower):
            self.available_columns_listbox.insert(tk.END, column)



        # TRANSFER BUTTONS FRAME
        self.transfer_right_button = tk.Button(self.transfer_buttons_frame, text=">>", command=self.transfer_right, font=("Arial", 50))
        self.transfer_right_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5, padx=5)

        self.transfer_left_button = tk.Button(self.transfer_buttons_frame, text="<<", command=self.transfer_left, font=("Arial", 50))
        self.transfer_left_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5, padx=5)



        # SELECTED COLUMNS FRAME
        self.selected_columns_label = tk.Label(self.selected_columns_frame, text="Selected Variables", font=("Arial", 24))
        self.selected_columns_label.pack(side=tk.TOP, pady=5)

        self.selected_columns_listbox = tk.Listbox(self.selected_columns_frame, selectmode=tk.MULTIPLE, font=("Arial", 24))
        self.selected_columns_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5, padx=5)



















        self.column_selection_menu_frame = tk.Frame(self.column_selection_frame, bg='lightgray')
        self.column_selection_menu_frame.pack(side=tk.TOP, fill=tk.X)

        self.advance_to_conditions_button = tk.Button(self.column_selection_menu_frame, command=self.switch_to_conditions_frame, text="Next", font=("Arial", 36))
        self.advance_to_conditions_button.pack(side=tk.RIGHT)


    def update_available_columns_listbox(self, *args):
        search_term = self.available_column_search_var.get().lower()
        self.available_columns_listbox.delete(0, tk.END)
        for column in sorted(self.df.columns, key=str.lower):
            if search_term in column.lower():
                self.available_columns_listbox.insert(tk.END, column)


    def transfer_right(self):
        selections = self.available_columns_listbox.curselection()
        selected_items = [self.available_columns_listbox.get(index) for index in selections]


        for item in selected_items:
            if item not in self.selected_columns:
                self.selected_columns_listbox.insert(tk.END, item)
                self.selected_columns.append(item)


        for index in reversed(selections):
            self.available_columns_listbox.delete(index)


    def transfer_left(self):
        selections = self.selected_columns_listbox.curselection()
        selected_items = [self.selected_columns_listbox.get(index) for index in selections]


        for item in selected_items:
            self.available_columns_listbox.insert(tk.END, item)
            self.selected_columns.remove(item)


        for index in reversed(selections):
            self.selected_columns_listbox.delete(index)




    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################


    def create_conditions_frame(self):
        self.condition_options_frame = tk.Frame(self.conditions_frame, bg='orange')
        self.condition_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)






        self.conditions_menu_frame = tk.Frame(self.conditions_frame, bg='lightgray')
        self.conditions_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_column_selection_button = tk.Button(self.conditions_menu_frame, command=self.switch_to_column_selection_frame, text="Back", font=("Arial", 36))
        self.return_to_column_selection_button.pack(side=tk.LEFT)

        self.advance_to_conditions_button = tk.Button(self.conditions_menu_frame, command=self.switch_to_finalize_frame, text="Next", font=("Arial", 36))
        self.advance_to_conditions_button.pack(side=tk.RIGHT)

        self.conditions_variable_name_label = tk.Label(self.conditions_menu_frame, text='Variable Name',font=("Arial", 36))
        self.conditions_variable_name_label.pack(side=tk.LEFT, fill=tk.X)


    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################

    def create_finalize_frame(self):
        # GRAPH DISPLAY FRAME
        self.finalize_display_frame = tk.Frame(self.finalize_frame, bg='purple')
        self.finalize_display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)




        # VARIABLE NAME FRAME
        self.column_name_frame = tk.Frame(self.finalize_frame, bg='green')
        self.column_name_frame.pack(side=tk.TOP, fill=tk.X)

        self.column_name_frame_label = tk.Label(self.column_name_frame, text="Name of new variable:", font=('Arial', 42), background='orange')
        self.column_name_frame_label.pack(side=tk.TOP, fill=tk.X)

        self.column_name_entry = tk.Entry(self.column_name_frame, font=('Arial', 24))
        self.column_name_entry.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)








        # MENU FRAME
        self.finalize_menu_frame = tk.Frame(self.finalize_frame, bg='lightgray')
        self.finalize_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_conditions_button = tk.Button(self.finalize_menu_frame, command=self.switch_to_conditions_frame, text="Back", font=("Arial", 36))
        self.return_to_conditions_button.pack(side=tk.LEFT)

        self.update_dataframe_button = tk.Button(self.finalize_menu_frame, command=self.update_dataframe, text="Update Dataframe", font=("Arial", 36))
        self.update_dataframe_button.pack(side=tk.RIGHT)

        self.finalize_variable_name_label = tk.Label(self.finalize_menu_frame, text='Variable Name',font=("Arial", 36))
        self.finalize_variable_name_label.pack(side=tk.LEFT, fill=tk.X)



    
    def switch_to_column_selection_frame(self):
        self.conditions_frame.pack_forget()
        self.finalize_frame.pack_forget()
        self.column_selection_frame.pack(fill=tk.BOTH, expand=True)

    def switch_to_conditions_frame(self):
        print(self.selected_columns)
        self.finalize_frame.pack_forget()
        self.column_selection_frame.pack_forget()
        self.conditions_frame.pack(fill=tk.BOTH, expand=True)

    def switch_to_finalize_frame(self):
        self.conditions_frame.pack_forget()
        self.column_selection_frame.pack_forget()
        self.finalize_frame.pack(fill=tk.BOTH, expand=True)


    def update_dataframe(self):
        return
















# Start the GUI event loop
main_window.mainloop()
