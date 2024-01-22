# Standard library imports
from cgitb import text
from math import exp
from pyexpat import features
import random
import re
from sre_parse import State
from statistics import LinearRegression
from telnetlib import STATUS
from tkinter import ANCHOR, Variable, filedialog, messagebox, simpledialog, ttk
import tkinter as tk
from tkinter import font
import tkinter.font as tkFont
from tkinter.font import Font

# Third party imports
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from scipy.stats import randint
from xgboost import XGBClassifier
import statsmodels.api as sm
import statsmodels.formula.api as smf
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Sklearn imports
from sklearn import model_selection
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Lasso, LogisticRegression
from sklearn.metrics import (accuracy_score, auc, brier_score_loss, classification_report, confusion_matrix, 
                             f1_score, mean_squared_error, precision_score, r2_score, recall_score, 
                             roc_auc_score, roc_curve, RocCurveDisplay)
from sklearn.model_selection import (GridSearchCV, KFold, StratifiedKFold, cross_val_predict, 
                                     cross_val_score, train_test_split, RandomizedSearchCV)
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.utils import resample

# Local application/library specific imports
import data_manager
import file_handling
import utils

########################

# TO DO NOTE
# REPLACE THE VARIABLE HANDLING FRAME IN THE MACHINE LEARNING WITH THE ONE IN REGRESSION
# USE THE MACHINE LEARNING CODE IN TESTER.PY TO IMPLEMENT MACHINE LEARNING

########################


def setup_visualize_tab(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame):
    df = data_manager.get_dataframe()
    if df is None:
        utils.show_message("Error", "Please open a file first.")
        return
    style.configure("file_button.TButton", background="gray")
    style.configure("dataframe_view_button.TButton", background="gray")
    style.configure("edit_button.TButton", background="gray")
    style.configure("visualize_button.TButton", background="white")
 
    utils.remove_frame_widgets(sub_button_frame)



    style.configure("comparison_table_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36, "bold"))
    comparison_table_button = ttk.Button(sub_button_frame, text="Comparison Table", style="comparison_table_button.TButton")
    comparison_table_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    comparison_table_button.config(command=lambda: ComparisonTableClass(visualize_content_frame, style))
 
    style.configure("regression_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36, "bold"))
    regression_button = ttk.Button(sub_button_frame, text="Regression", style="regression_button.TButton")
    regression_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    regression_button.config(command=lambda: RegressionAnalysisClass(visualize_content_frame, style))
 
    style.configure("create_plot_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36, "bold"))
    create_plot_button = ttk.Button(sub_button_frame, text="Create Plot", style="create_plot_button.TButton")
    create_plot_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    create_plot_button.config(command=lambda: CreatePlotClass(visualize_content_frame, style))
 
    style.configure("machine_learning_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36, "bold"))
    machine_learning_button = ttk.Button(sub_button_frame, text="Machine Learning", style="machine_learning_button.TButton")
    machine_learning_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    machine_learning_button.config(command=lambda: MachineLearningClass(visualize_content_frame, style))
 

    tab_dict = data_manager.get_tab_dict()

    try:
        if tab_dict['current_visualize_tab']:
            for tab in ['comparison_table', 'regression', 'create_plot', 'machine_learning']:
                if tab_dict['current_visualize_tab'] == tab:
                    style.configure(f"{tab_dict['current_visualize_tab']}_button.TButton", background="white")
                else:
                    style.configure(f"{tab}_button.TButton", background="gray")
    except:
        pass


    editing_content_frame.pack_forget()
    file_handling_content_frame.pack_forget()
    dataframe_content_frame.pack_forget()
    visualize_content_frame.pack(fill=tk.BOTH, expand=True)



    # UPDATE TAB IF DATAFRAME HAS BEEN CHANGED
    tab_update_status = data_manager.get_df_update_status_dict()

    if tab_update_status:
        if tab_update_status["visualize_tab"] == True:
            if "current_visualize_tab" in tab_dict:
                if tab_dict['current_visualize_tab']:
                    if tab_dict['current_visualize_tab'] == 'comparison_table':
                        ComparisonTableClass(visualize_content_frame, style)
                    elif tab_dict['current_visualize_tab'] == 'regression':
                        RegressionAnalysisClass(visualize_content_frame, style)
                    elif tab_dict['current_visualize_tab'] == 'comparison_table':
                        CreatePlotClass(visualize_content_frame, style)
                    elif tab_dict['current_visualize_tab'] == 'regression':
                        MachineLearningClass(visualize_content_frame, style)

                data_manager.add_df_update_status_to_dict("visualize_tab", False)



    visualize_content_frame.update_idletasks()





################################################################################################################
################################################################################################################
################################################################################################################

################################################################################################################
################################################################################################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
##############################################                    ##############################################
################################################################################################################
################################################################################################################

################################################################################################################
################################################################################################################
################################################################################################################


################################################################################################################
################################################################################################################
#                                                                                                              #
#                                               COMPARISON TABLE                                               #
#                                                                                                              #
################################################################################################################
################################################################################################################
 

class ComparisonTableClass:
    def __init__(self, visualize_content_frame, style):
        self.df = data_manager.get_dataframe()
        self.visualize_content_frame = visualize_content_frame

        self.style = style

        self.style.configure("comparison_table_button.TButton", background="white")
        self.style.configure("regression_button.TButton", background="gray")
        self.style.configure("create_plot_button.TButton", background="gray")
        self.style.configure("machine_learning_button.TButton", background="gray")

        data_manager.add_tab_to_tab_dict("current_visualize_tab", "comparison_table")


        self.selected_dependent_variable = data_manager.get_comp_tab_dep_var()
        self.selected_independent_variables = data_manager.get_comp_tab_ind_var_list()
        self.selected_percent_type = data_manager.get_comp_tab_percent_type()
        self.selected_data = data_manager.get_comp_tab_data_selection()
        self.variable_type_dict = data_manager.get_comp_tab_variable_type_dict()

        self.verify_saved_columns()

        utils.remove_frame_widgets(self.visualize_content_frame)

        self.error = False

        self.dependent_variable_frame = tk.Frame(self.visualize_content_frame, bg='beige')
        self.indedependent_variables_frame = tk.Frame(self.visualize_content_frame, bg='beige')
        self.variable_handling_frame = tk.Frame(self.visualize_content_frame, bg='beige')
        self.results_frame = tk.Frame(self.visualize_content_frame, bg='beige')



        self.create_dependent_variable_frame()
        self.create_independent_variables_frame()
        self.create_variable_handling_frame()
        self.create_results_frame()


        self.switch_to_dependent_variable_frame()






    def verify_saved_columns(self):
        if self.selected_dependent_variable not in self.df.columns:
            self.selected_dependent_variable = None

        for var in self.selected_independent_variables:
            if var not in self.df.columns:
                self.selected_independent_variables.remove(var)

################################################################################################################
################################################################################################################
################################################################################################################


    # CREATE DEPENDENT VARIABLE SELECTION FRAME

    def create_dependent_variable_frame(self):

        # MAIN CONTENT FRAME
        self.dependent_variable_options_frame = tk.Frame(self.dependent_variable_frame, bg='beige')
        self.dependent_variable_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # CONTENT TITLE LABEL
        self.choose_dependent_variable_label = tk.Label(self.dependent_variable_options_frame, text="Choose your DEPENDENT variable", font=("Arial", 36, "bold"), bg='beige')
        self.choose_dependent_variable_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.dependent_variable_options_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)

        # DEPENDENT VARIABLE SELECTION FRAME
        self.dependent_column_choice_frame = tk.Frame(self.dependent_variable_options_frame, bg='beige')
        self.dependent_column_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.dependent_search_var = tk.StringVar()
        self.dependent_search_var.trace("w", self.update_dependent_variable_listbox)
        self.dependent_var_search_entry = tk.Entry(self.dependent_column_choice_frame, textvariable=self.dependent_search_var, font=("Arial", 24))
        self.dependent_var_search_entry.pack(side=tk.TOP, pady=10)

        self.dependent_variable_listbox = tk.Listbox(self.dependent_column_choice_frame, selectmode=tk.SINGLE, font=("Arial", 24), exportselection=False)
        self.dependent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)

        for column in sorted(self.df.columns, key=str.lower):
            self.dependent_variable_listbox.insert(tk.END, column)

        self.dependent_variable_listbox.bind("<<ListboxSelect>>", self.on_dependent_variable_listbox_select)



        # NAVIGATION MENU
        self.dependent_variable_menu_frame = tk.Frame(self.dependent_variable_frame, bg='lightgray')
        self.dependent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.advance_to_independent_variables_button = tk.Button(self.dependent_variable_menu_frame, text="Next", command=self.switch_to_independent_variables_frame, font=("Arial", 36))
        self.advance_to_independent_variables_button.pack(side=tk.RIGHT)

        self.dependent_frame_dependent_label = tk.Label(self.dependent_variable_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.dependent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)


        if self.selected_dependent_variable:
            self.dependent_variable_listbox.selection_clear(0, tk.END)
            items = list(self.dependent_variable_listbox.get(0, tk.END))
            index = items.index(self.selected_dependent_variable)
            self.dependent_variable_listbox.selection_set(index)
            self.dependent_variable_listbox.yview(index)
            self.dependent_frame_dependent_label.config(text=f"Dependent Variable: {self.selected_dependent_variable}")


    def on_dependent_variable_listbox_select(self, event):
        if self.dependent_variable_listbox.curselection():
            self.selected_dependent_variable = self.dependent_variable_listbox.get(self.dependent_variable_listbox.curselection()[0])
            data_manager.set_comp_tab_dep_var(self.selected_dependent_variable)
            self.dependent_frame_dependent_label.config(text=f"Dependent Variable: {self.selected_dependent_variable}")


    def update_dependent_variable_listbox(self, *args):
        search_term = self.dependent_search_var.get().lower()
        self.dependent_variable_listbox.delete(0, tk.END)
        for column in self.df.columns:
            if search_term in column.lower():
                self.dependent_variable_listbox.insert(tk.END, column)




################################################################################################################
################################################################################################################
################################################################################################################


    # CREATE INDEPENDENT VARIABLE SELECTION FRAME

    def create_independent_variables_frame(self):

        # MAIN CONTENT FRAME
        self.independent_variable_options_frame = tk.Frame(self.indedependent_variables_frame, bg='beige')
        self.independent_variable_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # TITLE LABEL
        self.choose_independent_variables_label = tk.Label(self.independent_variable_options_frame, text="Choose your INDEPENDENT variables", font=("Arial", 36, "bold"), bg='beige')
        self.choose_independent_variables_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.independent_variable_options_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)


        # AVAILABLE INDEPENDENT VARIABLES SELECTION FRAME
        self.indedependent_variables_selection_frame = tk.Frame(self.independent_variable_options_frame, bg='beige')
        self.indedependent_variables_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.available_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='beige')
        self.available_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.available_independent_search_var = tk.StringVar()
        self.available_independent_search_var.trace("w", self.update_available_independent_variable_listbox)
        self.independent_var_search_entry = tk.Entry(self.available_independent_variables_frame, textvariable=self.available_independent_search_var, font=("Arial", 24))
        self.independent_var_search_entry.pack(side=tk.TOP, pady=10)

        self.available_independent_variable_listbox = tk.Listbox(self.available_independent_variables_frame, selectmode=tk.MULTIPLE, font=("Arial", 24))
        self.available_independent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)

        for column in sorted(self.df.columns, key=str.lower):
            self.available_independent_variable_listbox.insert(tk.END, column)


        # TRANSFER BUTTONS
        self.transfer_buttons_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='beige')
        self.transfer_buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.transfer_right_button = tk.Button(self.transfer_buttons_frame, text=">>>", command=self.transfer_right, font=("Arial", 48))
        self.transfer_right_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.transfer_left_button = tk.Button(self.transfer_buttons_frame, text="<<<", command=self.transfer_left, font=("Arial", 48))
        self.transfer_left_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.transfer_all_right_button = tk.Button(self.transfer_buttons_frame, text="Move All Right", command=self.transfer_all_right, font=("Arial", 36))
        self.transfer_all_right_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)

        self.transfer_all_left_button = tk.Button(self.transfer_buttons_frame, text="Clear Selection", command=self.transfer_all_left, font=("Arial", 36))
        self.transfer_all_left_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)



        # SELECTED INDEPENDENT VARIABLES FRAME
        self.selected_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='beige')
        self.selected_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.selected_independent_variables_label = tk.Label(self.selected_independent_variables_frame, text="Selected Variables", font=("Arial", 24))
        self.selected_independent_variables_label.pack(side=tk.TOP, pady=10)

        self.selected_independent_variable_listbox = tk.Listbox(self.selected_independent_variables_frame, selectmode=tk.MULTIPLE, font=("Arial", 24))
        self.selected_independent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)

        if len(self.selected_independent_variables) > 0:
            for var in self.selected_independent_variables:
                self.selected_independent_variable_listbox.insert(tk.END, var)
                self.available_independent_variable_listbox.selection_set(sorted(self.df.columns, key=str.lower).index(var))
            selections = self.available_independent_variable_listbox.curselection()
            for index in reversed(selections):
                self.available_independent_variable_listbox.delete(index)





        # TABLE OPTIONS
        self.table_options_frame = tk.Frame(self.independent_variable_options_frame, bg='beige')
        self.table_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        # ROW OR COLUMN PERCENTAGE SELECTION
        self.percentage_type_selection_frame = tk.Frame(self.table_options_frame, bg='beige')
        self.percentage_type_selection_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        def on_percentage_radio_button_selected():
            self.selected_percent_type = self.percentage_type_radio_var.get()
            data_manager.set_comp_tab_percent_type(self.selected_percent_type)

        if self.selected_percent_type:
            self.percentage_type_radio_var = tk.StringVar(value=self.selected_percent_type)
        else:
            self.percentage_type_radio_var = tk.StringVar(value="row")

        self.selected_percent_type = self.percentage_type_radio_var.get()

        self.row_percentage_radiobutton = tk.Radiobutton(self.percentage_type_selection_frame, text="Row Percentages", variable=self.percentage_type_radio_var, value="row", command=on_percentage_radio_button_selected, indicator=0, font=("Arial", 40), borderwidth=10)
        self.row_percentage_radiobutton.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.column_percentage_radiobutton = tk.Radiobutton(self.percentage_type_selection_frame, text="Column Percentages", variable=self.percentage_type_radio_var, value="column", command=on_percentage_radio_button_selected, indicator=0, font=("Arial", 40), borderwidth=10)
        self.column_percentage_radiobutton.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)




        # ALL DATA OR ONLY DATA COMPLETE SUBJECTS SELECTION
        self.data_choice_frame = tk.Frame(self.table_options_frame, bg='beige')
        self.data_choice_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        def on_data_choice_radio_button_selected():
            self.selected_data = self.data_choice_radio_var.get()
            data_manager.set_comp_tab_data_type(self.selected_data)

        if self.selected_data:
            self.data_choice_radio_var = tk.StringVar(value=self.selected_data)
        else:
            self.data_choice_radio_var = tk.StringVar(value="all data")

        self.selected_data = self.data_choice_radio_var.get()

        self.independent_data_radiobutton = tk.Radiobutton(self.data_choice_frame, text="All Data", variable=self.data_choice_radio_var, value="all data", command=on_data_choice_radio_button_selected, indicator=0, font=("Arial", 40), borderwidth=10)
        self.independent_data_radiobutton.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.dependent_data_radiobutton = tk.Radiobutton(self.data_choice_frame, text="Only Data-Complete Subjects", variable=self.data_choice_radio_var, value="data complete only", command=on_data_choice_radio_button_selected, indicator=0, font=("Arial", 40), borderwidth=10)
        self.dependent_data_radiobutton.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)





        # NAVIGATION MENU
        self.independent_variable_menu_frame = tk.Frame(self.indedependent_variables_frame, bg='lightgray')
        self.independent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_dependent_variable_frame_button = tk.Button(self.independent_variable_menu_frame, command=self.switch_to_dependent_variable_frame, text='Back', font=("Arial", 36))
        self.return_to_dependent_variable_frame_button.pack(side=tk.LEFT)

        self.advance_to_variable_handling_frame_button = tk.Button(self.independent_variable_menu_frame, command=self.switch_to_variable_handling_frame, text="Next", font=("Arial", 36))
        self.advance_to_variable_handling_frame_button.pack(side=tk.RIGHT)

        self.independent_frame_dependent_label = tk.Label(self.independent_variable_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.independent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)



    def update_available_independent_variable_listbox(self, *args):
        search_term = self.available_independent_search_var.get().lower()
        self.available_independent_variable_listbox.delete(0, tk.END)
        for column in sorted(self.df.columns, key=str.lower):
            if search_term in column.lower():
                self.available_independent_variable_listbox.insert(tk.END, column)


    def transfer_right(self):
        selections = self.available_independent_variable_listbox.curselection()
        selected_items = [self.available_independent_variable_listbox.get(index) for index in selections]

        for item in selected_items:
            if item not in self.selected_independent_variables:
                self.selected_independent_variable_listbox.insert(tk.END, item)
                self.selected_independent_variables.append(item)
                data_manager.add_variable_to_comp_tab_ind_var_list(item)

        for index in reversed(selections):
            self.available_independent_variable_listbox.delete(index)


    def transfer_all_right(self):

        for i in range(self.available_independent_variable_listbox.size()):
            self.available_independent_variable_listbox.selection_set(i)

        selections = self.available_independent_variable_listbox.curselection()
        selected_items = [self.available_independent_variable_listbox.get(index) for index in selections]

        for item in selected_items:
            self.selected_independent_variable_listbox.insert(tk.END, item)
            self.selected_independent_variables.append(item)

        for index in reversed(selections):
            self.available_independent_variable_listbox.delete(index)


    def transfer_left(self):
        selections = self.selected_independent_variable_listbox.curselection()
        selected_items = [self.selected_independent_variable_listbox.get(index) for index in selections]

        for item in selected_items:
            self.available_independent_variable_listbox.insert(tk.END, item)
            self.selected_independent_variables.remove(item)

        self.reorder_available_independent_variable_listbox_alphabetically()

        for index in reversed(selections):
            self.selected_independent_variable_listbox.delete(index)


    def transfer_all_left(self):

        for i in range(self.selected_independent_variable_listbox.size()):
            self.selected_independent_variable_listbox.selection_set(i)

        selections = self.selected_independent_variable_listbox.curselection()
        selected_items = [self.selected_independent_variable_listbox.get(index) for index in selections]

        for item in selected_items:
            self.available_independent_variable_listbox.insert(tk.END, item)
            self.selected_independent_variables.remove(item)

        self.reorder_available_independent_variable_listbox_alphabetically()

        for index in reversed(selections):
            self.selected_independent_variable_listbox.delete(index)


    def reorder_available_independent_variable_listbox_alphabetically(self):
        top_visible_index = self.available_independent_variable_listbox.nearest(0)
        top_visible_item = self.available_independent_variable_listbox.get(top_visible_index)

        items = list(self.available_independent_variable_listbox.get(0, tk.END))
        items = sorted(items, key=lambda x: x.lower())

        self.available_independent_variable_listbox.delete(0, tk.END)  # Clear the Listbox
        for item in items:
            self.available_independent_variable_listbox.insert(tk.END, item)

        if top_visible_index >= 0:
            index = items.index(top_visible_item)
            self.available_independent_variable_listbox.yview(index)

