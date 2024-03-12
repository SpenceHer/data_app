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
# from xgboost import XGBClassifier
import statsmodels.api as sm
import statsmodels.formula.api as smf
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pingouin as pg

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
from sklearn.linear_model import LinearRegression

# Local application/library specific imports
import data_manager
import file_handling
import utils
import styles
from styles import color_dict

########################

# TO DO NOTE

########################


def setup_visualize_tab(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame):

    df = data_manager.get_dataframe()
    if df is None:
        utils.show_message("Error", "Please open a file first.")
        return
    

    style.configure("file_button.TButton", background=color_dict["inactive_main_tab_bg"], foreground=color_dict["inactive_main_tab_txt"])
    style.configure("dataframe_view_button.TButton", background=color_dict["inactive_main_tab_bg"], foreground=color_dict["inactive_main_tab_txt"])
    style.configure("edit_button.TButton", background=color_dict["inactive_main_tab_bg"], foreground=color_dict["inactive_main_tab_txt"])
    style.configure("visualize_button.TButton", background=color_dict["active_main_tab_bg"], foreground=color_dict["active_main_tab_txt"])

    # CHECK FOR CURRRENT TAB
    tab_dict = data_manager.get_tab_dict()
    try:
        current_tab = tab_dict["current_visualize_tab"]
    except:
        current_tab = None

    # SET SUBTAB COLORS
    for tab in ["comparison_table", "regression", "create_plot", "machine_learning"]:
        button_style = f"{tab}_button.TButton"
        if tab == current_tab:
            style.configure(button_style, background=color_dict["active_subtab_bg"], foreground=color_dict["active_subtab_txt"], borderwidth=0, padding=0, font=styles.sub_tabs_font)
        else:
            style.configure(button_style, background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"], borderwidth=0, padding=0, font=styles.sub_tabs_font)

        style.map(
            button_style,
            background=[("active", color_dict["hover_subtab_bg"])],
            foreground=[("active", color_dict["hover_subtab_txt"])]
        )




    utils.remove_frame_widgets(sub_button_frame)

    comparison_table_button = ttk.Button(sub_button_frame, text="Comparison Table", style="comparison_table_button.TButton")
    comparison_table_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    comparison_table_button.config(command=lambda: ComparisonTableClass(visualize_content_frame, style))

    regression_button = ttk.Button(sub_button_frame, text="Regression", style="regression_button.TButton")
    regression_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    regression_button.config(command=lambda: RegressionAnalysisClass(visualize_content_frame, style))

    create_plot_button = ttk.Button(sub_button_frame, text="Create Plot", style="create_plot_button.TButton")
    create_plot_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    create_plot_button.config(command=lambda: CreatePlotClass(visualize_content_frame, style))

    machine_learning_button = ttk.Button(sub_button_frame, text="Machine Learning", style="machine_learning_button.TButton")
    machine_learning_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    machine_learning_button.config(command=lambda: MachineLearningClass(visualize_content_frame, style))


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
                    elif tab_dict['current_visualize_tab'] == 'machine_learning':
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
        self.df.replace("[MISSING VALUE]", np.nan, inplace=True)

        self.visualize_content_frame = visualize_content_frame

        self.style = style


        self.style.configure("comparison_table_button.TButton", background=color_dict["active_subtab_bg"], foreground=color_dict["active_subtab_txt"])
        self.style.configure("regression_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"])
        self.style.configure("create_plot_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"])
        self.style.configure("machine_learning_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"])

        data_manager.add_tab_to_tab_dict("current_visualize_tab", "comparison_table")

        self.selected_dependent_variable = data_manager.get_comp_tab_dep_var()
        self.selected_independent_variables = data_manager.get_comp_tab_ind_var_list()
        self.selected_percent_type = data_manager.get_comp_tab_percent_type()
        self.selected_data = data_manager.get_comp_tab_data_selection()
        self.variable_type_dict = data_manager.get_comp_tab_variable_type_dict()

        self.verify_saved_columns()

        utils.remove_frame_widgets(self.visualize_content_frame)

        self.error = False


        self.dependent_variable_frame = tk.Frame(self.visualize_content_frame, bg=color_dict["main_content_border"])
        self.indedependent_variables_frame = tk.Frame(self.visualize_content_frame, bg=color_dict["main_content_border"])
        self.variable_handling_frame = tk.Frame(self.visualize_content_frame, bg=color_dict["main_content_border"])
        self.results_frame = tk.Frame(self.visualize_content_frame, bg=color_dict["main_content_border"])



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
        self.dependent_variable_inner_frame, self.dependent_variable_canvas = utils.create_scrollable_frame(self.dependent_variable_frame)

################################################################################################################

        # DEPENDENT VARIABLE SELECTION

        self.dependent_variable_selection_subframe_border = tk.Frame(self.dependent_variable_inner_frame, bg=color_dict["sub_frame_border"])
        self.dependent_variable_selection_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.dependent_variable_selection_subframe = tk.Frame(self.dependent_variable_selection_subframe_border, bg=color_dict["sub_frame_bg"])
        self.dependent_variable_selection_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.dependent_variable_frame_label = ttk.Label(self.dependent_variable_selection_subframe, text="Dependent Variable Selection", style="sub_frame_header.TLabel")
        self.dependent_variable_frame_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.dependent_variable_selection_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)

        # DEPENDENT VARIABLE SELECTION FRAME
        self.dependent_column_choice_frame = tk.Frame(self.dependent_variable_selection_subframe, bg=color_dict["sub_frame_bg"])
        self.dependent_column_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

        self.dependent_search_var = tk.StringVar()
        self.dependent_search_var.trace("w", self.update_dependent_variable_listbox)
        self.dependent_var_search_entry = tk.Entry(self.dependent_column_choice_frame, textvariable=self.dependent_search_var, font=styles.entrybox_small_font)
        self.dependent_var_search_entry.pack(side=tk.TOP, pady=10)

        self.dependent_variable_listbox = tk.Listbox(self.dependent_column_choice_frame, selectmode=tk.SINGLE, font=styles.listbox_font, exportselection=False, bg=color_dict["listbox_bg"],
                     fg=color_dict["listbox_fg"],
                     highlightbackground=color_dict["listbox_highlight_bg"],
                     highlightcolor=color_dict["listbox_highlight_color"],
                     selectbackground=color_dict["listbox_select_bg"],
                     selectforeground=color_dict["listbox_select_fg"],
                     height=20)
        self.dependent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)
        self.dependent_variable_listbox.bind("<Enter>",lambda e: utils.bind_mousewheel_to_frame(self.dependent_variable_inner_frame, self.dependent_variable_canvas, False))
        self.dependent_variable_listbox.bind("<Leave>",lambda e: utils.bind_mousewheel_to_frame(self.dependent_variable_inner_frame, self.dependent_variable_canvas, True))



        for column in sorted(self.df.columns, key=str.lower):
            self.dependent_variable_listbox.insert(tk.END, column)

        self.dependent_variable_listbox.bind("<<ListboxSelect>>", self.on_dependent_variable_listbox_select)




################################################################################################################

        # NAVIGATION MENU
        self.dependent_variable_menu_frame = tk.Frame(self.dependent_variable_frame, bg=color_dict["nav_banner_bg"])
        self.dependent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.advance_to_independent_variables_button = ttk.Button(self.dependent_variable_menu_frame, text="Next", command=self.switch_to_independent_variables_frame, style='nav_menu_button.TButton')
        self.advance_to_independent_variables_button.pack(side=tk.RIGHT)

        self.dependent_frame_dependent_label = ttk.Label(self.dependent_variable_menu_frame, text="", style="nav_menu_label.TLabel")
        self.dependent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)



        if self.selected_dependent_variable:
            self.dependent_variable_listbox.selection_clear(0, tk.END)
            items = list(self.dependent_variable_listbox.get(0, tk.END))
            index = items.index(self.selected_dependent_variable)
            self.dependent_variable_listbox.selection_set(index)
            self.dependent_variable_listbox.yview(index)
            self.dependent_frame_dependent_label.config(text=f"Dependent Variable: {self.selected_dependent_variable}")



################################################################################################################

    def on_dependent_variable_listbox_select(self, event):
        if self.dependent_variable_listbox.curselection():
            self.selected_dependent_variable = self.dependent_variable_listbox.get(self.dependent_variable_listbox.curselection()[0])
            data_manager.set_comp_tab_dep_var(self.selected_dependent_variable)
            self.dependent_frame_dependent_label.config(text=f"Dependent Variable: {self.selected_dependent_variable}")


    def update_dependent_variable_listbox(self, *args):
        search_term = self.dependent_search_var.get().lower()
        self.dependent_variable_listbox.delete(0, tk.END)

        # Check if the search term is empty
        if search_term == "":
            # If search term is empty, insert all columns sorted alphabetically
            for column in sorted(self.df.columns, key=str.lower):
                self.dependent_variable_listbox.insert(tk.END, column)
            if self.selected_dependent_variable:
                self.dependent_variable_listbox.selection_clear(0, tk.END)
                items = list(self.dependent_variable_listbox.get(0, tk.END))
                index = items.index(self.selected_dependent_variable)
                self.dependent_variable_listbox.selection_set(index)
        else:
            # If there is a search term, filter and sort the columns based on the search term
            filtered_sorted_columns = sorted([column for column in self.df.columns if search_term in column.lower()], key=str.lower)
            # Populate the Listbox with the sorted list
            for column in filtered_sorted_columns:
                self.dependent_variable_listbox.insert(tk.END, column)
            if self.selected_dependent_variable in filtered_sorted_columns:
                self.dependent_variable_listbox.selection_clear(0, tk.END)
                items = list(self.dependent_variable_listbox.get(0, tk.END))
                index = items.index(self.selected_dependent_variable)
                self.dependent_variable_listbox.selection_set(index)





################################################################################################################
################################################################################################################
################################################################################################################


    # CREATE INDEPENDENT VARIABLE SELECTION FRAME

    def create_independent_variables_frame(self):

        # MAIN CONTENT FRAME
        self.independent_variables_inner_frame, self.independent_variables_canvas = utils.create_scrollable_frame(self.indedependent_variables_frame)

################################################################################################################

        # INDEPENDENT VARIABLES SELECTION
        self.independent_variables_selection_subframe_border = tk.Frame(self.independent_variables_inner_frame, bg=color_dict["sub_frame_border"])
        self.independent_variables_selection_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.independent_variables_selection_subframe = tk.Frame(self.independent_variables_selection_subframe_border, bg=color_dict["sub_frame_bg"])
        self.independent_variables_selection_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.choose_independent_variables_label = ttk.Label(self.independent_variables_selection_subframe, text="Independent Variable Selection", style="sub_frame_header.TLabel")
        self.choose_independent_variables_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.independent_variables_selection_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)


        # AVAILABLE INDEPENDENT VARIABLES SELECTION FRAME
        self.indedependent_variables_selection_frame = tk.Frame(self.independent_variables_selection_subframe, bg=color_dict["sub_frame_bg"])
        self.indedependent_variables_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

        self.available_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg=color_dict["sub_frame_bg"])
        self.available_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.available_independent_search_var = tk.StringVar()
        self.available_independent_search_var.trace("w", self.update_available_independent_variable_listbox)
        self.independent_var_search_entry = tk.Entry(self.available_independent_variables_frame, textvariable=self.available_independent_search_var, font=styles.entrybox_small_font)
        self.independent_var_search_entry.pack(side=tk.TOP, pady=10)

        self.available_independent_variable_listbox = tk.Listbox(self.available_independent_variables_frame, selectmode=tk.MULTIPLE, font=styles.listbox_font,
                                                                bg=color_dict["listbox_bg"],
                                                                fg=color_dict["listbox_fg"],
                                                                highlightbackground=color_dict["listbox_highlight_bg"],
                                                                highlightcolor=color_dict["listbox_highlight_color"],
                                                                selectbackground=color_dict["listbox_select_bg"],
                                                                selectforeground=color_dict["listbox_select_fg"]
                                                                )
        self.available_independent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)
        self.available_independent_variable_listbox.bind("<Enter>",lambda e: utils.bind_mousewheel_to_frame(self.independent_variables_inner_frame, self.independent_variables_canvas, False))
        self.available_independent_variable_listbox.bind("<Leave>",lambda e: utils.bind_mousewheel_to_frame(self.independent_variables_inner_frame, self.independent_variables_canvas, True))



        for column in sorted(self.df.columns, key=str.lower):
            if column not in self.selected_independent_variables:
                self.available_independent_variable_listbox.insert(tk.END, column)


        # TRANSFER BUTTONS
        self.buttons_frame = tk.Frame(self.indedependent_variables_selection_frame, bg=color_dict["sub_frame_bg"])
        self.buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Larger buttons with ">>>" and "<<<" symbols
        self.transfer_right_button = ttk.Button(self.buttons_frame, text="Transfer Right >>>", command=self.transfer_right, style="large_button.TButton")
        self.transfer_right_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.transfer_left_button = ttk.Button(self.buttons_frame, text="<<< Transfer Left", command=self.transfer_left, style="large_button.TButton")
        self.transfer_left_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)

        separator = ttk.Separator(self.buttons_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, pady=10)

        # Text buttons "Select All" and "Clear Selection"
        self.transfer_all_right_button = ttk.Button(self.buttons_frame, text="Select All", command=self.transfer_all_right, style="large_button.TButton")
        self.transfer_all_right_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)

        self.transfer_all_left_button = ttk.Button(self.buttons_frame, text="Clear Selection", command=self.transfer_all_left, style="large_button.TButton")
        self.transfer_all_left_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)


        separator = ttk.Separator(self.buttons_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

        # Import and export selected variables
        self.import_variable_list_button = ttk.Button(self.buttons_frame, text="Import Variable List", command=self.import_variable_list, style="large_button.TButton")
        self.import_variable_list_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)

        self.export_variable_list_button = ttk.Button(self.buttons_frame, text="Export Variable List", command=self.export_variable_list, style="large_button.TButton")
        self.export_variable_list_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)


        # SELECTED INDEPENDENT VARIABLES FRAME
        self.selected_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg=color_dict["sub_frame_bg"])
        self.selected_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.selected_independent_variables_label = ttk.Label(self.selected_independent_variables_frame, text="Selected Variables", style="sub_frame_sub_header.TLabel")
        self.selected_independent_variables_label.pack(side=tk.TOP, pady=10)



        self.selected_independent_variable_listbox = tk.Listbox(self.selected_independent_variables_frame, selectmode=tk.MULTIPLE, font=styles.listbox_font,
                                                                bg=color_dict["listbox_bg"],
                                                                fg=color_dict["listbox_fg"],
                                                                highlightbackground=color_dict["listbox_highlight_bg"],
                                                                highlightcolor=color_dict["listbox_highlight_color"],
                                                                selectbackground=color_dict["listbox_select_bg"],
                                                                selectforeground=color_dict["listbox_select_fg"]
                                                                )
        self.selected_independent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)
        self.selected_independent_variable_listbox.bind("<Enter>",lambda e: utils.bind_mousewheel_to_frame(self.independent_variables_inner_frame, self.independent_variables_canvas, False))
        self.selected_independent_variable_listbox.bind("<Leave>",lambda e: utils.bind_mousewheel_to_frame(self.independent_variables_inner_frame, self.independent_variables_canvas, True))

        if len(self.selected_independent_variables) > 0:
            for var in self.selected_independent_variables:
                self.selected_independent_variable_listbox.insert(tk.END, var)
                self.available_independent_variable_listbox.selection_set(sorted(self.df.columns, key=str.lower).index(var))
            selections = self.available_independent_variable_listbox.curselection()
            for index in reversed(selections):
                self.available_independent_variable_listbox.delete(index)






################################################################################################################

        # TABLE OPTIONS

        self.table_options_subframe_border = tk.Frame(self.independent_variables_inner_frame, bg=color_dict["sub_frame_border"])
        self.table_options_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.table_options_subframe = tk.Frame(self.table_options_subframe_border, bg=color_dict["sub_frame_bg"])
        self.table_options_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.choose_independent_variables_label = ttk.Label(self.table_options_subframe, text="Percent Type and Data Selection", style="sub_frame_header.TLabel")
        self.choose_independent_variables_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.table_options_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)


        self.table_options_frame = tk.Frame(self.table_options_subframe, bg=color_dict["sub_frame_bg"])
        self.table_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)
        self.table_options_frame.grid_columnconfigure(0, weight=1, uniform="group1")
        self.table_options_frame.grid_columnconfigure(2, weight=1, uniform="group1")


        # ROW OR COLUMN PERCENTAGE SELECTION

        self.percentage_type_selection_frame = tk.Frame(self.table_options_frame, bg=color_dict["sub_frame_bg"])
        self.percentage_type_selection_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        self.percent_type_label = ttk.Label(self.percentage_type_selection_frame, text="Table Percent Selection", style="sub_frame_sub_header.TLabel")
        self.percent_type_label.pack(side=tk.TOP, padx=10)


        separator = ttk.Separator(self.percentage_type_selection_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=10)

        # Initialize your buttons with the inactive style
        self.row_percentage_button = ttk.Button(self.percentage_type_selection_frame, text="Row Percentages", style="inactive_radio_button.TButton", command=lambda: self.toggle_button_style("Row"))
        self.row_percentage_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.column_percentage_button = ttk.Button(self.percentage_type_selection_frame, text="Column Percentages", style="inactive_radio_button.TButton", command=lambda: self.toggle_button_style("Column"))
        self.column_percentage_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Load Previously Chosen Percent Selection
        if self.selected_percent_type:
            if self.selected_percent_type == "Row":
                self.toggle_button_style("Row")
            elif self.selected_percent_type == "Column":
                self.toggle_button_style("Column")
        else:
            self.toggle_button_style("Row")

        # SEPARATOR
        separator = ttk.Separator(self.table_options_frame, orient="vertical", style="Separator.TSeparator")
        separator.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)



        # ALL DATA OR ONLY DATA COMPLETE SUBJECTS SELECTION
        self.data_choice_frame = tk.Frame(self.table_options_frame, bg=color_dict["sub_frame_bg"])
        self.data_choice_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=5)

        self.data_choice_label = ttk.Label(self.data_choice_frame, text="Data Selection", style="sub_frame_sub_header.TLabel")
        self.data_choice_label.pack(side=tk.TOP, padx=10)

        separator = ttk.Separator(self.data_choice_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=10)

        # Initialize your buttons with the inactive style
        self.all_data_radio_button = ttk.Button(self.data_choice_frame, text="All Data", style="inactive_radio_button.TButton", command=lambda: self.toggle_button_style("All Data"))
        self.all_data_radio_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.complete_data_only_radio_button = ttk.Button(self.data_choice_frame, text="Only Data-Complete Subjects", style="inactive_radio_button.TButton", command=lambda: self.toggle_button_style("Data Complete Only"))
        self.complete_data_only_radio_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Load Previously Chosen Data Selection
        if self.selected_data:
            self.toggle_button_style(self.selected_data)
        else:
            self.toggle_button_style("All Data")




################################################################################################################


        # NAVIGATION MENU
        self.independent_variable_menu_frame = tk.Frame(self.indedependent_variables_frame, bg=color_dict["nav_banner_bg"])
        self.independent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_dependent_variable_frame_button = ttk.Button(self.independent_variable_menu_frame, command=self.switch_to_dependent_variable_frame, text='Back', style='nav_menu_button.TButton')
        self.return_to_dependent_variable_frame_button.pack(side=tk.LEFT)

        self.advance_to_variable_handling_frame_button = ttk.Button(self.independent_variable_menu_frame, command=self.switch_to_variable_handling_frame, text='Next', style='nav_menu_button.TButton')
        self.advance_to_variable_handling_frame_button.pack(side=tk.RIGHT)

        self.independent_frame_dependent_label = ttk.Label(self.independent_variable_menu_frame, text="", style="nav_menu_label.TLabel")
        self.independent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)

################################################################################################################

    # Function to toggle button styles
    def toggle_button_style(self, selected):
        if selected in ["Row", "Column"]:
            if selected == "Row":
                self.row_percentage_button.configure(style="active_radio_button.TButton")
                self.column_percentage_button.configure(style="inactive_radio_button.TButton")
                self.selected_percent_type = "Row"
                data_manager.set_comp_tab_percent_type(self.selected_percent_type)
            elif selected == "Column":
                self.row_percentage_button.configure(style="inactive_radio_button.TButton")
                self.column_percentage_button.configure(style="active_radio_button.TButton")
                self.selected_percent_type = "Column"
                data_manager.set_comp_tab_percent_type(self.selected_percent_type)
        elif selected in ["All Data", "Data Complete Only"]:
            if selected == "All Data":
                self.all_data_radio_button.configure(style="active_radio_button.TButton")
                self.complete_data_only_radio_button.configure(style="inactive_radio_button.TButton")
                self.selected_data = "All Data"
                data_manager.set_comp_tab_data_type(self.selected_data)
            elif selected == "Data Complete Only":
                self.all_data_radio_button.configure(style="inactive_radio_button.TButton")
                self.complete_data_only_radio_button.configure(style="active_radio_button.TButton")
                self.selected_data = "Data Complete Only"
                data_manager.set_comp_tab_data_type(self.selected_data)



    def update_available_independent_variable_listbox(self, *args):
        search_term = self.available_independent_search_var.get().lower()
        self.available_independent_variable_listbox.delete(0, tk.END)
        for column in sorted(self.df.columns, key=str.lower):
            if search_term in column.lower():
                if column not in self.selected_independent_variables:
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
        
        self.independent_var_search_entry.focus_set()


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
            if item not in self.selected_independent_variables:
                self.available_independent_variable_listbox.insert(tk.END, item)

        if top_visible_index >= 0:
            index = items.index(top_visible_item)
            self.available_independent_variable_listbox.yview(index)


    def import_variable_list(self):
        imported_variable_list = data_manager.get_exported_variables_list()

        for var in imported_variable_list:
            if var in self.df.columns:
                self.selected_independent_variable_listbox.insert(tk.END, var)
                self.selected_independent_variables.append(var)


    def export_variable_list(self):
        data_manager.clear_exported_variables_list()
        for var in self.selected_independent_variables:
            data_manager.add_variable_to_exported_variables_list(var)
        






################################################################################################################
################################################################################################################
################################################################################################################

    # CREATE VARIABLE HANDLING FRAME

    def create_variable_handling_frame(self):

        # MAIN CONTENT FRAME
        self.variable_handling_inner_frame, self.variable_handling_canvas = utils.create_scrollable_frame(self.variable_handling_frame)

################################################################################################################

        # VARIABLE HANDLING
        self.variable_handling_subframe_border = tk.Frame(self.variable_handling_inner_frame, bg=color_dict["sub_frame_border"])
        self.variable_handling_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.variable_handling_subframe = tk.Frame(self.variable_handling_subframe_border, bg=color_dict["sub_frame_bg"])
        self.variable_handling_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.variable_handling_label = ttk.Label(self.variable_handling_subframe, text="Variable Type Selection", style="sub_frame_header.TLabel")
        self.variable_handling_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.variable_handling_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)





        self.variable_type_selection_frame = tk.Frame(self.variable_handling_subframe, bg=color_dict["sub_frame_bg"])
        self.variable_type_selection_frame.pack(side=tk.TOP, pady=10)


################################################################################################################


        # NAVIGATION MENU
        self.variable_handling_menu_frame = tk.Frame(self.variable_handling_frame, bg=color_dict["nav_banner_bg"])
        self.variable_handling_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_independent_variable_frame_button = ttk.Button(self.variable_handling_menu_frame, command=self.switch_to_independent_variables_frame, text='Back', style='nav_menu_button.TButton')
        self.return_to_independent_variable_frame_button.pack(side=tk.LEFT)

        self.view_results_button = ttk.Button(self.variable_handling_menu_frame, command=self.switch_to_results_frame, text='View Results', style='nav_menu_button.TButton')
        self.view_results_button.pack(side=tk.RIGHT)

        self.variable_handling_menu_frame_dependent_label = ttk.Label(self.variable_handling_menu_frame, text="", style="nav_menu_label.TLabel")
        self.variable_handling_menu_frame_dependent_label.pack(side=tk.RIGHT, expand=True)


################################################################################################################

    def handle_variables(self):
        utils.remove_frame_widgets(self.variable_type_selection_frame)

        for value in list(self.selected_independent_variables):
            options_frame = tk.Frame(self.variable_type_selection_frame, bg=color_dict["sub_frame_bg"])
            options_frame.pack(side=tk.TOP, anchor="e")

            value_string = value[0:19] + "..." if len(value) >= 20 else value

            value_label = ttk.Label(options_frame, text=value_string, style="sub_frame_sub_header.TLabel")
            value_label.pack(side=tk.LEFT, padx=5, pady=5, anchor="w")


            radio_button_frame = tk.Frame(options_frame, bg=color_dict["sub_frame_bg"])
            radio_button_frame.pack(side=tk.LEFT, anchor="w")

            continuous_button = ttk.Button(radio_button_frame, text="Continuous", style="inactive_radio_button.TButton")
            continuous_button.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)
            
            categorical_button = ttk.Button(radio_button_frame, text="Categorical", style="inactive_radio_button.TButton")
            categorical_button.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)

            both_button = ttk.Button(radio_button_frame, text="Both", style="inactive_radio_button.TButton")
            both_button.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)


            continuous_button.configure(command=lambda value=value, cb=continuous_button, catb=categorical_button, bb=both_button: self.toggle_variable_type_button_style(value, "Continuous", cb, catb, bb))
            categorical_button.configure(command=lambda value=value, cb=continuous_button, catb=categorical_button, bb=both_button: self.toggle_variable_type_button_style(value, "Categorical", cb, catb, bb))
            both_button.configure(command=lambda value=value, cb=continuous_button, catb=categorical_button, bb=both_button: self.toggle_variable_type_button_style(value, "Both", cb, catb, bb))



            separator = ttk.Separator(self.variable_type_selection_frame, orient="horizontal", style="Separator.TSeparator")
            separator.pack(fill=tk.X, pady=5)


            if value in self.variable_type_dict:

                selected_type = self.variable_type_dict[value]
            
                if selected_type == "Continuous":
                    continuous_button.configure(style="active_radio_button.TButton")
                elif selected_type == "Categorical":
                    categorical_button.configure(style="active_radio_button.TButton")
                elif selected_type == "Both":
                    both_button.configure(style="active_radio_button.TButton")
            else:
                self.variable_type_dict[value] = "Continuous"
                continuous_button.configure(style="active_radio_button.TButton")

    def toggle_variable_type_button_style(self, value, selection, continuous_button, categorical_button, both_button):
        styles = {"Continuous": ("active_radio_button.TButton", "inactive_radio_button.TButton", "inactive_radio_button.TButton"),
                  "Categorical": ("inactive_radio_button.TButton", "active_radio_button.TButton", "inactive_radio_button.TButton"),
                  "Both": ("inactive_radio_button.TButton", "inactive_radio_button.TButton", "active_radio_button.TButton")}

        cont_style, cat_style, both_style = styles[selection]
        continuous_button.configure(style=cont_style)
        categorical_button.configure(style=cat_style)
        both_button.configure(style=both_style)
        self.variable_type_dict[value] = selection

################################################################################################################
################################################################################################################
################################################################################################################

    # CREATE RESULTS FRAME

    def create_results_frame(self):

        # MAIN CONTENT FRAME
        self.results_inner_frame, self.results_canvas = utils.create_scrollable_frame(self.results_frame)

################################################################################################################

        # RESULTS TABLE DISPLAY FRAME
        self.results_table_subframe_border = tk.Frame(self.results_inner_frame, bg=color_dict["sub_frame_border"])
        self.results_table_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.results_table_subframe = tk.Frame(self.results_table_subframe_border, bg=color_dict["sub_frame_bg"])
        self.results_table_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.results_table_label = ttk.Label(self.results_table_subframe, text="Comparison Table Display", style="sub_frame_header.TLabel")
        self.results_table_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.results_table_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)


        self.results_display_frame = tk.Frame(self.results_table_subframe, bg=color_dict["sub_frame_bg"])
        self.results_display_frame.pack(side=tk.TOP, fill=tk.Y, expand=True, pady=10)


################################################################################################################

        # NAVIGATION MENU
        self.results_menu_frame = tk.Frame(self.results_frame, bg=color_dict["nav_banner_bg"])
        self.results_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_variable_handling_frame_button = ttk.Button(self.results_menu_frame, command=self.switch_to_variable_handling_frame, text='Back', style='nav_menu_button.TButton')
        self.return_to_variable_handling_frame_button.pack(side=tk.LEFT)

        self.results_frame_dependent_label = ttk.Label(self.results_menu_frame, text="", style="nav_menu_label.TLabel")
        self.results_frame_dependent_label.pack(side=tk.RIGHT, expand=True)

################################################################################################################

    def apply_comparison_table_variable_selection(self):
        self.selected_variable_types = {}

        for var in self.selected_independent_variables:
            if var in self.variable_type_dict:
                self.selected_variable_types[var] = self.variable_type_dict[var]



    def create_comparison_table(self):
        self.apply_comparison_table_variable_selection()
        utils.remove_frame_widgets(self.results_display_frame)

        if self.selected_data == "All Data":
            self.table_df = self.df[self.selected_independent_variables + [self.selected_dependent_variable]].copy()
            self.table_df = self.table_df.dropna(subset=self.selected_dependent_variable)

        if self.selected_data == "Data Complete Only":
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


                    # # Run Stats for Continuous Variable
                    # comparison_groups = []

                    # if len(self.unique_dependent_variable_values) > 2:
                    #     # More than two unique values, perform ANOVA
                    #     for value in self.unique_dependent_variable_values:
                    #         group = self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == value, independent_variable]
                    #         comparison_groups.append(group)

                    #     _, p_value = stats.f_oneway(*comparison_groups)
                    #     if p_value < 0.0001:
                    #         p_value = '< 0.0001'
                    #         row1.append(p_value)
                    #     else:
                    #         row1.append(f"{p_value:.4f}")
                    # else:
                    #     for value in self.unique_dependent_variable_values:
                    #         group = self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == value, independent_variable]
                    #         comparison_groups.append(group)

                    #     _, p_value = stats.ttest_ind(*comparison_groups)

                    #     if p_value < 0.0001:
                    #         p_value = '< 0.0001'
                    #         row1.append(p_value)
                    #         row1.append(np.nan)
                    #     else:
                    #         row1.append(f"{p_value:.4f}")
                    #         row1.append(np.nan)

                    comparison_groups = []

                    for value in self.unique_dependent_variable_values:
                        group = self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == value, independent_variable]
                        comparison_groups.append(group)

                    if self.check_normality(comparison_groups):
                        # Check for equal variances
                        if self.check_variances(comparison_groups):
                            if len(comparison_groups) == 2:
                                _, p_value = stats.ttest_ind(comparison_groups)  # Independent two-sample t-test
                            else:
                                _, p_value = stats.f_oneway(*comparison_groups)  # ANOVA
                        else:
                            # Welch's t-test for two groups with unequal variances
                            if len(comparison_groups) == 2:
                                _, p_value = stats.ttest_ind(comparison_groups, equal_var=False)
                            else:
                                p_value = self.run_welchs_anova(comparison_groups)

                    else:
                        # Non-parametric tests
                        if len(comparison_groups) == 2:
                            _, p_value = stats.mannwhitneyu(*comparison_groups)

                        else:
                            _, p_value = stats.kruskal(*comparison_groups)

                    if p_value < 0.0001:
                        p_value = '< 0.0001'
                        row1.append(p_value)
                    else:
                        row1.append(f"{p_value:.4f}")
                










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
                    # utils.show_message("Continuous variable change error", f"Cannot convert to continuous variable for: {independent_variable}")
                    # return
                    raise

            elif option == 'Categorical':
 

                self.clean_df = self.table_df[[independent_variable, self.selected_dependent_variable]].dropna()

                # Independent variable is categorical

                try:

                    observed = pd.crosstab(self.clean_df[independent_variable], self.clean_df[self.selected_dependent_variable])

                    # Calculate the odds ratio
                    numerator = observed.iloc[1, 1] * observed.iloc[0, 0]
                    denominator = (observed.iloc[1, 0] * observed.iloc[0, 1])

                    if denominator == 0:
                        odds_ratio = np.nan
                        ci_lower = np.nan
                        ci_upper = np.nan

                    else:
                        odds_ratio = numerator / denominator

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

                    if self.selected_percent_type == "Row":

                        for value in row:
                            new_row.append(f"{value} ({int(round(value/row_sum*100,0))}%)")

                    if self.selected_percent_type == "Column":

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
                    comparison_groups = []
                    if len(self.unique_dependent_variable_values) > 2:
                        # More than two unique values, perform ANOVA
                        for value in self.unique_dependent_variable_values:
                            group = self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == value, independent_variable]
                            comparison_groups.append(group)
                        _, p_value = stats.f_oneway(*comparison_groups)
                        if p_value < 0.0001:
                            p_value = '< 0.0001'
                            row1.append(p_value)
                        else:
                            row1.append(f"{p_value:.4f}")
                    else:
                        for value in self.unique_dependent_variable_values:
                            group = self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == value, independent_variable]
                            comparison_groups.append(group)
                        _, p_value = stats.ttest_ind(*comparison_groups)

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

                    if self.selected_percent_type == "Row":

                        for value in row:
                            new_row.append(f"{value} ({int(round(value/row_sum*100,0))}%)")

                    if self.selected_percent_type == "Column":

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


        
        height = int(len(self.summary_df) * 1.2)
        if height > 20:
            height = 20

        utils.create_table(self.results_display_frame, self.summary_df, self.style, height=height)

        save_summary_button = ttk.Button(self.results_display_frame, text="Save Table", command=lambda: file_handling.save_file(self.summary_df), style="large_button.TButton")
        save_summary_button.pack(side=tk.BOTTOM, pady=10)



    def check_normality(self, groups):
        normal = True
        for group in groups:
            stat, p = stats.shapiro(group)
            if p < 0.05:  # Not normal
                normal = False
                break
        return normal

    # Function to check equal variances
    def check_variances(self, groups):
        stat, p = stats.levene(groups)
        return p >= 0.05  # True if variances are equal

    def run_welchs_anova(self, groups):
        # Initialize an empty list for values and labels
        values = []
        labels = []

        # Loop through each group, appending the values to the values list
        # and the corresponding labels to the labels list
        for i, group in enumerate(groups, start=1):
            values.extend(group)
            labels.extend([f'Group{i}'] * len(group))

        # Create a DataFrame from the values and labels
        data = pd.DataFrame({'Value': values, 'Group': labels})

        # Perform Welch's ANOVA
        res = pg.welch_anova(dv='Value', between='Group', data=data)
        return res.loc[0, 'p-unc']  # Return the p-value from Welch's ANOVA


################################################################################################################
################################################################################################################
################################################################################################################


    # NAVIGATION MENU HANDLING FUNCTIONS

    def switch_to_dependent_variable_frame(self):

        self.variable_handling_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        self.visualize_content_frame.update_idletasks()
        self.dependent_var_search_entry.focus_set()

        utils.bind_mousewheel_to_frame(self.dependent_variable_inner_frame, self.dependent_variable_canvas, True)




    def switch_to_independent_variables_frame(self):
        if self.selected_dependent_variable == None:
            return

        self.variable_handling_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.indedependent_variables_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)



        self.dependent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.independent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.results_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.variable_handling_menu_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")


        utils.bind_mousewheel_to_frame(self.independent_variables_inner_frame, self.independent_variables_canvas, True)
        self.visualize_content_frame.update_idletasks()
        self.independent_var_search_entry.focus_set()






    def switch_to_variable_handling_frame(self):

        self.selected_independent_variables = [self.selected_independent_variable_listbox.get(index) for index in range(self.selected_independent_variable_listbox.size())]


        if (self.selected_percent_type not in ["Row", "Column"]):
            utils.show_message("Error", "Please select either Row or Column Percentages")
            return
        if (self.selected_data not in ["All Data","Data Complete Only"]):
            utils.show_message("Error", "Please select either All Data or Only Data-Complete Subjects to be used")
            return
        if (len(self.selected_independent_variables) < 1):
            utils.show_message("Error", "No independent variables selected")
            return
        else:
            self.handle_variables()
            self.results_frame.pack_forget()
            self.dependent_variable_frame.pack_forget()
            self.indedependent_variables_frame.pack_forget()
            self.variable_handling_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)


            utils.bind_mousewheel_to_frame(self.variable_handling_inner_frame, self.variable_handling_canvas, True)
            self.visualize_content_frame.update_idletasks()


    def switch_to_results_frame(self):

        self.create_comparison_table()
        if self.error:
            return

        self.indedependent_variables_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.variable_handling_frame.pack_forget()
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)
        self.visualize_content_frame.update_idletasks()

        utils.bind_mousewheel_to_frame(self.results_inner_frame, self.results_canvas, True)


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
        self.df.replace("[MISSING VALUE]", np.nan, inplace=True)

        self.visualize_content_frame = visualize_content_frame

        self.style = style

        self.style.configure("comparison_table_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"])
        self.style.configure("regression_button.TButton", background=color_dict["active_subtab_bg"], foreground=color_dict["active_subtab_txt"])
        self.style.configure("create_plot_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"])
        self.style.configure("machine_learning_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"])

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


        self.dependent_variable_frame = tk.Frame(self.visualize_content_frame, bg=color_dict["main_content_border"])
        self.indedependent_variables_frame = tk.Frame(self.visualize_content_frame, bg=color_dict["main_content_border"])
        self.variable_handling_frame = tk.Frame(self.visualize_content_frame, bg=color_dict["main_content_border"])
        self.results_frame = tk.Frame(self.visualize_content_frame, bg=color_dict["main_content_border"])


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
        self.dependent_variable_inner_frame, self.dependent_variable_canvas = utils.create_scrollable_frame(self.dependent_variable_frame)