################################################################################################################
################################################################################################################
################################################################################################################

    # CREATE VARIABLE HANDLING FRAME

    def create_variable_handling_frame(self):

        # MAIN CONTENT FRAME
        self.variable_handling_label_frame = tk.Frame(self.variable_handling_frame)
        self.variable_handling_label_frame.pack(side=tk.TOP)

        # TITLE LABEL
        self.variable_handling_label = tk.Label(self.variable_handling_label_frame, text="Choose your variable types", font=("Arial", 36, "bold"), bg='beige')
        self.variable_handling_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.variable_handling_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)

        # VARIABLE HANDLING FRAME
        self.variable_handling_options_frame = tk.Frame(self.variable_handling_frame, bg='green')
        self.variable_handling_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=200, pady=50)

        def on_canvas_configure(event):
            self.variable_type_canvas.configure(scrollregion=self.variable_type_canvas.bbox("all"))

        self.variable_type_canvas = tk.Canvas(self.variable_handling_options_frame, bg='yellow')
        self.variable_type_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.variable_handling_options_frame, command=self.variable_type_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.variable_type_canvas.configure(yscrollcommand=self.scrollbar.set)


        self.scrollable_frame = tk.Frame(self.variable_type_canvas, bg='yellow')
        self.variable_type_canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        
        self.scrollable_frame.bind("<Configure>", on_canvas_configure)

        def on_mousewheel(event):
            self.variable_type_canvas.yview_scroll(-1 * (event.delta // 120), "units")

        self.variable_type_canvas.bind("<MouseWheel>", on_mousewheel)



        # NAVIGATION MENU
        self.variable_handling_menu_frame = tk.Frame(self.variable_handling_frame, bg='lightgray')
        self.variable_handling_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_independent_variable_frame_button = tk.Button(self.variable_handling_menu_frame, command=self.switch_to_independent_variables_frame, text='Back', font=("Arial", 36))
        self.return_to_independent_variable_frame_button.pack(side=tk.LEFT)

        self.view_results_button = tk.Button(self.variable_handling_menu_frame, command=self.switch_to_results_frame, text="View Results", font=("Arial", 36))
        self.view_results_button.pack(side=tk.RIGHT)

        self.variable_handling_menu_frame_dependent_label = tk.Label(self.variable_handling_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.variable_handling_menu_frame_dependent_label.pack(side=tk.RIGHT, expand=True)




    def handle_variables(self):

        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.variable_handling_frame.pack(fill=tk.BOTH, expand=True)

        utils.forget_frame_widgets(self.scrollable_frame)

        self.selected_variable_types = {}


        for value in list(self.selected_independent_variables):
            options_frame = tk.Frame(self.scrollable_frame, bg='yellow')
            options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5, padx=20, anchor=tk.W)

            if len(value) >= 20:
                value_string = value[0:19] + "..."
            else:
                value_string = value

            value_label = tk.Label(options_frame, text=value_string, font=("Arial", 28), bg='yellow', fg='black')
            value_label.pack(side=tk.LEFT, padx=5, pady=5)




            if value in self.variable_type_dict:
                var = tk.StringVar(value=self.variable_type_dict[value].get())
                self.variable_type_dict[value] = var

            else:
                var = tk.StringVar(value="Continuous")  # Set default value to "Continuous"
                self.variable_type_dict[value] = var

            continuous_variable_radiobutton = tk.Radiobutton(options_frame, text="Continuous", variable=var, value="Continuous", indicator=0, font=("Arial", 28), selectcolor="hotpink", borderwidth=10)
            continuous_variable_radiobutton.pack(side=tk.RIGHT, padx=5, pady=5)

            categorical_variable_radiobutton = tk.Radiobutton(options_frame, text="Categorical", variable=var, value="Categorical", indicator=0, font=("Arial", 28), selectcolor="hotpink", borderwidth=10)
            categorical_variable_radiobutton.pack(side=tk.RIGHT, padx=5, pady=5)

            both_variable_types_radiobutton = tk.Radiobutton(options_frame, text="Both", variable=var, value="Both", indicator=0, font=("Arial", 28), selectcolor="hotpink", borderwidth=10)
            both_variable_types_radiobutton.pack(side=tk.RIGHT, padx=5, pady=5)


            separator = ttk.Separator(self.scrollable_frame, orient="horizontal", style="Separator.TSeparator")
            separator.pack(fill="x", padx=5, pady=5)



################################################################################################################
################################################################################################################
################################################################################################################

    # CREATE RESULTS FRAME

    def create_results_frame(self):


        # MAIN CONTENT FRAME
        self.results_display_frame_container_frame = tk.Frame(self.results_frame, bg='beige')
        self.results_display_frame_container_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=150)

        self.results_display_frame = tk.Frame(self.results_display_frame_container_frame, bg='beige')
        self.results_display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        # NAVIGATION MENU
        self.results_menu_frame = tk.Frame(self.results_frame, bg='lightgray')
        self.results_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_variable_handling_frame_button = tk.Button(self.results_menu_frame, command=self.switch_to_variable_handling_frame, text='Back', font=("Arial", 36))
        self.return_to_variable_handling_frame_button.pack(side=tk.LEFT)

        self.results_frame_dependent_label = tk.Label(self.results_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.results_frame_dependent_label.pack(side=tk.RIGHT, expand=True)


    def apply_comparison_table_variable_selection(self):
        self.selected_variable_types.clear()
        
        for value, var in self.variable_type_dict.items():
            if value in self.selected_independent_variables:

                option = var.get()
                self.selected_variable_types[value] = option


    def create_comparison_table(self):
        self.apply_comparison_table_variable_selection()
        utils.remove_frame_widgets(self.results_display_frame)

        if self.selected_data == "all data":
            self.table_df = self.df[self.selected_independent_variables + [self.selected_dependent_variable]].copy()
            self.table_df = self.table_df.dropna(subset=self.selected_dependent_variable)
        
        if self.selected_data == "data complete only":
            self.table_df = self.df[self.selected_independent_variables + [self.selected_dependent_variable]].copy()
            self.table_df = self.table_df.dropna()

        self.unique_dependent_variable_values = sorted(self.table_df[self.selected_dependent_variable].unique())
        self.summary_table = []
        for independent_variable, option in self.selected_variable_types.items():
            if option == 'Continuous':

                self.clean_df = self.table_df[[independent_variable, self.selected_dependent_variable]].dropna()

                try:
                    self.clean_df[independent_variable] = self.clean_df[independent_variable].astype(float)
                    self.error = False

                    row1 = []
                    row2 = []
                    row3 = []

                    row1.append(f"{independent_variable}")
                    row1.extend([np.nan] * (len(self.unique_dependent_variable_values)))


                    # Run Stats for Continuous Variable
                    f_values = []
                    if len(self.unique_dependent_variable_values) > 2:
                        # More than two unique values, perform ANOVA
                        for value in self.unique_dependent_variable_values:
                            group = self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == value, independent_variable]
                            f_values.append(group)
                        _, p_value = stats.f_oneway(*f_values)
                        if p_value < 0.0001:
                            p_value = '< 0.0001'
                            row1.append(p_value)
                        else:
                            row1.append(f"{p_value:.4f}")
                    else:
                        for value in self.unique_dependent_variable_values:
                            group = self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == value, independent_variable]
                            f_values.append(group)
                        _, p_value = stats.ttest_ind(*f_values)

                        if p_value < 0.0001:
                            p_value = '< 0.0001'
                            row1.append(p_value)
                            row1.append(np.nan)
                        else:
                            row1.append(f"{p_value:.4f}")
                            row1.append(np.nan)

                    row2.append("  Mean (SD)")
                    for value in self.unique_dependent_variable_values:
                        row2.append(f"{self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == value, independent_variable].mean():.1f} ({self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == value, independent_variable].std():.1f})")
                    row2.append(np.nan)
                    if len(self.unique_dependent_variable_values) == 2:
                        row2.append(np.nan)

                    row3.append("  Range")
                    for value in self.unique_dependent_variable_values:
                        row3.append(f"{self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == value, independent_variable].min():.1f} - {self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == value, independent_variable].max():.1f}")

                    row3.append(np.nan)
                    if len(self.unique_dependent_variable_values) == 2:
                        row3.append(np.nan)

                    self.summary_table.append(row1)
                    self.summary_table.append(row2)
                    self.summary_table.append(row3)
                    self.summary_table.append([np.nan] * len(row1))

                except:
                    self.error = True
                    utils.show_message("Continuous variable change error", f"Cannot convert to continuous variable for: {independent_variable}")
                    return

            elif option == 'Categorical':

                self.clean_df = self.table_df[[independent_variable, self.selected_dependent_variable]].dropna()

                # Independent variable is categorical

                try:

                    observed = pd.crosstab(self.clean_df[independent_variable], self.clean_df[self.selected_dependent_variable])

                    # Calculate the odds ratio
                    odds_ratio = observed.iloc[1, 1] * observed.iloc[0, 0] / (observed.iloc[1, 0] * observed.iloc[0, 1])

                    a = observed.iloc[0, 0]
                    b = observed.iloc[0, 1]
                    c = observed.iloc[1, 0]
                    d = observed.iloc[1, 1]

                    # Calculate odds ratio
                    odds_ratio = (a * d) / (b * c)

                    # Calculate standard error of log odds ratio
                    se_ln_or = np.sqrt(1/a + 1/b + 1/c + 1/d)

                    # Calculate 95% confidence interval for log odds ratio
                    ci_lower_ln = np.log(odds_ratio) - 1.96 * se_ln_or
                    ci_upper_ln = np.log(odds_ratio) + 1.96 * se_ln_or

                    # Convert confidence interval back to odds ratio scale
                    ci_lower = np.exp(ci_lower_ln)
                    ci_upper = np.exp(ci_upper_ln)

                except:

                    odds_ratio = np.nan
                    ci_lower = np.nan
                    ci_upper = np.nan

                _, p_value, _, _ = stats.chi2_contingency(observed)

                row1 = []
                row1.append(f"{independent_variable}")
                row1.extend([np.nan] * len(self.unique_dependent_variable_values))
    
                if p_value < 0.0001:
                    p_value = '< 0.0001'
                    row1.append(p_value)
                else:
                    row1.append(f"{p_value:.4f}")

                if (len(self.unique_dependent_variable_values) == 2) & (len(self.clean_df[independent_variable].unique()) == 2):
                    row1.append(f"{odds_ratio:.2f} ({ci_lower:.2f} - {ci_upper:.2f})")

                elif (len(self.unique_dependent_variable_values) == 2) & (len(self.clean_df[independent_variable].unique()) != 2):
                    row1.append(np.nan)

                self.summary_table.append(row1)
    
                for index, row in observed.iterrows():

                    new_row = [f"  {index}"]
                    row_sum = row.sum()
                    column_sums = observed.sum(axis=0)

                    if self.selected_percent_type == "row":

                        for value in row:
                            new_row.append(f"{value} ({int(round(value/row_sum*100,0))}%)")

                    if self.selected_percent_type == "column":

                        for value, column_sum in zip(row, column_sums):
                            new_row.append(f"{value} ({int(round(value / column_sum * 100, 0))}%)")

                    new_row.append(np.nan)

                    if len(self.unique_dependent_variable_values) == 2:
                        new_row.append(np.nan)

                    self.summary_table.append(new_row)

                self.summary_table.append([np.nan] * len(row1))

            elif option == 'Both':

                self.clean_df = self.table_df[[independent_variable, self.selected_dependent_variable]].dropna()

                try:
                    self.clean_df[independent_variable] = self.clean_df[independent_variable].astype(float)
                    self.error = False

                    row1 = []
                    row2 = []
                    row3 = []

                    row1.append(f"{independent_variable}")
                    row1.extend([np.nan] * (len(self.unique_dependent_variable_values)))


                    # Run Stats for Continuous Variable
                    f_values = []
                    if len(self.unique_dependent_variable_values) > 2:
                        # More than two unique values, perform ANOVA
                        for value in self.unique_dependent_variable_values:
                            group = self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == value, independent_variable]
                            f_values.append(group)
                        _, p_value = stats.f_oneway(*f_values)
                        if p_value < 0.0001:
                            p_value = '< 0.0001'
                            row1.append(p_value)
                        else:
                            row1.append(f"{p_value:.4f}")
                    else:
                        for value in self.unique_dependent_variable_values:
                            group = self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == value, independent_variable]
                            f_values.append(group)
                        _, p_value = stats.ttest_ind(*f_values)

                        if p_value < 0.0001:
                            p_value = '< 0.0001'
                            row1.append(p_value)
                            row1.append(np.nan)
                        else:
                            row1.append(f"{p_value:.4f}")
                            row1.append(np.nan)

                    row2.append("  Mean (SD)")
                    for value in self.unique_dependent_variable_values:
                        row2.append(f"{self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == value, independent_variable].mean():.1f} ({self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == value, independent_variable].std():.1f})")
                    row2.append(np.nan)
                    if len(self.unique_dependent_variable_values) == 2:
                        row2.append(np.nan)

                    row3.append("  Range")
                    for value in self.unique_dependent_variable_values:
                        row3.append(f"{self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == value, independent_variable].min():.1f} - {self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == value, independent_variable].max():.1f}")

                    row3.append(np.nan)
                    if len(self.unique_dependent_variable_values) == 2:
                        row3.append(np.nan)

                    self.summary_table.append(row1)
                    self.summary_table.append(row2)
                    self.summary_table.append(row3)
                    self.summary_table.append([np.nan] * len(row1))

                except:
                    self.error = True
                    utils.show_message("Continuous variable change error", f"Cannot convert to continuous variable for: {independent_variable}")
                    return

                self.clean_df = self.table_df[[independent_variable, self.selected_dependent_variable]].dropna()

                # Independent variable is categorical

                try:

                    observed = pd.crosstab(self.clean_df[independent_variable], self.clean_df[self.selected_dependent_variable])

                    # Calculate the odds ratio
                    odds_ratio = observed.iloc[1, 1] * observed.iloc[0, 0] / (observed.iloc[1, 0] * observed.iloc[0, 1])

                    a = observed.iloc[0, 0]
                    b = observed.iloc[0, 1]
                    c = observed.iloc[1, 0]
                    d = observed.iloc[1, 1]

                    # Calculate odds ratio
                    odds_ratio = (a * d) / (b * c)

                    # Calculate standard error of log odds ratio
                    se_ln_or = np.sqrt(1/a + 1/b + 1/c + 1/d)

                    # Calculate 95% confidence interval for log odds ratio
                    ci_lower_ln = np.log(odds_ratio) - 1.96 * se_ln_or
                    ci_upper_ln = np.log(odds_ratio) + 1.96 * se_ln_or

                    # Convert confidence interval back to odds ratio scale
                    ci_lower = np.exp(ci_lower_ln)
                    ci_upper = np.exp(ci_upper_ln)

                except:

                    odds_ratio = np.nan
                    ci_lower = np.nan
                    ci_upper = np.nan

                _, p_value, _, _ = stats.chi2_contingency(observed)

                row1 = []
                row1.append(f"{independent_variable}")
                row1.extend([np.nan] * len(self.unique_dependent_variable_values))
    
                if p_value < 0.0001:
                    p_value = '< 0.0001'
                    row1.append(p_value)
                else:
                    row1.append(f"{p_value:.4f}")

                if (len(self.unique_dependent_variable_values) == 2) & (len(self.clean_df[independent_variable].unique()) == 2):
                    row1.append(f"{odds_ratio:.2f} ({ci_lower:.2f} - {ci_upper:.2f})")

                elif (len(self.unique_dependent_variable_values) == 2) & (len(self.clean_df[independent_variable].unique()) != 2):
                    row1.append(np.nan)

                self.summary_table.append(row1)
    
                for index, row in observed.iterrows():

                    new_row = [f"  {index}"]
                    row_sum = row.sum()
                    column_sums = observed.sum(axis=0)

                    if self.selected_percent_type == "row":

                        for value in row:
                            new_row.append(f"{value} ({int(round(value/row_sum*100,0))}%)")

                    if self.selected_percent_type == "column":

                        for value, column_sum in zip(row, column_sums):
                            new_row.append(f"{value} ({int(round(value / column_sum * 100, 0))}%)")

                    new_row.append(np.nan)

                    if len(self.unique_dependent_variable_values) == 2:
                        new_row.append(np.nan)

                    self.summary_table.append(new_row)

                self.summary_table.append([np.nan] * len(row1))



        columns = ['Characteristic']
        for value in self.unique_dependent_variable_values:
            count_of_value = len(self.table_df.loc[self.table_df[self.selected_dependent_variable] == value])
            columns.append(f"{value} (N = {count_of_value})")
            
        columns.append('p-value')
        if len(self.unique_dependent_variable_values) == 2:
            columns.append("Odds ratio")
        
        self.summary_df = pd.DataFrame(self.summary_table, columns=columns)


        utils.create_table(self.results_display_frame, self.summary_df)

        save_summary_button = tk.Button(self.results_display_frame, text="Save Table", command=lambda: file_handling.save_file(self.summary_df), font=("Arial", 36))
        save_summary_button.pack(side=tk.BOTTOM)




################################################################################################################
################################################################################################################
################################################################################################################


    # NAVIGATION MENU HANDLING FUNCTIONS

    def switch_to_dependent_variable_frame(self):

        self.variable_handling_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack(fill=tk.BOTH, expand=True)

        self.visualize_content_frame.update_idletasks()
        self.dependent_var_search_entry.focus_set()




    def switch_to_independent_variables_frame(self):
        if self.selected_dependent_variable == None:
            return
   
        self.variable_handling_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.indedependent_variables_frame.pack(fill=tk.BOTH, expand=True)

        self.dependent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.independent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.results_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.variable_handling_menu_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")

        self.visualize_content_frame.update_idletasks()
        self.independent_var_search_entry.focus_set()

        



    def switch_to_variable_handling_frame(self):
        if (self.selected_percent_type not in ["row", "column"]) | (self.selected_data not in ["all data","data complete only"]) | (len(self.selected_independent_variables) < 1):
            return
        else:
            self.handle_variables()
            self.visualize_content_frame.update_idletasks()


    def switch_to_results_frame(self):

        self.create_comparison_table()
        if self.error:
            return

        self.indedependent_variables_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.variable_handling_frame.pack_forget()
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        self.visualize_content_frame.update_idletasks()


################################################################################################################
################################################################################################################
################################################################################################################

################################################################################################################
################################################################################################################
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                    ########################################################################################
####                    ########################################################################################
####                    ########################################################################################
####                    ########################################################################################
####                    ########################################################################################
####                    ########################################################################################
####                    ########################################################################################
####                    ########################################################################################
####                    ########################################################################################
####                    ########################################################################################
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
################################################################################################################
################################################################################################################

################################################################################################################
################################################################################################################
################################################################################################################


################################################################################################################
################################################################################################################
#                                                                                                              #
#                                           MULTIVARIABLE REGRESSION                                           #
#                                                                                                              #
################################################################################################################
################################################################################################################