################################################################################################################


        # DEPENDENT VARIABLE SELECTION

        self.dependent_variable_selection_subframe_border = tk.Frame(self.dependent_variable_inner_frame, bg=color_dict["sub_frame_border"])
        self.dependent_variable_selection_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.dependent_variable_selection_subframe = tk.Frame(self.dependent_variable_selection_subframe_border, bg=color_dict["sub_frame_bg"])
        self.dependent_variable_selection_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.dependent_variable_frame_label = ttk.Label(self.dependent_variable_selection_subframe, text="Dependent Variable Selection", style="sub_frame_header.TLabel")
        self.dependent_variable_frame_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.dependent_variable_selection_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)

        # DEPENDENT VARIABLE SELECTION FRAME
        self.dependent_column_choice_frame = tk.Frame(self.dependent_variable_selection_subframe, bg=color_dict["sub_frame_bg"])
        self.dependent_column_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

        self.dependent_search_var = tk.StringVar()
        self.dependent_search_var.trace("w", self.update_dependent_variable_listbox)
        self.dependent_var_search_entry = tk.Entry(self.dependent_column_choice_frame, textvariable=self.dependent_search_var, font=styles.entrybox_small_font)
        self.dependent_var_search_entry.pack(side=tk.TOP, pady=10)

        self.dependent_variable_listbox = tk.Listbox(self.dependent_column_choice_frame, selectmode=tk.SINGLE, font=styles.listbox_font, exportselection=False, bg=color_dict["listbox_bg"],
                     fg=color_dict["listbox_fg"],
                     highlightbackground=color_dict["listbox_highlight_bg"],
                     highlightcolor=color_dict["listbox_highlight_color"],
                     selectbackground=color_dict["listbox_select_bg"],
                     selectforeground=color_dict["listbox_select_fg"],
                     height=20)
        self.dependent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)
        self.dependent_variable_listbox.bind("<Enter>",lambda e: utils.bind_mousewheel_to_frame(self.dependent_variable_inner_frame, self.dependent_variable_canvas, False))
        self.dependent_variable_listbox.bind("<Leave>",lambda e: utils.bind_mousewheel_to_frame(self.dependent_variable_inner_frame, self.dependent_variable_canvas, True))

        for column in sorted(self.df.columns, key=str.lower):
            self.dependent_variable_listbox.insert(tk.END, column)

        self.dependent_variable_listbox.bind("<<ListboxSelect>>", self.on_dependent_variable_listbox_select)




################################################################################################################

        # NAVIGATION MENU
        self.dependent_variable_menu_frame = tk.Frame(self.dependent_variable_frame, bg=color_dict["nav_banner_bg"])
        self.dependent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.advance_to_independent_variables_button = ttk.Button(self.dependent_variable_menu_frame, text="Next", command=self.switch_to_independent_variables_frame, style='nav_menu_button.TButton')
        self.advance_to_independent_variables_button.pack(side=tk.RIGHT)

        self.dependent_frame_dependent_label = ttk.Label(self.dependent_variable_menu_frame, text="", style="nav_menu_label.TLabel")
        self.dependent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)



        if self.selected_dependent_variable:
            self.dependent_variable_listbox.selection_clear(0, tk.END)
            items = list(self.dependent_variable_listbox.get(0, tk.END))
            index = items.index(self.selected_dependent_variable)
            self.dependent_variable_listbox.selection_set(index)
            self.dependent_variable_listbox.yview(index)
            self.dependent_frame_dependent_label.config(text=f"Dependent Variable: {self.selected_dependent_variable}")



################################################################################################################

    def on_dependent_variable_listbox_select(self, event):
        if self.dependent_variable_listbox.curselection():
            self.selected_dependent_variable = self.dependent_variable_listbox.get(self.dependent_variable_listbox.curselection()[0])
            data_manager.set_reg_tab_dep_var(self.selected_dependent_variable)
            self.dependent_frame_dependent_label.config(text=f"Dependent Variable: {self.selected_dependent_variable}")


    def update_dependent_variable_listbox(self, *args):
        search_term = self.dependent_search_var.get().lower()
        self.dependent_variable_listbox.delete(0, tk.END)

        # Check if the search term is empty
        if search_term == "":
            # If search term is empty, insert all columns sorted alphabetically
            for column in sorted(self.df.columns, key=str.lower):
                self.dependent_variable_listbox.insert(tk.END, column)
            if self.selected_dependent_variable:
                self.dependent_variable_listbox.selection_clear(0, tk.END)
                items = list(self.dependent_variable_listbox.get(0, tk.END))
                index = items.index(self.selected_dependent_variable)
                self.dependent_variable_listbox.selection_set(index)
        else:
            # If there is a search term, filter and sort the columns based on the search term
            filtered_sorted_columns = sorted([column for column in self.df.columns if search_term in column.lower()], key=str.lower)
            # Populate the Listbox with the sorted list
            for column in filtered_sorted_columns:
                self.dependent_variable_listbox.insert(tk.END, column)
            if self.selected_dependent_variable in filtered_sorted_columns:
                self.dependent_variable_listbox.selection_clear(0, tk.END)
                items = list(self.dependent_variable_listbox.get(0, tk.END))
                index = items.index(self.selected_dependent_variable)
                self.dependent_variable_listbox.selection_set(index)


################################################################################################################
################################################################################################################
################################################################################################################


    # CREATE INDEPENDENT VARIABLE SELECTION FRAME

    def create_independent_variables_frame(self):

        # MAIN CONTENT FRAME
        self.independent_variables_inner_frame, self.independent_variables_canvas = utils.create_scrollable_frame(self.indedependent_variables_frame)

################################################################################################################

        # INDEPENDENT VARIABLES SELECTION
        self.independent_variables_selection_subframe_border = tk.Frame(self.independent_variables_inner_frame, bg=color_dict["sub_frame_border"])
        self.independent_variables_selection_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.independent_variables_selection_subframe = tk.Frame(self.independent_variables_selection_subframe_border, bg=color_dict["sub_frame_bg"])
        self.independent_variables_selection_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.choose_independent_variables_label = ttk.Label(self.independent_variables_selection_subframe, text="Independent Variable Selection", style="sub_frame_header.TLabel")
        self.choose_independent_variables_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.independent_variables_selection_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)


        # AVAILABLE INDEPENDENT VARIABLES SELECTION FRAME
        self.indedependent_variables_selection_frame = tk.Frame(self.independent_variables_selection_subframe, bg=color_dict["sub_frame_bg"])
        self.indedependent_variables_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

        self.available_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg=color_dict["sub_frame_bg"])
        self.available_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.available_independent_search_var = tk.StringVar()
        self.available_independent_search_var.trace("w", self.update_available_independent_variable_listbox)
        self.independent_var_search_entry = tk.Entry(self.available_independent_variables_frame, textvariable=self.available_independent_search_var, font=styles.entrybox_small_font)
        self.independent_var_search_entry.pack(side=tk.TOP, pady=10)

        self.available_independent_variable_listbox = tk.Listbox(self.available_independent_variables_frame, selectmode=tk.MULTIPLE, font=styles.listbox_font,
                                                                bg=color_dict["listbox_bg"],
                                                                fg=color_dict["listbox_fg"],
                                                                highlightbackground=color_dict["listbox_highlight_bg"],
                                                                highlightcolor=color_dict["listbox_highlight_color"],
                                                                selectbackground=color_dict["listbox_select_bg"],
                                                                selectforeground=color_dict["listbox_select_fg"]
                                                                )
        self.available_independent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)
        self.available_independent_variable_listbox.bind("<Enter>",lambda e: utils.bind_mousewheel_to_frame(self.independent_variables_inner_frame, self.independent_variables_canvas, False))
        self.available_independent_variable_listbox.bind("<Leave>",lambda e: utils.bind_mousewheel_to_frame(self.independent_variables_inner_frame, self.independent_variables_canvas, True))



        for column in sorted(self.df.columns, key=str.lower):
            if column not in self.selected_independent_variables:
                self.available_independent_variable_listbox.insert(tk.END, column)


        # TRANSFER BUTTONS
        self.buttons_frame = tk.Frame(self.indedependent_variables_selection_frame, bg=color_dict["sub_frame_bg"])
        self.buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Larger buttons with ">>>" and "<<<" symbols
        self.transfer_right_button = ttk.Button(self.buttons_frame, text="Transfer Right >>>", command=self.transfer_right, style="large_button.TButton")
        self.transfer_right_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.transfer_left_button = ttk.Button(self.buttons_frame, text="<<< Transfer Left", command=self.transfer_left, style="large_button.TButton")
        self.transfer_left_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)

        separator = ttk.Separator(self.buttons_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, pady=10)

        # Text buttons "Select All" and "Clear Selection"
        self.transfer_all_right_button = ttk.Button(self.buttons_frame, text="Select All", command=self.transfer_all_right, style="large_button.TButton")
        self.transfer_all_right_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)

        self.transfer_all_left_button = ttk.Button(self.buttons_frame, text="Clear Selection", command=self.transfer_all_left, style="large_button.TButton")
        self.transfer_all_left_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)


        separator = ttk.Separator(self.buttons_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

        # Import and export selected variables
        self.import_variable_list_button = ttk.Button(self.buttons_frame, text="Import Variable List", command=self.import_variable_list, style="large_button.TButton")
        self.import_variable_list_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)

        self.export_variable_list_button = ttk.Button(self.buttons_frame, text="Export Variable List", command=self.export_variable_list, style="large_button.TButton")
        self.export_variable_list_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)


        # SELECTED INDEPENDENT VARIABLES FRAME
        self.selected_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg=color_dict["sub_frame_bg"])
        self.selected_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.selected_independent_variables_label = ttk.Label(self.selected_independent_variables_frame, text="Selected Variables", style="sub_frame_sub_header.TLabel")
        self.selected_independent_variables_label.pack(side=tk.TOP, pady=10)



        self.selected_independent_variable_listbox = tk.Listbox(self.selected_independent_variables_frame, selectmode=tk.MULTIPLE, font=styles.listbox_font,
                                                                bg=color_dict["listbox_bg"],
                                                                fg=color_dict["listbox_fg"],
                                                                highlightbackground=color_dict["listbox_highlight_bg"],
                                                                highlightcolor=color_dict["listbox_highlight_color"],
                                                                selectbackground=color_dict["listbox_select_bg"],
                                                                selectforeground=color_dict["listbox_select_fg"]
                                                                )
        self.selected_independent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)
        self.selected_independent_variable_listbox.bind("<Enter>",lambda e: utils.bind_mousewheel_to_frame(self.independent_variables_inner_frame, self.independent_variables_canvas, False))
        self.selected_independent_variable_listbox.bind("<Leave>",lambda e: utils.bind_mousewheel_to_frame(self.independent_variables_inner_frame, self.independent_variables_canvas, True))

        if len(self.selected_independent_variables) > 0:
            for var in self.selected_independent_variables:
                self.selected_independent_variable_listbox.insert(tk.END, var)
                self.available_independent_variable_listbox.selection_set(sorted(self.df.columns, key=str.lower).index(var))
            selections = self.available_independent_variable_listbox.curselection()
            for index in reversed(selections):
                self.available_independent_variable_listbox.delete(index)



################################################################################################################

        # MODEL OPTIONS

        self.model_options_subframe_border = tk.Frame(self.independent_variables_inner_frame, bg=color_dict["sub_frame_border"])
        self.model_options_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.model_options_subframe = tk.Frame(self.model_options_subframe_border, bg=color_dict["sub_frame_bg"])
        self.model_options_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.choose_independent_variables_label = ttk.Label(self.model_options_subframe, text="Regression Model Selection", style="sub_frame_header.TLabel")
        self.choose_independent_variables_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.model_options_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)

 
        # MODEL OPTIONS
        self.regression_type_selection_frame = tk.Frame(self.model_options_subframe, bg=color_dict["sub_frame_bg"])
        self.regression_type_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)


        # Initialize your buttons with the inactive style
        self.logistic_regression_button = ttk.Button(self.regression_type_selection_frame, text="Logistic Regression", style="inactive_radio_button.TButton", command=lambda: self.toggle_regression_model_button_style("Logistic Regression"))
        self.logistic_regression_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.linear_regression_button = ttk.Button(self.regression_type_selection_frame, text="Linear Regression", style="inactive_radio_button.TButton", command=lambda: self.toggle_regression_model_button_style("Linear Regression"))
        self.linear_regression_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Load Previously Chosen Percent Selection
        if self.selected_regression:
            if self.selected_regression == "Logistic Regression":
                self.toggle_regression_model_button_style("Logistic Regression")
            elif self.selected_regression == "Linear Regression":
                self.toggle_regression_model_button_style("Linear Regression")
        else:
            self.toggle_regression_model_button_style("Logistic Regression")






################################################################################################################



        # NAVIGATION MENU
        self.independent_variable_menu_frame = tk.Frame(self.indedependent_variables_frame, bg=color_dict["nav_banner_bg"])
        self.independent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_dependent_variable_frame_button = ttk.Button(self.independent_variable_menu_frame, command=self.switch_to_dependent_variable_frame, text='Back', style='nav_menu_button.TButton')
        self.return_to_dependent_variable_frame_button.pack(side=tk.LEFT)

        self.advance_to_variable_handling_frame_button = ttk.Button(self.independent_variable_menu_frame, command=self.switch_to_variable_handling_frame, text="Next", style='nav_menu_button.TButton')
        self.advance_to_variable_handling_frame_button.pack(side=tk.RIGHT)

        self.independent_frame_dependent_label = ttk.Label(self.independent_variable_menu_frame, text="", style="nav_menu_label.TLabel")
        self.independent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)


################################################################################################################

    # INDEPENDENT VARIABLES FUNCTIONS


    def update_available_independent_variable_listbox(self, *args):
        search_term = self.available_independent_search_var.get().lower()
        self.available_independent_variable_listbox.delete(0, tk.END)
        for column in sorted(self.df.columns, key=str.lower):
            if search_term in column.lower():
                if column not in self.selected_independent_variables:
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

        self.independent_var_search_entry.focus_set()


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
            if item not in self.selected_independent_variables:
                self.available_independent_variable_listbox.insert(tk.END, item)

        if top_visible_index >= 0:
            index = items.index(top_visible_item)
            self.available_independent_variable_listbox.yview(index)



    # Function to toggle button styles
    def toggle_regression_model_button_style(self, selected):
        if selected == "Logistic Regression":
            self.logistic_regression_button.configure(style="active_radio_button.TButton")
            self.linear_regression_button.configure(style="inactive_radio_button.TButton")
            self.selected_regression = "Logistic Regression"
            data_manager.set_reg_tab_selected_regression(self.selected_regression)
        elif selected == "Linear Regression":
            self.logistic_regression_button.configure(style="inactive_radio_button.TButton")
            self.linear_regression_button.configure(style="active_radio_button.TButton")
            self.selected_regression = "Linear Regression"
            data_manager.set_reg_tab_selected_regression(self.selected_regression)

    def import_variable_list(self):
        imported_variable_list = data_manager.get_exported_variables_list()

        for var in imported_variable_list:
            if var in self.df.columns:
                self.selected_independent_variable_listbox.insert(tk.END, var)
                self.selected_independent_variables.append(var)

    def export_variable_list(self):
        data_manager.clear_exported_variables_list()
        for var in self.selected_independent_variables:
            data_manager.add_variable_to_exported_variables_list(var)

################################################################################################################
################################################################################################################
################################################################################################################


    # CREATE VARIABLE HANDLING FRAME

    def create_variable_handling_frame(self):

        # MAIN CONTENT FRAME
        self.variable_handling_inner_frame, self.variable_handling_canvas = utils.create_scrollable_frame(self.variable_handling_frame)

################################################################################################################

        # NAVIGATION MENU
        self.variable_handling_menu_frame = tk.Frame(self.variable_handling_frame, bg=color_dict["nav_banner_bg"])
        self.variable_handling_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_independent_variable_frame_button = ttk.Button(self.variable_handling_menu_frame, command=self.switch_to_independent_variables_frame, text='Back', style='nav_menu_button.TButton')
        self.return_to_independent_variable_frame_button.pack(side=tk.LEFT)

        self.view_results_button = ttk.Button(self.variable_handling_menu_frame, command=self.switch_to_results_frame, text='View Results', style='nav_menu_button.TButton')
        self.view_results_button.pack(side=tk.RIGHT)

        self.variable_handling_menu_frame_dependent_label = ttk.Label(self.variable_handling_menu_frame, text="", style="nav_menu_label.TLabel")
        self.variable_handling_menu_frame_dependent_label.pack(side=tk.RIGHT, expand=True)