class RegressionAnalysisClass:

    def __init__(self, visualize_content_frame, style):
        self.df = data_manager.get_dataframe()

        self.visualize_content_frame = visualize_content_frame

        self.style = style

        self.style.configure("comparison_table_button.TButton", background="gray")
        self.style.configure("regression_button.TButton", background="white")
        self.style.configure("create_plot_button.TButton", background="gray")
        self.style.configure("machine_learning_button.TButton", background="gray")

        data_manager.add_tab_to_tab_dict("current_visualize_tab", "regression")

        self.selected_dependent_variable = data_manager.get_reg_tab_dep_var()
        self.selected_independent_variables = data_manager.get_reg_tab_ind_var_list()
        self.selected_regression = data_manager.get_reg_tab_selected_regression()

        self.verify_saved_columns()

        self.non_numeric_input_var_dict = data_manager.get_non_numeric_ind_dict()

        self.log_reg_target_value_var_dict = data_manager.get_reg_tab_log_reg_target_value_dict()
        self.log_reg_variable_type_dict = data_manager.get_log_reg_var_type_dict()
        self.log_reg_reference_variable_dict = data_manager.get_log_reg_ref_dict()

        utils.remove_frame_widgets(self.visualize_content_frame)


        self.dependent_variable_frame = tk.Frame(self.visualize_content_frame, bg='beige')
        self.indedependent_variables_frame = tk.Frame(self.visualize_content_frame, bg='beige')
        self.variable_handling_frame = tk.Frame(self.visualize_content_frame, bg='beige')
        self.results_frame = tk.Frame(self.visualize_content_frame, bg='beige')


        self.create_dependent_variable_frame()
        self.create_independent_variables_frame()
        self.create_variable_handling_frame()
        self.create_results_frame()


        self.switch_to_dependent_variable_frame()


    def verify_saved_columns(self):
        if self.selected_dependent_variable not in self.df.columns:
            self.selected_dependent_variable = None

        for var in self.selected_independent_variables:
            if var not in self.df.columns:
                self.selected_independent_variables.remove(var)

################################################################################################################
################################################################################################################
################################################################################################################

    # CREATE DEPENDENT VARIABLE SELECTION FRAME

    def create_dependent_variable_frame(self):

        # MAIN CONTENT FRAME
        self.dependent_variable_options_frame = tk.Frame(self.dependent_variable_frame, bg='beige')
        self.dependent_variable_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # CONTENT TITLE LABEL
        self.choose_dependent_variable_label = tk.Label(self.dependent_variable_options_frame, text="Choose your DEPENDENT variable", font=("Arial", 36, "bold"), bg='beige')
        self.choose_dependent_variable_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.dependent_variable_options_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)

        # DEPENDENT VARIABLE SELECTION FRAME
        self.dependent_column_choice_frame = tk.Frame(self.dependent_variable_options_frame, bg='beige')
        self.dependent_column_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.dependent_search_var = tk.StringVar()
        self.dependent_search_var.trace("w", self.update_dependent_variable_listbox)
        self.dependent_var_search_entry = tk.Entry(self.dependent_column_choice_frame, textvariable=self.dependent_search_var, font=("Arial", 24))
        self.dependent_var_search_entry.pack(side=tk.TOP, pady=10)

        self.dependent_variable_listbox = tk.Listbox(self.dependent_column_choice_frame, selectmode=tk.SINGLE, font=("Arial", 24), exportselection=False)
        self.dependent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)

        for column in sorted(self.df.columns, key=str.lower):
            self.dependent_variable_listbox.insert(tk.END, column)

        self.dependent_variable_listbox.bind("<<ListboxSelect>>", self.on_dependent_variable_listbox_select)



        # NAVIGATION MENU
        self.dependent_variable_menu_frame = tk.Frame(self.dependent_variable_frame, bg='lightgray')
        self.dependent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.advance_to_independent_variables_button = tk.Button(self.dependent_variable_menu_frame, text="Next", command=self.switch_to_independent_variables_frame, font=("Arial", 36))
        self.advance_to_independent_variables_button.pack(side=tk.RIGHT)

        self.dependent_frame_dependent_label = tk.Label(self.dependent_variable_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.dependent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)


        if self.selected_dependent_variable:
            self.dependent_variable_listbox.selection_clear(0, tk.END)
            items = list(self.dependent_variable_listbox.get(0, tk.END))
            index = items.index(self.selected_dependent_variable)
            self.dependent_variable_listbox.selection_set(index)
            self.dependent_variable_listbox.yview(index)
            self.dependent_frame_dependent_label.config(text=f"Dependent Variable: {self.selected_dependent_variable}")

            
    def on_dependent_variable_listbox_select(self, event):
        if self.dependent_variable_listbox.curselection():
            self.selected_dependent_variable = self.dependent_variable_listbox.get(self.dependent_variable_listbox.curselection()[0])
            data_manager.set_reg_tab_dep_var(self.selected_dependent_variable)
            self.dependent_frame_dependent_label.config(text=f"Dependent Variable: {self.selected_dependent_variable}")


    def update_dependent_variable_listbox(self, *args):
        search_term = self.dependent_search_var.get().lower()
        self.dependent_variable_listbox.delete(0, tk.END)
        for column in self.df.columns:
            if search_term in column.lower():
                self.dependent_variable_listbox.insert(tk.END, column)


################################################################################################################
################################################################################################################
################################################################################################################


    # CREATE INDEPENDENT VARIABLE SELECTION FRAME

    def create_independent_variables_frame(self):

        # MAIN CONTENT FRAME
        self.independent_variable_options_frame = tk.Frame(self.indedependent_variables_frame, bg='beige')
        self.independent_variable_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # TITLE LABEL
        self.choose_independent_variables_label = tk.Label(self.independent_variable_options_frame, text="Choose your INDEPENDENT variables", font=("Arial", 36, "bold"), bg='beige')
        self.choose_independent_variables_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.independent_variable_options_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)


        # AVAILABLE INDEPENDENT VARIABLES SELECTION FRAME
        self.indedependent_variables_selection_frame = tk.Frame(self.independent_variable_options_frame, bg='beige')
        self.indedependent_variables_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.available_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='beige')
        self.available_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.available_independent_search_var = tk.StringVar()
        self.available_independent_search_var.trace("w", self.update_available_independent_variable_listbox)
        self.independent_var_search_entry = tk.Entry(self.available_independent_variables_frame, textvariable=self.available_independent_search_var, font=("Arial", 24))
        self.independent_var_search_entry.pack(side=tk.TOP, pady=10)

        self.available_independent_variable_listbox = tk.Listbox(self.available_independent_variables_frame, selectmode=tk.MULTIPLE, font=("Arial", 24))
        self.available_independent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)

        for column in sorted(self.df.columns, key=str.lower):
            self.available_independent_variable_listbox.insert(tk.END, column)


        # TRANSFER BUTTONS
        self.transfer_buttons_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='beige')
        self.transfer_buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.transfer_right_button = tk.Button(self.transfer_buttons_frame, text=">>>", command=self.transfer_right, font=("Arial", 48))
        self.transfer_right_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.transfer_left_button = tk.Button(self.transfer_buttons_frame, text="<<<", command=self.transfer_left, font=("Arial", 48))
        self.transfer_left_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.transfer_all_right_button = tk.Button(self.transfer_buttons_frame, text="Move All Right", command=self.transfer_all_right, font=("Arial", 36))
        self.transfer_all_right_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)

        self.transfer_all_left_button = tk.Button(self.transfer_buttons_frame, text="Clear Selection", command=self.transfer_all_left, font=("Arial", 36))
        self.transfer_all_left_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)



        # SELECTED INDEPENDENT VARIABLES FRAME
        self.selected_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='beige')
        self.selected_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.selected_independent_variables_label = tk.Label(self.selected_independent_variables_frame, text="Selected Variables", font=("Arial", 24))
        self.selected_independent_variables_label.pack(side=tk.TOP, pady=10)

        self.selected_independent_variable_listbox = tk.Listbox(self.selected_independent_variables_frame, selectmode=tk.MULTIPLE, font=("Arial", 24))
        self.selected_independent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)

        if len(self.selected_independent_variables) > 0:
            for var in self.selected_independent_variables:
                self.selected_independent_variable_listbox.insert(tk.END, var)
                self.available_independent_variable_listbox.selection_set(sorted(self.df.columns, key=str.lower).index(var))
            selections = self.available_independent_variable_listbox.curselection()
            for index in reversed(selections):
                self.available_independent_variable_listbox.delete(index)


        # MODEL OPTIONS
        self.regression_type_selection_frame = tk.Frame(self.independent_variable_options_frame, bg='beige')
        self.regression_type_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)






        # MODEL TYPE SELECTION
        def on_selected_regression_radio_button_selected():
            self.selected_regression = self.regression_type_radio_var.get()
            data_manager.set_reg_tab_selected_regression(self.selected_regression)

        if self.selected_regression:
            self.regression_type_radio_var = tk.StringVar(value=self.selected_regression)
        else:
            self.regression_type_radio_var = tk.StringVar(value="logistic")

        self.selected_regression = self.regression_type_radio_var.get()

        self.logistic_regression_radiobutton = tk.Radiobutton(self.regression_type_selection_frame, text="Logistic Regression", variable=self.regression_type_radio_var, value="logistic", command=on_selected_regression_radio_button_selected, indicator = 0,font=("Arial", 40), borderwidth=10)
        self.logistic_regression_radiobutton.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.linear_regression_radiobutton = tk.Radiobutton(self.regression_type_selection_frame, text="Linear Regression", variable=self.regression_type_radio_var, value="linear", command=on_selected_regression_radio_button_selected, indicator = 0, font=("Arial", 40), borderwidth=10)
        self.linear_regression_radiobutton.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)




        # NAVIGATION MENU
        self.independent_variable_menu_frame = tk.Frame(self.indedependent_variables_frame, bg='lightgray')
        self.independent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_dependent_variable_frame_button = tk.Button(self.independent_variable_menu_frame, command=self.switch_to_dependent_variable_frame, text='Back', font=("Arial", 36))
        self.return_to_dependent_variable_frame_button.pack(side=tk.LEFT)

        self.advance_to_variable_handling_frame_button = tk.Button(self.independent_variable_menu_frame, command=self.switch_to_variable_handling_frame, text="Next", font=("Arial", 36))
        self.advance_to_variable_handling_frame_button.pack(side=tk.RIGHT)

        self.independent_frame_dependent_label = tk.Label(self.independent_variable_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.independent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)


    def update_available_independent_variable_listbox(self, *args):
        search_term = self.available_independent_search_var.get().lower()
        self.available_independent_variable_listbox.delete(0, tk.END)
        for column in sorted(self.df.columns, key=str.lower):
            if search_term in column.lower():
                self.available_independent_variable_listbox.insert(tk.END, column)


    def transfer_right(self):
        selections = self.available_independent_variable_listbox.curselection()
        selected_items = [self.available_independent_variable_listbox.get(index) for index in selections]

        for item in selected_items:
            if item not in self.selected_independent_variables:
                self.selected_independent_variable_listbox.insert(tk.END, item)
                self.selected_independent_variables.append(item)
                data_manager.add_variable_to_reg_tab_ind_var_list(item)

        for index in reversed(selections):
            self.available_independent_variable_listbox.delete(index)


    def transfer_all_right(self):

        for i in range(self.available_independent_variable_listbox.size()):
            self.available_independent_variable_listbox.selection_set(i)

        selections = self.available_independent_variable_listbox.curselection()
        selected_items = [self.available_independent_variable_listbox.get(index) for index in selections]

        for item in selected_items:
            self.selected_independent_variable_listbox.insert(tk.END, item)
            self.selected_independent_variables.append(item)

        for index in reversed(selections):
            self.available_independent_variable_listbox.delete(index)


    def transfer_left(self):
        selections = self.selected_independent_variable_listbox.curselection()
        selected_items = [self.selected_independent_variable_listbox.get(index) for index in selections]

        for item in selected_items:
            self.available_independent_variable_listbox.insert(tk.END, item)
            self.selected_independent_variables.remove(item)

        self.reorder_available_independent_variable_listbox_alphabetically()

        for index in reversed(selections):
            self.selected_independent_variable_listbox.delete(index)


    def transfer_all_left(self):

        for i in range(self.selected_independent_variable_listbox.size()):
            self.selected_independent_variable_listbox.selection_set(i)

        selections = self.selected_independent_variable_listbox.curselection()
        selected_items = [self.selected_independent_variable_listbox.get(index) for index in selections]

        for item in selected_items:
            self.available_independent_variable_listbox.insert(tk.END, item)
            self.selected_independent_variables.remove(item)

        self.reorder_available_independent_variable_listbox_alphabetically()

        for index in reversed(selections):
            self.selected_independent_variable_listbox.delete(index)


    def reorder_available_independent_variable_listbox_alphabetically(self):
        top_visible_index = self.available_independent_variable_listbox.nearest(0)
        top_visible_item = self.available_independent_variable_listbox.get(top_visible_index)

        items = list(self.available_independent_variable_listbox.get(0, tk.END))
        items = sorted(items, key=lambda x: x.lower())

        self.available_independent_variable_listbox.delete(0, tk.END)  # Clear the Listbox
        for item in items:
            self.available_independent_variable_listbox.insert(tk.END, item)

        if top_visible_index >= 0:
            index = items.index(top_visible_item)
            self.available_independent_variable_listbox.yview(index)