################################################################################################################

    # HANDLE VARIABLES FOR LINEAR REGRESSION

    def handle_variables_linear_regression(self):

        utils.remove_frame_widgets(self.variable_handling_inner_frame)

        # VARIABLE HANDLING
        self.linear_regression_variable_handling_subframe_border = tk.Frame(self.variable_handling_inner_frame, bg=color_dict["sub_frame_border"])
        self.linear_regression_variable_handling_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.linear_regression_variable_handling_subframe = tk.Frame(self.linear_regression_variable_handling_subframe_border, bg=color_dict["sub_frame_bg"])
        self.linear_regression_variable_handling_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.value_entry_frame_label = ttk.Label(self.linear_regression_variable_handling_subframe, text="Change Non-Numeric Values in The Following Independent Variables", style="sub_frame_header.TLabel")
        self.value_entry_frame_label.pack(side=tk.TOP, pady=10)
        
        separator = ttk.Separator(self.linear_regression_variable_handling_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)

        self.value_entry_frame = tk.Frame(self.linear_regression_variable_handling_subframe, bg=color_dict["sub_frame_bg"])
        self.value_entry_frame.pack(side=tk.TOP, pady=10)

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
            proceed_to_results_label = ttk.Label(self.value_entry_frame, text="No Non-Numeric Variables. Click VIEW RESULTS", style="sub_frame_sub_header.TLabel")
            proceed_to_results_label.pack(side=tk.TOP, fill=tk.X, pady=10, padx=20)

        # HANDLE NON-NUMERIC VARIABLES
        for variable in self.non_numeric_columns:

            options_frame = tk.Frame(self.value_entry_frame, bg=color_dict["sub_frame_bg"])
            options_frame.pack(side=tk.TOP, pady=10, padx=20)


            if len(variable) > 20:
                variable_string = variable[0:19] + "..."
            else:
                variable_string = variable

            variable_label = ttk.Label(options_frame, text=variable_string, style="sub_frame_sub_header.TLabel")
            variable_label.pack(side=tk.TOP)


            non_numeric_values = []

            for value in self.clean_df[variable].unique():
                if isinstance(value, str) and not value.isdigit():
                    non_numeric_values.append(value)

            for value in non_numeric_values:

                value_frame = tk.Frame(options_frame, bg=color_dict["sub_frame_bg"])
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



                input_entry = tk.Entry(value_frame, textvariable=user_input_var, font=styles.entrybox_large_font, width=10)
                input_entry.pack(side=tk.LEFT)

                value_label = ttk.Label(value_frame, text=value, style="sub_frame_text.TLabel")
                value_label.pack(side=tk.LEFT)

                # Bind the entry widget to an event
                input_entry.bind("<KeyRelease>", lambda event, var=variable, val=value: self.on_key_release(event, var, val))

            separator = ttk.Separator(self.value_entry_frame, orient="horizontal", style="Separator.TSeparator")
            separator.pack(fill=tk.X, padx=5, pady=5)


    def on_key_release(self, event, variable, value):
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
                        raise

                self.clean_df[variable] = self.clean_df[variable].astype(float)


    ################################################################################################################

    # HANDLE VARIABLES FOR LOGISTIC REGRESSION

    def handle_variables_logistic_regression(self):

        self.clean_df = self.df[self.selected_independent_variables + [self.selected_dependent_variable]].copy()
        self.clean_df.dropna(inplace=True)

        if len(self.clean_df) < 1:
            first_column_with_missing_data = self.df.columns[self.df.isnull().all()].tolist()[0]
            utils.show_message("error message", f"The Variable, {first_column_with_missing_data.upper()}, has no data")
            raise utils.MyCustomError("error")

        utils.remove_frame_widgets(self.variable_handling_inner_frame)

        # TARGET VALUE SUBFRAME
        self.target_value_subframe_border = tk.Frame(self.variable_handling_inner_frame, bg=color_dict["sub_frame_border"])
        self.target_value_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.target_value_subframe = tk.Frame(self.target_value_subframe_border, bg=color_dict["sub_frame_bg"])
        self.target_value_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.target_value_label = ttk.Label(self.target_value_subframe, text="Target Value Selection", style="sub_frame_header.TLabel")
        self.target_value_label.pack(side=tk.TOP, pady=10)
        
        separator = ttk.Separator(self.target_value_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)


        

        self.target_value_1 = f"{self.clean_df[self.selected_dependent_variable].unique()[0]}"
        self.target_value_2 = f"{self.clean_df[self.selected_dependent_variable].unique()[1]}"

        # Initialize your buttons with the inactive style
        self.target_value_1_button = ttk.Button(self.target_value_subframe, text=self.target_value_1, style="inactive_radio_button.TButton", command=lambda: self.toggle_target_value_button_style(self.target_value_1))
        self.target_value_1_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.target_value_2_button = ttk.Button(self.target_value_subframe, text=self.target_value_2, style="inactive_radio_button.TButton", command=lambda: self.toggle_target_value_button_style(self.target_value_2))
        self.target_value_2_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Load Previously Chosen Percent Selection
        if self.selected_dependent_variable in self.log_reg_target_value_var_dict:
            
            if self.log_reg_target_value_var_dict[self.selected_dependent_variable] == self.target_value_1:
                self.toggle_target_value_button_style(self.target_value_1)
            elif self.log_reg_target_value_var_dict[self.selected_dependent_variable] == self.target_value_2:
                self.toggle_target_value_button_style(self.target_value_2)
        else:
            self.toggle_target_value_button_style(self.target_value_1)








        # VARIABLE TYPES AND REFERENCE VALUES FRAME
        self.variable_type_subframe_border = tk.Frame(self.variable_handling_inner_frame, bg=color_dict["sub_frame_border"])
        self.variable_type_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.variable_type_subframe = tk.Frame(self.variable_type_subframe_border, bg=color_dict["sub_frame_bg"])
        self.variable_type_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.target_value_label = ttk.Label(self.variable_type_subframe, text="Variable Type and Reference Value Selection", style="sub_frame_header.TLabel")
        self.target_value_label.pack(side=tk.TOP, pady=10)
        
        separator = ttk.Separator(self.variable_type_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)




        self.variable_type_selection_frame = tk.Frame(self.variable_type_subframe, bg=color_dict["sub_frame_bg"])
        self.variable_type_selection_frame.pack(side=tk.TOP)

        self.variable_name_label = ttk.Label(self.variable_type_selection_frame, text='Variable', style="sub_frame_sub_header.TLabel")
        self.variable_name_label.grid(row=0, column=0, padx=5, pady=5)

        self.variable_type_label = ttk.Label(self.variable_type_selection_frame, text='Variable Type', style="sub_frame_sub_header.TLabel")
        self.variable_type_label.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        self.reference_variable_label = ttk.Label(self.variable_type_selection_frame, text='Reference Value', style="sub_frame_sub_header.TLabel")
        self.reference_variable_label.grid(row=0, column=3, padx=5, pady=5)

        separator = ttk.Separator(self.variable_type_selection_frame, orient="horizontal", style="Separator.TSeparator")
        separator.grid(row=2, column=0, columnspan=4, sticky="ew", padx=5, pady=5)




        self.unique_values = list(self.clean_df[self.selected_independent_variables].columns)
        self.selected_options = {}


        row_count = 3

        for variable in self.selected_independent_variables:


            variable_string = variable[0:19] + "..." if len(variable) >= 20 else variable

            variable_label = ttk.Label(self.variable_type_selection_frame, text=variable_string, style="sub_frame_sub_header.TLabel")
            variable_label.grid(row=row_count+1, column=0, padx=10, pady=5)



            # Initialize your buttons with the inactive style

            continuous_variable_button = ttk.Button(self.variable_type_selection_frame, text="Continuous", style="inactive_radio_button.TButton")
            continuous_variable_button.grid(row=row_count+1, column=1, padx=10, pady=5)
            
            categorical_variable_button = ttk.Button(self.variable_type_selection_frame, text="Categorical", style="inactive_radio_button.TButton")
            categorical_variable_button.grid(row=row_count+1, column=2, padx=10, pady=5)















            reference_value_combobox = ttk.Combobox(self.variable_type_selection_frame, state=tk.DISABLED, font=styles.large_button_font)
            values = [str(val) for val in self.clean_df[variable].unique()]
            reference_value_combobox['values'] = values
            reference_value_combobox.grid(row=row_count+1, column=3, padx=10, pady=5)
            reference_value_combobox.bind("<<ComboboxSelected>>", lambda event, combobox=reference_value_combobox, variable=variable: self.on_combobox_select(combobox, variable))


            # Bind the state of the reference_value_combobox to the selection of 'Categorical' radio button
            continuous_variable_button.bind("<Button-1>", lambda event, combobox=reference_value_combobox: combobox.configure(state=tk.DISABLED))

            if variable in self.log_reg_reference_variable_dict:
                categorical_variable_button.bind("<Button-1>", lambda event, combobox=reference_value_combobox: combobox.configure(state="readonly"))
                reference_value_combobox.set(self.log_reg_reference_variable_dict[variable])
            else:
                categorical_variable_button.bind("<Button-1>", lambda event, combobox=reference_value_combobox: combobox.configure(state="readonly"))

            if variable in self.log_reg_variable_type_dict:
                if self.log_reg_variable_type_dict[variable] == "Categorical":
                    reference_value_combobox.configure(state="readonly")
                    if variable in self.log_reg_reference_variable_dict:
                        reference_value_combobox.set(self.log_reg_reference_variable_dict[variable])



            separator_2 = ttk.Separator(self.variable_type_selection_frame, orient="horizontal", style="Separator.TSeparator")
            separator_2.grid(row=row_count+2, column=0, columnspan=4, sticky="ew", pady=5)

            continuous_variable_button.configure(command=lambda var=variable, conb=continuous_variable_button, catb=categorical_variable_button, comb=reference_value_combobox: self.toggle_variable_type_button_style(var, "Continuous", conb, catb, comb))
            categorical_variable_button.configure(command=lambda var=variable, conb=continuous_variable_button, catb=categorical_variable_button, comb=reference_value_combobox: self.toggle_variable_type_button_style(var, "Categorical", conb, catb, comb))


            # Load Previously Chosen Variable Type Selection
            if variable in self.log_reg_variable_type_dict:
                self.toggle_variable_type_button_style(variable, self.log_reg_variable_type_dict[variable], continuous_variable_button, categorical_variable_button, reference_value_combobox)
            else:
                self.toggle_variable_type_button_style(variable, "Continuous", continuous_variable_button, categorical_variable_button, reference_value_combobox)


            row_count += 3



    # Function to toggle button styles
    def toggle_target_value_button_style(self, selected):
        if selected in [self.target_value_1, self.target_value_2]:
            if selected == self.target_value_1:
                self.target_value_1_button.configure(style="active_radio_button.TButton")
                self.target_value_2_button.configure(style="inactive_radio_button.TButton")
                self.selected_target_value = self.target_value_1
                data_manager.add_variable_to_reg_tab_log_reg_target_value_dict(self.selected_dependent_variable, selected)
            elif selected == self.target_value_2:
                self.target_value_1_button.configure(style="inactive_radio_button.TButton")
                self.target_value_2_button.configure(style="active_radio_button.TButton")
                self.selected_target_value = self.target_value_2
                data_manager.add_variable_to_reg_tab_log_reg_target_value_dict(self.selected_dependent_variable, selected)


    # Function to toggle button styles
    def toggle_variable_type_button_style(self, variable, selection, continuous_button, categorical_button, combobox):
        styles = {"Continuous": ("active_radio_button.TButton", "inactive_radio_button.TButton", "disabled"),
                  "Categorical": ("inactive_radio_button.TButton", "active_radio_button.TButton", "readonly")
                  }

        cont_style, cat_style, combobox_style = styles[selection]
        continuous_button.configure(style=cont_style)
        categorical_button.configure(style=cat_style)
        combobox.configure(state=combobox_style)
        self.log_reg_variable_type_dict[variable] = selection



    def on_combobox_select(self, combobox, variable):
        selected_value = combobox.get()
        data_manager.add_variable_to_log_reg_ref_dict(variable, selected_value)


    def apply_logistic_regression_variable_selection(self):


        self.clean_df[self.selected_dependent_variable] = self.clean_df[self.selected_dependent_variable].astype(str)

        # MAKE VALUES OF DEPENDENT VARIABLE BINARY
        self.corrected_dependent_variable = "new_outcome_variable"

        self.clean_df.loc[self.clean_df[self.selected_dependent_variable]==self.selected_target_value, self.corrected_dependent_variable] = 1
        self.clean_df.loc[self.clean_df[self.selected_dependent_variable]!=self.selected_target_value, self.corrected_dependent_variable] = 0



        self.selected_options.clear()

        for variable in self.selected_independent_variables:

            # Get variable type of the current independent variable
            variable_type = self.log_reg_variable_type_dict[variable]

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
        self.results_inner_frame, self.results_frame_canvas = utils.create_scrollable_frame(self.results_frame)

################################################################################################################

        # RESULTS TABLE DISPLAY FRAME
        self.results_table_subframe_border = tk.Frame(self.results_inner_frame, bg=color_dict["sub_frame_border"])
        self.results_table_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.results_table_subframe = tk.Frame(self.results_table_subframe_border, bg=color_dict["sub_frame_bg"])
        self.results_table_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.results_table_label = ttk.Label(self.results_table_subframe, text="", style="sub_frame_header.TLabel")
        self.results_table_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.results_table_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)


        self.results_display_frame = tk.Frame(self.results_table_subframe, bg=color_dict["sub_frame_bg"])
        self.results_display_frame.pack(side=tk.TOP, fill=tk.Y, expand=True, pady=10)


################################################################################################################

        # NAVIGATION MENU
        self.results_menu_frame = tk.Frame(self.results_frame, bg=color_dict["nav_banner_bg"])
        self.results_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_variable_handling_frame_button = ttk.Button(self.results_menu_frame, command=self.switch_to_variable_handling_frame, text='Back', style='nav_menu_button.TButton')
        self.return_to_variable_handling_frame_button.pack(side=tk.LEFT)

        self.results_frame_dependent_label = ttk.Label(self.results_menu_frame, text="", style="nav_menu_label.TLabel")
        self.results_frame_dependent_label.pack(side=tk.RIGHT, expand=True)

################################################################################################################

    def run_analysis(self):
        utils.remove_frame_widgets(self.results_display_frame)

        if self.selected_regression == "Logistic Regression":
            self.logistic_regression()

        elif self.selected_regression == "Linear Regression":
            self.linear_regression()


    def logistic_regression(self):
        


        model_string = f"{self.corrected_dependent_variable} ~ "
        self.clean_df[self.corrected_dependent_variable] = self.clean_df[self.corrected_dependent_variable].astype(int)


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
        coefs['CI_low'] = coefs['CI_low'].astype(str)

        coefs = coefs.reset_index().rename(columns={'index': 'Characteristic'})
        for i in range(len(coefs['Characteristic'])):
            variable_string = coefs['Characteristic'].iloc[i]

            if variable_string[0:1] == "C(":
                column_string = re.search(r'C\((.*?),', variable_string).group(1)
                reference_value = re.search(r"\[T\.(.*?)\]", variable_string).group(1)
                new_value = column_string + f" ({reference_value})"
                coefs.loc[i, 'Characteristic'] = new_value
            if float(coefs.loc[i, 'CI_high']) > 50000:
                coefs.loc[i, 'CI_high'] = 'inf'
            if float(coefs.loc[i, 'CI_low']) < -50000:
                coefs.loc[i, 'CI_low'] = '-inf'


        summary_text = tk.Text(self.results_display_frame, height=20, width=120)
        summary_text.pack(side=tk.TOP)
        summary_text.insert(tk.END, str(results.summary()))

        utils.create_table(self.results_display_frame, coefs, self.style)

        save_summary_button = ttk.Button(self.results_display_frame, text="Save Table", command=lambda: file_handling.save_file(coefs), style="large_button.TButton")
        save_summary_button.pack(side=tk.TOP)







    def linear_regression(self):

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



        summary_text = tk.Text(self.results_display_frame, height=20, width=120)
        summary_text.pack(side=tk.TOP)
        summary_text.insert(tk.END, str(model.summary()))


        utils.create_table(self.results_display_frame, coefs, self.style)


        save_summary_button = ttk.Button(self.results_display_frame, text="Save Table", command=lambda: file_handling.save_file(coefs), style="large_button.TButton")
        save_summary_button.pack()

        view_correlation_matrix_button = ttk.Button(self.results_display_frame, text="View Correlation Matrix", command=lambda: plot_correlation_matrix(), style="large_button.TButton")
        view_correlation_matrix_button.pack()

        def plot_correlation_matrix():
            # Exclude the constant column before generating the correlation matrix
            x_no_constant = x.drop('const', axis=1)  # Assuming 'const' is the name of the constant column

            correlation_matrix = x_no_constant.corr()
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
        self.dependent_variable_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        self.dependent_var_search_entry.focus_set()

        utils.bind_mousewheel_to_frame(self.dependent_variable_inner_frame, self.dependent_variable_canvas, True)
        self.visualize_content_frame.update_idletasks()

    def switch_to_independent_variables_frame(self):
        if self.selected_dependent_variable == None:
            return

        self.variable_handling_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.indedependent_variables_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        

        self.dependent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.independent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.results_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.variable_handling_menu_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")


        utils.bind_mousewheel_to_frame(self.independent_variables_inner_frame, self.independent_variables_canvas, True)
        self.visualize_content_frame.update_idletasks()
        self.independent_var_search_entry.focus_set()


    def switch_to_variable_handling_frame(self):

        if self.selected_regression not in ["Logistic Regression", "Linear Regression"]:
            utils.show_message('Error', 'Please select either Logistic Regression or Linear Regression')
            return

        if len(self.selected_independent_variables) < 1:
            utils.show_message('Error', 'No Independent Variables Selected')
            return



        if self.selected_regression == "Logistic Regression":
            # CHECK FOR BINARY OUTCOME BEFORE LOGISTIC REGRESSION
            if len(self.df[self.selected_dependent_variable].dropna().unique()) != 2:
                utils.show_message('dependent variable error', 'Dependent Variable not binary for logistic regression')
                return

            self.handle_variables_logistic_regression()


        if self.selected_regression == "Linear Regression":
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
        self.variable_handling_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        utils.bind_mousewheel_to_frame(self.variable_handling_frame, self.variable_handling_canvas, True)
        self.visualize_content_frame.update_idletasks()

    def switch_to_results_frame(self):

        if self.selected_regression == "Linear Regression":
            try:
                self.apply_linear_regression_variable_selection()
                self.results_table_label.config(text="Linear Regression Results")
            except:
                utils.show_message("error message", f"Make sure all values are NUMERICAL")
                raise
        if self.selected_regression == "Logistic Regression":
            try:
                self.apply_logistic_regression_variable_selection()
                self.results_table_label.config(text="Logistic Regression Results")
            except:
                raise

        self.run_analysis()

        self.indedependent_variables_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.variable_handling_frame.pack_forget()
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)


        utils.bind_mousewheel_to_frame(self.results_frame, self.results_frame_canvas, True)
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
        self.df.replace("[MISSING VALUE]", np.nan, inplace=True)

        self.style = style

        self.style.configure("comparison_table_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"])
        self.style.configure("regression_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"])
        self.style.configure("create_plot_button.TButton", background=color_dict["active_subtab_bg"], foreground=color_dict["active_subtab_txt"])
        self.style.configure("machine_learning_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"])

        data_manager.add_tab_to_tab_dict("current_visualize_tab", "create_plot")

        self.selected_plot = data_manager.get_plot_tab_plot_selection()

        self.visualize_content_frame = visualize_content_frame
        utils.remove_frame_widgets(self.visualize_content_frame)



        self.plot_selection_frame = tk.Frame(self.visualize_content_frame, bg=color_dict["main_content_border"])
        self.plot_settings_frame = tk.Frame(self.visualize_content_frame, bg=color_dict["main_content_border"])
        self.plot_display_frame = tk.Frame(self.visualize_content_frame, bg=color_dict["main_content_border"])



        self.plot_options = ["Scatter Plot"]


        self.create_plot_selection_frame()
        self.create_plot_settings_frame()
        self.create_plot_display_frame()

        self.switch_to_plot_selection_frame()