################################################################################################################
################################################################################################################
################################################################################################################


    # CREATE VARIABLE HANDLING FRAME

    def create_variable_handling_frame(self):
        # MAIN CONTENT FRAME
        self.variable_handling_label_frame = tk.Frame(self.variable_handling_frame)
        self.variable_handling_label_frame.pack(side=tk.TOP)

        # TITLE LABEL
        self.variable_handling_label = tk.Label(self.variable_handling_label_frame, text="", font=("Arial", 36, "bold"), bg='beige')
        self.variable_handling_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.variable_handling_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)

        # VARIABLE HANDLING FRAME
        self.variable_handling_options_frame = tk.Frame(self.variable_handling_frame, bg='green')
        self.variable_handling_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=200, pady=50)

        def on_canvas_configure(event):
            self.variable_type_canvas.configure(scrollregion=self.variable_type_canvas.bbox("all"))

        self.variable_type_canvas = tk.Canvas(self.variable_handling_options_frame, bg='yellow')
        self.variable_type_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.variable_handling_options_frame, command=self.variable_type_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.variable_type_canvas.configure(yscrollcommand=self.scrollbar.set)


        self.scrollable_frame = tk.Frame(self.variable_type_canvas, bg='yellow')
        self.variable_type_canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)

        self.scrollable_frame.bind("<Configure>", on_canvas_configure)

        def on_mousewheel(event):
            self.variable_type_canvas.yview_scroll(-1 * (event.delta // 120), "units")

        self.variable_type_canvas.bind("<MouseWheel>", on_mousewheel)



        # NAVIGATION MENU FRAME
        self.variable_handling_menu_frame = tk.Frame(self.variable_handling_frame, bg='lightgray')
        self.variable_handling_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_independent_variable_frame_button = tk.Button(self.variable_handling_menu_frame, command=self.switch_to_independent_variables_frame, text='Back', font=("Arial", 36))
        self.return_to_independent_variable_frame_button.pack(side=tk.LEFT)

        self.view_results_button = tk.Button(self.variable_handling_menu_frame, command=self.switch_to_results_frame, text="View Results", font=("Arial", 36))
        self.view_results_button.pack(side=tk.RIGHT)

        self.variable_handling_menu_frame_dependent_label = tk.Label(self.variable_handling_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.variable_handling_menu_frame_dependent_label.pack(side=tk.RIGHT, expand=True)


    ################################################################################################################

    # HANDLE VARIABLES FOR LINEAR REGRESSION
        
    def handle_variables_linear_regression(self):

        self.variable_handling_label.configure(text="Change Non-Numeric Values in The Following Independent Variables")

        utils.remove_frame_widgets(self.scrollable_frame)

        self.clean_df = self.df[self.selected_independent_variables + [self.selected_dependent_variable]].copy().dropna()

        # DETERMINE NON-NUMERIC VARIABLES
        self.non_numeric_columns = []

        self.selected_options = {}

        for independent_variable in self.selected_independent_variables:
            try:
                self.clean_df[independent_variable] = self.clean_df[independent_variable].astype(float)
            except:
                self.non_numeric_columns.append(independent_variable)

        if len(self.non_numeric_columns) == 0:
            proceed_to_results_label = tk.Label(self.scrollable_frame, text="No Non-Numeric Variables. Click VIEW RESULTS", font=("Arial", 28, "bold"), bg='yellow')
            proceed_to_results_label.pack(side=tk.TOP, fill=tk.X, pady=5, padx=20)

        # HANDLE NON-NUMERIC VARIABLES
        for variable in self.non_numeric_columns:

            separator = ttk.Separator(self.scrollable_frame, orient="horizontal", style="Separator.TSeparator")
            separator.pack(fill=tk.X, padx=5, pady=5)

            options_frame = tk.Frame(self.scrollable_frame, bg='yellow')
            options_frame.pack(side=tk.TOP, fill=tk.X, pady=5, padx=20)


            if len(variable) > 20:
                variable_string = variable[0:19] + "..."
            else:
                variable_string = variable

            variable_label = tk.Label(options_frame, text=variable_string, font=("Arial", 28), bg='yellow', fg='black')
            variable_label.pack(side=tk.TOP)


            non_numeric_values = []

            for value in self.clean_df[variable].unique():
                if isinstance(value, str) and not value.isdigit():
                    non_numeric_values.append(value)
            
            for value in non_numeric_values:

                value_frame = tk.Frame(options_frame, bg='yellow')
                value_frame.pack(side=tk.TOP, fill=tk.X, expand=True)

                if variable in self.non_numeric_input_var_dict:
                    if value in self.non_numeric_input_var_dict[variable]:
                        input_var = self.non_numeric_input_var_dict[variable][value]
                            
                        user_input_var = tk.StringVar(value=input_var)
                        data_manager.add_variable_to_non_numeric_ind_dict(variable, value, input_var)
                    else:
                        input_var = ""
                        user_input_var = tk.StringVar(value=input_var)
                        data_manager.add_variable_to_non_numeric_ind_dict(variable, value, input_var)
                else:
                    input_var = ""
                    user_input_var = tk.StringVar()
                    data_manager.add_variable_to_non_numeric_ind_dict(variable, value, input_var)



                input_entry = tk.Entry(value_frame, textvariable=user_input_var, font=("Arial", 28), width=10)
                input_entry.pack(side=tk.LEFT)

                value_label = tk.Label(value_frame, text=value, font=("Arial", 28), bg='yellow', fg='black')
                value_label.pack(side=tk.LEFT)

                # Bind the entry widget to an event
                input_entry.bind("<KeyRelease>", lambda event, var=variable, val=value: self.on_key_release(event, var, val))


    def on_key_release(self, event, variable, value):
        # Update the dictionary with the entry's current value
        data_manager.add_variable_to_non_numeric_ind_dict(variable, value, event.widget.get())


    def apply_linear_regression_variable_selection(self):
        for variable in self.selected_independent_variables:

            if variable in self.non_numeric_columns:

                non_numeric_values = [] 

                for value in self.clean_df[variable].unique():
                    if isinstance(value, str) and not value.isdigit():
                        non_numeric_values.append(value)

                for value in non_numeric_values:

                    input_var = self.non_numeric_input_var_dict[variable][value]

                    try:
                        self.clean_df.loc[self.clean_df[variable] == value, variable] = int(input_var)

                    except:
                        utils.show_message("error message", f"Make sure all values are NUMERICAL")
                        raise

                self.clean_df[variable] = self.clean_df[variable].astype(float)


    ################################################################################################################

    # HANDLE VARIABLES FOR LOGISTIC REGRESSION

    def handle_variables_logistic_regression(self):

        self.variable_handling_label.configure(text="Logistic Regression Variable Settings")

        utils.remove_frame_widgets(self.scrollable_frame)

        
        self.clean_df = self.df[self.selected_independent_variables + [self.selected_dependent_variable]].copy()
        self.clean_df.dropna(inplace=True)


        if len(self.clean_df) < 1:
            first_column_with_missing_data = self.df.columns[self.df.isnull().all()].tolist()[0]
            utils.show_message("error message", f"The Variable, {first_column_with_missing_data.upper()}, has no data")
            raise utils.MyCustomError("error")



        # TARGET VALUE FRAME
        self.dependent_variable_handling_frame = tk.Frame(self.scrollable_frame, bg='yellow')
        self.dependent_variable_handling_frame.grid(row=0, column=0, sticky="nsew")


        self.dependent_variable_handling_frame_label = tk.Label(self.dependent_variable_handling_frame, text='Choose Target Value', font=('Arial', 32), bg='yellow')
        self.dependent_variable_handling_frame_label.pack(side=tk.TOP)

        def on_dependent_variable_value_selected():
            data_manager.add_variable_to_reg_tab_log_reg_target_value_dict(self.selected_dependent_variable, self.log_reg_target_value_var)

        if self.selected_dependent_variable in self.log_reg_target_value_var_dict:
            self.log_reg_target_value_var = tk.StringVar(value=self.log_reg_target_value_var_dict[self.selected_dependent_variable].get())
        else:
            self.log_reg_target_value_var = tk.StringVar(value=f"{self.clean_df[self.selected_dependent_variable].unique()[0]}")
            self.log_reg_target_value_var_dict[self.selected_dependent_variable] = self.log_reg_target_value_var
            

        self.dependent_variable_unique_value_1 = tk.Radiobutton(self.dependent_variable_handling_frame, text=f"{self.clean_df[self.selected_dependent_variable].unique()[0]}", variable=self.log_reg_target_value_var, value=f"{self.clean_df[self.selected_dependent_variable].unique()[0]}", command=on_dependent_variable_value_selected, indicator=0, font=("Arial", 40), selectcolor="hotpink", borderwidth=10)
        self.dependent_variable_unique_value_1.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.dependent_variable_unique_value_2 = tk.Radiobutton(self.dependent_variable_handling_frame, text=f"{self.clean_df[self.selected_dependent_variable].unique()[1]}", variable=self.log_reg_target_value_var, value=f"{self.clean_df[self.selected_dependent_variable].unique()[1]}", command=on_dependent_variable_value_selected, indicator=0, font=("Arial", 40), selectcolor="hotpink", borderwidth=10)
        self.dependent_variable_unique_value_2.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)




        # VARIABLE TYPES AND REFERENCE VALUES FRAME
        self.independent_variable_handling_frame = tk.Frame(self.scrollable_frame, bg='yellow')
        self.independent_variable_handling_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)


        self.independent_variable_handling_frame_label = tk.Label(self.independent_variable_handling_frame, text='Choose variable types and reference values', font=('Arial', 32), bg='yellow', fg='black')
        self.independent_variable_handling_frame_label.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        self.variable_name_label = tk.Label(self.independent_variable_handling_frame, text='Variable', font=Font(family="Arial", size=28, weight="bold", underline=True), bg='yellow', fg='black')  
        self.variable_name_label.grid(row=1, column=0, padx=5, pady=5)

        self.variable_type_label = tk.Label(self.independent_variable_handling_frame, text='Variable Type', font=Font(family="Arial", size=28, weight="bold", underline=True), bg='yellow', fg='black')  
        self.variable_type_label.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        self.reference_variable_label = tk.Label(self.independent_variable_handling_frame, text='Reference Value', font=Font(family="Arial", size=28, weight="bold", underline=True), bg='yellow', fg='black')  
        self.reference_variable_label.grid(row=1, column=3, padx=5, pady=5)

        separator = ttk.Separator(self.independent_variable_handling_frame, orient="horizontal", style="Separator.TSeparator")
        separator.grid(row=2, column=0, columnspan=4, sticky="ew", padx=5, pady=5)




        self.unique_values = list(self.clean_df[self.selected_independent_variables].columns)
        self.selected_options = {}


        row_count = 3
        
        for variable in self.selected_independent_variables:

            if len(variable) > 20:
                variable_string = variable[0:19] + "..."
            else:
                variable_string = variable

            variable_label = tk.Label(self.independent_variable_handling_frame, text=variable_string, font=("Arial", 28), bg='yellow', fg='black')
            variable_label.grid(row=row_count, column=0, padx=5, pady=5)

            if variable in self.log_reg_variable_type_dict:
                var = tk.StringVar(value=self.log_reg_variable_type_dict[variable].get())
                self.log_reg_variable_type_dict[variable] = var

            else:
                var = tk.StringVar(value="Continuous")  # Set default value to "Continuous"
                self.log_reg_variable_type_dict[variable] = var

            continuous_variable_button = tk.Radiobutton(self.independent_variable_handling_frame, text="Continuous", variable=var, value="Continuous", indicator=0, font=("Arial", 28), selectcolor="hotpink", borderwidth=10)
            continuous_variable_button.grid(row=row_count, column=1, padx=5, pady=5)

            categorical_variable_button = tk.Radiobutton(self.independent_variable_handling_frame, text="Categorical", variable=var, value="Categorical", indicator=0, font=("Arial", 28), selectcolor="hotpink", borderwidth=10)
            categorical_variable_button.grid(row=row_count, column=2, padx=5, pady=5)




            reference_value_combobox = ttk.Combobox(self.independent_variable_handling_frame, state=tk.DISABLED, font=("Arial", 28))
            values = [str(val) for val in self.clean_df[variable].unique()]
            reference_value_combobox['values'] = values
            reference_value_combobox.grid(row=row_count, column=3, padx=5, pady=5)
            reference_value_combobox.bind("<<ComboboxSelected>>", lambda event, combobox=reference_value_combobox, variable=variable: self.on_combobox_select(combobox, variable))


            # Bind the state of the reference_value_combobox to the selection of 'Categorical' radio button
            continuous_variable_button.bind("<Button-1>", lambda event, combobox=reference_value_combobox: combobox.configure(state=tk.DISABLED))

            if variable in self.log_reg_reference_variable_dict:
                categorical_variable_button.bind("<Button-1>", lambda event, combobox=reference_value_combobox: combobox.configure(state="readonly"))
                reference_value_combobox.set(self.log_reg_reference_variable_dict[variable])
            else:
                categorical_variable_button.bind("<Button-1>", lambda event, combobox=reference_value_combobox: combobox.configure(state="readonly"))


            if var.get() == "Categorical":
                reference_value_combobox.configure(state="readonly")
                if variable in self.log_reg_reference_variable_dict:
                    reference_value_combobox.set(self.log_reg_reference_variable_dict[variable])


            separator_2 = ttk.Separator(self.independent_variable_handling_frame, orient="horizontal", style="Separator.TSeparator")
            separator_2.grid(row=row_count+1, column=0, columnspan=4, sticky="ew", padx=5, pady=5)

            row_count += 2


    def on_combobox_select(self, combobox, variable):
        selected_value = combobox.get()
        data_manager.add_variable_to_log_reg_ref_dict(variable, selected_value)


    def apply_logistic_regression_variable_selection(self):

        # MAKE VALUES OF DEPENDENT VARIABLE BINARY
        selected_target_var = self.log_reg_target_value_var.get()
        self.clean_df.loc[self.clean_df[self.selected_dependent_variable] != selected_target_var, self.selected_dependent_variable] = 0
        self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == selected_target_var, self.selected_dependent_variable] = 1
        

        self.selected_options.clear()

        for variable in self.selected_independent_variables:

            # Get variable type of the current independent variable
            variable_type = self.log_reg_variable_type_dict[variable].get()
            
            if variable_type == "Continuous":
                try:
                    self.clean_df[variable] = self.clean_df[variable].astype(float)
                except:
                    utils.show_message("Error", f"Cannot convert to continuous variable for: {variable}")
                    raise
            # Add the variable type to the current variable type dict
            self.selected_options[variable] = variable_type

            if variable_type == "Categorical":
                try:
                    input_value = self.log_reg_reference_variable_dict[variable]
                except:
                    utils.show_message("Error", f"No reference value for: {variable}")
            
                column_data_type = self.df[variable].dtype
                if column_data_type == 'object':
                    self.log_reg_reference_variable_dict[variable] = input_value  # Treat as string
                elif column_data_type == 'int64':
                    input_value = int(input_value)  # Convert to int
                    self.log_reg_reference_variable_dict[variable] = input_value
                elif column_data_type == 'float64':
                    input_value = float(input_value)  # Convert to float
                    self.log_reg_reference_variable_dict[variable] = input_value
            