################################################################################################################
################################################################################################################
################################################################################################################

    # CREATE PLOT OPTIONS FRAME

    def create_plot_selection_frame(self):

        # MAIN CONTENT FRAME
        self.plot_selection_inner_frame, self.plot_selection_canvas = utils.create_scrollable_frame(self.plot_selection_frame)


################################################################################################################

        # PLOT SELECTION

        self.plot_selection_subframe_border = tk.Frame(self.plot_selection_inner_frame, bg=color_dict["sub_frame_border"])
        self.plot_selection_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.plot_selection_subframe = tk.Frame(self.plot_selection_subframe_border, bg=color_dict["sub_frame_bg"])
        self.plot_selection_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.plot_selection_frame_label = ttk.Label(self.plot_selection_subframe, text="Plot Selection", style="sub_frame_header.TLabel")
        self.plot_selection_frame_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.plot_selection_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)

        # PLOT SELECTION FRAME
        self.plot_choice_frame = tk.Frame(self.plot_selection_subframe, bg=color_dict["sub_frame_bg"])
        self.plot_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

        self.plot_search_var = tk.StringVar()
        self.plot_search_var.trace("w", self.update_plot_selection_listbox)
        self.plot_var_search_entry = tk.Entry(self.plot_choice_frame, textvariable=self.plot_search_var, font=styles.entrybox_small_font)
        self.plot_var_search_entry.pack(side=tk.TOP, pady=10)

        self.plot_selection_listbox = tk.Listbox(self.plot_choice_frame, selectmode=tk.SINGLE, font=styles.listbox_font, exportselection=False, bg=color_dict["listbox_bg"],
                     fg=color_dict["listbox_fg"],
                     highlightbackground=color_dict["listbox_highlight_bg"],
                     highlightcolor=color_dict["listbox_highlight_color"],
                     selectbackground=color_dict["listbox_select_bg"],
                     selectforeground=color_dict["listbox_select_fg"],
                     height=20)
        self.plot_selection_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)
        self.plot_selection_listbox.bind("<Enter>",lambda e: utils.bind_mousewheel_to_frame(self.plot_selection_inner_frame, self.plot_selection_canvas, False))
        self.plot_selection_listbox.bind("<Leave>",lambda e: utils.bind_mousewheel_to_frame(self.plot_selection_inner_frame, self.plot_selection_canvas, True))

        for plot in sorted(self.plot_options):
            self.plot_selection_listbox.insert(tk.END, plot)

        self.plot_selection_listbox.bind("<<ListboxSelect>>", self.on_plot_selection_listbox_select)


################################################################################################################

        # NAVIGATION MENU
        self.plot_selection_menu_frame = tk.Frame(self.plot_selection_frame, bg=color_dict["nav_banner_bg"])
        self.plot_selection_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.advance_to_plot_selections_button = ttk.Button(self.plot_selection_menu_frame, text="Next", command=self.switch_to_plot_settings_frame, style='nav_menu_button.TButton')
        self.advance_to_plot_selections_button.pack(side=tk.RIGHT)



        if self.selected_plot:
            self.plot_selection_listbox.selection_clear(0, tk.END)
            items = list(self.plot_selection_listbox.get(0, tk.END))
            index = items.index(self.selected_plot)
            self.plot_selection_listbox.selection_set(index)
            self.plot_selection_listbox.yview(index)
            


################################################################################################################

    # PLOT SELECTION FUNCTIONS

    def on_plot_selection_listbox_select(self, event):
        if self.plot_selection_listbox.curselection():
            self.selected_plot = self.plot_selection_listbox.get(self.plot_selection_listbox.curselection()[0])
            data_manager.set_plot_tab_plot_selection(self.selected_plot)



    def update_plot_selection_listbox(self, *args):
        search_term = self.plot_search_var.get().lower()
        self.plot_selection_listbox.delete(0, tk.END)

        # Check if the search term is empty
        if search_term == "":
            # If search term is empty, insert all plots sorted alphabetically
            for plot in sorted(self.plot_options, key=str.lower):
                self.plot_selection_listbox.insert(tk.END, plot)
        else:
            # If there is a search term, filter and sort the columns based on the search term
            filtered_sorted_columns = sorted([plot for plot in self.plot_options if search_term in plot.lower()], key=str.lower)
            # Populate the Listbox with the sorted list
            for plot in filtered_sorted_columns:
                self.plot_selection_listbox.insert(tk.END, plot)






################################################################################################################
################################################################################################################
################################################################################################################

    def create_plot_settings_frame(self):

        # MAIN CONTENT FRAME
        self.plot_settings_inner_frame, self.plot_settings_canvas = utils.create_scrollable_frame(self.plot_settings_frame)

################################################################################################################

        # PLOT SELECTION

        self.plot_settings_subframe_border = tk.Frame(self.plot_settings_inner_frame, bg=color_dict["sub_frame_border"])
        self.plot_settings_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.plot_settings_subframe = tk.Frame(self.plot_settings_subframe_border, bg=color_dict["sub_frame_bg"])
        self.plot_settings_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)


################################################################################################################

        # NAVIGATION MENU


        self.plot_settings_menu_frame = tk.Frame(self.plot_settings_frame, bg=color_dict["nav_banner_bg"])
        self.plot_settings_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_plot_selection_button = ttk.Button(self.plot_settings_menu_frame, text="Back", command=self.switch_to_plot_selection_frame, style='nav_menu_button.TButton')
        self.return_to_plot_selection_button.pack(side=tk.LEFT)

        self.advance_to_plot_display_frame_button = ttk.Button(self.plot_settings_menu_frame, text="Next", command=self.switch_to_plot_display_frame, style='nav_menu_button.TButton')
        self.advance_to_plot_display_frame_button.pack(side=tk.RIGHT)




################################################################################################################


    def display_scatter_plot_settings(self):

        self.plot_settings_frame_label = ttk.Label(self.plot_settings_subframe, text="Scatter Plot Settings", style="sub_frame_header.TLabel")
        self.plot_settings_frame_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.plot_settings_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)

        ############################################################################################################

        self.column_choice_frame = tk.Frame(self.plot_settings_subframe, bg=color_dict["sub_frame_bg"])
        self.column_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
        ###################### X AXIS ######################
        self.selected_x_axis_variable = data_manager.get_x_axis_selection()

        self.x_axis_frame = tk.Frame(self.column_choice_frame, bg=color_dict["sub_frame_bg"])
        self.x_axis_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.x_axis_frame_label = ttk.Label(self.x_axis_frame, text="X-Axis Selection", style="sub_frame_sub_header.TLabel")
        self.x_axis_frame_label.pack(side=tk.TOP)


        self.x_axis_search_var = tk.StringVar()
        self.x_axis_search_var.trace("w", self.update_x_axis_variable_listbox)
        self.x_axis_var_search_entry = tk.Entry(self.x_axis_frame, textvariable=self.x_axis_search_var, font=styles.listbox_font)
        self.x_axis_var_search_entry.pack(side=tk.TOP, pady=10)

        self.x_axis_variable_listbox = tk.Listbox(self.x_axis_frame, selectmode=tk.SINGLE, font=styles.listbox_font, exportselection=False, bg=color_dict["listbox_bg"],
                     fg=color_dict["listbox_fg"],
                     highlightbackground=color_dict["listbox_highlight_bg"],
                     highlightcolor=color_dict["listbox_highlight_color"],
                     selectbackground=color_dict["listbox_select_bg"],
                     selectforeground=color_dict["listbox_select_fg"])
        self.x_axis_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)
        self.x_axis_variable_listbox.bind("<Enter>",lambda e: utils.bind_mousewheel_to_frame(self.plot_settings_inner_frame, self.plot_settings_canvas, False))
        self.x_axis_variable_listbox.bind("<Leave>",lambda e: utils.bind_mousewheel_to_frame(self.plot_settings_inner_frame, self.plot_settings_canvas, True))


        for column in sorted(self.df.columns, key=str.lower):
            self.x_axis_variable_listbox.insert(tk.END, column)

        self.x_axis_variable_listbox.bind("<<ListboxSelect>>", self.on_x_axis_variable_listbox_select)

        self.x_axis_variable_label = ttk.Label(self.x_axis_frame, text="No Variable Selected", style="sub_frame_sub_header.TLabel")
        self.x_axis_variable_label.pack(side=tk.TOP, pady=10)

        if self.selected_x_axis_variable:
            self.x_axis_variable_label.config(text=f"X-Axis: {self.selected_x_axis_variable}")
            self.x_axis_variable_listbox.selection_clear(0, tk.END)
            items = list(self.x_axis_variable_listbox.get(0, tk.END))
            index = items.index(self.selected_x_axis_variable)
            self.x_axis_variable_listbox.selection_set(index)
            self.x_axis_variable_listbox.yview(index)
        ###################### X AXIS ######################


        ###################### Y AXIS ######################
        self.selected_y_axis_variable = data_manager.get_y_axis_selection()

        self.y_axis_frame = tk.Frame(self.column_choice_frame, bg=color_dict["sub_frame_bg"])
        self.y_axis_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.y_axis_frame_label = ttk.Label(self.y_axis_frame, text="Y-Axis Selection", style="sub_frame_sub_header.TLabel")
        self.y_axis_frame_label.pack(side=tk.TOP)


        self.y_axis_search_var = tk.StringVar()
        self.y_axis_search_var.trace("w", self.update_y_axis_variable_listbox)
        self.y_axis_var_search_entry = tk.Entry(self.y_axis_frame, textvariable=self.y_axis_search_var, font=styles.entrybox_small_font)
        self.y_axis_var_search_entry.pack(side=tk.TOP, pady=10)

        self.y_axis_variable_listbox = tk.Listbox(self.y_axis_frame, selectmode=tk.SINGLE, font=styles.listbox_font, exportselection=False, bg=color_dict["listbox_bg"],
                     fg=color_dict["listbox_fg"],
                     highlightbackground=color_dict["listbox_highlight_bg"],
                     highlightcolor=color_dict["listbox_highlight_color"],
                     selectbackground=color_dict["listbox_select_bg"],
                     selectforeground=color_dict["listbox_select_fg"])
        self.y_axis_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)
        self.y_axis_variable_listbox.bind("<Enter>",lambda e: utils.bind_mousewheel_to_frame(self.plot_settings_inner_frame, self.plot_settings_canvas, False))
        self.y_axis_variable_listbox.bind("<Leave>",lambda e: utils.bind_mousewheel_to_frame(self.plot_settings_inner_frame, self.plot_settings_canvas, True))

        for column in sorted(self.df.columns, key=str.lower):
            self.y_axis_variable_listbox.insert(tk.END, column)

        self.y_axis_variable_listbox.bind("<<ListboxSelect>>", self.on_y_axis_variable_listbox_select)

        self.y_axis_variable_label = ttk.Label(self.y_axis_frame, text="No Variable Selected", style="sub_frame_sub_header.TLabel")
        self.y_axis_variable_label.pack(side=tk.TOP, pady=10)

        if self.selected_y_axis_variable:
            self.y_axis_variable_label.config(text=f"Y-Axis: {self.selected_y_axis_variable}")
            self.y_axis_variable_listbox.selection_clear(0, tk.END)
            items = list(self.y_axis_variable_listbox.get(0, tk.END))
            index = items.index(self.selected_y_axis_variable)
            self.y_axis_variable_listbox.selection_set(index)
            self.y_axis_variable_listbox.yview(index)
        ###################### Y AXIS ######################


    def on_y_axis_variable_listbox_select(self, event):
        if self.y_axis_variable_listbox.curselection():
            self.selected_y_axis_variable = self.y_axis_variable_listbox.get(self.y_axis_variable_listbox.curselection()[0])
            data_manager.set_plot_tab_y_axis_selection(self.selected_y_axis_variable)
            self.y_axis_variable_label.config(text=f"Y-Axis: {self.selected_y_axis_variable}")


    def update_y_axis_variable_listbox(self, *args):
        search_term = self.y_axis_search_var.get().lower()
        self.y_axis_variable_listbox.delete(0, tk.END)

        # Check if the search term is empty
        if search_term == "":
            # If search term is empty, insert all columns sorted alphabetically
            for column in sorted(self.df.columns, key=str.lower):
                self.y_axis_variable_listbox.insert(tk.END, column)
        else:
            # If there is a search term, filter and sort the columns based on the search term
            filtered_sorted_columns = sorted([column for column in self.df.columns if search_term in column.lower()], key=str.lower)
            # Populate the Listbox with the sorted list
            for column in filtered_sorted_columns:
                self.y_axis_variable_listbox.insert(tk.END, column)


    def on_x_axis_variable_listbox_select(self, event):
        if self.x_axis_variable_listbox.curselection():
            self.selected_x_axis_variable = self.x_axis_variable_listbox.get(self.x_axis_variable_listbox.curselection()[0])
            data_manager.set_plot_tab_x_axis_selection(self.selected_x_axis_variable)
            self.x_axis_variable_label.config(text=f"X-Axis: {self.selected_x_axis_variable}")


    def update_x_axis_variable_listbox(self, *args):
        search_term = self.x_axis_search_var.get().lower()
        self.x_axis_variable_listbox.delete(0, tk.END)

        # Check if the search term is empty
        if search_term == "":
            # If search term is empty, insert all columns sorted alphabetically
            for column in sorted(self.df.columns, key=str.lower):
                self.x_axis_variable_listbox.insert(tk.END, column)
        else:
            # If there is a search term, filter and sort the columns based on the search term
            filtered_sorted_columns = sorted([column for column in self.df.columns if search_term in column.lower()], key=str.lower)
            # Populate the Listbox with the sorted list
            for column in filtered_sorted_columns:
                self.x_axis_variable_listbox.insert(tk.END, column)




################################################################################################################
################################################################################################################
################################################################################################################

    def create_plot_display_frame(self):

        # MAIN CONTENT FRAME
        self.plot_display_inner_frame, self.plot_display_canvas = utils.create_scrollable_frame(self.plot_display_frame)

################################################################################################################

        # PLOT SELECTION

        self.plot_display_subframe_border = tk.Frame(self.plot_display_inner_frame, bg=color_dict["sub_frame_border"])
        self.plot_display_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.plot_display_subframe = tk.Frame(self.plot_display_subframe_border, bg=color_dict["sub_frame_bg"])
        self.plot_display_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.plot_display_label = ttk.Label(self.plot_display_subframe, text="", style="sub_frame_header.TLabel")
        self.plot_display_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.plot_display_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)

        self.graph_frame = tk.Frame(self.plot_display_subframe, bg=color_dict["sub_frame_bg"])
        self.graph_frame.pack(side=tk.TOP, pady=10)



        # Save button
        self.save_graph_button = ttk.Button(self.plot_display_subframe, text="Save Graph", command=self.save_figure, style='large_button.TButton')
        self.save_graph_button.pack(side=tk.BOTTOM, padx=10, pady=10)
################################################################################################################

        # NAVIGATION MENU


        self.plot_display_menu_frame = tk.Frame(self.plot_display_frame, bg=color_dict["nav_banner_bg"])
        self.plot_display_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_plot_selection_button = ttk.Button(self.plot_display_menu_frame, text="Back", command=self.switch_to_plot_settings_frame, style='nav_menu_button.TButton')
        self.return_to_plot_selection_button.pack(side=tk.LEFT)