################################################################################################################
################################################################################################################
################################################################################################################


    # CREATE RESULTS FRAME

    def create_results_frame(self):

        # MAIN CONTENT FRAME
        self.results_display_frame_container_frame = tk.Frame(self.results_frame, bg='beige')
        self.results_display_frame_container_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=150)

        self.results_display_frame = tk.Frame(self.results_display_frame_container_frame, bg='beige')
        self.results_display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        # NAVIGATION MENU
        self.results_menu_frame = tk.Frame(self.results_frame, bg='lightgray')
        self.results_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_independent_variable_frame_button = tk.Button(self.results_menu_frame, command=self.switch_to_variable_handling_frame, text='Back', font=("Arial", 36))
        self.return_to_independent_variable_frame_button.pack(side=tk.LEFT)

        self.results_frame_dependent_label = tk.Label(self.results_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.results_frame_dependent_label.pack(side=tk.RIGHT, expand=True)


    def run_analysis(self):
        utils.remove_frame_widgets(self.results_display_frame)

        if self.selected_regression == "logistic":
            self.logistic_regression()

        elif self.selected_regression == "linear":
            self.linear_regression()


    def logistic_regression(self):
        self.apply_logistic_regression_variable_selection()
        model_string = f"{self.selected_dependent_variable} ~ "
        self.clean_df[self.selected_dependent_variable] = self.clean_df[self.selected_dependent_variable].astype(int)


        for variable, data_type in self.selected_options.items():

            if variable in self.selected_independent_variables:
                if data_type == 'Continuous':
                    model_string = model_string + f"{variable} + "
                elif data_type == 'Categorical':
                    self.clean_df[variable] = self.clean_df[variable].astype(str)
                    model_string = model_string + f"C({variable}, Treatment('{self.log_reg_reference_variable_dict[variable]}')) + "


        model_string = model_string.rstrip(" +")

        model = smf.logit(model_string, data=self.clean_df)
        results = model.fit(method='bfgs', maxiter=1000)
   
        p_values = results.pvalues[1:]
        p_values = p_values.astype(str)

        for i in range(len(p_values)):

            if float(p_values.iloc[i]) < 0.0001:
                p_values.iloc[i] = "< 0.0001"
            else:
                p_values.iloc[i] = str(round(float(p_values.iloc[i]), 4))
   


        # Print out the results
        coefs = pd.DataFrame({
            'coef': np.round(results.params.values[1:],3),
            'p_value': p_values,
            'odds ratio': np.round(np.exp(results.params.values[1:]),2),
            'CI_low': round(np.exp(results.conf_int()[0])[1:],2),
            'CI_high': round(np.exp(results.conf_int()[1])[1:],2)
        })

        coefs['CI_high'] = coefs['CI_high'].astype(str)
        coefs['CI_low'] = coefs['CI_high'].astype(str)

        coefs = coefs.reset_index().rename(columns={'index': 'Characteristic'})
        for i in range(len(coefs['Characteristic'])):
            variable_string = coefs['Characteristic'].iloc[i]
            if variable_string[0] == "C":
                column_string = re.search(r'C\((.*?),', variable_string).group(1)
                reference_value = re.search(r"\[T\.(.*?)\]", variable_string).group(1)
                new_value = column_string + f" ({reference_value})"
                coefs.loc[i, 'Characteristic'] = new_value
            if float(coefs.loc[i, 'CI_high']) > 50000:
                coefs.loc[i, 'CI_high'] = 'inf'
            if float(coefs.loc[i, 'CI_low']) < -50000:
                coefs.loc[i, 'CI_low'] = '-inf'


        utils.create_table(self.results_display_frame, coefs)


        summary_text = tk.Text(self.results_display_frame, height=20, width=120)
        summary_text.pack(side=tk.TOP)
        summary_text.insert(tk.END, str(results.summary()))


        save_summary_button = ttk.Button(self.results_display_frame, text="Save Table", command=lambda: file_handling.save_file(coefs))
        save_summary_button.pack()


    def linear_regression(self):
        self.apply_linear_regression_variable_selection()

        x = self.clean_df[self.selected_independent_variables]
        y = self.clean_df[self.selected_dependent_variable]


        x = sm.add_constant(x)
        model = sm.OLS(y, x).fit()

        results = {
            'Variable': model.params.index,
            'Coefficient': model.params.values,
            'p_value': model.pvalues.values,
            'CI_low': model.conf_int()[0],
            'CI_high': model.conf_int()[1]
        }
        coefs = pd.DataFrame(results)
        coefs = coefs.reset_index(drop=True)

        

        for i in range(len(coefs)):

            if coefs.loc[i, 'CI_high'] > 50000:
                coefs.loc[i, 'CI_high'] = 'inf'
            else:
                coefs.loc[i, 'CI_high'] = round(coefs.loc[i, 'CI_high'], 2)

            if coefs.loc[i, 'CI_low'] < -50000:
                coefs.loc[i, 'CI_low'] = '-inf'
            else:
                coefs.loc[i, 'CI_low'] = round(coefs.loc[i, 'CI_low'], 2)

            if coefs.loc[i, 'p_value'] < 0.0001:
                coefs.loc[i, 'p_value'] = "< 0.0001"
            else:
                coefs.loc[i, 'p_value'] = round(coefs.loc[i, 'p_value'], 4)

            coefs.loc[i, 'Coefficient'] = round(coefs.loc[i, 'Coefficient'], 2)


        utils.create_table(self.results_display_frame, coefs)


        summary_text = tk.Text(self.results_display_frame, height=20, width=120)
        summary_text.pack(side=tk.TOP)
        summary_text.insert(tk.END, str(model.summary()))


        save_summary_button = ttk.Button(self.results_display_frame, text="Save Table", command=lambda: file_handling.save_file(coefs))
        save_summary_button.pack()

        view_correlation_matrix_button = ttk.Button(self.results_display_frame, text="View Correlation Matrix", command=lambda: plot_correlation_matrix())
        view_correlation_matrix_button.pack()

        def plot_correlation_matrix():
            correlation_matrix = x.corr()
            plt.figure(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
            plt.title('Correlation Matrix')
            plt.show()



################################################################################################################
################################################################################################################
################################################################################################################

    # NAVIGATION MENU HANDLING FUNCTIONS

    def switch_to_dependent_variable_frame(self):

        self.variable_handling_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack(fill=tk.BOTH, expand=True)

        self.dependent_var_search_entry.focus_set()

        self.visualize_content_frame.update_idletasks()

    def switch_to_independent_variables_frame(self):
        if self.selected_dependent_variable == None:
            return

        self.variable_handling_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.indedependent_variables_frame.pack(fill=tk.BOTH, expand=True)

        self.independent_var_search_entry.focus_set()

        self.dependent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.independent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.results_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.variable_handling_menu_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")

        self.visualize_content_frame.update_idletasks()


    def switch_to_variable_handling_frame(self):

        if self.selected_regression not in ["logistic", "linear"]:
            utils.show_message('Error', 'Please select either Logistic Regression or Linear Regression')
            return
        
        if len(self.selected_independent_variables) < 1:
            utils.show_message('Error', 'No Independent Variables Selected')
            return

    
        
        if self.selected_regression == "logistic":
            # CHECK FOR BINARY OUTCOME BEFORE LOGISTIC REGRESSION
            if len(self.df[self.selected_dependent_variable].dropna().unique()) != 2:
                utils.show_message('dependent variable error', 'Dependent Variable not binary for logistic regression')
                return
            
            self.handle_variables_logistic_regression()


        if self.selected_regression == "linear":
            # CHECK FOR CONTINUOUS VARIABLE BEFORE LINEAR REGRESSION
            try:
                self.df[self.selected_dependent_variable] = self.df[self.selected_dependent_variable].dropna().astype(float)
            except:
                utils.show_message('dependent variable error', 'Dependent Variable not numeric for linear regression')
                return
            
            self.handle_variables_linear_regression()

        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.variable_handling_frame.pack(fill=tk.BOTH, expand=True)

        self.visualize_content_frame.update_idletasks()

    def switch_to_results_frame(self):

        self.run_analysis()
    
        self.indedependent_variables_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.variable_handling_frame.pack_forget()
        self.results_frame.pack(fill=tk.BOTH, expand=True)

        self.visualize_content_frame.update_idletasks()

################################################################################################################
################################################################################################################
################################################################################################################

################################################################################################################
################################################################################################################
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
################################################################################################################
################################################################################################################

################################################################################################################
################################################################################################################
################################################################################################################


################################################################################################################
################################################################################################################
#                                                                                                              #
#                                                 CREATE PLOT                                                  #
#                                                                                                              #
################################################################################################################
################################################################################################################


class CreatePlotClass():
 
    def __init__(self, visualize_content_frame, style):
        self.df = data_manager.get_dataframe()
 
        self.style = style

        self.style.configure("comparison_table_button.TButton", background="gray")
        self.style.configure("regression_button.TButton", background="gray")
        self.style.configure("create_plot_button.TButton", background="white")
        self.style.configure("machine_learning_button.TButton", background="gray")

        data_manager.add_tab_to_tab_dict("current_visualize_tab", "create_plot")

        self.visualize_content_frame = visualize_content_frame
        utils.remove_frame_widgets(self.visualize_content_frame)
 
        self.plot_options_frame = tk.Frame(self.visualize_content_frame, bg='beige')
        self.plot_options_frame.pack(side=tk.LEFT, fill=tk.BOTH)
 
        self.figure_settings_frame = tk.Frame(self.visualize_content_frame, bg='beige')
        self.figure_settings_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        self.figure_display_frame = tk.Frame(self.visualize_content_frame, bg='beige')
        self.figure_display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.figure_display_frame.pack_forget()
 

        self.create_plot_options_list()

    def update_column_listbox(self, *args):
        search_term = self.column_search_var.get().lower()
        self.plot_choice_listbox.delete(0, tk.END)
        for plot in self.available_plots:
            if search_term in plot.lower():
                self.plot_choice_listbox.insert(tk.END, plot)


    def create_plot_options_list(self):
 
        self.available_plots = ["Scatter Plot"]
        self.selected_plot = None
        self.selected_plot = tk.StringVar(value=self.selected_plot)

        self.radiobuttons = []

        self.choice_frame = tk.Frame(self.plot_options_frame, bg='beige')
        self.choice_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.choice_frame_label = tk.Label(self.choice_frame, text="Choose a Graph", font=("Arial", 30, "bold"), bg="beige")
        self.choice_frame_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.choice_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.column_search_var = tk.StringVar()
        self.column_search_var.trace("w", self.update_column_listbox)
        self.column_search_entry = tk.Entry(self.choice_frame, textvariable=self.column_search_var, font=("Arial", 24))
        self.column_search_entry.pack(side=tk.TOP, pady=5)
        self.column_search_entry.focus_set()


        self.plot_type_selection = tk.StringVar()
        self.plot_choice_listbox = tk.Listbox(self.choice_frame, font=("Arial", 24))
        self.plot_choice_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
 
        for plot in self.available_plots:
            self.plot_choice_listbox.insert(tk.END, plot)

        self.plot_choice_listbox.update()

        def on_plot_choice_listbox_selection(event):
            selected_index = self.plot_choice_listbox.curselection()
            if selected_index:
                selected_plot_type = self.plot_choice_listbox.get(selected_index[0])
                self.plot_type_selection.set(selected_plot_type)
 
       
        self.plot_choice_listbox.bind("<<ListboxSelect>>", on_plot_choice_listbox_selection)
 

        self.plot_options_button_frame = tk.Frame(self.plot_options_frame, bg='beige')
        self.plot_options_button_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        self.choose_plot_button = tk.Button(self.plot_options_button_frame, text="Choose Plot", bg='beige', command=lambda: self.choose_plot())
        self.choose_plot_button.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)












    def choose_plot(self):
        selected_index = self.plot_choice_listbox.curselection()
        if selected_index:
            self.selected_plot = self.plot_choice_listbox.get(selected_index[0])
 
            self.display_plot_settings()



    def display_plot_settings(self):
 
        if self.selected_plot == "Scatter Plot":
            self.display_scatter_plot_settings()

        # if self.selected_plot == "Histogram":
        #     self.display_histogram_settings()



    def display_scatter_plot_settings(self):
        self.column_choice_frame = tk.Frame(self.figure_settings_frame, bg='beige')
        self.column_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
 
        self.submit_settings_button_frame = tk.Frame(self.figure_settings_frame, bg='beige')
        self.submit_settings_button_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
 
        self.x_axis_selection = tk.StringVar()
        self.y_axis_selection = tk.StringVar()
 
        ###################### X AXIS ######################
        self.x_axis_frame = tk.Frame(self.column_choice_frame, bg='beige')
        self.x_axis_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        self.x_axis_frame_label = tk.Label(self.x_axis_frame, text="X-AXIS SELECTION", font=("Arial", 30, "bold"))
        self.x_axis_frame_label.pack(side=tk.TOP)




        self.x_axis_search_var = tk.StringVar()
        self.x_axis_search_var.trace("w", self.update_x_axis_variable_listbox)
        self.x_axis_search_entry = tk.Entry(self.x_axis_frame, textvariable=self.x_axis_search_var, font=("Arial", 24))
        self.x_axis_search_entry.pack(side=tk.TOP, pady=10)

        self.x_axis_listbox = tk.Listbox(self.x_axis_frame, font=('Arial', 24))
        self.x_axis_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for column in sorted(self.df.columns):
            self.x_axis_listbox.insert(tk.END, column)
 
        def on_x_axis_listbox_selection(event):
            selected_index = self.x_axis_listbox.curselection()
            if selected_index:
                selected_column = self.x_axis_listbox.get(selected_index[0])
                self.x_axis_selection.set(selected_column)
                self.x_axis_label.config(text=self.x_axis_selection.get(), font=("Arial", 30, "bold"))  # Update x_axis_label text
        

        self.x_axis_listbox.bind("<<ListboxSelect>>", on_x_axis_listbox_selection)
 
        self.x_axis_label = tk.Label(self.x_axis_frame, textvariable=self.x_axis_selection)
        self.x_axis_label.pack(side=tk.TOP)
        self.x_axis_label.config(text='No Variable Selected', font=("Arial", 30, "bold"))
        ###################### X AXIS ######################
 
        ###################### Y AXIS ######################
        self.y_axis_frame = tk.Frame(self.column_choice_frame, bg='beige')
        self.y_axis_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        self.y_axis_frame_label = tk.Label(self.y_axis_frame, text="Y-AXIS SELECTION", font=("Arial", 30, "bold"))
        self.y_axis_frame_label.pack(side=tk.TOP)
 


        self.y_axis_search_var = tk.StringVar()
        self.y_axis_search_var.trace("w", self.update_y_axis_variable_listbox)
        self.y_axis_search_entry = tk.Entry(self.y_axis_frame, textvariable=self.y_axis_search_var, font=("Arial", 24))
        self.y_axis_search_entry.pack(side=tk.TOP, pady=10)

        self.y_axis_listbox = tk.Listbox(self.y_axis_frame, font=('Arial', 24))
        self.y_axis_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for column in sorted(self.df.columns):
            self.y_axis_listbox.insert(tk.END, column)


        def on_y_axis_listbox_selection(event):
            selected_index = self.y_axis_listbox.curselection()
            if selected_index:
                selected_column = self.y_axis_listbox.get(selected_index[0])
                self.y_axis_selection.set(selected_column)
                self.y_axis_label.config(text=self.y_axis_selection.get(), font=("Arial", 30, "bold"))  # Update y_axis_label text
 
       
        self.y_axis_listbox.bind("<<ListboxSelect>>", on_y_axis_listbox_selection)
 
        self.y_axis_label = tk.Label(self.y_axis_frame, textvariable=self.y_axis_selection)
        self.y_axis_label.pack(side=tk.TOP)
        self.y_axis_label.config(text='No Variable Selected', font=("Arial", 30, "bold"))
 
        # Force update the Listboxes after the frame becomes visible
        self.x_axis_listbox.update()
        self.y_axis_listbox.update()
        ###################### Y AXIS ######################
 
        # Add the Submit button
        self.submit_button = tk.Button(self.submit_settings_button_frame, text="Submit", command=self.submit_plot_settings, font=('Arial', 40))
        self.submit_button.pack(pady=10)
 
    def update_x_axis_variable_listbox(self, *args):
        search_term = self.x_axis_search_var.get().lower()
        self.x_axis_listbox.delete(0, tk.END)
        for column in sorted(self.df.columns):
            if search_term in column.lower():
                self.x_axis_listbox.insert(tk.END, column)

    def update_y_axis_variable_listbox(self, *args):
        search_term = self.y_axis_search_var.get().lower()
        self.y_axis_listbox.delete(0, tk.END)
        for column in sorted(self.df.columns):
            if search_term in column.lower():
                self.y_axis_listbox.insert(tk.END, column)

    def submit_plot_settings(self):
        self.figure_settings_frame.pack_forget()
        self.figure_display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        self.fig = self.create_scatter_plot()
 
        canvas = FigureCanvasTkAgg(self.fig, master=self.figure_display_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
   
 
        # Add code here to perform additional actions or plotting based on the selections
 

    def create_scatter_plot(self):
 
        x_axis_variable = self.x_axis_selection.get()
        if not x_axis_variable:
            utils.show_message("No Columns Selected", "No X-AXIS VARIABLE selected")
            return
        try:
            self.df[x_axis_variable] = self.df[x_axis_variable].astype(float)
        except:
            utils.show_message("Error", "X-AXIS VARIABLE not a continuous variable. Pick Again")
            return
        y_axis_variable = self.y_axis_selection.get()
        if not y_axis_variable:
            utils.show_message("No Columns Selected", "No Y-AXIS VARIABLE selected")
            return
        try:
            self.df[y_axis_variable] = self.df[y_axis_variable].astype(float)
        except:
            utils.show_message("Error", "Y-AXIS VARIABLE not a continuous variable. Pick Again")
            return
        clean_df = self.df[[x_axis_variable, y_axis_variable]].dropna()
 
        # Create scatter plot with seaborn
        sns.set(style="ticks")
        fig, ax = plt.subplots()
        sns.scatterplot(data=clean_df, x=x_axis_variable, y=y_axis_variable, ax=ax)
       
        # Calculate regression line parameters
        slope, intercept, r_value, p_value, _ = stats.linregress(clean_df[x_axis_variable], clean_df[y_axis_variable])
        line = slope * clean_df[x_axis_variable] + intercept
       
        # Add regression line to the plot
        sns.lineplot(x=clean_df[x_axis_variable], y=line, color='r', ax=ax)
       
        # Add R-squared and p-value to the plot
        plt.text(0.05, 0.95, f"R-squared: {r_value**2:.4f}\nP-value: {p_value:.4f}", transform=ax.transAxes)
       
        # Customize plot aesthetics (title, labels, etc.)
        plt.title("")
        plt.xlabel(x_axis_variable)
        plt.ylabel(y_axis_variable)
        plt.tight_layout()
       
        return fig
 

       





def create_histogram(visualize_content_frame, df):
    text_prompt1 = "Choose your VARIABLE for Histogram"
    chosen_continuous_variable = utils.get_single_choice(visualize_content_frame, df.columns, text_prompt1)
    if not chosen_continuous_variable:
        utils.show_message("No Columns Selected", "No X-AXIS VARIABLE selected")
        return
    try:
        df[chosen_continuous_variable] = df[chosen_continuous_variable].astype(float)
    except:
        utils.show_message("Error", "X-AXIS VARIABLE not a continuous variable. Pick Again")
        return
 
    clean_df = df[chosen_continuous_variable].dropna()
 
    sns.set(style="ticks")
    fig, ax = plt.subplots()
    sns.histplot(data=clean_df, kde=True, ax=ax)
 
    # Customize plot aesthetics (title, labels, etc.)
    plt.xlabel(chosen_continuous_variable)
    plt.ylabel("Frequency")
    plt.tight_layout()
 
    return fig







def create_box_and_whisker_plot(visualize_content_frame, df):
    return











################################################################################################################
################################################################################################################
################################################################################################################

################################################################################################################
################################################################################################################
####                    ################################################################                    ####
####                    ################################################################                    ####
####                    ################################################################                    ####
####                    ################################################################                    ####
####                    ################################################################                    ####
####                    ################################################################                    ####
####                    ################################################################                    ####
####                    ################################################################                    ####
####                    ################################################################                    ####
####                    ################################################################                    ####
####                    ################################################################                    ####
####                    ################################################################                    ####
####                    ################################################################                    ####
####                    ################################################################                    ####
####                    ################################################################                    ####
####                    ################################################################                    ####
####                    ################################################################                    ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
####                                                                                                        ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
########################################################################################                    ####
################################################################################################################
################################################################################################################

################################################################################################################
################################################################################################################
################################################################################################################


################################################################################################################
################################################################################################################
#                                                                                                              #
#                                               MACHINE LEARNING                                               #
#                                                                                                              #
################################################################################################################
################################################################################################################


class MachineLearningClass:
    def __init__(self, visualize_content_frame, style):
        self.df = data_manager.get_dataframe()
        self.visualize_content_frame = visualize_content_frame

        self.style = style


        self.style.configure("comparison_table_button.TButton", background="gray")
        self.style.configure("regression_button.TButton", background="gray")
        self.style.configure("create_plot_button.TButton", background="gray")
        self.style.configure("machine_learning_button.TButton", background="white")

        data_manager.add_tab_to_tab_dict("current_visualize_tab", "machine_learning")

        self.selected_dependent_variable = data_manager.get_mach_learn_tab_dep_var()
        self.selected_independent_variables = data_manager.get_mach_learn_tab_ind_var_list()

        self.log_reg_target_value_var_dict = data_manager.get_reg_tab_log_reg_target_value_dict()
        
        self.selected_model_type = data_manager.get_mach_learn_tab_selected_model_type()
        self.selected_categorical_model = data_manager.get_mach_learn_tab_selected_cat_model()
        self.selected_continuous_model = data_manager.get_mach_learn_tab_selected_cont_model()

        self.null_values_handling_option = data_manager.get_mach_learn_tab_null_values_choice()
        self.null_value_entry_value = data_manager.get_mach_learn_tab_null_value_entry_value()
        self.number_of_folds_choice = data_manager.get_mach_learn_tab_num_folds()
        self.train_percent = data_manager.get_mach_learn_tab_train_percent()
        self.hypertune_parameters_choice = data_manager.get_mach_learn_tab_hyper_param_choice()


    
        self.available_categorical_models_dict = {
            "Random Forest":RandomForestClassifier(random_state=69),
            "XGBoost":XGBClassifier(random_state=69),
            "Logistic Regression":LogisticRegression(max_iter=100000000, random_state=69)
        }


        self.available_continuous_models_dict = {
            "test":"test"
            # "Linear Regression":LinearRegression()
        }


        self.non_numeric_input_var_dict = data_manager.get_non_numeric_ind_dict()

        self.verify_saved_columns()

        self.machine_learning_model_options = ['cat_rf', 'cat_xgb', 'cat_logreg', 'cont_linreg']
        self.model_dict = {'cat_rf':'Random Forest', 'cat_xgb':'XGBoost', 'cat_logreg':'Logistic Regression', 'cont_linreg':'Linear Regression'}
        # self.model_function_dict = {'cat_rf':self.create_random_forest_classifier_model()}

        utils.remove_frame_widgets(self.visualize_content_frame)


        self.dependent_variable_frame = tk.Frame(self.visualize_content_frame, bg='beige')
        self.indedependent_variables_frame = tk.Frame(self.visualize_content_frame, bg='beige')
        self.variable_handling_frame = tk.Frame(self.visualize_content_frame, bg='beige')
        self.settings_frame = tk.Frame(self.visualize_content_frame, bg='beige')
        self.results_frame = tk.Frame(self.visualize_content_frame, bg='beige')
        self.prediction_tool_frame = tk.Frame(self.visualize_content_frame, bg='beige')
        
        self.create_dependent_variable_frame()
        self.create_independent_variables_frame()
        self.create_variable_handling_frame()
        self.create_settings_frame()
        self.create_results_frame()
        self.create_prediction_tool_frame()

        self.switch_to_dependent_variable_frame()

    def verify_saved_columns(self):
        if self.selected_dependent_variable not in self.df.columns:
            self.selected_dependent_variable = None

        for var in self.selected_independent_variables:
            if var not in self.df.columns:
                self.selected_independent_variables.remove(var)

################################################################################################################
################################################################################################################
################################################################################################################

    # CREATE DEPENDENT VARIABLE SELECTION FRAME

    def create_dependent_variable_frame(self):

        # MAIN CONTENT FRAME
        self.dependent_variable_options_frame = tk.Frame(self.dependent_variable_frame, bg='beige')
        self.dependent_variable_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # CONTENT TITLE LABEL
        self.choose_dependent_variable_label = tk.Label(self.dependent_variable_options_frame, text="Choose your DEPENDENT variable", font=("Arial", 36, "bold"), bg='beige')
        self.choose_dependent_variable_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.dependent_variable_options_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)

        # DEPENDENT VARIABLE SELECTION FRAME
        self.dependent_column_choice_frame = tk.Frame(self.dependent_variable_options_frame, bg='beige')
        self.dependent_column_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.dependent_search_var = tk.StringVar()
        self.dependent_search_var.trace("w", self.update_dependent_variable_listbox)
        self.dependent_var_search_entry = tk.Entry(self.dependent_column_choice_frame, textvariable=self.dependent_search_var, font=("Arial", 24))
        self.dependent_var_search_entry.pack(side=tk.TOP, pady=10)

        self.dependent_variable_listbox = tk.Listbox(self.dependent_column_choice_frame, selectmode=tk.SINGLE, font=("Arial", 24), exportselection=False)
        self.dependent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)

        for column in sorted(self.df.columns, key=str.lower):
            self.dependent_variable_listbox.insert(tk.END, column)

        self.dependent_variable_listbox.bind("<<ListboxSelect>>", self.on_dependent_variable_listbox_select)



        # NAVIGATION MENU
        self.dependent_variable_menu_frame = tk.Frame(self.dependent_variable_frame, bg='lightgray')
        self.dependent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.advance_to_independent_variables_button = tk.Button(self.dependent_variable_menu_frame, text="Next", command=self.switch_to_independent_variables_frame, font=("Arial", 36))
        self.advance_to_independent_variables_button.pack(side=tk.RIGHT)

        self.dependent_frame_dependent_label = tk.Label(self.dependent_variable_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.dependent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)


        if self.selected_dependent_variable:
            self.dependent_variable_listbox.selection_clear(0, tk.END)
            items = list(self.dependent_variable_listbox.get(0, tk.END))
            index = items.index(self.selected_dependent_variable)
            self.dependent_variable_listbox.selection_set(index)
            self.dependent_variable_listbox.yview(index)
            self.dependent_frame_dependent_label.config(text=f"Dependent Variable: {self.selected_dependent_variable}")

            
    def on_dependent_variable_listbox_select(self, event):
        if self.dependent_variable_listbox.curselection():
            self.selected_dependent_variable = self.dependent_variable_listbox.get(self.dependent_variable_listbox.curselection()[0])
            data_manager.set_mach_learn_tab_dep_var(self.selected_dependent_variable)
            self.dependent_frame_dependent_label.config(text=f"Dependent Variable: {self.selected_dependent_variable}")


    def update_dependent_variable_listbox(self, *args):
        search_term = self.dependent_search_var.get().lower()
        self.dependent_variable_listbox.delete(0, tk.END)
        for column in self.df.columns:
            if search_term in column.lower():
                self.dependent_variable_listbox.insert(tk.END, column)