################################################################################################################

    def save_figure(self):

        # Prompt the user to choose the save location
        filetypes = [("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("TIFF files", "*.tiff")]
        save_path = filedialog.asksaveasfilename(filetypes=filetypes)

        # Check if the user canceled the dialog
        if not save_path:
            return

        # Save the figure with the specified DPI and path
        self.fig.savefig(save_path, dpi=300)




################################################################################################################
################################################################################################################
################################################################################################################





    def create_scatter_plot(self):
        if not self.selected_x_axis_variable or not self.selected_y_axis_variable:
            utils.show_message("No Columns Selected", "Both X and Y AXIS VARIABLES must be selected")
            raise

        try:
            self.df[self.selected_x_axis_variable] = self.df[self.selected_x_axis_variable].astype(float)
            self.df[self.selected_y_axis_variable] = self.df[self.selected_y_axis_variable].astype(float)
        except ValueError:
            utils.show_message("Error", "Selected variables must be continuous")
            raise

        clean_df = self.df[[self.selected_x_axis_variable, self.selected_y_axis_variable]].dropna().reset_index(drop=True)

        # Create scatter plot with seaborn
        sns.set(style="ticks")
        fig = Figure(figsize=(8, 7))
        ax = fig.add_subplot(111)  # Add subplot to the figure

        sns.scatterplot(data=clean_df, x=self.selected_x_axis_variable, y=self.selected_y_axis_variable, ax=ax)

        # Calculate regression line parameters
        slope, intercept, r_value, p_value, _ = stats.linregress(clean_df[self.selected_x_axis_variable], clean_df[self.selected_y_axis_variable])
        
        line = slope * clean_df[self.selected_x_axis_variable] + intercept

        # Add regression line to the plot
        sns.lineplot(x=clean_df[self.selected_x_axis_variable], y=line, color='r', ax=ax)

        # Add R-squared and p-value to the plot
        ax.text(0.05, 0.95, f"R-squared: {r_value**2:.4f}\nP-value: {p_value:.4f}", transform=ax.transAxes)

        # Customize plot aesthetics (title, labels, etc.)
        ax.set_title("")
        ax.set_xlabel(self.selected_x_axis_variable)
        ax.set_ylabel(self.selected_y_axis_variable)
        fig.tight_layout()

        return fig


    def display_graph(self):
        utils.remove_frame_widgets(self.graph_frame)

        fig_canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        fig_canvas_widget = fig_canvas.get_tk_widget()
        fig_canvas_widget.pack(fill=tk.Y, expand=True)






    # def create_histogram(visualize_content_frame, df):
    #     text_prompt1 = "Choose your VARIABLE for Histogram"
    #     chosen_continuous_variable = utils.get_single_choice(visualize_content_frame, df.columns, text_prompt1)
    #     if not chosen_continuous_variable:
    #         utils.show_message("No Columns Selected", "No X-AXIS VARIABLE selected")
    #         return
    #     try:
    #         df[chosen_continuous_variable] = df[chosen_continuous_variable].astype(float)
    #     except:
    #         utils.show_message("Error", "X-AXIS VARIABLE not a continuous variable. Pick Again")
    #         return

    #     clean_df = df[chosen_continuous_variable].dropna()

    #     sns.set(style="ticks")
    #     fig, ax = plt.subplots()
    #     sns.histplot(data=clean_df, kde=True, ax=ax)

    #     # Customize plot aesthetics (title, labels, etc.)
    #     plt.xlabel(chosen_continuous_variable)
    #     plt.ylabel("Frequency")
    #     plt.tight_layout()

    #     return fig







    # def create_box_and_whisker_plot(visualize_content_frame, df):
    #     return



################################################################################################################
################################################################################################################
################################################################################################################


    def switch_to_plot_selection_frame(self):

        self.plot_settings_frame.pack_forget()
        self.plot_display_frame.pack_forget()
        self.plot_selection_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        utils.bind_mousewheel_to_frame(self.plot_selection_inner_frame, self.plot_selection_canvas, True)
        self.visualize_content_frame.update_idletasks()
        self.plot_var_search_entry.focus_set()



    def switch_to_plot_settings_frame(self):
        if self.selected_plot == None:
            return

        utils.remove_frame_widgets(self.plot_settings_subframe)

        if self.selected_plot == "Scatter Plot":
            self.display_scatter_plot_settings()

        self.plot_selection_frame.pack_forget()
        self.plot_display_frame.pack_forget()
        self.plot_settings_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        utils.bind_mousewheel_to_frame(self.plot_settings_inner_frame, self.plot_settings_canvas, True)
        self.visualize_content_frame.update_idletasks()


    def switch_to_plot_display_frame(self):

        if self.selected_plot == "Scatter Plot":
            self.fig = self.create_scatter_plot()
            self.plot_display_label.config(text="Scatter Plot")

        
        self.display_graph()


        self.plot_selection_frame.pack_forget()
        self.plot_settings_frame.pack_forget()
        self.plot_display_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        utils.bind_mousewheel_to_frame(self.plot_display_inner_frame, self.plot_display_canvas, True)
        self.visualize_content_frame.update_idletasks()




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
        self.df.replace("[MISSING VALUE]", np.nan, inplace=True)

        self.visualize_content_frame = visualize_content_frame

        self.style = style


        self.style.configure("comparison_table_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"])
        self.style.configure("regression_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"])
        self.style.configure("create_plot_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"])
        self.style.configure("machine_learning_button.TButton", background=color_dict["active_subtab_bg"], foreground=color_dict["active_subtab_txt"])

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
            # "XGBoost":XGBClassifier(random_state=69),
            "Logistic Regression":LogisticRegression(max_iter=100000000, random_state=69)
        }


        self.available_continuous_models_dict = {
            # "test":"test"
            "Linear Regression":LinearRegression()
        }


        self.non_numeric_input_var_dict = data_manager.get_non_numeric_ind_dict()

        self.verify_saved_columns()

        self.machine_learning_model_options = ['cat_rf', 'cat_xgb', 'cat_logreg', 'cont_linreg']
        self.model_dict = {'cat_rf':'Random Forest', 'cat_logreg':'Logistic Regression', 'cont_linreg':'Linear Regression'}
        # self.model_function_dict = {'cat_rf':self.create_random_forest_classifier_model()}

        utils.remove_frame_widgets(self.visualize_content_frame)


        self.dependent_variable_frame = tk.Frame(self.visualize_content_frame, bg=color_dict["main_content_border"])
        self.indedependent_variables_frame = tk.Frame(self.visualize_content_frame, bg=color_dict["main_content_border"])
        self.variable_handling_frame = tk.Frame(self.visualize_content_frame, bg=color_dict["main_content_border"])
        self.settings_frame = tk.Frame(self.visualize_content_frame, bg=color_dict["main_content_border"])
        self.results_frame = tk.Frame(self.visualize_content_frame, bg=color_dict["main_content_border"])
        self.prediction_tool_frame = tk.Frame(self.visualize_content_frame, bg=color_dict["main_content_border"])

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
        self.dependent_variable_inner_frame, self.dependent_variable_canvas = utils.create_scrollable_frame(self.dependent_variable_frame)

################################################################################################################


        # DEPENDENT VARIABLE SELECTION

        self.dependent_variable_selection_subframe_border = tk.Frame(self.dependent_variable_inner_frame, bg=color_dict["sub_frame_border"])
        self.dependent_variable_selection_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.dependent_variable_selection_subframe = tk.Frame(self.dependent_variable_selection_subframe_border, bg=color_dict["sub_frame_bg"])
        self.dependent_variable_selection_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.dependent_variable_frame_label = ttk.Label(self.dependent_variable_selection_subframe, text="Dependent Variable Selection", style="sub_frame_header.TLabel")
        self.dependent_variable_frame_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.dependent_variable_selection_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)

        # DEPENDENT VARIABLE SELECTION FRAME
        self.dependent_column_choice_frame = tk.Frame(self.dependent_variable_selection_subframe, bg=color_dict["sub_frame_bg"])
        self.dependent_column_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

        self.dependent_search_var = tk.StringVar()
        self.dependent_search_var.trace("w", self.update_dependent_variable_listbox)
        self.dependent_var_search_entry = tk.Entry(self.dependent_column_choice_frame, textvariable=self.dependent_search_var, font=styles.entrybox_small_font)
        self.dependent_var_search_entry.pack(side=tk.TOP, pady=10)

        self.dependent_variable_listbox = tk.Listbox(self.dependent_column_choice_frame, selectmode=tk.SINGLE, font=styles.listbox_font, exportselection=False, bg=color_dict["listbox_bg"],
                     fg=color_dict["listbox_fg"],
                     highlightbackground=color_dict["listbox_highlight_bg"],
                     highlightcolor=color_dict["listbox_highlight_color"],
                     selectbackground=color_dict["listbox_select_bg"],
                     selectforeground=color_dict["listbox_select_fg"],
                     height=20)
        self.dependent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)
        self.dependent_variable_listbox.bind("<Enter>",lambda e: utils.bind_mousewheel_to_frame(self.dependent_variable_inner_frame, self.dependent_variable_canvas, False))
        self.dependent_variable_listbox.bind("<Leave>",lambda e: utils.bind_mousewheel_to_frame(self.dependent_variable_inner_frame, self.dependent_variable_canvas, True))

        for column in sorted(self.df.columns, key=str.lower):
            self.dependent_variable_listbox.insert(tk.END, column)

        self.dependent_variable_listbox.bind("<<ListboxSelect>>", self.on_dependent_variable_listbox_select)




################################################################################################################

        # NAVIGATION MENU
        self.dependent_variable_menu_frame = tk.Frame(self.dependent_variable_frame, bg=color_dict["nav_banner_bg"])
        self.dependent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.advance_to_independent_variables_button = ttk.Button(self.dependent_variable_menu_frame, text="Next", command=self.switch_to_independent_variables_frame, style='nav_menu_button.TButton')
        self.advance_to_independent_variables_button.pack(side=tk.RIGHT)

        self.dependent_frame_dependent_label = ttk.Label(self.dependent_variable_menu_frame, text="", style="nav_menu_label.TLabel")
        self.dependent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)



        if self.selected_dependent_variable:
            self.dependent_variable_listbox.selection_clear(0, tk.END)
            items = list(self.dependent_variable_listbox.get(0, tk.END))
            index = items.index(self.selected_dependent_variable)
            self.dependent_variable_listbox.selection_set(index)
            self.dependent_variable_listbox.yview(index)
            self.dependent_frame_dependent_label.config(text=f"Dependent Variable: {self.selected_dependent_variable}")



################################################################################################################

    def on_dependent_variable_listbox_select(self, event):
        if self.dependent_variable_listbox.curselection():
            self.selected_dependent_variable = self.dependent_variable_listbox.get(self.dependent_variable_listbox.curselection()[0])
            data_manager.set_mach_learn_tab_dep_var(self.selected_dependent_variable)
            self.dependent_frame_dependent_label.config(text=f"Dependent Variable: {self.selected_dependent_variable}")



    def update_dependent_variable_listbox(self, *args):
        search_term = self.dependent_search_var.get().lower()
        self.dependent_variable_listbox.delete(0, tk.END)

        # Check if the search term is empty
        if search_term == "":
            # If search term is empty, insert all columns sorted alphabetically
            for column in sorted(self.df.columns, key=str.lower):
                self.dependent_variable_listbox.insert(tk.END, column)
            if self.selected_dependent_variable:
                self.dependent_variable_listbox.selection_clear(0, tk.END)
                items = list(self.dependent_variable_listbox.get(0, tk.END))
                index = items.index(self.selected_dependent_variable)
                self.dependent_variable_listbox.selection_set(index)
        else:
            # If there is a search term, filter and sort the columns based on the search term
            filtered_sorted_columns = sorted([column for column in self.df.columns if search_term in column.lower()], key=str.lower)
            # Populate the Listbox with the sorted list
            for column in filtered_sorted_columns:
                self.dependent_variable_listbox.insert(tk.END, column)
            if self.selected_dependent_variable in filtered_sorted_columns:
                self.dependent_variable_listbox.selection_clear(0, tk.END)
                items = list(self.dependent_variable_listbox.get(0, tk.END))
                index = items.index(self.selected_dependent_variable)
                self.dependent_variable_listbox.selection_set(index)


################################################################################################################
################################################################################################################
################################################################################################################


    # CREATE INDEPENDENT VARIABLE SELECTION FRAME

    def create_independent_variables_frame(self):

        # MAIN CONTENT FRAME
        self.independent_variables_inner_frame, self.independent_variables_canvas = utils.create_scrollable_frame(self.indedependent_variables_frame)

################################################################################################################

        # INDEPENDENT VARIABLES SELECTION
        self.independent_variables_selection_subframe_border = tk.Frame(self.independent_variables_inner_frame, bg=color_dict["sub_frame_border"])
        self.independent_variables_selection_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.independent_variables_selection_subframe = tk.Frame(self.independent_variables_selection_subframe_border, bg=color_dict["sub_frame_bg"])
        self.independent_variables_selection_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.choose_independent_variables_label = ttk.Label(self.independent_variables_selection_subframe, text="Independent Variable Selection", style="sub_frame_header.TLabel")
        self.choose_independent_variables_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.independent_variables_selection_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)


        # AVAILABLE INDEPENDENT VARIABLES SELECTION FRAME
        self.indedependent_variables_selection_frame = tk.Frame(self.independent_variables_selection_subframe, bg=color_dict["sub_frame_bg"])
        self.indedependent_variables_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

        self.available_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg=color_dict["sub_frame_bg"])
        self.available_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.available_independent_search_var = tk.StringVar()
        self.available_independent_search_var.trace("w", self.update_available_independent_variable_listbox)
        self.independent_var_search_entry = tk.Entry(self.available_independent_variables_frame, textvariable=self.available_independent_search_var, font=styles.entrybox_small_font)
        self.independent_var_search_entry.pack(side=tk.TOP, pady=10)

        self.available_independent_variable_listbox = tk.Listbox(self.available_independent_variables_frame, selectmode=tk.MULTIPLE, font=styles.listbox_font,
                                                                bg=color_dict["listbox_bg"],
                                                                fg=color_dict["listbox_fg"],
                                                                highlightbackground=color_dict["listbox_highlight_bg"],
                                                                highlightcolor=color_dict["listbox_highlight_color"],
                                                                selectbackground=color_dict["listbox_select_bg"],
                                                                selectforeground=color_dict["listbox_select_fg"]
                                                                )
        self.available_independent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)
        self.available_independent_variable_listbox.bind("<Enter>",lambda e: utils.bind_mousewheel_to_frame(self.independent_variables_inner_frame, self.independent_variables_canvas, False))
        self.available_independent_variable_listbox.bind("<Leave>",lambda e: utils.bind_mousewheel_to_frame(self.independent_variables_inner_frame, self.independent_variables_canvas, True))



        for column in sorted(self.df.columns, key=str.lower):
            if column not in self.selected_independent_variables:
                self.available_independent_variable_listbox.insert(tk.END, column)


        # TRANSFER BUTTONS
        self.buttons_frame = tk.Frame(self.indedependent_variables_selection_frame, bg=color_dict["sub_frame_bg"])
        self.buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Larger buttons with ">>>" and "<<<" symbols
        self.transfer_right_button = ttk.Button(self.buttons_frame, text="Transfer Right >>>", command=self.transfer_right, style="large_button.TButton")
        self.transfer_right_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.transfer_left_button = ttk.Button(self.buttons_frame, text="<<< Transfer Left", command=self.transfer_left, style="large_button.TButton")
        self.transfer_left_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)

        separator = ttk.Separator(self.buttons_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, pady=10)

        # Text buttons "Select All" and "Clear Selection"
        self.transfer_all_right_button = ttk.Button(self.buttons_frame, text="Select All", command=self.transfer_all_right, style="large_button.TButton")
        self.transfer_all_right_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)

        self.transfer_all_left_button = ttk.Button(self.buttons_frame, text="Clear Selection", command=self.transfer_all_left, style="large_button.TButton")
        self.transfer_all_left_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)


        separator = ttk.Separator(self.buttons_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

        # Import and export selected variables
        self.import_variable_list_button = ttk.Button(self.buttons_frame, text="Import Variable List", command=self.import_variable_list, style="large_button.TButton")
        self.import_variable_list_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)

        self.export_variable_list_button = ttk.Button(self.buttons_frame, text="Export Variable List", command=self.export_variable_list, style="large_button.TButton")
        self.export_variable_list_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)


        # SELECTED INDEPENDENT VARIABLES FRAME
        self.selected_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg=color_dict["sub_frame_bg"])
        self.selected_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.selected_independent_variables_label = ttk.Label(self.selected_independent_variables_frame, text="Selected Variables", style="sub_frame_sub_header.TLabel")
        self.selected_independent_variables_label.pack(side=tk.TOP, pady=10)



        self.selected_independent_variable_listbox = tk.Listbox(self.selected_independent_variables_frame, selectmode=tk.MULTIPLE, font=styles.listbox_font,
                                                                bg=color_dict["listbox_bg"],
                                                                fg=color_dict["listbox_fg"],
                                                                highlightbackground=color_dict["listbox_highlight_bg"],
                                                                highlightcolor=color_dict["listbox_highlight_color"],
                                                                selectbackground=color_dict["listbox_select_bg"],
                                                                selectforeground=color_dict["listbox_select_fg"]
                                                                )
        self.selected_independent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)
        self.selected_independent_variable_listbox.bind("<Enter>",lambda e: utils.bind_mousewheel_to_frame(self.independent_variables_inner_frame, self.independent_variables_canvas, False))
        self.selected_independent_variable_listbox.bind("<Leave>",lambda e: utils.bind_mousewheel_to_frame(self.independent_variables_inner_frame, self.independent_variables_canvas, True))

        if len(self.selected_independent_variables) > 0:
            for var in self.selected_independent_variables:
                self.selected_independent_variable_listbox.insert(tk.END, var)
                self.available_independent_variable_listbox.selection_set(sorted(self.df.columns, key=str.lower).index(var))
            selections = self.available_independent_variable_listbox.curselection()
            for index in reversed(selections):
                self.available_independent_variable_listbox.delete(index)


################################################################################################################



        # MACHINE LEARNING MODEL SELECTION FRAME

        self.model_options_subframe_border = tk.Frame(self.independent_variables_inner_frame, bg=color_dict["sub_frame_border"])
        self.model_options_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.model_options_subframe = tk.Frame(self.model_options_subframe_border, bg=color_dict["sub_frame_bg"])
        self.model_options_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.choose_independent_variables_label = ttk.Label(self.model_options_subframe, text="Machine Learning Model Selection", style="sub_frame_header.TLabel")
        self.choose_independent_variables_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.model_options_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)



        self.model_selection_frame = tk.Frame(self.model_options_subframe, bg=color_dict["sub_frame_bg"])
        self.model_selection_frame.pack(side=tk.TOP, fill=tk.X)




        # Categorical Model Frame
        self.categorical_model_frame = tk.Frame(self.model_selection_frame, bg=color_dict["sub_frame_bg"])
        self.categorical_model_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.categorical_model_type_button = ttk.Button(self.categorical_model_frame, text="Categorical Model", style="inactive_radio_button.TButton", command=lambda: self.toggle_model_type_button_style("Categorical"))
        self.categorical_model_type_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Combobox Frame
        self.categorical_model_selection_frame = tk.Frame(self.categorical_model_frame, bg=color_dict["sub_frame_bg"])
        self.categorical_model_selection_frame.pack(side=tk.TOP, fill=tk.X, expand=True)


        def on_categorical_model_combobox_selected(event):
            self.selected_model = self.categorical_model_selection_combobox.get()
            data_manager.set_mach_learn_tab_selected_cat_model(self.selected_model)

        self.categorical_model_selection_combobox = ttk.Combobox(self.categorical_model_selection_frame, values=list(self.available_categorical_models_dict.keys()), font=styles.large_button_font, state="disabled", style="TCombobox")
        self.categorical_model_selection_combobox.bind("<<ComboboxSelected>>", on_categorical_model_combobox_selected)
        self.categorical_model_selection_combobox.pack(side=tk.TOP, pady=10)
        self.categorical_model_selection_combobox.current(0)
        data_manager.set_mach_learn_tab_selected_cat_model("Random Forest")



        # Continuous Model Frame
        self.continuous_model_frame = tk.Frame(self.model_selection_frame, bg=color_dict["sub_frame_bg"])
        self.continuous_model_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.continuous_model_type_button = ttk.Button(self.continuous_model_frame, text="Continuous Model", style="inactive_radio_button.TButton", command=lambda: self.toggle_model_type_button_style("Continuous"))
        self.continuous_model_type_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Combobox Frame
        self.continuous_model_selection_frame = tk.Frame(self.continuous_model_frame, bg=color_dict["sub_frame_bg"])
        self.continuous_model_selection_frame.pack(side=tk.TOP, fill=tk.X, expand=True)


        def on_continuous_model_combobox_selected(event):
            self.selected_model = self.continuous_model_selection_combobox.get()
            data_manager.set_mach_learn_tab_selected_cont_model(self.selected_model)

        self.continuous_model_selection_combobox = ttk.Combobox(self.continuous_model_selection_frame, values=list(self.available_continuous_models_dict.keys()), font=styles.large_button_font, state="disabled", style="TCombobox")
        self.continuous_model_selection_combobox.bind("<<ComboboxSelected>>", on_continuous_model_combobox_selected)
        self.continuous_model_selection_combobox.pack(side=tk.TOP, pady=10)
        self.continuous_model_selection_combobox.current(0)
        data_manager.set_mach_learn_tab_selected_cont_model("Test")






        # Load Previously Chosen Percent Selection
        if self.selected_model_type:

            if self.selected_model_type == "Categorical":

                self.toggle_model_type_button_style("Categorical")
                self.categorical_model_selection_combobox.configure(state="readonly")
                self.continuous_model_selection_combobox.configure(state="disabled")

                self.categorical_model_selection_combobox.set(self.selected_categorical_model)

                self.selected_model = self.selected_categorical_model


            elif self.selected_model_type == "Continuous":

                self.toggle_model_type_button_style("Continuous")
                self.categorical_model_selection_combobox.configure(state="disabled")
                self.continuous_model_selection_combobox.configure(state="readonly")

                self.continuous_model_selection_combobox.set(self.selected_continuous_model)

                self.selected_model = self.selected_continuous_model
        else:
            self.toggle_model_type_button_style("Categorical")