################################################################################################################
################################################################################################################
################################################################################################################

    # CREATE INDEPENDENT VARIABLE SELECTION FRAME


    def create_independent_variables_frame(self):

        # MAIN CONTENT FRAME
        self.independent_variable_options_frame = tk.Frame(self.indedependent_variables_frame, bg='beige')
        self.independent_variable_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # TITLE LABEL
        self.choose_independent_variables_label = tk.Label(self.independent_variable_options_frame, text="Choose your INDEPENDENT variables", font=("Arial", 36, "bold"), bg='beige')
        self.choose_independent_variables_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.independent_variable_options_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)


        # AVAILABLE INDEPENDENT VARIABLES SELECTION FRAME
        self.indedependent_variables_selection_frame = tk.Frame(self.independent_variable_options_frame, bg='beige')
        self.indedependent_variables_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.available_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='beige')
        self.available_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.available_independent_search_var = tk.StringVar()
        self.available_independent_search_var.trace("w", self.update_available_independent_variable_listbox)
        self.independent_var_search_entry = tk.Entry(self.available_independent_variables_frame, textvariable=self.available_independent_search_var, font=("Arial", 24))
        self.independent_var_search_entry.pack(side=tk.TOP, pady=10)

        self.available_independent_variable_listbox = tk.Listbox(self.available_independent_variables_frame, selectmode=tk.MULTIPLE, font=("Arial", 24))
        self.available_independent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)

        for column in sorted(self.df.columns, key=str.lower):
            self.available_independent_variable_listbox.insert(tk.END, column)


        # TRANSFER BUTTONS
        self.transfer_buttons_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='beige')
        self.transfer_buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.transfer_right_button = tk.Button(self.transfer_buttons_frame, text=">>>", command=self.transfer_right, font=("Arial", 48))
        self.transfer_right_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.transfer_left_button = tk.Button(self.transfer_buttons_frame, text="<<<", command=self.transfer_left, font=("Arial", 48))
        self.transfer_left_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.transfer_all_right_button = tk.Button(self.transfer_buttons_frame, text="Move All Right", command=self.transfer_all_right, font=("Arial", 36))
        self.transfer_all_right_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)

        self.transfer_all_left_button = tk.Button(self.transfer_buttons_frame, text="Clear Selection", command=self.transfer_all_left, font=("Arial", 36))
        self.transfer_all_left_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)



        # SELECTED INDEPENDENT VARIABLES FRAME
        self.selected_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='beige')
        self.selected_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.selected_independent_variables_label = tk.Label(self.selected_independent_variables_frame, text="Selected Variables", font=("Arial", 24))
        self.selected_independent_variables_label.pack(side=tk.TOP, pady=10)

        self.selected_independent_variable_listbox = tk.Listbox(self.selected_independent_variables_frame, selectmode=tk.MULTIPLE, font=("Arial", 24))
        self.selected_independent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)

        if len(self.selected_independent_variables) > 0:
            for var in self.selected_independent_variables:
                self.selected_independent_variable_listbox.insert(tk.END, var)
                self.available_independent_variable_listbox.selection_set(sorted(self.df.columns, key=str.lower).index(var))
            selections = self.available_independent_variable_listbox.curselection()
            for index in reversed(selections):
                self.available_independent_variable_listbox.delete(index)



        # MACHINE LEARNING MODEL SELECTION FRAME
        self.model_selection_frame = tk.Frame(self.independent_variable_options_frame, bg='beige')
        self.model_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=20)

        self.model_selection_label = tk.Label(self.model_selection_frame, text="Model Selection", font=("Arial", 36, "bold"), bg='beige')
        self.model_selection_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.model_selection_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)


        if self.selected_model_type:
            self.model_type_var = tk.StringVar(value=self.selected_model_type)
        else:
            self.model_type_var = tk.StringVar(value="Categorical")

        def on_model_type_radio_button_selected():
            self.selected_model_type = self.model_type_var.get()
            data_manager.set_mach_learn_tab_selected_model_type(self.selected_model_type)
            
            if self.selected_model_type == "Categorical":
                self.selected_model = self.categorical_model_var.get()
                self.categorical_model_selection_combobox.configure(state="readonly")
                self.style.configure("categorical_model.TCombobox", foreground='black', background='darkgray')
                
                self.continuous_model_selection_combobox.configure(state="disabled")
                self.style.configure("continuous_model.TCombobox", foreground='lightgray', background='lightgray')
            if self.selected_model_type == "Continuous":
                self.selected_model = self.continuous_model_var.get()
                self.continuous_model_selection_combobox.configure(state="readonly")
                self.style.configure("continuous_model.TCombobox", foreground='black', background='darkgray')
                
                self.categorical_model_selection_combobox.configure(state="disabled")
                self.style.configure("categorical_model.TCombobox", foreground='lightgray', background='lightgray')


        # Categorical Model Frame
        self.categorical_model_frame = tk.Frame(self.model_selection_frame, bg='beige')
        self.categorical_model_frame.pack(side=tk.TOP, fill=tk.X)

        self.categorical_variable_type_button = tk.Radiobutton(self.categorical_model_frame, text="Categorical Model", variable=self.model_type_var, value='Categorical', command=on_model_type_radio_button_selected, indicator = 0,font=("Arial", 40), selectcolor="hotpink", borderwidth=10)
        self.categorical_variable_type_button.pack(side=tk.TOP, fill=tk.X, padx=400, pady=10)

        # Combobox Frame
        self.categorical_model_selection_frame = tk.Frame(self.categorical_model_frame, bg='beige')
        self.categorical_model_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        if self.selected_categorical_model:
            self.categorical_model_var = tk.StringVar(value=self.selected_categorical_model)
        else:
            self.categorical_model_var = tk.StringVar(value="Random Forest")

        def on_categorical_model_combobox_selected(event):
            self.selected_categorical_model = self.categorical_model_var.get()
            self.selected_model = self.selected_categorical_model
            data_manager.set_mach_learn_tab_selected_cat_model(self.selected_categorical_model)


        self.style.configure('categorical_model.TCombobox', selectbackground="darkgray", selectforeground="black")
        self.style.map("categorical_model.TCombobox", fieldbackground=[("readonly", "darkgray"), ("disabled", "lightgray")])
        self.categorical_model_selection_combobox = ttk.Combobox(self.categorical_model_selection_frame, textvariable=self.categorical_model_var, values=list(self.available_categorical_models_dict.keys()), font=("Arial", 36), state="readonly", style="categorical_model.TCombobox", name="cat_model_combobox")
        self.categorical_model_selection_combobox.bind("<<ComboboxSelected>>", on_categorical_model_combobox_selected)
        self.categorical_model_selection_combobox.pack(side=tk.TOP, pady=10)



        # Continuous Model Frame
        self.continuous_model_frame = tk.Frame(self.model_selection_frame, bg='beige')
        self.continuous_model_frame.pack(side=tk.TOP, fill=tk.X)

        self.continuous_variable_type_button = tk.Radiobutton(self.continuous_model_frame, text="Continuous Model", variable=self.model_type_var, value='Continuous', command=on_model_type_radio_button_selected, indicator = 0,font=("Arial", 40), selectcolor="hotpink", borderwidth=10)
        self.continuous_variable_type_button.pack(side=tk.TOP, fill=tk.X, padx=400, pady=10)

        # Combobox Frame
        self.continuous_model_selection_frame = tk.Frame(self.continuous_model_frame, bg='beige')
        self.continuous_model_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        if self.selected_continuous_model:
            self.continuous_model_var = tk.StringVar(value=self.selected_continuous_model)
        else:
            self.continuous_model_var = tk.StringVar(value="Linear Regression")

        def on_continuous_model_combobox_selected(event):
            self.selected_continuous_model = self.continuous_model_var.get()
            self.selected_model = self.selected_continuous_model
            data_manager.set_mach_learn_tab_selected_cont_model(self.selected_continuous_model)
        
        self.style.configure('continuous_model.TCombobox', selectbackground="darkgray", selectforeground="black")
        self.style.map("continuous_model.TCombobox", fieldbackground=[("readonly", "darkgray"), ("disabled", "lightgray")])
        self.continuous_model_selection_combobox = ttk.Combobox(self.continuous_model_selection_frame, textvariable=self.continuous_model_var, values=self.available_continuous_models_dict, font=("Arial", 36), state="readonly", style="continuous_model.TCombobox")
        self.continuous_model_selection_combobox.bind("<<ComboboxSelected>>", on_continuous_model_combobox_selected)
        self.continuous_model_selection_combobox.pack(side=tk.TOP)
        

        

        self.selected_model_type = self.model_type_var.get()

        if self.selected_model_type == "Categorical":
            self.selected_model = self.categorical_model_var.get()

            self.categorical_model_selection_combobox.configure(state="readonly")
            self.style.configure("categorical_model.TCombobox", foreground='black', background='darkgray')
            
            self.continuous_model_selection_combobox.configure(state="disabled")
            self.style.configure("continuous_model.TCombobox", foreground='lightgray', background='lightgray')

        if self.selected_model_type == "Continuous":
            self.selected_model = self.continuous_model_var.get()

            self.continuous_model_selection_combobox.configure(state="readonly")
            self.style.configure("continuous_model.TCombobox", foreground='black', background='darkgray')
            
            self.categorical_model_selection_combobox.configure(state="disabled")
            self.style.configure("categorical_model.TCombobox", foreground='lightgray', background='lightgray')









        # NAVIGATION MENU
        self.independent_variable_menu_frame = tk.Frame(self.indedependent_variables_frame, bg='lightgray')
        self.independent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_dependent_variable_frame_button = tk.Button(self.independent_variable_menu_frame, command=self.switch_to_dependent_variable_frame, text='Back', font=("Arial", 36))
        self.return_to_dependent_variable_frame_button.pack(side=tk.LEFT)

        self.advance_to_variable_handling_frame_button = tk.Button(self.independent_variable_menu_frame, command=self.switch_to_variable_handling_frame, text="Next", font=("Arial", 36))
        self.advance_to_variable_handling_frame_button.pack(side=tk.RIGHT)

        self.independent_frame_dependent_label = tk.Label(self.independent_variable_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.independent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)


    def update_available_independent_variable_listbox(self, *args):
        search_term = self.available_independent_search_var.get().lower()
        self.available_independent_variable_listbox.delete(0, tk.END)
        for column in sorted(self.df.columns, key=str.lower):
            if search_term in column.lower():
                self.available_independent_variable_listbox.insert(tk.END, column)


    def transfer_right(self):
        selections = self.available_independent_variable_listbox.curselection()
        selected_items = [self.available_independent_variable_listbox.get(index) for index in selections]

        for item in selected_items:
            if item not in self.selected_independent_variables:
                self.selected_independent_variable_listbox.insert(tk.END, item)
                self.selected_independent_variables.append(item)
                data_manager.add_variable_to_mach_learn_tab_ind_var_list(item)

        for index in reversed(selections):
            self.available_independent_variable_listbox.delete(index)


    def transfer_all_right(self):

        for i in range(self.available_independent_variable_listbox.size()):
            self.available_independent_variable_listbox.selection_set(i)

        selections = self.available_independent_variable_listbox.curselection()
        selected_items = [self.available_independent_variable_listbox.get(index) for index in selections]

        for item in selected_items:
            self.selected_independent_variable_listbox.insert(tk.END, item)
            self.selected_independent_variables.append(item)

        for index in reversed(selections):
            self.available_independent_variable_listbox.delete(index)


    def transfer_left(self):
        selections = self.selected_independent_variable_listbox.curselection()
        selected_items = [self.selected_independent_variable_listbox.get(index) for index in selections]

        for item in selected_items:
            self.available_independent_variable_listbox.insert(tk.END, item)
            self.selected_independent_variables.remove(item)

        self.reorder_available_independent_variable_listbox_alphabetically()

        for index in reversed(selections):
            self.selected_independent_variable_listbox.delete(index)


    def transfer_all_left(self):

        for i in range(self.selected_independent_variable_listbox.size()):
            self.selected_independent_variable_listbox.selection_set(i)

        selections = self.selected_independent_variable_listbox.curselection()
        selected_items = [self.selected_independent_variable_listbox.get(index) for index in selections]

        for item in selected_items:
            self.available_independent_variable_listbox.insert(tk.END, item)
            self.selected_independent_variables.remove(item)

        self.reorder_available_independent_variable_listbox_alphabetically()

        for index in reversed(selections):
            self.selected_independent_variable_listbox.delete(index)


    def reorder_available_independent_variable_listbox_alphabetically(self):
        top_visible_index = self.available_independent_variable_listbox.nearest(0)
        top_visible_item = self.available_independent_variable_listbox.get(top_visible_index)

        items = list(self.available_independent_variable_listbox.get(0, tk.END))
        items = sorted(items, key=lambda x: x.lower())

        self.available_independent_variable_listbox.delete(0, tk.END)  # Clear the Listbox
        for item in items:
            self.available_independent_variable_listbox.insert(tk.END, item)

        if top_visible_index >= 0:
            index = items.index(top_visible_item)
            self.available_independent_variable_listbox.yview(index)