################################################################################################################


        # NAVIGATION MENU
        self.independent_variable_menu_frame = tk.Frame(self.indedependent_variables_frame, bg=color_dict["nav_banner_bg"])
        self.independent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_dependent_variable_frame_button = ttk.Button(self.independent_variable_menu_frame, command=self.switch_to_dependent_variable_frame, text='Back', style='nav_menu_button.TButton')
        self.return_to_dependent_variable_frame_button.pack(side=tk.LEFT)

        self.advance_to_variable_handling_frame_button = ttk.Button(self.independent_variable_menu_frame, command=self.switch_to_variable_handling_frame, text="Next", style='nav_menu_button.TButton')
        self.advance_to_variable_handling_frame_button.pack(side=tk.RIGHT)

        self.independent_frame_dependent_label = ttk.Label(self.independent_variable_menu_frame, text="", style="nav_menu_label.TLabel")
        self.independent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)




################################################################################################################


    def update_available_independent_variable_listbox(self, *args):
        search_term = self.available_independent_search_var.get().lower()
        self.available_independent_variable_listbox.delete(0, tk.END)
        for column in sorted(self.df.columns, key=str.lower):
            if search_term in column.lower():
                if column not in self.selected_independent_variables:
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
        
        self.independent_var_search_entry.focus_set()


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
            if item not in self.selected_independent_variables:
                self.available_independent_variable_listbox.insert(tk.END, item)

        if top_visible_index >= 0:
            index = items.index(top_visible_item)
            self.available_independent_variable_listbox.yview(index)


    def toggle_model_type_button_style(self, selected):

        if selected == "Categorical":
            self.continuous_model_type_button.configure(style="inactive_radio_button.TButton")
            self.categorical_model_type_button.configure(style="active_radio_button.TButton")
            self.selected_model_type = "Categorical"
            data_manager.set_mach_learn_tab_selected_model_type(self.selected_model_type)
            self.selected_model = self.categorical_model_selection_combobox.get()

            self.continuous_model_selection_combobox.configure(state="disabled")
            self.categorical_model_selection_combobox.configure(state="readonly")

        elif selected == "Continuous":
            self.continuous_model_type_button.configure(style="active_radio_button.TButton")
            self.categorical_model_type_button.configure(style="inactive_radio_button.TButton")
            self.selected_model_type = "Continuous"
            data_manager.set_mach_learn_tab_selected_model_type(self.selected_model_type)
            self.selected_model = self.continuous_model_selection_combobox.get()

            self.continuous_model_selection_combobox.configure(state="readonly")
            self.categorical_model_selection_combobox.configure(state="disabled")

    def import_variable_list(self):
        imported_variable_list = data_manager.get_exported_variables_list()

        for var in imported_variable_list:
            if var in self.df.columns:
                self.selected_independent_variable_listbox.insert(tk.END, var)
                self.selected_independent_variables.append(var)

    def export_variable_list(self):
        data_manager.clear_exported_variables_list()
        for var in self.selected_independent_variables:
            data_manager.add_variable_to_exported_variables_list(var)
            
################################################################################################################
################################################################################################################
################################################################################################################

    # CREATE VARIABLE HANDLING FRAME

    def create_variable_handling_frame(self):

        # MAIN CONTENT FRAME
        self.variable_handling_inner_frame, self.variable_handling_canvas = utils.create_scrollable_frame(self.variable_handling_frame)

        ########################################################################################################


        # NAVIGATION MENU FRAME
        self.variable_handling_menu_frame = tk.Frame(self.variable_handling_frame, bg=color_dict["nav_banner_bg"])
        self.variable_handling_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_independent_variable_frame_button = ttk.Button(self.variable_handling_menu_frame, command=self.switch_to_independent_variables_frame, text='Back', style='nav_menu_button.TButton')
        self.return_to_independent_variable_frame_button.pack(side=tk.LEFT)

        self.advance_to_settings_frame_button = ttk.Button(self.variable_handling_menu_frame, command=self.switch_to_settings_frame, text="Next ->", style='nav_menu_button.TButton')
        self.advance_to_settings_frame_button.pack(side=tk.RIGHT)

        self.variable_handling_menu_frame_dependent_label = ttk.Label(self.variable_handling_menu_frame, text="", style="nav_menu_label.TLabel")
        self.variable_handling_menu_frame_dependent_label.pack(side=tk.RIGHT, expand=True)


    ################################################################################################################

    # HANDLE VARIABLES FOR MACHINE LEARNING

    def handle_variables_machine_learning(self):
        
        utils.remove_frame_widgets(self.variable_handling_inner_frame)


        self.temp_df = self.df[self.selected_independent_variables + [self.selected_dependent_variable]].copy()
        self.clean_df = self.temp_df[self.selected_dependent_variable].copy().dropna()



################################################################################################################

        # TARGET VALUE SUBFRAME
        self.target_value_subframe_border = tk.Frame(self.variable_handling_inner_frame, bg=color_dict["sub_frame_border"])
        self.target_value_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=10)

        self.target_value_subframe = tk.Frame(self.target_value_subframe_border, bg=color_dict["sub_frame_bg"])
        self.target_value_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.target_value_label = ttk.Label(self.target_value_subframe, text="Target Value Selection", style="sub_frame_header.TLabel")
        self.target_value_label.pack(side=tk.TOP, pady=10)
        
        separator = ttk.Separator(self.target_value_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)


        self.target_value_1 = f"{self.clean_df.unique()[0]}"
        self.target_value_2 = f"{self.clean_df.unique()[1]}"

        self.target_value_1_button = ttk.Button(self.target_value_subframe, text=self.target_value_1, style="inactive_radio_button.TButton", command=lambda: self.toggle_target_value_button_style(self.target_value_1))
        self.target_value_1_button.pack(side=tk.TOP, fill=tk.X, padx=100, pady=10)

        self.target_value_2_button = ttk.Button(self.target_value_subframe, text=self.target_value_2, style="inactive_radio_button.TButton", command=lambda: self.toggle_target_value_button_style(self.target_value_2))
        self.target_value_2_button.pack(side=tk.TOP, fill=tk.X, padx=100, pady=10)

        # Load Previously Chosen Percent Selection
        if self.selected_dependent_variable in self.log_reg_target_value_var_dict:
            
            if self.log_reg_target_value_var_dict[self.selected_dependent_variable] == self.target_value_1:
                self.toggle_target_value_button_style(self.target_value_1)
            elif self.log_reg_target_value_var_dict[self.selected_dependent_variable] == self.target_value_2:
                self.toggle_target_value_button_style(self.target_value_2)
        else:
            self.toggle_target_value_button_style(self.target_value_1)




################################################################################################################

        # VARIABLE HANDLING FRAME
        self.variable_handling_subframe_border = tk.Frame(self.variable_handling_inner_frame, bg=color_dict["sub_frame_border"])
        self.variable_handling_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.variable_handling_subframe = tk.Frame(self.variable_handling_subframe_border, bg=color_dict["sub_frame_bg"])
        self.variable_handling_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.variable_handling_frame_label = ttk.Label(self.variable_handling_subframe, text="Change Non-Numeric Values in The Following Independent Variables", style="sub_frame_header.TLabel")
        self.variable_handling_frame_label.pack(side=tk.TOP, pady=10)
        
        separator = ttk.Separator(self.variable_handling_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)

        self.value_entry_frame = tk.Frame(self.variable_handling_subframe, bg=color_dict["sub_frame_bg"])
        self.value_entry_frame.pack(side=tk.TOP, pady=10)


        # DETERMINE NON-NUMERIC VARIABLES
        self.non_numeric_columns = []

        self.selected_options = {}

        for independent_variable in self.selected_independent_variables:
            try:
                self.temp_df[independent_variable] = self.temp_df[independent_variable].astype(float)
            except:
                self.non_numeric_columns.append(independent_variable)

        if len(self.non_numeric_columns) == 0:
            proceed_to_results_label = ttk.Label(self.value_entry_frame, text="No Non-Numeric Variables. Click NEXT", style="sub_frame_sub_header.TLabel")
            proceed_to_results_label.pack(side=tk.TOP, fill=tk.X, pady=5, padx=20)

        else:

            # HANDLE NON-NUMERIC VARIABLES
            for variable in self.non_numeric_columns:



                options_frame = tk.Frame(self.value_entry_frame, bg=color_dict["sub_frame_bg"])
                options_frame.pack(side=tk.TOP, pady=10, padx=20)


                if len(variable) > 20:
                    variable_string = variable[0:19] + "..."
                else:
                    variable_string = variable

                variable_label = ttk.Label(options_frame, text=variable_string, style="sub_frame_sub_header.TLabel")
                variable_label.pack(side=tk.TOP)


                non_numeric_values = []

                for value in self.temp_df[variable].unique():
                    if isinstance(value, str) and not value.isdigit():
                        non_numeric_values.append(value)

                for value in non_numeric_values:

                    value_frame = tk.Frame(options_frame, bg=color_dict["sub_frame_bg"])
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



                    input_entry = tk.Entry(value_frame, textvariable=user_input_var, font=styles.entrybox_large_font, width=10)
                    input_entry.pack(side=tk.LEFT)

                    value_label = ttk.Label(value_frame, text=value, style="sub_frame_sub_header.TLabel")
                    value_label.pack(side=tk.LEFT)

                    # Bind the entry widget to an event
                    input_entry.bind("<KeyRelease>", lambda event, var=variable, val=value: self.on_key_release(event, var, val))

                separator = ttk.Separator(self.value_entry_frame, orient="horizontal", style="Separator.TSeparator")
                separator.pack(fill=tk.X, padx=5, pady=5)



    def on_key_release(self, event, variable, value):
        data_manager.add_variable_to_non_numeric_ind_dict(variable, value, event.widget.get())


    # Function to toggle button styles
    def toggle_target_value_button_style(self, selected):
        if selected in [self.target_value_1, self.target_value_2]:
            if selected == self.target_value_1:
                self.target_value_1_button.configure(style="active_radio_button.TButton")
                self.target_value_2_button.configure(style="inactive_radio_button.TButton")
                self.selected_target_value = self.target_value_1
                data_manager.add_variable_to_reg_tab_log_reg_target_value_dict(self.selected_dependent_variable, selected)
            elif selected == self.target_value_2:
                self.target_value_1_button.configure(style="inactive_radio_button.TButton")
                self.target_value_2_button.configure(style="active_radio_button.TButton")
                self.selected_target_value = self.target_value_2
                data_manager.add_variable_to_reg_tab_log_reg_target_value_dict(self.selected_dependent_variable, selected)


    def apply_variable_handling(self):
        self.settings_subframe_label.configure(text=f"{self.selected_model} Model Settings")


        self.temp_df[self.selected_dependent_variable] = self.temp_df[self.selected_dependent_variable].astype(str)

        # MAKE VALUES OF DEPENDENT VARIABLE BINARY
        self.corrected_dependent_variable = "new_outcome_variable"

        self.temp_df.dropna(subset=[self.selected_dependent_variable])

        self.temp_df.loc[self.temp_df[self.selected_dependent_variable]==self.selected_target_value, self.corrected_dependent_variable] = 1
        self.temp_df.loc[self.temp_df[self.selected_dependent_variable]!=self.selected_target_value, self.corrected_dependent_variable] = 0


        self.temp_df[self.corrected_dependent_variable] = self.temp_df[self.corrected_dependent_variable].astype(int)

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

        self.settings_inner_frame, self.settings_canvas = utils.create_scrollable_frame(self.settings_frame)

################################################################################################################


        # SETTINGS FRAME
        self.settings_subframe_border = tk.Frame(self.settings_inner_frame, bg=color_dict["sub_frame_border"])
        self.settings_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.settings_subframe = tk.Frame(self.settings_subframe_border, bg=color_dict["sub_frame_bg"])
        self.settings_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.settings_subframe_label = ttk.Label(self.settings_subframe, text="", style="sub_frame_header.TLabel")
        self.settings_subframe_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.settings_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)


################################################################################################################


        #NULL VALUE HANDLING
        self.null_value_handling_frame = tk.Frame(self.settings_subframe, bg=color_dict["sub_frame_bg"])
        self.null_value_handling_frame.pack(side=tk.TOP, fill=tk.X)


        if self.null_values_handling_option:
            self.null_value_option_var = tk.StringVar(value=self.null_values_handling_option)
        else:
            self.null_value_option_var = tk.StringVar(value="REMOVE null values")


        self.null_value_handling_option_label = ttk.Label(self.null_value_handling_frame, text="MISSING/NULL values", style="sub_frame_sub_header.TLabel")
        self.null_value_handling_option_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.null_value_handling_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=400, pady=5)

        self.null_value_combobox_selection_frame = tk.Frame(self.null_value_handling_frame, bg=color_dict["sub_frame_bg"])
        self.null_value_combobox_selection_frame.pack(side=tk.TOP)

        def on_null_value_combobox_select(event):
            selected_option = self.null_value_option_var.get()
            data_manager.set_mach_learn_tab_null_values_choice(selected_option)
            if selected_option == 'REPLACE with user choice':
                self.null_value_user_choice_entry.pack(side=tk.LEFT, padx=5, pady=5)
                self.null_value_user_choice_entry.focus_set()
            else:
                self.null_value_user_choice_entry.pack_forget()

        self.null_value_option_combobox = ttk.Combobox(self.null_value_combobox_selection_frame, textvariable=self.null_value_option_var, font=("Arial", 24), width=25, state='readonly')
        self.null_value_option_combobox['values'] = ['REMOVE null values', 'REPLACE with mean', 'REPLACE with median', 'REPLACE with mode', 'REPLACE with user choice']
        self.null_value_option_combobox.bind("<<ComboboxSelected>>", on_null_value_combobox_select)
        self.null_value_option_combobox.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=20)


        # NULL VALUE ENTRY
        if self.null_value_entry_value:
            self.null_value_entry_var = tk.StringVar(value=self.null_value_entry_value)
        else:
            self.null_value_entry_var = tk.StringVar(value="")

        self.null_value_user_choice_entry = tk.Entry(self.null_value_combobox_selection_frame, textvariable=self.null_value_entry_var, font=styles.entrybox_large_font)

        def on_null_value_entry_release(event):
            current_value = event.widget.get()
            data_manager.set_mach_learn_tab_null_value_entry_value(current_value)

        self.null_value_user_choice_entry.bind("<KeyRelease>", lambda event: on_null_value_entry_release(event))

        if self.null_value_option_var.get() == "REPLACE with user choice":
            self.null_value_user_choice_entry.pack(side=tk.LEFT, padx=5, pady=5)
            self.null_value_user_choice_entry.focus_set()

################################################################################################################


        # NUMBER OF FOLDS SELECTION
        self.number_of_folds_frame = tk.Frame(self.settings_subframe, bg=color_dict["sub_frame_bg"])
        self.number_of_folds_frame.pack(side=tk.TOP, fill=tk.BOTH)

        self.number_of_folds_label = ttk.Label(self.number_of_folds_frame, text="TRAIN/TEST Folds", style="sub_frame_sub_header.TLabel")
        self.number_of_folds_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.number_of_folds_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=400, pady=5)


        self.number_of_folds_combobox_selection_frame = tk.Frame(self.number_of_folds_frame, bg=color_dict["sub_frame_bg"])
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




        self.train_fold_percent_frame = tk.Frame(self.number_of_folds_combobox_selection_frame, bg=color_dict["sub_frame_bg"])

        self.train_fold_percent_label_1 = ttk.Label(self.train_fold_percent_frame, text="Train model on ", style="sub_frame_text.TLabel")
        self.train_fold_percent_label_1.pack(side=tk.LEFT,padx=5)

        self.train_fold_percent_entry = tk.Entry(self.train_fold_percent_frame, textvariable=self.train_percent_var, font=styles.entrybox_small_font, width=5)
        self.train_fold_percent_entry.pack(side=tk.LEFT,padx=5)

        self.train_fold_percent_label_2 = ttk.Label(self.train_fold_percent_frame, text="% of the dataframe", style="sub_frame_text.TLabel")
        self.train_fold_percent_label_2.pack(side=tk.LEFT,padx=5)


        def on_entry_release(event):
            current_value = event.widget.get()
            data_manager.set_mach_learn_tab_train_percent(current_value)

        self.train_fold_percent_entry.bind("<KeyRelease>", lambda event: on_entry_release(event))

        if self.number_of_folds_var.get() == 2:
            self.train_fold_percent_frame.pack(side=tk.LEFT, padx=5, pady=5)




################################################################################################################

        # HYPERTUNING PARAMETERS CHECKBOX
        self.hypertune_parameters_frame = tk.Frame(self.settings_subframe, bg=color_dict["sub_frame_bg"])
        self.hypertune_parameters_frame.pack(side=tk.TOP, fill=tk.BOTH)

        self.hypertune_parameters_label = ttk.Label(self.hypertune_parameters_frame, text="Hypertune Model Parameters", style="sub_frame_sub_header.TLabel")
        self.hypertune_parameters_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.hypertune_parameters_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=400, pady=5)


        self.hypertune_parameters_button_frame = tk.Frame(self.hypertune_parameters_frame, bg=color_dict["sub_frame_bg"])
        self.hypertune_parameters_button_frame.pack(side=tk.TOP)

        self.hypertune_parameters_yes_button = ttk.Button(self.hypertune_parameters_button_frame, text="Yes", style="inactive_radio_button.TButton", command=lambda: self.toggle_hypertune_button_style("Yes"))
        self.hypertune_parameters_yes_button.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=10)

        self.hypertune_parameters_no_button = ttk.Button(self.hypertune_parameters_button_frame, text="No", style="inactive_radio_button.TButton", command=lambda: self.toggle_hypertune_button_style("No"))
        self.hypertune_parameters_no_button.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=10)

        # Load Previously Chosen Percent Selection
        if self.hypertune_parameters_choice:
            
            if self.hypertune_parameters_choice == "Yes":
                self.toggle_hypertune_button_style("Yes")
            elif self.hypertune_parameters_choice == "No":
                self.toggle_hypertune_button_style("No")
        else:
            self.toggle_hypertune_button_style("No")





################################################################################################################


        # PLOT SETTINGS
        self.plot_settings_frame = tk.Frame(self.settings_subframe, bg=color_dict["sub_frame_bg"])
        self.plot_settings_frame.pack(side=tk.TOP, padx=5, pady=10, fill=tk.BOTH)

        self.plot_settings_label = ttk.Label(self.plot_settings_frame, text="Select plot features to include", style="sub_frame_sub_header.TLabel")
        self.plot_settings_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.plot_settings_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=400, pady=5)

        self.plot_features_grid_frame = tk.Frame(self.plot_settings_frame, bg=color_dict["sub_frame_bg"])
        self.plot_features_grid_frame.pack(side=tk.TOP, pady=5)

        self.accuracy_checkbox_var = tk.BooleanVar()
        self.accuracy_checkbox = tk.Checkbutton(self.plot_features_grid_frame, text="Accuracy", variable=self.accuracy_checkbox_var, font=("Arial", 36), bg=color_dict["sub_frame_bg"])
        self.accuracy_checkbox.grid(row=0, column=0, sticky=tk.W, padx=40)
        self.accuracy_checkbox_var.set(True)

        self.sensitivity_checkbox_var = tk.BooleanVar()
        self.sensitivity_checkbox = tk.Checkbutton(self.plot_features_grid_frame, text="Sensitivity", variable=self.sensitivity_checkbox_var, font=("Arial", 36), bg=color_dict["sub_frame_bg"])
        self.sensitivity_checkbox.grid(row=0, column=1, sticky=tk.W, padx=40)
        self.sensitivity_checkbox_var.set(True)

        self.specificity_checkbox_var = tk.BooleanVar()
        self.specificity_checkbox = tk.Checkbutton(self.plot_features_grid_frame, text="Specificity", variable=self.specificity_checkbox_var, font=("Arial", 36), bg=color_dict["sub_frame_bg"])
        self.specificity_checkbox.grid(row=1, column=0, sticky=tk.W, padx=40)
        self.specificity_checkbox_var.set(True)

        self.shap_values_checkbox_var = tk.BooleanVar()
        self.shap_values_checkbox = tk.Checkbutton(self.plot_features_grid_frame, text="Shap Values", variable=self.shap_values_checkbox_var, font=("Arial", 36), bg=color_dict["sub_frame_bg"])
        self.shap_values_checkbox.grid(row=1, column=1, sticky=tk.W, padx=40)
        self.shap_values_checkbox_var.set(False)

################################################################################################################

        # NAVIGATION MENU FRAME
        self.model_settings_menu_frame = tk.Frame(self.settings_frame, bg=color_dict["nav_banner_bg"])
        self.model_settings_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_variable_handling_frame_button = ttk.Button(self.model_settings_menu_frame, command=self.switch_to_variable_handling_frame, text='Back', style='nav_menu_button.TButton')
        self.return_to_variable_handling_frame_button.pack(side=tk.LEFT)

        self.advance_to_results_frame_button = ttk.Button(self.model_settings_menu_frame, command=self.switch_to_results_frame, text='View Results', style='nav_menu_button.TButton')
        self.advance_to_results_frame_button.pack(side=tk.RIGHT)

        self.model_settings_frame_dependent_label = ttk.Label(self.model_settings_menu_frame, text="", style="nav_menu_label.TLabel")
        self.model_settings_frame_dependent_label.pack(side=tk.RIGHT, expand=True)

################################################################################################################


    # Function to toggle button styles
    def toggle_hypertune_button_style(self, selected):

        if selected == "Yes":
            self.hypertune_parameters_yes_button.configure(style="active_radio_button.TButton")
            self.hypertune_parameters_no_button.configure(style="inactive_radio_button.TButton")
            self.hypertune_parameters_choice = "Yes"
            data_manager.set_mach_learn_tab_hyper_param_choice(selected)

        elif selected == "No":
            self.hypertune_parameters_yes_button.configure(style="inactive_radio_button.TButton")
            self.hypertune_parameters_no_button.configure(style="active_radio_button.TButton")
            self.hypertune_parameters_choice = "No"
            data_manager.set_mach_learn_tab_hyper_param_choice(selected)

################################################################################################################
################################################################################################################
################################################################################################################

    # CREATE RESULTS FRAME

    def create_results_frame(self):

        self.results_inner_frame, self.results_canvas = utils.create_scrollable_frame(self.results_frame)

################################################################################################################


        # RESULTS FRAME
        self.results_subframe_border = tk.Frame(self.results_inner_frame, bg=color_dict["sub_frame_border"])
        self.results_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.results_subframe = tk.Frame(self.results_subframe_border, bg=color_dict["sub_frame_bg"])
        self.results_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)





################################################################################################################

        # GRAPH FRAMES
        self.results_display_frame = tk.Frame(self.results_subframe, bg='red')
        self.results_display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.auc_results_frame = tk.Frame(self.results_display_frame, bg=color_dict["sub_frame_bg"])
        self.auc_results_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.auc_graph_label = ttk.Label(self.auc_results_frame, text="AUC Graph", style="sub_frame_header.TLabel")
        self.auc_graph_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.auc_results_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)

        self.auc_graph_display_frame = tk.Frame(self.auc_results_frame, bg=color_dict["sub_frame_bg"])
        self.auc_graph_display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)




        self.feature_importance_results_frame = tk.Frame(self.results_display_frame, bg=color_dict["sub_frame_bg"])

        self.feature_importance_label = ttk.Label(self.feature_importance_results_frame, text="Feature Importances", style="sub_frame_header.TLabel")
        self.feature_importance_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.feature_importance_results_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)

        self.feature_importance_display_frame = tk.Frame(self.feature_importance_results_frame, bg=color_dict["sub_frame_bg"])
        self.feature_importance_display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)


        # SAVE FIGURE AND SWITCH BETWEEN GRAPHS FRAME
        self.results_button_frame = tk.Frame(self.results_subframe, bg=color_dict["sub_frame_bg"])
        self.results_button_frame.pack(side=tk.TOP, fill=tk.X)

        # Calculate the maximum text width based on the longest possible text for both buttons
        max_text_width = max(len("Save Graph"), len("View Feature Importances"))

        # Save button
        self.save_graph_button = ttk.Button(self.results_button_frame, text="Save Graph", command=self.save_figure, style='large_button.TButton', width=max_text_width)
        self.save_graph_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Switch button
        self.switch_graph_button = ttk.Button(self.results_button_frame, text="View Feature Importances", command=self.switch_display_frames, style='large_button.TButton', width=max_text_width)
        self.switch_graph_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Configure column weights to make them occupy half of the frame
        self.results_button_frame.columnconfigure(0, weight=1)
        self.results_button_frame.columnconfigure(1, weight=1)

        self.current_graph = "AUC"






################################################################################################################



        # NAVIGATION MENU FRAME
        self.results_menu_frame = tk.Frame(self.results_frame, bg=color_dict["nav_banner_bg"])
        self.results_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_settings_frame_button = ttk.Button(self.results_menu_frame, command=self.switch_to_settings_frame, text='<- Back', style='nav_menu_button.TButton')
        self.return_to_settings_frame_button.pack(side=tk.LEFT)

        self.results_frame_dependent_label = ttk.Label(self.results_menu_frame, text="", style="nav_menu_label.TLabel")
        self.results_frame_dependent_label.pack(side=tk.LEFT, expand=True)

        self.advance_to_prediction_tool_buton = ttk.Button(self.results_menu_frame, command=self.switch_to_prediction_tool, text='Prediction Tool ->', style='nav_menu_button.TButton')
        self.advance_to_prediction_tool_buton.pack(side=tk.RIGHT)






################################################################################################################

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

        self.final_df = self.temp_df.loc[self.temp_df[self.corrected_dependent_variable].notna()].reset_index(drop=True).copy()

        # NULL VALUES
        if self.null_value_option_var.get() == "REMOVE null values":
            self.final_df = self.final_df.dropna()

        ############################################################

        # GET MODEL
        if self.hypertune_parameters_choice == "Yes":
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
        auc_canvas_widget.pack(fill=tk.Y, expand=True)

        features_canvas = FigureCanvasTkAgg(self.features_graph, master=self.feature_importance_display_frame)
        features_canvas_widget = features_canvas.get_tk_widget()
        features_canvas_widget.pack(fill=tk.Y, expand=True)





################################################################################################################

# SINGLE TRAINING SET MACHINE LEARNING


    def ML_single_fold(self):

        ############################################################

        # DATA LOADING AND MODEL FITTING #
        X = self.final_df[self.selected_independent_variables]
        y = self.final_df[self.corrected_dependent_variable]

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
        auc_fig = Figure(figsize=(7,7))
        features_fig = Figure(figsize=(8,7))

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
        auc_ax.legend(loc='lower right', fontsize=15)
        auc_ax.axis("square")

        ############################

        # FEATURE IMPORTANCES GRAPH #
        features_ax = features_fig.add_subplot(111)
        features_ax.barh(feature_importances.index, feature_importances)
        features_ax.set_xlabel("Feature Importance")
        features_ax.tick_params(axis='y', labelsize=18)

        features_fig.tight_layout()
        auc_fig.tight_layout()

        return auc_fig, features_fig



    def ML_x_fold(self):

        X = self.final_df[self.selected_independent_variables].values
        y = self.final_df[self.corrected_dependent_variable].values

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

        # PLOTTING GRAPHS #
        auc_fig = Figure(figsize=(7,7))
        features_fig = Figure(figsize=(8,7))

        auc_ax = auc_fig.add_subplot(111)
        auc_ax.plot([0, 1], [0, 1], "k--")

        auc_ax.plot(mean_fpr, mean_tpr, color="b", label=r"Mean ROC (AUC = %0.2f $\pm$ %0.2f)" % (mean_auc, std_auc), lw=2, alpha=0.8)

        std_tpr = np.std(tprs, axis=0)
        tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
        tprs_lower = np.maximum(mean_tpr - std_tpr, 0)

        auc_ax.fill_between(mean_fpr, tprs_lower, tprs_upper, color="grey", alpha=0.2, label=r"$\pm$ 1 std. dev.")
        auc_ax.set(xlim=[0.00, 1.00], ylim=[0.0, 1.0], xlabel="False Positive Rate", ylabel="True Positive Rate", title="")
        auc_ax.legend(loc='lower right', fontsize=15)
        auc_ax.axis("square")

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
        features_ax.tick_params(axis='y', labelsize=18)

        features_fig.tight_layout()
        auc_fig.tight_layout()

        return auc_fig, features_fig




    def ML_tune(self):

        X = self.final_df[self.selected_independent_variables].values
        y = self.final_df[self.corrected_dependent_variable].values

        if self.selected_model == 'Random Forest':
            model = RandomForestClassifier()
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [None, 10, 20, 30],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
        # elif self.selected_model == 'XGBoost':
        #     model = XGBClassifier()
        #     param_grid = {
        #         'n_estimators': [100, 200, 300],
        #         'max_depth': [3, 4, 5, 6],
        #         'learning_rate': [0.01, 0.1, 0.2],
        #         'subsample': [0.8, 0.9, 1.0],
        #         'min_child_weight': [1, 2, 3]
        #     }
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
        self.prediction_tool_inner_frame, self.prediction_tool_canvas = utils.create_scrollable_frame(self.prediction_tool_frame)


################################################################################################################

        self.prediction_tool_subframe_border = tk.Frame(self.prediction_tool_inner_frame, bg=color_dict["sub_frame_border"])
        self.prediction_tool_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=3, pady=3)

        self.prediction_tool_subframe = tk.Frame(self.prediction_tool_subframe_border, bg=color_dict["sub_frame_bg"])
        self.prediction_tool_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=3, pady=3)

        self.prediction_tool_header_label = ttk.Label(self.prediction_tool_subframe, text="Predict Dependent Variable", style="sub_frame_header.TLabel")
        self.prediction_tool_header_label.pack(side=tk.TOP, padx=5, pady=5)

        separator = ttk.Separator(self.prediction_tool_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.prediction_frame = tk.Frame(self.prediction_tool_subframe)
        self.prediction_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # USER INPUT FRAME
        self.user_input_frame = tk.Frame(self.prediction_frame, bg=color_dict["sub_frame_bg"])
        self.user_input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.user_input_scrollable_frame, self.user_input_canvas = utils.create_scrollable_frame(self.user_input_frame, color=color_dict["sub_frame_bg"], scrollbar=True)

        self.user_input_scrollable_frame.bind("<Enter>",lambda e: utils.bind_mousewheel_to_frame(self.prediction_tool_inner_frame, self.prediction_tool_canvas, False))
        self.user_input_scrollable_frame.bind("<Enter>",lambda e: utils.bind_mousewheel_to_frame(self.user_input_scrollable_frame, self.user_input_canvas, True))
        self.user_input_scrollable_frame.bind("<Leave>",lambda e: utils.bind_mousewheel_to_frame(self.prediction_tool_inner_frame, self.prediction_tool_canvas, True))


################################################################################################################


        # PREDICTION RESULTS FRAME
        self.prediction_results_frame = tk.Frame(self.prediction_frame, bg=color_dict["sub_frame_bg"])
        self.prediction_results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.get_prediction_button = ttk.Button(self.prediction_results_frame, text="Get Prediction", command=self.get_prediction, style="large_button.TButton")
        self.get_prediction_button.pack(side=tk.TOP, anchor="center", fill=tk.BOTH, expand=True, padx=100, pady=100)

        self.prediction_outcome_frame = tk.Frame(self.prediction_results_frame, bg=color_dict["sub_frame_bg"])
        self.prediction_outcome_frame.pack(side=tk.TOP, anchor="center", fill=tk.BOTH, expand=True, padx=100, pady=100)

        self.prediction_outcome_outcome_label = ttk.Label(self.prediction_outcome_frame, text="", style="sub_frame_header.TLabel")
        self.prediction_outcome_outcome_label.pack(side=tk.TOP)

        self.prediction_outcome_percent_label = ttk.Label(self.prediction_outcome_frame, text="", style="sub_frame_header.TLabel")
        self.prediction_outcome_percent_label.pack(side=tk.TOP)


################################################################################################################

        # NAVIGATION MENU FRAME
        self.prediction_tool_menu_frame = tk.Frame(self.prediction_tool_frame, bg=color_dict["nav_banner_bg"])
        self.prediction_tool_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_results_frame_button = ttk.Button(self.prediction_tool_menu_frame, command=self.switch_to_results_frame, text='<- Back', style="nav_menu_button.TButton")
        self.return_to_results_frame_button.pack(side=tk.LEFT)

        self.prediction_tool_frame_dependent_label = ttk.Label(self.prediction_tool_menu_frame, text="", style="nav_menu_label.TLabel")
        self.prediction_tool_frame_dependent_label.pack(side=tk.LEFT, expand=True)


    def add_user_input_boxes_to_prediction_frame(self):

        utils.remove_frame_widgets(self.user_input_scrollable_frame)

        self.input_values_label = ttk.Label(self.user_input_scrollable_frame, text="Input Values for Each Variable", style="sub_frame_header.TLabel")
        self.input_values_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.user_input_scrollable_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        variables_frame = tk.Frame(self.user_input_scrollable_frame, bg=color_dict["sub_frame_bg"])
        variables_frame.pack(side=tk.TOP, padx=5, pady=5)

        self.prediction_input_dict = {}


        for variable in self.selected_independent_variables:

            if len(variable) > 20:
                variable_string = variable[0:19] + "..."
            else:
                variable_string = variable

            variable_frame = tk.Frame(variables_frame, bg=color_dict["sub_frame_bg"])
            variable_frame.pack(side=tk.TOP, fill=tk.X, pady=5, padx=20)

            input_entry = tk.Entry(variable_frame, font=styles.entrybox_large_font, width=10)
            input_entry.pack(side=tk.LEFT)

            variable_label = ttk.Label(variable_frame, text=variable_string, style="sub_frame_sub_header.TLabel")
            variable_label.pack(side=tk.LEFT)

            separator = ttk.Separator(variables_frame, orient="horizontal", style="Separator.TSeparator")
            separator.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

            input_entry.bind("<KeyRelease>", lambda event, var=variable: self.on_key_release_prediction(event, var))

    def on_key_release_prediction(self, event, variable):
        self.prediction_input_dict[variable] = event.widget.get()


    def get_prediction(self):

        X = self.final_df[self.selected_independent_variables].values
        y = self.final_df[self.corrected_dependent_variable].values

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



################################################################################################################
################################################################################################################
################################################################################################################

    def switch_to_dependent_variable_frame(self):

        self.settings_frame.pack_forget()
        self.variable_handling_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.results_frame.pack_forget()
        self.prediction_tool_frame.pack_forget()
        self.dependent_variable_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)


        utils.bind_mousewheel_to_frame(self.dependent_variable_inner_frame, self.dependent_variable_canvas, True)
        self.dependent_var_search_entry.focus_set()


    def switch_to_independent_variables_frame(self):
        if self.selected_dependent_variable == None:
            return


        self.settings_frame.pack_forget()
        self.variable_handling_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.prediction_tool_frame.pack_forget()
        self.indedependent_variables_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        

        self.dependent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.independent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.variable_handling_menu_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.model_settings_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.results_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.prediction_tool_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")

        utils.bind_mousewheel_to_frame(self.independent_variables_inner_frame, self.independent_variables_canvas, True)

        self.independent_var_search_entry.focus_set()
        self.visualize_content_frame.update_idletasks()






    def switch_to_variable_handling_frame(self):


        if not self.selected_model:
            utils.show_message('error message', "CHOOSE A MACHINE LEARNING MODEL")
            return

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
        self.variable_handling_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)


        utils.bind_mousewheel_to_frame(self.variable_handling_inner_frame, self.variable_handling_canvas, True)
        self.visualize_content_frame.update_idletasks()


    def switch_to_settings_frame(self):
        self.initialize_results_frame = True

        try:
            self.apply_variable_handling()
        except:
            return

        self.variable_handling_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.prediction_tool_frame.pack_forget()
        self.settings_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        utils.bind_mousewheel_to_frame(self.settings_inner_frame, self.settings_canvas, True)
        self.visualize_content_frame.update_idletasks()
        


    def switch_to_results_frame(self):

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
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        self.prediction_outcome_percent_label.configure(text="")
        self.prediction_outcome_outcome_label.configure(text=f"Chance of {self.selected_dependent_variable}")

        utils.bind_mousewheel_to_frame(self.results_inner_frame, self.results_canvas, True)
        self.visualize_content_frame.update_idletasks()

    def switch_to_prediction_tool(self):

        self.initialize_results_frame = False

        self.add_user_input_boxes_to_prediction_frame()

        self.settings_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.variable_handling_frame.pack_forget()
        self.results_frame.pack_forget()
        self.prediction_tool_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        utils.bind_mousewheel_to_frame(self.user_input_frame, self.user_input_canvas, True)

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