################################################################################################################
################################################################################################################
################################################################################################################

    # CREATE VARIABLE HANDLING FRAME

    def create_variable_handling_frame(self):
        # MAIN CONTENT FRAME
        self.variable_handling_label_frame = tk.Frame(self.variable_handling_frame)
        self.variable_handling_label_frame.pack(side=tk.TOP)

        # TITLE LABEL
        self.variable_handling_label = tk.Label(self.variable_handling_label_frame, text="", font=("Arial", 36, "bold"), bg='beige')
        self.variable_handling_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.variable_handling_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)

        ########################################################################################################

        # SCROLLABLE FRAME 
        self.variable_handling_options_frame = tk.Frame(self.variable_handling_frame)
        self.variable_handling_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Canvas for scrollable content
        self.variable_type_canvas = tk.Canvas(self.variable_handling_options_frame, bg='yellow')
        self.variable_type_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for the canvas
        self.scrollbar = tk.Scrollbar(self.variable_handling_options_frame, command=self.variable_type_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.variable_type_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Scrollable frame inside the canvas
        self.scrollable_frame = tk.Frame(self.variable_type_canvas, bg='yellow')
        self.scrollable_frame_window = self.variable_type_canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)

        # Bind events
        self.variable_type_canvas.bind("<Configure>", self.on_variable_handling_canvas_configure)
        self.scrollable_frame.bind("<Configure>", lambda e: self.variable_type_canvas.configure(scrollregion=self.variable_type_canvas.bbox("all")))

        # Cross-platform scroll event binding
        if self.visualize_content_frame.tk.call('tk', 'windowingsystem') == 'aqua':  # macOS
            self.variable_handling_options_frame.bind_all("<MouseWheel>", self.on_variable_handling_mousewheel)
        else:  # Windows and others
            self.variable_handling_options_frame.bind_all("<MouseWheel>", self.on_variable_handling_mousewheel)
            self.variable_handling_options_frame.bind_all("<Button-4>", self.on_variable_handling_mousewheel)
            self.variable_handling_options_frame.bind_all("<Button-5>", self.on_variable_handling_mousewheel)

        ########################################################################################################

        # NAVIGATION MENU FRAME
        self.variable_handling_menu_frame = tk.Frame(self.variable_handling_frame, bg='lightgray')
        self.variable_handling_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_independent_variable_frame_button = tk.Button(self.variable_handling_menu_frame, command=self.switch_to_independent_variables_frame, text='Back', font=("Arial", 36))
        self.return_to_independent_variable_frame_button.pack(side=tk.LEFT)

        self.advance_to_settings_frame_button = tk.Button(self.variable_handling_menu_frame, command=self.switch_to_settings_frame, text="Next ->", font=("Arial", 36))
        self.advance_to_settings_frame_button.pack(side=tk.RIGHT)

        self.variable_handling_menu_frame_dependent_label = tk.Label(self.variable_handling_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.variable_handling_menu_frame_dependent_label.pack(side=tk.RIGHT, expand=True)


    def on_variable_handling_canvas_configure(self, event):
        # Update the width of the scrollable frame to match the canvas
        canvas_width = event.width
        self.variable_type_canvas.itemconfig(self.scrollable_frame_window, width=canvas_width)

    def on_variable_handling_mousewheel(self, event):
        if self.variable_type_canvas.winfo_exists():
            if event.num == 4 or event.delta > 0:  # Scroll up
                self.variable_type_canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:  # Scroll down
                self.variable_type_canvas.yview_scroll(1, "units")


    # def on_variable_handling_mousewheel(self, event):
    #     if self.variable_type_canvas.winfo_exists():
    #         self.variable_type_canvas.yview_scroll(-1 * (event.delta // 120), "units")

    ################################################################################################################

    # HANDLE VARIABLES FOR MACHINE LEARNING
        
    def handle_variables_machine_learning(self):

        self.variable_handling_label.configure(text=f"{self.selected_model} Model Variable Settings")

        utils.remove_frame_widgets(self.scrollable_frame)

        self.temp_df = self.df[self.selected_independent_variables + [self.selected_dependent_variable]].copy()

        self.clean_df = self.temp_df[self.selected_dependent_variable].copy().dropna()


        # TARGET VALUE FRAME
        self.dependent_variable_handling_frame = tk.Frame(self.scrollable_frame, bg='yellow')
        self.dependent_variable_handling_frame.pack(fill=tk.BOTH, expand=True)


        self.dependent_variable_handling_frame_label = tk.Label(self.dependent_variable_handling_frame, text='Choose Target Value', font=('Arial', 32, "bold"), bg='yellow')
        self.dependent_variable_handling_frame_label.pack(side=tk.TOP)

        def on_dependent_variable_value_selected():
            data_manager.add_variable_to_reg_tab_log_reg_target_value_dict(self.selected_dependent_variable, self.log_reg_target_value_var)

        if self.selected_dependent_variable in self.log_reg_target_value_var_dict:
            self.log_reg_target_value_var = tk.StringVar(value=self.log_reg_target_value_var_dict[self.selected_dependent_variable].get())
        else:
            self.log_reg_target_value_var = tk.StringVar(value=f"{self.clean_df.unique()[0]}")
            self.log_reg_target_value_var_dict[self.selected_dependent_variable] = self.log_reg_target_value_var
            

        self.dependent_variable_unique_value_1 = tk.Radiobutton(self.dependent_variable_handling_frame, text=f"{self.clean_df.unique()[0]}", variable=self.log_reg_target_value_var, value=f"{self.clean_df.unique()[0]}", command=on_dependent_variable_value_selected, indicator=0, font=("Arial", 40), selectcolor="hotpink", borderwidth=10)
        self.dependent_variable_unique_value_1.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.dependent_variable_unique_value_2 = tk.Radiobutton(self.dependent_variable_handling_frame, text=f"{self.clean_df.unique()[1]}", variable=self.log_reg_target_value_var, value=f"{self.clean_df.unique()[1]}", command=on_dependent_variable_value_selected, indicator=0, font=("Arial", 40), selectcolor="hotpink", borderwidth=10)
        self.dependent_variable_unique_value_2.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        

        # DETERMINE NON-NUMERIC VARIABLES
        self.non_numeric_columns = []

        self.selected_options = {}

        for independent_variable in self.selected_independent_variables:
            try:
                self.temp_df[independent_variable] = self.temp_df[independent_variable].astype(float)
            except:
                self.non_numeric_columns.append(independent_variable)

        if len(self.non_numeric_columns) == 0:
            proceed_to_results_label = tk.Label(self.scrollable_frame, text="No Non-Numeric Variables. Click NEXT", font=("Arial", 28, "bold"), bg='yellow')
            proceed_to_results_label.pack(side=tk.TOP, fill=tk.X, pady=5, padx=20)

        else:
            # Scrollable frame label
            self.scrollable_frame_label = tk.Label(self.scrollable_frame, text="Change Non-Numeric Values in The Following Independent Variables", font=("Arial", 36,"bold"), bg='yellow')
            self.scrollable_frame_label.pack(side=tk.TOP)

            separator = ttk.Separator(self.scrollable_frame, orient="horizontal", style="Separator.TSeparator")
            separator.pack(fill=tk.X, padx=5, pady=5)


            # HANDLE NON-NUMERIC VARIABLES
            for variable in self.non_numeric_columns:



                options_frame = tk.Frame(self.scrollable_frame, bg='yellow')
                options_frame.pack(side=tk.TOP, fill=tk.X, pady=5, padx=20)


                if len(variable) > 20:
                    variable_string = variable[0:19] + "..."
                else:
                    variable_string = variable

                variable_label = tk.Label(options_frame, text=variable_string, font=("Arial", 28), bg='yellow', fg='black')
                variable_label.pack(side=tk.TOP)

                separator = ttk.Separator(self.scrollable_frame, orient="horizontal", style="Separator.TSeparator")
                separator.pack(fill=tk.X, padx=5, pady=5)

                non_numeric_values = []

                for value in self.temp_df[variable].unique():
                    if isinstance(value, str) and not value.isdigit():
                        non_numeric_values.append(value)
                
                for value in non_numeric_values:

                    value_frame = tk.Frame(options_frame, bg='yellow')
                    value_frame.pack(side=tk.TOP, fill=tk.X, expand=True)

                    if variable in self.non_numeric_input_var_dict:
                        if value in self.non_numeric_input_var_dict[variable]:
                            input_var = self.non_numeric_input_var_dict[variable][value]
                                
                            user_input_var = tk.StringVar(value=input_var)
                            data_manager.add_variable_to_non_numeric_ind_dict(variable, value, input_var)
                        else:
                            input_var = ""
                            user_input_var = tk.StringVar(value=input_var)
                            data_manager.add_variable_to_non_numeric_ind_dict(variable, value, input_var)
                    else:
                        input_var = ""
                        user_input_var = tk.StringVar()
                        data_manager.add_variable_to_non_numeric_ind_dict(variable, value, input_var)



                    input_entry = tk.Entry(value_frame, textvariable=user_input_var, font=("Arial", 28), width=10)
                    input_entry.pack(side=tk.LEFT)

                    value_label = tk.Label(value_frame, text=value, font=("Arial", 28), bg='yellow', fg='black')
                    value_label.pack(side=tk.LEFT)

                    # Bind the entry widget to an event
                    input_entry.bind("<KeyRelease>", lambda event, var=variable, val=value: self.on_key_release(event, var, val))


    def on_key_release(self, event, variable, value):
        data_manager.add_variable_to_non_numeric_ind_dict(variable, value, event.widget.get())


    def apply_variable_handling(self):

        def check_column_only_0_and_1(df, column_name):
            unique_values = df[column_name].unique()
            return set(unique_values) == {0, 1}

        if not check_column_only_0_and_1(self.temp_df, self.selected_dependent_variable):

            # MAKE VALUES OF DEPENDENT VARIABLE BINARY
            self.temp_df.dropna(subset=[self.selected_dependent_variable])
            selected_target_var = self.log_reg_target_value_var.get()

            self.temp_df.loc[(self.temp_df[self.selected_dependent_variable] != selected_target_var) & (self.temp_df[self.selected_dependent_variable] != 1), self.selected_dependent_variable] = 0
            self.temp_df.loc[self.temp_df[self.selected_dependent_variable] == selected_target_var, self.selected_dependent_variable] = 1


        self.temp_df[self.selected_dependent_variable] = self.temp_df[self.selected_dependent_variable].astype(int)

        for variable in self.selected_independent_variables:

            if variable in self.non_numeric_columns:

                non_numeric_values = [] 

                for value in self.temp_df[variable].unique():
                    if isinstance(value, str) and not value.isdigit():
                        non_numeric_values.append(value)

                for value in non_numeric_values:

                    input_var = self.non_numeric_input_var_dict[variable][value]

                    try:
                        self.temp_df.loc[self.temp_df[variable] == value, variable] = float(input_var)

                    except:
                        utils.show_message("error message", f"Make sure all values are NUMERICAL")
                        raise

                self.temp_df[variable] = self.temp_df[variable].astype(float)






################################################################################################################
################################################################################################################
################################################################################################################
            
    # CREATE SETTINGS FRAME
    
    def create_settings_frame(self):

        self.settings_frame_label = tk.Label(self.settings_frame, text=f"Settings for {self.selected_model} Model", font=("Arial", 36, "bold"), bg='beige')
        self.settings_frame_label.pack(side=tk.TOP, fill=tk.X)

        separator = ttk.Separator(self.settings_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)

        # MODEL SETTINGS
        self.model_settings_frame = tk.Frame(self.settings_frame, bg='beige')
        self.model_settings_frame.pack(side=tk.TOP, padx=5, pady=50, fill=tk.BOTH)


        #NULL VALUE HANDLING
        self.null_value_handling_frame = tk.Frame(self.model_settings_frame, bg='beige')
        self.null_value_handling_frame.pack(side=tk.TOP, fill=tk.X)


        if self.null_values_handling_option:
            self.null_value_option_var = tk.StringVar(value=self.null_values_handling_option)
        else:
            self.null_value_option_var = tk.StringVar(value="REMOVE null values")


        self.null_value_handling_option_label = tk.Label(self.null_value_handling_frame, text="MISSING/NULL values", font=("Arial", 36), bg='beige')
        self.null_value_handling_option_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.null_value_handling_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=400, pady=5)

        self.null_value_combobox_selection_frame = tk.Frame(self.null_value_handling_frame, bg='beige')
        self.null_value_combobox_selection_frame.pack(side=tk.TOP)

        def on_null_value_combobox_select(event):
            selected_option = self.null_value_option_var.get()
            data_manager.set_mach_learn_tab_null_values_choice(selected_option)
            if selected_option == 'REPLACE with user choice':
                self.null_value_user_choice_entry.pack(side=tk.LEFT, padx=5, pady=5)
                self.null_value_user_choice_entry.focus_set()
            else:
                self.null_value_user_choice_entry.pack_forget()

        self.null_value_option_combobox = ttk.Combobox(self.null_value_combobox_selection_frame, textvariable=self.null_value_option_var, font=("Arial", 24), width=25, state='disabled')
        self.null_value_option_combobox['values'] = ['REMOVE null values', 'REPLACE with mean', 'REPLACE with median', 'REPLACE with mode', 'REPLACE with user choice']
        self.null_value_option_combobox.bind("<<ComboboxSelected>>", on_null_value_combobox_select)
        self.null_value_option_combobox.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=20)


        # NULL VALUE ENTRY
        if self.null_value_entry_value:
            self.null_value_entry_var = tk.StringVar(value=self.null_value_entry_value)
        else:
            self.null_value_entry_var = tk.StringVar(value="")

        self.null_value_user_choice_entry = tk.Entry(self.null_value_combobox_selection_frame, textvariable=self.null_value_entry_var, font=("Arial", 24))

        def on_null_value_entry_release(event):
            current_value = event.widget.get()
            data_manager.set_mach_learn_tab_null_value_entry_value(current_value)

        self.null_value_user_choice_entry.bind("<KeyRelease>", lambda event: on_null_value_entry_release(event))

        if self.null_value_option_var.get() == "REPLACE with user choice":
            self.null_value_user_choice_entry.pack(side=tk.LEFT, padx=5, pady=5)
            self.null_value_user_choice_entry.focus_set()

        ##############################################


        # NUMBER OF FOLDS SELECTION
        self.number_of_folds_frame = tk.Frame(self.model_settings_frame, bg='beige')
        self.number_of_folds_frame.pack(side=tk.TOP, fill=tk.BOTH)

        self.number_of_folds_label = tk.Label(self.number_of_folds_frame, text="TRAIN/TEST Folds", font=("Arial", 36), bg='beige')
        self.number_of_folds_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.number_of_folds_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=400, pady=5)


        self.number_of_folds_combobox_selection_frame = tk.Frame(self.number_of_folds_frame, bg='beige')
        self.number_of_folds_combobox_selection_frame.pack(side=tk.TOP)

        def on_number_of_folds_combobox_select(event):
            selected_option = self.number_of_folds_var.get()
            data_manager.set_mach_learn_tab_num_folds(selected_option)
            if selected_option == 2:
                self.train_fold_percent_frame.pack(side=tk.LEFT, padx=5, pady=5)
                self.train_fold_percent_entry.focus_set()
            else:
                self.train_fold_percent_frame.pack_forget()

        if self.number_of_folds_choice:
            self.number_of_folds_var = tk.IntVar(value=self.number_of_folds_choice)
        else:
            self.number_of_folds_var = tk.IntVar(value=10)
            

        self.number_of_folds_combobox = ttk.Combobox(self.number_of_folds_combobox_selection_frame, textvariable=self.number_of_folds_var, state="readonly", font=("Arial", 24), width=3)
        self.number_of_folds_combobox['values'] = [2,3,4,5,6,7,8,9,10]
        self.number_of_folds_combobox.bind("<<ComboboxSelected>>", on_number_of_folds_combobox_select)
        self.number_of_folds_combobox.pack(side=tk.LEFT, padx=5, pady=20)

        # TRAIN PERCENT
        if self.train_percent:
            self.train_percent_var = tk.StringVar(value=self.train_percent)
        else:
            self.train_percent_var = tk.StringVar(value="75")




        self.train_fold_percent_frame = tk.Frame(self.number_of_folds_combobox_selection_frame, bg='beige')
        
        self.train_fold_percent_label_1 = tk.Label(self.train_fold_percent_frame, text="Train model on ", font=("Arial", 24), bg='beige')
        self.train_fold_percent_label_1.pack(side=tk.LEFT,padx=5)

        self.train_fold_percent_entry = tk.Entry(self.train_fold_percent_frame, textvariable=self.train_percent_var, font=("Arial", 24), width=5)
        self.train_fold_percent_entry.pack(side=tk.LEFT,padx=5)

        self.train_fold_percent_label_2 = tk.Label(self.train_fold_percent_frame, text="% of the dataframe", font=("Arial", 24), bg='beige')
        self.train_fold_percent_label_2.pack(side=tk.LEFT,padx=5)


        def on_entry_release(event):
            current_value = event.widget.get()
            data_manager.set_mach_learn_tab_train_percent(current_value)

        self.train_fold_percent_entry.bind("<KeyRelease>", lambda event: on_entry_release(event))

        if self.number_of_folds_var.get() == 2:
            self.train_fold_percent_frame.pack(side=tk.LEFT, padx=5, pady=5)




        ##############################################

        # HYPERTUNING PARAMETERS CHECKBOX
        self.hypertune_parameters_frame = tk.Frame(self.model_settings_frame, bg='beige')
        self.hypertune_parameters_frame.pack(side=tk.TOP, fill=tk.BOTH)

        self.hypertune_parameters_label = tk.Label(self.hypertune_parameters_frame, text="Hypertune Model Parameters", font=("Arial", 36), bg='beige')
        self.hypertune_parameters_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.hypertune_parameters_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=400, pady=5)

        if self.hypertune_parameters_choice:
            self.hypertune_parameters_var = tk.StringVar(value=self.hypertune_parameters_choice)
        else:
            self.hypertune_parameters_choice = "No"
            self.hypertune_parameters_var = tk.StringVar(value=self.hypertune_parameters_choice)

        def on_hypertune_parameters_select():
            selected_option = self.hypertune_parameters_var.get()
            data_manager.set_mach_learn_tab_hyper_param_choice(selected_option)

        self.hypertune_parameters_button_frame = tk.Frame(self.hypertune_parameters_frame, bg='beige')
        self.hypertune_parameters_button_frame.pack(side=tk.TOP)

        self.hypertune_parameters_yes_button = tk.Radiobutton(self.hypertune_parameters_button_frame, text="Yes", value="Yes", variable=self.hypertune_parameters_var, command=on_hypertune_parameters_select, indicator=0, font=("Arial", 24), borderwidth=10, width=20)
        self.hypertune_parameters_yes_button.grid(row=0, column=0,)

        self.hypertune_parameters_no_button = tk.Radiobutton(self.hypertune_parameters_button_frame, text="No", value="No", variable=self.hypertune_parameters_var, command=on_hypertune_parameters_select, indicator=0, font=("Arial", 24), borderwidth=10, width=20)
        self.hypertune_parameters_no_button.grid(row=0, column=1)


        ##############################################


        # PLOT SETTINGS
        self.plot_settings_frame = tk.Frame(self.settings_frame, bg='beige')
        self.plot_settings_frame.pack(side=tk.TOP, padx=5, pady=10, fill=tk.BOTH)

        self.plot_settings_label = tk.Label(self.plot_settings_frame, text="Select plot features to include", font=("Arial", 40), bg='beige')
        self.plot_settings_label.pack(side=tk.TOP, fill=tk.X)

        separator = ttk.Separator(self.plot_settings_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=400, pady=5)

        self.plot_features_grid_frame = tk.Frame(self.plot_settings_frame, bg='beige')
        self.plot_features_grid_frame.pack(side=tk.TOP, pady=5)

        self.accuracy_checkbox_var = tk.BooleanVar()
        self.accuracy_checkbox = tk.Checkbutton(self.plot_features_grid_frame, text="Accuracy", variable=self.accuracy_checkbox_var, font=("Arial", 36), bg='beige')
        self.accuracy_checkbox.grid(row=0, column=0, sticky=tk.W, padx=40)
        self.accuracy_checkbox_var.set(True)

        self.sensitivity_checkbox_var = tk.BooleanVar()
        self.sensitivity_checkbox = tk.Checkbutton(self.plot_features_grid_frame, text="Sensitivity", variable=self.sensitivity_checkbox_var, font=("Arial", 36), bg='beige')
        self.sensitivity_checkbox.grid(row=0, column=1, sticky=tk.W, padx=40)
        self.sensitivity_checkbox_var.set(True)

        self.specificity_checkbox_var = tk.BooleanVar()
        self.specificity_checkbox = tk.Checkbutton(self.plot_features_grid_frame, text="Specificity", variable=self.specificity_checkbox_var, font=("Arial", 36), bg='beige')
        self.specificity_checkbox.grid(row=1, column=0, sticky=tk.W, padx=40)
        self.specificity_checkbox_var.set(True)
        
        self.shap_values_checkbox_var = tk.BooleanVar()
        self.shap_values_checkbox = tk.Checkbutton(self.plot_features_grid_frame, text="Shap Values", variable=self.shap_values_checkbox_var, font=("Arial", 36), bg='beige')
        self.shap_values_checkbox.grid(row=1, column=1, sticky=tk.W, padx=40)
        self.shap_values_checkbox_var.set(False)

        ##############################################

        # NAVIGATION MENU FRAME
        self.model_settings_menu_frame = tk.Frame(self.settings_frame, bg='lightgray')
        self.model_settings_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_variable_handling_frame_button = tk.Button(self.model_settings_menu_frame, command=self.switch_to_variable_handling_frame, text='Back', font=("Arial", 36))
        self.return_to_variable_handling_frame_button.pack(side=tk.LEFT)

        self.advance_to_results_frame_button = tk.Button(self.model_settings_menu_frame, command=self.switch_to_results_frame, text='View Results', font=("Arial", 36))
        self.advance_to_results_frame_button.pack(side=tk.RIGHT)

        self.model_settings_frame_dependent_label = tk.Label(self.model_settings_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.model_settings_frame_dependent_label.pack(side=tk.RIGHT, expand=True)





################################################################################################################
################################################################################################################
################################################################################################################

    # CREATE RESULTS FRAME
    
    def create_results_frame(self):

        # GRAPH FRAMES
        self.results_display_frame = tk.Frame(self.results_frame, bg='red')
        self.results_display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.auc_results_frame = tk.Frame(self.results_display_frame, bg='beige')
        self.auc_results_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.auc_graph_label = tk.Label(self.auc_results_frame, text="AUC Graph", font=("Arial", 36, "bold"), bg='beige')
        self.auc_graph_label.pack(side=tk.TOP, fill=tk.X)

        separator = ttk.Separator(self.auc_results_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)

        self.auc_graph_display_frame = tk.Frame(self.auc_results_frame, bg='beige')
        self.auc_graph_display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)




        self.feature_importance_results_frame = tk.Frame(self.results_display_frame, bg='beige')

        self.feature_importance_label = tk.Label(self.feature_importance_results_frame, text="Feature Importances", font=("Arial", 36, "bold"), bg='beige')
        self.feature_importance_label.pack(side=tk.TOP, fill=tk.X)

        separator = ttk.Separator(self.feature_importance_results_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)

        self.feature_importance_display_frame = tk.Frame(self.feature_importance_results_frame, bg='beige')
        self.feature_importance_display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)


        # SAVE FIGURE AND SWITCH BETWEEN GRAPHS FRAME
        self.results_button_frame = tk.Frame(self.results_frame,bg='purple')
        self.results_button_frame.pack(side=tk.TOP, fill=tk.X)

        # Calculate the maximum text width based on the longest possible text for both buttons
        max_text_width = max(len("Save Graph"), len("View Feature Importances"))

        # Save button
        self.save_graph_button = tk.Button(self.results_button_frame, text="Save Graph", command=self.save_figure, font=("Arial", 36), width=max_text_width)
        self.save_graph_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Switch button
        self.switch_graph_button = tk.Button(self.results_button_frame, text="View Feature Importances", command=self.switch_display_frames, font=("Arial", 36), width=max_text_width)
        self.switch_graph_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Configure column weights to make them occupy half of the frame
        self.results_button_frame.columnconfigure(0, weight=1)
        self.results_button_frame.columnconfigure(1, weight=1)

        self.current_graph = "AUC"










        # NAVIGATION MENU FRAME
        self.results_menu_frame = tk.Frame(self.results_frame, bg='lightgray')
        self.results_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_settings_frame_button = tk.Button(self.results_menu_frame, command=self.switch_to_settings_frame, text='<- Back', font=("Arial", 36))
        self.return_to_settings_frame_button.pack(side=tk.LEFT)

        self.results_frame_dependent_label = tk.Label(self.results_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.results_frame_dependent_label.pack(side=tk.LEFT, expand=True)

        self.advance_to_prediction_tool_buton = tk.Button(self.results_menu_frame, command=self.switch_to_prediction_tool, text='Prediction Tool ->', font=("Arial", 36))
        self.advance_to_prediction_tool_buton.pack(side=tk.RIGHT)


    def switch_display_frames(self):

        if self.current_graph == "AUC":
            self.auc_results_frame.pack_forget()
            self.feature_importance_results_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.switch_graph_button.configure(text="View AUC Graph")
            self.current_graph = "Features"

            self.visualize_content_frame.update_idletasks()

        else:
            self.feature_importance_results_frame.pack_forget()
            self.auc_results_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            self.switch_graph_button.configure(text="View Feature Importances")
            self.current_graph = "AUC"

            self.visualize_content_frame.update_idletasks()


    def apply_settings(self):

        self.final_df = self.temp_df.loc[self.temp_df[self.selected_dependent_variable].notna()].reset_index(drop=True).copy()


        # self.null_value_option_var
        # self.null_value_entry_var

        # self.number_of_folds_var
        # self.train_fold_percent_entry

        # self.hypertune_parameters_var


        # NULL VALUES
        if self.null_value_option_var.get() == "REMOVE null values":
            self.final_df = self.final_df.dropna()

        ############################################################
            
        # GET MODEL 
        if self.hypertune_parameters_var.get() == "Yes":
            self.ML_model = self.ML_tune()
        else:
            if self.selected_model_type == "Categorical":
                self.ML_model = self.available_categorical_models_dict[self.selected_model]
            else:
                self.ML_model = self.available_continuous_models_dict[self.selected_model]


        ############################################################
        
        # NUMBER OF FOLDS
        if self.number_of_folds_var.get() == 2:
            self.ML_train_percent = self.train_percent_var.get()
            
            self.auc_graph, self.features_graph = self.ML_single_fold()

            self.display_graphs()
        else:
            self.auc_graph, self.features_graph = self.ML_x_fold()

            self.display_graphs()







    def display_graphs(self):
        utils.remove_frame_widgets(self.auc_graph_display_frame)
        utils.remove_frame_widgets(self.feature_importance_display_frame)

        auc_canvas = FigureCanvasTkAgg(self.auc_graph, master=self.auc_graph_display_frame)
        auc_canvas_widget = auc_canvas.get_tk_widget()
        auc_canvas_widget.pack(fill=tk.BOTH, expand=True)

        features_canvas = FigureCanvasTkAgg(self.features_graph, master=self.feature_importance_display_frame)
        features_canvas_widget = features_canvas.get_tk_widget()
        features_canvas_widget.pack(fill=tk.BOTH, expand=True)





################################################################################################################

# SINGLE TRAINING SET MACHINE LEARNING


    def ML_single_fold(self):

        ############################################################

        # DATA LOADING AND MODEL FITTING #
        X = self.final_df[self.selected_independent_variables]
        y = self.final_df[self.selected_dependent_variable]

        train_percent = float(self.ML_train_percent) / 100
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_percent)

        model = self.ML_model
        model.fit(X_train, y_train)

        ############################################################

        # MODEL ASSESSMENT #
        try:
            y_pred_prob = model.predict_proba(X_test)[:,1]
        except:
            y_pred_prob = model.predict_proba(X_test)[:, 0]

        
        fpr, tpr, _ = roc_curve(y_test, y_pred_prob)
        auc_score = auc(fpr, tpr)

        thresholds = np.arange(0, 1.01, 0.005)

        youden_js = []

        for threshold in thresholds:

            # Convert predicted probabilities into class labels
            y_pred = np.where(y_pred_prob > threshold, 1, 0)

            # Calculate true positive, false positive, true negative, false negative counts
            tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

            # Calculate sensitivity and specificity
            sensitivity = tp / (tp + fn)
            specificity = tn / (tn + fp)

            # Calculate Youden's J statistic
            youden_j = sensitivity + specificity - 1
            youden_js.append(youden_j)

        best_threshold = thresholds[np.argmax(youden_js)]

        y_pred = np.where(y_pred_prob > best_threshold, 1, 0)

        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        sensitivity = tp/(tp+fn)
        specificity = tn/(tn+fp)
        f1 = f1_score(y_test, y_pred)
        accuracy = accuracy_score(y_test, y_pred)


        ############################################################

        # FEATURE IMPORTANCES #
        if hasattr(model, 'feature_importances_'):
            feature_importances = pd.Series(model.feature_importances_, index=X.columns)
            feature_importances = feature_importances.sort_values(ascending=True)
        else:
            feature_importances = pd.Series(model.coef_[0], index=X.columns)
            feature_importances = feature_importances.abs().sort_values(ascending=True)


        # if shap_importances == True:
        #     # explainer = shap.Explainer(model.predict_proba, X_train)
        #     shap_values = explainer(X_test)
        #     shap_plot_values = shap_values[:, :, 1]

        ############################################################

        # PLOTTING GRAPHS #
        auc_fig = Figure()
        features_fig = Figure()

        ############################

        # AUC GRAPH #
        auc_ax = auc_fig.add_subplot(111)
        auc_ax.plot([0, 1], [0, 1], "k--")
        auc_ax.plot(fpr, tpr, label='AUC = %0.2f' % auc_score)

        vertical_position = 0.98

        if self.accuracy_checkbox_var.get():
            auc_ax.text(0.01, vertical_position, 'Accuracy: {}%'.format(round(accuracy*100,1)), fontsize=15, transform=auc_ax.transAxes, ha='left', va='top')
            vertical_position -= 0.04
        if self.sensitivity_checkbox_var.get():
            auc_ax.text(0.01, vertical_position, 'Sensitivity/Recall: {}%'.format(round(sensitivity*100,1)), fontsize=15, transform=auc_ax.transAxes, ha='left', va='top')
            vertical_position -= 0.04
        if self.specificity_checkbox_var.get():
            auc_ax.text(0.01, vertical_position, 'Specificity: {}%'.format(round(specificity*100,1)), fontsize=15, transform=auc_ax.transAxes, ha='left', va='top')
            vertical_position -= 0.04

        # ax1.text(0.01, 0.86, 'F1 Score: {}'.format(round(f1,3)), fontsize=15, transform=ax1.transAxes, ha='left', va='top')
        auc_ax.set(xlim=[-0.00, 1.00], ylim=[0.0, 1.0], xlabel="False Positive Rate", ylabel="True Positive Rate", title=" ")
        auc_ax.legend(loc='lower right', fontsize=24)
        auc_ax.axis("square")

        ############################

        # FEATURE IMPORTANCES GRAPH #
        features_ax = features_fig.add_subplot(111)
        features_ax.barh(feature_importances.index, feature_importances)
        features_ax.set_xlabel("Feature Importance")
        # ax2.set_ylabel('',fontsize=15)

        return auc_fig, features_fig



    def ML_x_fold(self):

        X = self.final_df[self.selected_independent_variables].values
        y = self.final_df[self.selected_dependent_variable].values

        tprs = []
        aucs = []

        cv_num = self.number_of_folds_var.get()

        mean_fpr = np.linspace(0, 1, 100)
        importances = np.zeros((cv_num, X.shape[1]))
        sensitivities = np.zeros((cv_num, 1))
        specificities = np.zeros((cv_num, 1))
        accuracies = np.zeros((cv_num, 1))

        model = self.ML_model

        ###########################################################################################################

        cv = StratifiedKFold(n_splits=cv_num)

        for fold, (train, test) in enumerate(cv.split(X, y)):

            # DATA LOADING AND MODEL FITTING #
            model.fit(X[train], y[train])

            # MODEL ASSESSMENT #
            y_pred_prob = model.predict_proba(X[test])[:,1]
            fpr, tpr, _ = roc_curve(y[test], y_pred_prob)
            auc_score = auc(fpr, tpr)

            thresholds = np.arange(0, 1.01, 0.001)
            youden_js = []

            for threshold in thresholds:

                # Convert predicted probabilities into class labels
                y_pred = np.where(y_pred_prob > threshold, 1, 0)

                # Calculate true positive, false positive, true negative, false negative counts
                tn, fp, fn, tp = confusion_matrix(y[test], y_pred).ravel()

                # Calculate sensitivity and specificity
                sensitivity = tp / (tp + fn)
                specificity = tn / (tn + fp)

                # Calculate Youden's J statistic
                youden_j = sensitivity + specificity - 1
                youden_js.append(youden_j)

            best_threshold = thresholds[np.argmax(youden_js)]

            y_pred = np.where(y_pred_prob > best_threshold, 1, 0)

            tn, fp, fn, tp = confusion_matrix(y[test], y_pred).ravel()

            sensitivity = tp/(tp+fn)
            specificity = tn/(tn+fp)
            accuracy = accuracy_score(y[test], y_pred)

    
            interp_tpr = np.interp(mean_fpr, fpr, tpr)
            interp_tpr[0] = 0.0

            tprs.append(interp_tpr)
            aucs.append(auc_score)

            accuracies[fold, :] = accuracy
            sensitivities[fold, :] = sensitivity
            specificities[fold, :] = specificity


            ############################################################

            # FEATURE IMPORTANCES #

            if hasattr(model, 'feature_importances_'):
                importances[fold, :] = pd.Series(model.feature_importances_, index=self.selected_independent_variables)

            else:
                importances[fold, :] = pd.Series(model.coef_[0], index=self.selected_independent_variables)


        # Calculate mean and standard deviation of feature importances

        mean_importances = pd.Series(importances.mean(axis=0), index=self.selected_independent_variables).sort_values(ascending=True)
        # std_importances = importances.std(axis=0)
        mean_sensitivity = sensitivities.mean(axis=0)
        mean_specificity = specificities.mean(axis=0)
        mean_accuracy = accuracies.mean(axis=0)
        sorted_indices = list(reversed(mean_importances.argsort()[::-1]))


        mean_tpr = np.mean(tprs, axis=0)
        mean_tpr[-1] = 1.0
        mean_auc = auc(mean_fpr, mean_tpr)
        std_auc = np.std(aucs)




        ############################################################

        # GRAPHS

        auc_fig = Figure()
        features_fig = Figure()

        auc_ax = auc_fig.add_subplot(111)
        auc_ax.plot([0, 1], [0, 1], "k--")

        auc_ax.plot(mean_fpr, mean_tpr, color="b", label=r"Mean ROC (AUC = %0.2f $\pm$ %0.2f)" % (mean_auc, std_auc), lw=2, alpha=0.8)

        std_tpr = np.std(tprs, axis=0)
        tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
        tprs_lower = np.maximum(mean_tpr - std_tpr, 0)

        auc_ax.fill_between(mean_fpr, tprs_lower, tprs_upper, color="grey", alpha=0.2, label=r"$\pm$ 1 std. dev.")
        auc_ax.set(xlim=[-0.05, 1.05], ylim=[-0.05, 1.05], xlabel="False Positive Rate", ylabel="True Positive Rate", title=" ")
        auc_ax.axis("square")
        auc_ax.legend(loc="lower right")

        vertical_position = 0.98

        if self.accuracy_checkbox_var.get():
            auc_ax.text(0.01, vertical_position, 'Accuracy: {}%'.format(round(mean_accuracy[0]*100,1)), fontsize=15, transform=auc_ax.transAxes, ha='left', va='top')
            vertical_position -= 0.04
        if self.sensitivity_checkbox_var.get():
            auc_ax.text(0.01, vertical_position, 'Sensitivity: {}%'.format(round(mean_sensitivity[0]*100,1)), fontsize=15, transform=auc_ax.transAxes, ha='left', va='top')
            vertical_position -= 0.04
        if self.specificity_checkbox_var.get():
            auc_ax.text(0.01, vertical_position, 'Specificity: {}%'.format(round(mean_specificity[0]*100,1)), fontsize=15, transform=auc_ax.transAxes, ha='left', va='top')
            vertical_position -= 0.04


        features_ax = features_fig.add_subplot(111)
        features_ax.barh(mean_importances.index, mean_importances.values)
        features_ax.set_xlabel("Feature Importance")
        features_ax.tick_params(axis='x', labelsize=24)

        return auc_fig, features_fig




    def ML_tune(self):

        X = self.final_df[self.selected_independent_variables].values
        y = self.final_df[self.selected_dependent_variable].values

        if self.selected_model == 'Random Forest':
            model = RandomForestClassifier()
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [None, 10, 20, 30],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
        elif self.selected_model == 'XGBoost':
            model = XGBClassifier()
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 4, 5, 6],
                'learning_rate': [0.01, 0.1, 0.2],
                'subsample': [0.8, 0.9, 1.0],
                'min_child_weight': [1, 2, 3]
            }
        elif self.selected_model == 'Logistic Regression':
            model = LogisticRegression()
            param_grid = {
                'penalty': ['l1', 'l2'],
                'C': [0.001, 0.01, 0.1, 1, 10],
                'solver': ['liblinear', 'lbfgs']
            }
        else:
            raise ValueError("Invalid model name")

        # Perform RandomizedSearchCV for hyperparameter tuning
        random_search = RandomizedSearchCV(
            model, param_distributions=param_grid, n_iter=50, scoring='accuracy', cv=self.number_of_folds_var.get(), n_jobs=-1, verbose=2, random_state=69
        )
        
        random_search.fit(X, y)


        # Return the best-tuned model
        best_model = random_search.best_estimator_
        
        return best_model



    def save_figure(self):

        # Prompt the user to choose the save location
        filetypes = [("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("TIFF files", "*.tiff")]
        save_path = filedialog.asksaveasfilename(filetypes=filetypes)

        # Check if the user canceled the dialog
        if not save_path:
            return

        # Save the figure with the specified DPI and path
        if self.current_graph == "AUC":
            self.auc_graph.savefig(save_path, dpi=300)

        elif self.current_graph == "Features":
            self.features_graph.savefig(save_path, dpi=300)



################################################################################################################
################################################################################################################
################################################################################################################
    
    def create_prediction_tool_frame(self):

        # MAIN CONTENT FRAME
        self.prediction_tool_main_content_frame = tk.Frame(self.prediction_tool_frame, bg='beige')
        self.prediction_tool_main_content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.prediction_tool_header_label = tk.Label(self.prediction_tool_main_content_frame, text="Predict Dependent Variable", font=("Arial", 36, "bold"), bg='beige')
        self.prediction_tool_header_label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        separator = ttk.Separator(self.prediction_tool_main_content_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.prediction_frame = tk.Frame(self.prediction_tool_main_content_frame)
        self.prediction_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # USER INPUT FRAME
        self.user_input_frame = tk.Frame(self.prediction_frame, bg='beige')
        self.user_input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        def on_mousewheel(event):
            self.user_input_canvas.yview_scroll(-1 * (event.delta // 120), "units")

        self.user_input_canvas = tk.Canvas(self.user_input_frame, bg='beige')
        self.user_input_scrollbar = tk.Scrollbar(self.user_input_frame, orient="vertical", command=self.user_input_canvas.yview)
        self.user_input_scrollable_frame = tk.Frame(self.user_input_canvas, bg='beige')

        self.user_input_canvas.create_window((0, 0), window=self.user_input_scrollable_frame, anchor="nw")
        self.user_input_canvas.configure(yscrollcommand=self.user_input_scrollbar.set)

        self.user_input_canvas.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        self.user_input_scrollbar.pack(side=tk.RIGHT, fill="y")
        self.user_input_scrollable_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)

        # Bind mouse wheel event to the canvas
        self.user_input_canvas.bind("<MouseWheel>", on_mousewheel)

        self.user_input_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.user_input_canvas.configure(
                scrollregion=self.user_input_canvas.bbox("all")
            )
        )



        # PREDICTION RESULTS FRAME
        self.prediction_results_frame = tk.Frame(self.prediction_frame, bg='beige')
        self.prediction_results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.get_prediction_button = tk.Button(self.prediction_results_frame, text="Get Prediction", command=self.get_prediction, font=("Arial", 28))
        self.get_prediction_button.pack(side=tk.TOP, anchor="center", fill=tk.BOTH, expand=True, padx=100, pady=100)

        self.prediction_outcome_frame = tk.Frame(self.prediction_results_frame, bg='beige')
        self.prediction_outcome_frame.pack(side=tk.TOP, anchor="center", fill=tk.BOTH, expand=True, padx=100, pady=100)

        self.prediction_outcome_percent_label = tk.Label(self.prediction_outcome_frame, text="", bg='beige',font=("Arial", 48, "bold"))
        self.prediction_outcome_percent_label.pack(side=tk.TOP)

        self.prediction_outcome_outcome_label = tk.Label(self.prediction_outcome_frame, text="", bg='beige',font=("Arial", 28))
        self.prediction_outcome_outcome_label.pack(side=tk.TOP)


        # NAVIGATION MENU FRAME
        self.prediction_tool_menu_frame = tk.Frame(self.prediction_tool_frame, bg='lightgray')
        self.prediction_tool_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_results_frame_button = tk.Button(self.prediction_tool_menu_frame, command=self.switch_to_results_frame, text='<- Back', font=("Arial", 36))
        self.return_to_results_frame_button.pack(side=tk.LEFT)

        self.prediction_tool_frame_dependent_label = tk.Label(self.prediction_tool_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.prediction_tool_frame_dependent_label.pack(side=tk.LEFT, expand=True)


    def add_user_input_boxes_to_prediction_frame(self):

        utils.remove_frame_widgets(self.user_input_scrollable_frame)

        self.input_values_label = tk.Label(self.user_input_scrollable_frame, text="Input Values for Each Variable", font=("Arial", 36), bg='beige')
        self.input_values_label.pack(side=tk.TOP, fill=tk.X)

        separator = ttk.Separator(self.user_input_scrollable_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.prediction_input_dict = {}


        for variable in self.selected_independent_variables:

            if len(variable) > 20:
                variable_string = variable[0:19] + "..."
            else:
                variable_string = variable

            variable_frame = tk.Frame(self.user_input_scrollable_frame, bg='beige')
            variable_frame.pack(side=tk.TOP, fill=tk.X, pady=5, padx=20)
        
            input_entry = tk.Entry(variable_frame, font=("Arial", 28), width=10)
            input_entry.pack(side=tk.LEFT)

            variable_label = tk.Label(variable_frame, text=variable_string, font=("Arial", 28), bg='beige', fg='black')
            variable_label.pack(side=tk.LEFT)

            separator = ttk.Separator(self.user_input_scrollable_frame, orient="horizontal", style="Separator.TSeparator")
            separator.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

            input_entry.bind("<KeyRelease>", lambda event, var=variable: self.on_key_release_prediction(event, var))

    def on_key_release_prediction(self, event, variable):
        self.prediction_input_dict[variable] = event.widget.get()


    def get_prediction(self):

        X = self.final_df[self.selected_independent_variables].values
        y = self.final_df[self.selected_dependent_variable].values

        self.ML_model.fit(X, y)



        input_data = []
        for var in self.prediction_input_dict:
            try:
                input_data.append(float(self.prediction_input_dict[var]))
            except:
                utils.show_message("error", "Make sure all values are NUMERICAL")
                return
        if len(input_data) < 1:
            return


        input_data = np.array(input_data).reshape(1, -1)
        predicted_probabilities = self.ML_model.predict_proba(input_data)

        outcome_probability = predicted_probabilities[0][1]
        percentage = outcome_probability * 100
        formatted_percentage = "{:.2f}%".format(percentage)

        prediction_string_percentage = f"{formatted_percentage}"
        prediction_string_rest = f"chance of {self.selected_dependent_variable}"

        self.prediction_outcome_percent_label.configure(text=prediction_string_percentage)
        self.prediction_outcome_outcome_label.configure(text=prediction_string_rest)


################################################################################################################
################################################################################################################
################################################################################################################

    def switch_to_dependent_variable_frame(self):

        self.settings_frame.pack_forget()
        self.variable_handling_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.results_frame.pack_forget()
        self.prediction_tool_frame.pack_forget()
        self.dependent_variable_frame.pack(fill=tk.BOTH, expand=True)

        self.dependent_var_search_entry.focus_set()


    def switch_to_independent_variables_frame(self):
        if self.selected_dependent_variable == None:
            return


        self.settings_frame.pack_forget()
        self.variable_handling_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.prediction_tool_frame.pack_forget()
        self.indedependent_variables_frame.pack(fill=tk.BOTH, expand=True)

        self.independent_var_search_entry.focus_set()

        self.dependent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.independent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.variable_handling_menu_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.model_settings_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.results_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.prediction_tool_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")


    def switch_to_variable_handling_frame(self):

        if self.selected_model == "Linear Regression":
            utils.show_message('error message', "LINEAR REGRESSION NOT READY YET!!!!!")
            return
        if self.selected_model_type == "Categorical":
            if len(self.df[self.selected_dependent_variable].dropna().unique()) != 2:
                utils.show_message('dependent variable error', 'Dependent Variable not binary for logistic regression')
                return

        if len(self.selected_independent_variables) < 1:
            utils.show_message('error message', "Please add independent variables")
            return
        elif self.check_variables_unique_values():
            utils.show_message("error message", "Error with chosen variables. Make sure each variable has more than one unique value")
            return
        elif self.check_variables_duplicates():
            utils.show_message("error message", "Error. Can't have same variables as both dependent and independent variable")
            return
        




        self.handle_variables_machine_learning()


        self.settings_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.prediction_tool_frame.pack_forget()
        self.variable_handling_frame.pack(fill=tk.BOTH, expand=True)

        self.visualize_content_frame.update_idletasks()


    def switch_to_settings_frame(self):
        self.initialize_results_frame = True

        try:
            self.apply_variable_handling()
        except:
            raise
            utils.show_message("error message", "Make sure all values are NUMERICAL")
            return
        
        self.variable_handling_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.prediction_tool_frame.pack_forget()
        self.settings_frame.pack(fill=tk.BOTH, expand=True)

        self.visualize_content_frame.update_idletasks()


    def switch_to_results_frame(self, initialize=True):

        # VERIFY USER INPUT
        if self.null_value_option_var.get() == 'REPLACE with user choice':
            try:
                float(self.null_value_user_choice_entry.get())
            except:
                utils.show_message("error message", "User choice must be a number")
                return

        if self.number_of_folds_var.get() == 2:
            try:
                float(self.train_fold_percent_entry.get())
            except:
                utils.show_message("error message", "User choice must be a number")
                return
        
        if self.initialize_results_frame == True:
            self.apply_settings()

        self.settings_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.variable_handling_frame.pack_forget()
        self.prediction_tool_frame.pack_forget()
        self.results_frame.pack(fill=tk.BOTH, expand=True)

        self.prediction_outcome_percent_label.configure(text="")
        self.prediction_outcome_outcome_label.configure(text="")

        self.visualize_content_frame.update_idletasks()

    def switch_to_prediction_tool(self):

        self.initialize_results_frame = False

        self.add_user_input_boxes_to_prediction_frame()

        self.settings_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.variable_handling_frame.pack_forget()
        self.results_frame.pack_forget()
        self.prediction_tool_frame.pack(fill=tk.BOTH, expand=True)

        self.visualize_content_frame.update_idletasks()



################################################################################################################
################################################################################################################
################################################################################################################
    
    # INPUT VALIDATION

    def check_variables_unique_values(self):
        for column in self.selected_independent_variables + [self.selected_dependent_variable]:
            unique_count = self.df[column].nunique()
            if unique_count <= 1:
                return True
            else:
                return False

    def check_variables_duplicates(self):
        if self.selected_dependent_variable in self.selected_independent_variables:
            return True
        else:
            return False
