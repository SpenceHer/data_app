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


 


    style.configure("comparison_table_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36))
    comparison_table_button = ttk.Button(sub_button_frame, text="Comparison Table", style="comparison_table_button.TButton")
    comparison_table_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    comparison_table_button.config(command=lambda: ComparisonTableClass(visualize_content_frame, df, style))
 
    style.configure("regression_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36))
    regression_button = ttk.Button(sub_button_frame, text="Regression", style="regression_button.TButton")
    regression_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    regression_button.config(command=lambda: RegressionAnalysisClass(visualize_content_frame, df, style))
 
    style.configure("create_plot_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36))
    create_plot_button = ttk.Button(sub_button_frame, text="Create Plot", style="create_plot_button.TButton")
    create_plot_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    create_plot_button.config(command=lambda: CreatePlotClass(visualize_content_frame, df, style))
 
    style.configure("machine_learning_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36))
    machine_learning_button = ttk.Button(sub_button_frame, text="Machine Learning", style="machine_learning_button.TButton")
    machine_learning_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    machine_learning_button.config(command=lambda: MachineLearningClass(visualize_content_frame, df, style))
 

    tab_dict = data_manager.get_tab_dict()
    try:
        if tab_dict:
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




















################################################################################################################################################################################################
################################################################################################################################################################################################
################################################################################################################################################################################################



################################################
################################################
 
        # CREATE COMPARISON TABLE #
 
################################################
################################################
 
class ComparisonTableClass:
    def __init__(self, visualize_content_frame, df, style):
        self.df = data_manager.get_dataframe()
        self.visualize_content_frame = visualize_content_frame

        self.style = style

        self.style.configure("comparison_table_button.TButton", background="white")
        self.style.configure("regression_button.TButton", background="gray")
        self.style.configure("create_plot_button.TButton", background="gray")
        self.style.configure("machine_learning_button.TButton", background="gray")

        data_manager.add_tab_to_dict("current_visualize_tab", "comparison_table")


        self.selected_dependent_variable = ""
        self.selected_independent_variables = []
        self.selected_percent_type = ""
        self.selected_data = ""
        


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



    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################

    def create_dependent_variable_frame(self):


        self.dependent_variable_options_frame = tk.Frame(self.dependent_variable_frame, bg='beige')
        self.dependent_variable_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.dependent_variable_menu_frame = tk.Frame(self.dependent_variable_frame, bg='lightgray')
        self.dependent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.advance_to_independent_variables_button = tk.Button(self.dependent_variable_menu_frame, text="Next", command=self.switch_to_independent_variables_frame, font=("Arial", 36))
        self.advance_to_independent_variables_button.pack(side=tk.RIGHT)

        self.dependent_frame_dependent_label = tk.Label(self.dependent_variable_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.dependent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)










        self.dependent_column_choice_frame = tk.Frame(self.dependent_variable_options_frame, bg='beige')
        self.dependent_column_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.choose_dependent_variable_label = tk.Label(self.dependent_column_choice_frame, text="Choose your DEPENDENT variable", font=("Arial", 36))
        self.choose_dependent_variable_label.pack(side=tk.TOP)


        self.dependent_search_var = tk.StringVar()
        self.dependent_search_var.trace("w", self.update_dependent_variable_listbox)
        self.dependent_var_search_entry = tk.Entry(self.dependent_column_choice_frame, textvariable=self.dependent_search_var, font=("Arial", 24))
        self.dependent_var_search_entry.pack(side=tk.TOP, pady=10)

        

        self.dependent_variable_listbox = tk.Listbox(self.dependent_column_choice_frame, selectmode=tk.SINGLE, font=("Arial", 24))
        self.dependent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)


        for column in sorted(self.df.columns, key=str.lower):
            self.dependent_variable_listbox.insert(tk.END, column)


        self.dependent_variable_listbox.bind("<<ListboxSelect>>", self.on_dependent_variable_listbox_select)


        self.dependent_variable_listbox.selection_set(0)
        self.dependent_frame_dependent_label.config(text="")


        self.dependent_variable_listbox.update_idletasks()


    def on_dependent_variable_listbox_select(self, event):
        if self.dependent_variable_listbox.curselection():
            self.selected_dependent_variable = self.dependent_variable_listbox.get(self.dependent_variable_listbox.curselection()[0])
            self.dependent_frame_dependent_label.config(text=f"Dependent Variable: {self.selected_dependent_variable}")
        else:
            self.dependent_frame_dependent_label.config(text="")




    def update_dependent_variable_listbox(self, *args):
        search_term = self.dependent_search_var.get().lower()
        self.dependent_variable_listbox.delete(0, tk.END)
        for column in self.df.columns:
            if search_term in column.lower():
                self.dependent_variable_listbox.insert(tk.END, column)


















    def create_independent_variables_frame(self):


        self.independent_variable_options_frame = tk.Frame(self.indedependent_variables_frame, bg='beige')
        self.independent_variable_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.independent_variable_menu_frame = tk.Frame(self.indedependent_variables_frame, bg='lightgray')
        self.independent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)


        self.return_to_dependent_variable_frame_button = tk.Button(self.independent_variable_menu_frame, command=self.switch_to_dependent_variable_frame, text='Back', font=("Arial", 36))
        self.return_to_dependent_variable_frame_button.pack(side=tk.LEFT)


        self.advance_to_variable_handling_frame_button = tk.Button(self.independent_variable_menu_frame, command=self.switch_to_variable_handling_frame, text="Next", font=("Arial", 36))
        self.advance_to_variable_handling_frame_button.pack(side=tk.RIGHT)


        self.independent_frame_dependent_label = tk.Label(self.independent_variable_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.independent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)



        self.choose_independent_variables_label = tk.Label(self.independent_variable_options_frame, text="Choose your INDEPENDENT variables", font=("Arial", 36))
        self.choose_independent_variables_label.pack(side=tk.TOP)


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



        self.transfer_buttons_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='beige')
        self.transfer_buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        self.transfer_right_button = tk.Button(self.transfer_buttons_frame, text=">>>", command=self.transfer_right, font=("Arial", 60))
        self.transfer_right_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)


        self.transfer_left_button = tk.Button(self.transfer_buttons_frame, text="<<<", command=self.transfer_left, font=("Arial", 60))
        self.transfer_left_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)



        self.selected_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='beige')
        self.selected_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        self.selected_independent_variables_label = tk.Label(self.selected_independent_variables_frame, text="Selected Variables", font=("Arial", 24))
        self.selected_independent_variables_label.pack(side=tk.TOP, pady=10)




        self.selected_independent_variable_listbox = tk.Listbox(self.selected_independent_variables_frame, selectmode=tk.MULTIPLE, font=("Arial", 24))
        self.selected_independent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)





        self.table_options_frame = tk.Frame(self.independent_variable_options_frame, bg='beige')
        self.table_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.percentage_type_selection_frame = tk.Frame(self.table_options_frame, bg='beige')
        self.percentage_type_selection_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        def on_percentage_radio_button_selected():
            self.selected_percent_type = self.percentage_type_radio_var.get()

        self.percentage_type_radio_var = tk.IntVar(value=2)
        self.selected_percent_type = self.percentage_type_radio_var.get()

        self.row_percentage_radiobutton = tk.Radiobutton(self.percentage_type_selection_frame, text="Row Percentages", variable=self.percentage_type_radio_var, value=1, command=on_percentage_radio_button_selected, indicator=0, font=("Arial", 40))
        self.row_percentage_radiobutton.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.column_percentage_radiobutton = tk.Radiobutton(self.percentage_type_selection_frame, text="Column Percentages", variable=self.percentage_type_radio_var, value=2, command=on_percentage_radio_button_selected, indicator=0, font=("Arial", 40))
        self.column_percentage_radiobutton.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)




        self.data_choice_frame = tk.Frame(self.table_options_frame, bg='beige')
        self.data_choice_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        def on_data_choice_radio_button_selected():
            self.selected_data = self.data_choice_radio_var.get()

        self.data_choice_radio_var = tk.IntVar(value=1)
        self.selected_data = self.data_choice_radio_var.get()

        self.independent_data_radiobutton = tk.Radiobutton(self.data_choice_frame, text="All Data", variable=self.data_choice_radio_var, value=1, command=on_data_choice_radio_button_selected, indicator=0, font=("Arial", 40))
        self.independent_data_radiobutton.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.dependent_data_radiobutton = tk.Radiobutton(self.data_choice_frame, text="Only Data-Complete Subjects", variable=self.data_choice_radio_var, value=2, command=on_data_choice_radio_button_selected, indicator=0, font=("Arial", 40))
        self.dependent_data_radiobutton.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)




        self.indedependent_variables_frame.update_idletasks()



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


        for index in reversed(selections):
            self.available_independent_variable_listbox.delete(index)


    def transfer_left(self):
        selections = self.selected_independent_variable_listbox.curselection()
        selected_items = [self.selected_independent_variable_listbox.get(index) for index in selections]


        for item in selected_items:
            self.available_independent_variable_listbox.insert(tk.END, item)
            self.selected_independent_variables.remove(item)


        for index in reversed(selections):
            self.selected_independent_variable_listbox.delete(index)


    def create_variable_handling_frame(self):


        self.variable_handling_label_frame = tk.Frame(self.variable_handling_frame, bg='purple')
        self.variable_handling_label_frame.pack(side=tk.TOP)


        self.variable_handling_label = tk.Label(self.variable_handling_label_frame, text="Choose your variable types", font=("Arial", 36))
        self.variable_handling_label.pack(side=tk.TOP)


        self.variable_handling_options_frame = tk.Frame(self.variable_handling_frame, bg='beige')
        self.variable_handling_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        def on_mousewheel(event):
            self.condition_canvas.yview_scroll(-1 * (event.delta // 120), "units")

        self.condition_canvas = tk.Canvas(self.variable_handling_options_frame)
        self.scrollbar = ttk.Scrollbar(self.variable_handling_options_frame, orient="vertical", command=self.condition_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.condition_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.condition_canvas.configure(
                scrollregion=self.condition_canvas.bbox("all")
            )
        )

        self.condition_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.condition_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.condition_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel event to the canvas
        self.condition_canvas.bind("<MouseWheel>", on_mousewheel)



        self.variable_handling_menu_frame = tk.Frame(self.variable_handling_frame, bg='lightgray')
        self.variable_handling_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)


        self.return_to_independent_variable_frame_button = tk.Button(self.variable_handling_menu_frame, command=self.switch_to_independent_variables_frame, text='Back', font=("Arial", 36))
        self.return_to_independent_variable_frame_button.pack(side=tk.LEFT)


        self.view_results_button = tk.Button(self.variable_handling_menu_frame, command=self.switch_to_results_frame, text="View Results", font=("Arial", 36))
        self.view_results_button.pack(side=tk.RIGHT)


        self.variable_handling_frame_dependent_label = tk.Label(self.variable_handling_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.variable_handling_frame_dependent_label.pack(side=tk.RIGHT, expand=True)



    def create_results_frame(self):


        self.results_display_frame = tk.Frame(self.results_frame, bg='beige')
        self.results_display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.results_menu_frame = tk.Frame(self.results_frame, bg='lightgray')
        self.results_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)


        self.return_to_independent_variable_frame_button = tk.Button(self.results_menu_frame, command=self.switch_to_independent_variables_frame, text='Back', font=("Arial", 36))
        self.return_to_independent_variable_frame_button.pack(side=tk.LEFT)


        self.results_frame_dependent_label = tk.Label(self.results_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.results_frame_dependent_label.pack(side=tk.RIGHT, expand=True)


    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################

    def switch_to_dependent_variable_frame(self):


        self.variable_handling_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack(fill=tk.BOTH, expand=True)

        self.dependent_var_search_entry.focus_set()

        self.dependent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")


    def switch_to_independent_variables_frame(self):
        if self.selected_dependent_variable == "":
            return
   
        self.variable_handling_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.indedependent_variables_frame.pack(fill=tk.BOTH, expand=True)

        self.independent_var_search_entry.focus_set()

        self.independent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.available_independent_variable_listbox.update_idletasks()


    def switch_to_variable_handling_frame(self):

        if (self.selected_percent_type not in [1,2]) | (self.selected_data not in [1,2]) | (len(self.selected_independent_variables) < 1):
            return

        else:
            self.handle_variables()


    def switch_to_results_frame(self):
        self.create_comparison_table()
        # self.display_comparison_table()

        self.indedependent_variables_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.variable_handling_frame.pack_forget()
        self.results_frame.pack(fill=tk.BOTH, expand=True)


        self.results_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")


    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################

    def handle_variables(self):
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.variable_handling_frame.pack(fill=tk.BOTH, expand=True)

        self.variable_handling_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")

        utils.forget_frame_widgets(self.scrollable_frame)



        self.unique_values = list(self.df[self.selected_independent_variables].columns)
        self.selected_options = {}
        self.variable_type_radio_var = {}

        for value in self.unique_values:

            options_frame = tk.Frame(self.scrollable_frame)
            options_frame.pack(side=tk.TOP)

            value_label = tk.Label(options_frame, text=value, font=("Arial", 36))
            value_label.pack(side=tk.LEFT)

            var = tk.StringVar(value="Continuous")  # Set default value to "Continuous"
            self.variable_type_radio_var[value] = var

            radio1 = tk.Radiobutton(options_frame, text="Continuous", variable=var, value="Continuous", indicator=0, font=("Arial", 36))
            radio1.pack(side=tk.LEFT)

            radio2 = tk.Radiobutton(options_frame, text="Categorical", variable=var, value="Categorical", indicator=0, font=("Arial", 36))
            radio2.pack(side=tk.LEFT)


    def apply_comparison_table_variable_selection(self):
        self.selected_options.clear()
        for value, var in self.variable_type_radio_var.items():
            option = var.get()
            self.selected_options[value] = option




    def create_comparison_table(self):
        self.apply_comparison_table_variable_selection()
        utils.remove_frame_widgets(self.results_display_frame)

    
        if self.selected_data == 1:
            self.create_independent_table()
        
        if self.selected_data == 2:
            self.create_dependent_table()


    def create_independent_table(self):

        self.table_df = self.df[self.selected_independent_variables + [self.selected_dependent_variable]].copy()
        self.table_df = self.table_df.dropna(subset=self.selected_dependent_variable)

        self.unique_dependent_variable_values = sorted(self.table_df[self.selected_dependent_variable].unique())
        self.summary_table = []
        for independent_variable, option in self.selected_options.items():
            if option == 'Continuous':
                self.clean_df = self.table_df[[independent_variable, self.selected_dependent_variable]].dropna()

                try:
                    self.clean_df[independent_variable] = self.clean_df[independent_variable].astype(float)

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
                    pass

            elif option == 'Categorical':
                self.clean_df = self.table_df[[independent_variable, self.selected_dependent_variable]].dropna()
                # Independent variable is categorical
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

                    if self.selected_percent_type == 1:

                        for value in row:
                            new_row.append(f"{value} ({int(round(value/row_sum*100,0))}%)")

                    if self.selected_percent_type == 2:

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




    def create_dependent_table(self):
        self.table_df = self.df[self.selected_independent_variables + [self.selected_dependent_variable]].copy()
        self.clean_df = self.table_df.dropna()

        self.unique_dependent_variable_values = sorted(self.clean_df[self.selected_dependent_variable].unique())
        self.summary_table = []
        for independent_variable, option in self.selected_options.items():
            if option == 'Continuous':

                try:
                    self.clean_df[independent_variable] = self.clean_df[independent_variable].astype(float)

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
                    pass

            elif option == 'Categorical':

                # Independent variable is categorical
                observed = pd.crosstab(self.clean_df[independent_variable], self.clean_df[self.selected_dependent_variable])

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
                    new_row = [index]
                    row_sum = row.sum()
                    column_sums = observed.sum(axis=0)

                    if self.selected_percent_type == 1:

                        for value in row:
                            new_row.append(f"{value} ({int(round(value/row_sum*100,0))}%)")

                    if self.selected_percent_type == 2:

                        for value, column_sum in zip(row, column_sums):
                            new_row.append(f"{value} ({int(round(value / column_sum * 100, 0))}%)")

                    new_row.append(np.nan)

                    if len(self.unique_dependent_variable_values) == 2:
                        new_row.append(np.nan)


                    self.summary_table.append(new_row)
                self.summary_table.append([np.nan] * len(row1))



        columns = ['Characteristic']
        for value in self.unique_dependent_variable_values:
            count_of_value = len(self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == value])
            columns.append(f"{value} (N = {count_of_value})")
            
        columns.append('p-value')
        if len(self.unique_dependent_variable_values) == 2:
            columns.append("Odds ratio")

        self.summary_df = pd.DataFrame(self.summary_table, columns=columns)


        utils.create_table(self.results_display_frame, self.summary_df)

        save_summary_button = ttk.Button(self.results_display_frame, text="Save Table", command=lambda: file_handling.save_file(self.summary_df))
        save_summary_button.pack()


















################################################################################################################################################################################################
################################################################################################################################################################################################
################################################################################################################################################################################################




################################################
################################################
 
        # MULTIVARIABLE REGRESSION #
 
################################################
################################################

class RegressionAnalysisClass:
    def __init__(self, visualize_content_frame, df, style):
        self.df = data_manager.get_dataframe()
        self.visualize_content_frame = visualize_content_frame

        self.style = style

        self.style.configure("comparison_table_button.TButton", background="gray")
        self.style.configure("regression_button.TButton", background="white")
        self.style.configure("create_plot_button.TButton", background="gray")
        self.style.configure("machine_learning_button.TButton", background="gray")

        data_manager.add_tab_to_dict("current_visualize_tab", "regression")

        self.selected_dependent_variable = ""
        self.selected_independent_variables = []
        self.selected_analysis = ""
        self.selected_dependent_variable_value = ""

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






    def create_dependent_variable_frame(self):


        self.dependent_variable_options_frame = tk.Frame(self.dependent_variable_frame, bg='beige')
        self.dependent_variable_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.dependent_variable_menu_frame = tk.Frame(self.dependent_variable_frame, bg='lightgray')
        self.dependent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)


        self.advance_to_independent_variables_button = tk.Button(self.dependent_variable_menu_frame, text="Next", command=self.switch_to_independent_variables_frame, font=("Arial", 36))
        self.advance_to_independent_variables_button.pack(side=tk.RIGHT)

        self.dependent_frame_dependent_label = tk.Label(self.dependent_variable_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.dependent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)










        self.dependent_column_choice_frame = tk.Frame(self.dependent_variable_options_frame, bg='beige')
        self.dependent_column_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.choose_dependent_variable_label = tk.Label(self.dependent_column_choice_frame, text="Choose your DEPENDENT variable", font=("Arial", 36))
        self.choose_dependent_variable_label.pack(side=tk.TOP)


        self.dependent_search_var = tk.StringVar()
        self.dependent_search_var.trace("w", self.update_dependent_variable_listbox)
        self.dependent_var_search_entry = tk.Entry(self.dependent_column_choice_frame, textvariable=self.dependent_search_var, font=("Arial", 24))
        self.dependent_var_search_entry.pack(side=tk.TOP, pady=10)



        self.dependent_variable_listbox = tk.Listbox(self.dependent_column_choice_frame, selectmode=tk.SINGLE, font=("Arial", 24))
        self.dependent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)


        for column in sorted(self.df.columns, key=str.lower):
            self.dependent_variable_listbox.insert(tk.END, column)


        self.dependent_variable_listbox.bind("<<ListboxSelect>>", self.on_dependent_variable_listbox_select)


        self.dependent_variable_listbox.selection_set(0)
        self.dependent_frame_dependent_label.config(text="")


        self.dependent_variable_listbox.update_idletasks()


    def on_dependent_variable_listbox_select(self, event):
        if self.dependent_variable_listbox.curselection():
            self.selected_dependent_variable = self.dependent_variable_listbox.get(self.dependent_variable_listbox.curselection()[0])
            self.dependent_frame_dependent_label.config(text=f"Dependent Variable: {self.selected_dependent_variable}")

        else:
            self.dependent_frame_dependent_label.config(text="")




    def update_dependent_variable_listbox(self, *args):
        search_term = self.dependent_search_var.get().lower()
        self.dependent_variable_listbox.delete(0, tk.END)
        for column in self.df.columns:
            if search_term in column.lower():
                self.dependent_variable_listbox.insert(tk.END, column)


















    def create_independent_variables_frame(self):


        self.independent_variable_options_frame = tk.Frame(self.indedependent_variables_frame, bg='beige')
        self.independent_variable_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.independent_variable_menu_frame = tk.Frame(self.indedependent_variables_frame, bg='lightgray')
        self.independent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)


        self.return_to_dependent_variable_frame_button = tk.Button(self.independent_variable_menu_frame, command=self.switch_to_dependent_variable_frame, text='Back', font=("Arial", 36))
        self.return_to_dependent_variable_frame_button.pack(side=tk.LEFT)


        self.advance_to_variable_handling_frame_button = tk.Button(self.independent_variable_menu_frame, command=self.switch_to_variable_handling_frame, text="Next", font=("Arial", 36))
        self.advance_to_variable_handling_frame_button.pack(side=tk.RIGHT)


        self.independent_frame_dependent_label = tk.Label(self.independent_variable_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.independent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)










        self.choose_independent_variables_label = tk.Label(self.independent_variable_options_frame, text="Choose your INDEPENDENT variables", font=("Arial", 36))
        self.choose_independent_variables_label.pack(side=tk.TOP)


        self.indedependent_variables_selection_frame = tk.Frame(self.independent_variable_options_frame, bg='beige')
        self.indedependent_variables_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)












        self.available_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='beige')
        self.available_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        self.available_independent_search_var = tk.StringVar()
        self.available_independent_search_var.trace("w", self.update_available_independent_variable_listbox)
        self.independent_var_search_entry = tk.Entry(self.available_independent_variables_frame, textvariable=self.available_independent_search_var, font=("Arial", 24))
        self.independent_var_search_entry.pack(side=tk.TOP, pady=10)


        self.available_independent_variable_listbox = tk.Listbox(self.available_independent_variables_frame, selectmode=tk.MULTIPLE, font=("Arial", 24))
        self.available_independent_variable_listbox.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)


        for column in sorted(self.df.columns, key=str.lower):
            self.available_independent_variable_listbox.insert(tk.END, column)


        self.available_independent_variable_listbox.update_idletasks()






        self.transfer_buttons_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='beige')
        self.transfer_buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        self.transfer_right_button = tk.Button(self.transfer_buttons_frame, text=">>>", command=self.transfer_right, font=("Arial", 60))
        self.transfer_right_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)


        self.transfer_left_button = tk.Button(self.transfer_buttons_frame, text="<<<", command=self.transfer_left, font=("Arial", 60))
        self.transfer_left_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)








        self.selected_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='beige')
        self.selected_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        self.selected_independent_variables_label = tk.Label(self.selected_independent_variables_frame, text="Selected Variables", font=("Arial", 24))
        self.selected_independent_variables_label.pack(side=tk.TOP, pady=10)




        self.selected_independent_variable_listbox = tk.Listbox(self.selected_independent_variables_frame, selectmode=tk.MULTIPLE, font=("Arial", 24))
        self.selected_independent_variable_listbox.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)


        self.available_independent_variable_listbox.update_idletasks()



        self.regression_type_selection_frame = tk.Frame(self.independent_variable_options_frame, bg='beige')
        self.regression_type_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)




        def on_radio_button_selected():
            self.selected_analysis = self.regression_type_radio_var.get()


        self.regression_type_radio_var = tk.IntVar(value=1)
        self.selected_analysis = self.regression_type_radio_var.get()


        self.logistic_regression_radiobutton = tk.Radiobutton(self.regression_type_selection_frame, text="Logistic Regression", variable=self.regression_type_radio_var, value=1, command=on_radio_button_selected, indicator = 0,font=("Arial", 40))
        self.logistic_regression_radiobutton.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)


        self.linear_regression_radiobutton = tk.Radiobutton(self.regression_type_selection_frame, text="Linear Regression", variable=self.regression_type_radio_var, value=2, command=on_radio_button_selected, indicator = 0, font=("Arial", 40))
        self.linear_regression_radiobutton.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)




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


        for index in reversed(selections):
            self.available_independent_variable_listbox.delete(index)


    def transfer_left(self):
        selections = self.selected_independent_variable_listbox.curselection()
        selected_items = [self.selected_independent_variable_listbox.get(index) for index in selections]


        for item in selected_items:
            self.available_independent_variable_listbox.insert(tk.END, item)
            self.selected_independent_variables.remove(item)


        for index in reversed(selections):
            self.selected_independent_variable_listbox.delete(index)






    def create_variable_handling_frame(self):


        self.variable_handling_label_frame = tk.Frame(self.variable_handling_frame, bg='purple')
        self.variable_handling_label_frame.pack(side=tk.TOP)


        self.variable_handling_label = tk.Label(self.variable_handling_label_frame, text="Variable Handling", font=("Arial", 36))
        self.variable_handling_label.pack(side=tk.TOP)

        self.variable_handling_options_frame = tk.Frame(self.variable_handling_frame, bg='beige')
        self.variable_handling_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.variable_handling_menu_frame = tk.Frame(self.variable_handling_frame, bg='lightgray')
        self.variable_handling_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_independent_variable_frame_button = tk.Button(self.variable_handling_menu_frame, command=self.switch_to_independent_variables_frame, text='Back', font=("Arial", 36))
        self.return_to_independent_variable_frame_button.pack(side=tk.LEFT)

        self.view_results_button = tk.Button(self.variable_handling_menu_frame, command=self.switch_to_results_frame, text="View Results", font=("Arial", 36))
        self.view_results_button.pack(side=tk.RIGHT)

        self.variable_handling_frame_dependent_label = tk.Label(self.variable_handling_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.variable_handling_frame_dependent_label.pack(side=tk.RIGHT, expand=True)










    def create_results_frame(self):


        self.results_display_frame = tk.Frame(self.results_frame, bg='beige')
        self.results_display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.results_menu_frame = tk.Frame(self.results_frame, bg='lightgray')
        self.results_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)


        self.return_to_independent_variable_frame_button = tk.Button(self.results_menu_frame, command=self.switch_to_independent_variables_frame, text='Back', font=("Arial", 36))
        self.return_to_independent_variable_frame_button.pack(side=tk.LEFT)


        self.results_frame_dependent_label = tk.Label(self.results_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.results_frame_dependent_label.pack(side=tk.RIGHT, expand=True)





    def switch_to_dependent_variable_frame(self):


        self.variable_handling_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack(fill=tk.BOTH, expand=True)

        self.dependent_var_search_entry.focus_set()

        self.dependent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")








    def switch_to_independent_variables_frame(self):
        if self.selected_dependent_variable == "":
            return

        self.variable_handling_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.indedependent_variables_frame.pack(fill=tk.BOTH, expand=True)

        self.independent_var_search_entry.focus_set()

        self.independent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")



    def switch_to_variable_handling_frame(self):

        if self.selected_analysis not in [1,2]:
            return
        
        if self.selected_analysis == 1:
            if len(self.df[self.selected_dependent_variable].dropna().unique()) != 2:
                
                utils.show_message('dependent variable error', 'Dependent Variable not binary for logistic regression')
                return
            self.handle_variables_logistic_regression()

        if self.selected_analysis == 2:
            print('eeeeeee')
            try:
                self.df[self.selected_dependent_variable] = self.df[self.selected_dependent_variable].dropna().astype(float)
            except:
                utils.show_message('dependent variable error', 'Dependent Variable not numeric for linear regression')
                return
            self.handle_variables_linear_regression()


    def handle_variables_linear_regression(self):
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.variable_handling_frame.pack(fill=tk.BOTH, expand=True)


        self.variable_handling_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.variable_handling_label.configure(text="Linear Regression Variable Settings")

        utils.forget_frame_widgets(self.variable_handling_options_frame)


        self.clean_df = self.df[self.selected_independent_variables + [self.selected_dependent_variable]].copy()
        self.clean_df.dropna(inplace=True)

        self.unique_values = list(self.clean_df[self.selected_independent_variables].columns)
        self.non_numeric_columns = []

        self.input_var = {}
        self.selected_options = {}
        self.selected_column_map = {}

        for column in self.unique_values:
            try:
                self.clean_df[column] = self.clean_df[column].astype(float)
            except:
                self.non_numeric_columns.append(column)

        for variable in self.non_numeric_columns:
            options_frame = tk.Frame(self.variable_handling_options_frame)
            options_frame.pack(side=tk.TOP)

            variable_label = tk.Label(options_frame, text=variable)
            variable_label.pack(side=tk.TOP)

            for value in self.clean_df[variable].unique():
                self.selected_column_map[value] = variable
                value_frame = tk.Frame(options_frame)
                value_frame.pack(side=tk.TOP)

                value_label = tk.Label(value_frame, text=value)
                value_label.pack(side=tk.LEFT)

                input_var = tk.StringVar()
                self.input_var[value] = input_var

                input_combobox = ttk.Combobox(value_frame, textvariable=input_var, state="readonly")
                values = list(range(len(self.clean_df[variable].unique())))

                input_combobox['values'] = values
                input_combobox.current(0)  # Set default selection to the first item
                # input_combobox.bind("<<ComboboxSelected>>", lambda event, combobox=input_combobox: self.on_combobox_select(combobox, value))
                input_combobox.bind("<<ComboboxSelected>>", lambda event, combobox=input_combobox, value=value: self.on_combobox_select(combobox, value))
                input_combobox.pack(side=tk.LEFT)


    def apply_linear_regression_selection(self):
        for value, input_var in self.input_var.items():
            selected_value = (input_var.get())
            column_to_update = self.selected_column_map[value]
            self.clean_df.loc[self.clean_df[column_to_update] == value, column_to_update] = int(selected_value)
        for column in self.non_numeric_columns:
            self.clean_df[column] = self.clean_df[column].astype(float)






    def handle_variables_logistic_regression(self):
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.variable_handling_frame.pack(fill=tk.BOTH, expand=True)


        self.variable_handling_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.variable_handling_label.configure(text="Logistic Regression Variable Settings")

        utils.forget_frame_widgets(self.variable_handling_options_frame)


        self.clean_df = self.df[self.selected_independent_variables + [self.selected_dependent_variable]].copy()
        self.clean_df.dropna(inplace=True)


        self.dependent_variable_handling_frame = tk.Frame(self.variable_handling_options_frame, bg='beige')
        self.dependent_variable_handling_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.dependent_variable_handling_frame_label = tk.Label(self.dependent_variable_handling_frame, text='Choose Target Value', font=('Arial', 32))
        self.dependent_variable_handling_frame_label.pack(side=tk.TOP)

        def on_dependent_variable_value_selected():
            self.selected_dependent_variable_value = self.selected_dependent_variable_radio_value.get()


        self.selected_dependent_variable_radio_value = tk.IntVar()

        self.dependent_variable_unique_value_1 = tk.Radiobutton(self.dependent_variable_handling_frame, text=f"{self.clean_df[self.selected_dependent_variable].unique()[0]}", variable=self.selected_dependent_variable_radio_value, value=1, command=on_dependent_variable_value_selected, indicator=0, font=("Arial", 40))
        self.dependent_variable_unique_value_1.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.dependent_variable_unique_value_2 = tk.Radiobutton(self.dependent_variable_handling_frame, text=f"{self.clean_df[self.selected_dependent_variable].unique()[1]}", variable=self.selected_dependent_variable_radio_value, value=2, command=on_dependent_variable_value_selected, indicator=0, font=("Arial", 40))
        self.dependent_variable_unique_value_2.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)








    
        self.independent_variable_handling_frame = tk.Frame(self.variable_handling_options_frame, bg='beige')
        self.independent_variable_handling_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.independent_variable_handling_frame_label = tk.Label(self.independent_variable_handling_frame, text='Choose variable types', font=('Arial', 32))
        self.independent_variable_handling_frame_label.pack(side=tk.TOP)





        self.unique_values = list(self.clean_df[self.selected_independent_variables].columns)
        self.selected_options = {}
        self.reference_value_dict = {}


        self.variable_type_radio_var = {}
        self.input_var = {}


        for value in self.unique_values:


            options_frame = tk.Frame(self.independent_variable_handling_frame)
            options_frame.pack(side=tk.TOP)


            value_label = tk.Label(options_frame, text=value)
            value_label.pack(side=tk.LEFT)


            var = tk.StringVar(value="Continuous")  # Set default value to "Continuous"
            self.variable_type_radio_var[value] = var


            input_var = tk.StringVar()
            self.input_var[value] = input_var


            radio1 = tk.Radiobutton(options_frame, text="Continuous", variable=var, value="Continuous", indicator=0)
            radio1.pack(side=tk.LEFT, padx=5)

            radio3 = tk.Radiobutton(options_frame, text="Categorical", variable=var, value="Categorical", indicator=0)
            radio3.pack(side=tk.LEFT, padx=5)


            input_combobox = ttk.Combobox(options_frame, textvariable=input_var, state="readonly")
            values = [str(val) for val in self.clean_df[value].unique()]
            input_combobox['values'] = values
            input_combobox.current(0)  # Set default selection to the first item
            # input_combobox.bind("<<ComboboxSelected>>", lambda event, combobox=input_combobox: self.on_combobox_select(combobox, value))
            input_combobox.bind("<<ComboboxSelected>>", lambda event, combobox=input_combobox, value=value: self.on_combobox_select(combobox, value))


            input_combobox.pack(side=tk.LEFT)


            # Bind the state of the input_combobox to the selection of 'Categorical' radio button
            radio3.bind("<Button-1>", lambda event, combobox=input_combobox: combobox.configure(state="readonly"))
            radio1.bind("<Button-1>", lambda event, combobox=input_combobox: combobox.configure(state=tk.DISABLED))


    def on_combobox_select(self, combobox, value):
        selected_value = combobox.get()
        self.input_var[value].set(selected_value)


    def apply_logistic_regression_selection(self):
        if self.selected_dependent_variable_value == 1:
            self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == self.clean_df[self.selected_dependent_variable].unique()[0], self.selected_dependent_variable] = 1
            self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == self.clean_df[self.selected_dependent_variable].unique()[1], self.selected_dependent_variable] = 0

        if self.selected_dependent_variable_value == 2:
            self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == self.clean_df[self.selected_dependent_variable].unique()[0], self.selected_dependent_variable] = 0
            self.clean_df.loc[self.clean_df[self.selected_dependent_variable] == self.clean_df[self.selected_dependent_variable].unique()[1], self.selected_dependent_variable] = 1

        self.selected_options.clear()
        for value, var in self.variable_type_radio_var.items():
            option = var.get()
            self.selected_options[value] = option


            if option == 'Categorical':
                input_value = self.input_var[value].get()
                column_data_type = self.df[value].dtype
                if column_data_type == 'object':
                    self.reference_value_dict[value] = input_value  # Treat as string
                elif column_data_type == 'int64':
                    input_value = int(input_value)  # Convert to int
                    self.reference_value_dict[value] = input_value
                elif column_data_type == 'float64':
                    input_value = float(input_value)  # Convert to float
                    self.reference_value_dict[value] = input_value
        



    def switch_to_results_frame(self):
        self.run_analysis()

        self.indedependent_variables_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.variable_handling_frame.pack_forget()
        self.results_frame.pack(fill=tk.BOTH, expand=True)


        self.results_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")





    def run_analysis(self):
        utils.remove_frame_widgets(self.results_display_frame)


        if self.selected_analysis == 1:
            self.logistic_regression()
        elif self.selected_analysis == 2:
            self.linear_regression()

        

    def logistic_regression(self):
        self.apply_logistic_regression_selection()
        model_string = f"{self.selected_dependent_variable} ~ "
        self.clean_df[self.selected_dependent_variable] = self.clean_df[self.selected_dependent_variable].astype(int)

        for value, option in self.selected_options.items():
            if option == 'Continuous':
                model_string = model_string + f"{value} + "
            elif option == 'Categorical':
                if self.clean_df[value].dtype == 'object':
                    model_string = model_string + f"C({value}, Treatment('{self.reference_value_dict[value]}')) + "
                else:
                    model_string = model_string + f"C({value}, Treatment({self.reference_value_dict[value]})) + "

        model_string = model_string.rstrip(" +")
        print(model_string)
        model = smf.logit(model_string, data=self.clean_df)
        results = model.fit(method='bfgs', maxiter=1000)
   
        p_values = results.pvalues[1:]
        for i in range(len(p_values)):
            if p_values[i] < 0.0001:
                p_values[i] = "< 0.0001"
            else:
                p_values[i] = round(p_values[i], 4)
   


        # Print out the results
        coefs = pd.DataFrame({
            'coef': np.round(results.params.values[1:],3),
            'p_value': p_values,
            'odds ratio': np.round(np.exp(results.params.values[1:]),2),
            'CI_low': round(np.exp(results.conf_int()[0])[1:],2),
            'CI_high': round(np.exp(results.conf_int()[1])[1:],2)
        })
   
        coefs = coefs.reset_index().rename(columns={'index': 'Characteristic'})
        for i in range(len(coefs['Characteristic'])):
            variable_string = coefs['Characteristic'].iloc[i]
            if variable_string[0] == "C":
                column_string = re.search(r'C\((.*?),', variable_string).group(1)
                reference_value = re.search(r"\[T\.(.*?)\]", variable_string).group(1)
                new_value = column_string + f" ({reference_value})"
                coefs.loc[i, 'Characteristic'] = new_value
            if coefs.loc[i, 'CI_high'] > 50000:
                coefs.loc[i, 'CI_high'] = 'inf'
            if coefs.loc[i, 'CI_low'] < -50000:
                coefs.loc[i, 'CI_low'] = '-inf'


        utils.create_table(self.results_display_frame, coefs)


        summary_text = tk.Text(self.results_display_frame, height=20, width=120)
        summary_text.pack(side=tk.TOP)
        summary_text.insert(tk.END, str(results.summary()))


        save_summary_button = ttk.Button(self.results_display_frame, text="Save Table", command=lambda: file_handling.save_file(coefs))
        save_summary_button.pack()


    def linear_regression(self):
        self.apply_linear_regression_selection()

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

















################################################################################################################################################################################################
################################################################################################################################################################################################
################################################################################################################################################################################################



################################################
################################################
 
                # CREATE PLOT #
 
################################################
################################################



class CreatePlotClass():
 
    def __init__(self, visualize_content_frame, df, style):
        self.df = df
 
        self.style = style

        self.style.configure("comparison_table_button.TButton", background="gray")
        self.style.configure("regression_button.TButton", background="gray")
        self.style.configure("create_plot_button.TButton", background="white")
        self.style.configure("machine_learning_button.TButton", background="gray")

        data_manager.add_tab_to_dict("current_visualize_tab", "create_plot")

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

 
        self.choice_frame_label = tk.Label(self.choice_frame, text="COLUMN SELECTION", font=("Arial", 30, "bold"))
        self.choice_frame_label.pack(side=tk.TOP)

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










################################################################################################################################################################################################
################################################################################################################################################################################################
################################################################################################################################################################################################




################################################
################################################
 
        # MACHINE LEARNING #
 
################################################
################################################

class MachineLearningClass:
    def __init__(self, visualize_content_frame, df, style):
        self.df = data_manager.get_dataframe()
        self.visualize_content_frame = visualize_content_frame

        self.style = style

        self.style.configure("comparison_table_button.TButton", background="gray")
        self.style.configure("regression_button.TButton", background="gray")
        self.style.configure("create_plot_button.TButton", background="gray")
        self.style.configure("machine_learning_button.TButton", background="white")

        data_manager.add_tab_to_dict("current_visualize_tab", "machine_learning")

        self.selected_dependent_variable = ""
        self.selected_independent_variables = []
        self.selected_analysis = ""
        self.selected_dependent_variable_value = ""

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






    def create_dependent_variable_frame(self):


        self.dependent_variable_options_frame = tk.Frame(self.dependent_variable_frame, bg='beige')
        self.dependent_variable_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.dependent_variable_menu_frame = tk.Frame(self.dependent_variable_frame, bg='lightgray')
        self.dependent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)


        self.advance_to_independent_variables_button = tk.Button(self.dependent_variable_menu_frame, text="Next", command=self.switch_to_independent_variables_frame, font=("Arial", 36))
        self.advance_to_independent_variables_button.pack(side=tk.RIGHT)

        self.dependent_frame_dependent_label = tk.Label(self.dependent_variable_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.dependent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)










        self.dependent_column_choice_frame = tk.Frame(self.dependent_variable_options_frame, bg='beige')
        self.dependent_column_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.choose_dependent_variable_label = tk.Label(self.dependent_column_choice_frame, text="Choose your DEPENDENT variable", font=("Arial", 36))
        self.choose_dependent_variable_label.pack(side=tk.TOP)


        self.dependent_search_var = tk.StringVar()
        self.dependent_search_var.trace("w", self.update_dependent_variable_listbox)
        self.dependent_var_search_entry = tk.Entry(self.dependent_column_choice_frame, textvariable=self.dependent_search_var, font=("Arial", 24))
        self.dependent_var_search_entry.pack(side=tk.TOP, pady=10)



        self.dependent_variable_listbox = tk.Listbox(self.dependent_column_choice_frame, selectmode=tk.SINGLE, font=("Arial", 24))
        self.dependent_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)


        for column in sorted(self.df.columns, key=str.lower):
            self.dependent_variable_listbox.insert(tk.END, column)


        self.dependent_variable_listbox.bind("<<ListboxSelect>>", self.on_dependent_variable_listbox_select)


        self.dependent_variable_listbox.selection_set(0)
        self.dependent_frame_dependent_label.config(text="")


        self.dependent_variable_listbox.update_idletasks()


    def on_dependent_variable_listbox_select(self, event):
        if self.dependent_variable_listbox.curselection():
            self.selected_dependent_variable = self.dependent_variable_listbox.get(self.dependent_variable_listbox.curselection()[0])
            self.dependent_frame_dependent_label.config(text=f"Dependent Variable: {self.selected_dependent_variable}")

        else:
            self.dependent_frame_dependent_label.config(text="")




    def update_dependent_variable_listbox(self, *args):
        search_term = self.dependent_search_var.get().lower()
        self.dependent_variable_listbox.delete(0, tk.END)
        for column in self.df.columns:
            if search_term in column.lower():
                self.dependent_variable_listbox.insert(tk.END, column)


















    def create_independent_variables_frame(self):


        self.independent_variable_options_frame = tk.Frame(self.indedependent_variables_frame, bg='beige')
        self.independent_variable_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.independent_variable_menu_frame = tk.Frame(self.indedependent_variables_frame, bg='lightgray')
        self.independent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)


        self.return_to_dependent_variable_frame_button = tk.Button(self.independent_variable_menu_frame, command=self.switch_to_dependent_variable_frame, text='Back', font=("Arial", 36))
        self.return_to_dependent_variable_frame_button.pack(side=tk.LEFT)


        self.advance_to_variable_handling_frame_button = tk.Button(self.independent_variable_menu_frame, command=self.switch_to_variable_handling_frame, text="Next", font=("Arial", 36))
        self.advance_to_variable_handling_frame_button.pack(side=tk.RIGHT)


        self.independent_frame_dependent_label = tk.Label(self.independent_variable_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.independent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)










        self.choose_independent_variables_label = tk.Label(self.independent_variable_options_frame, text="Choose your INDEPENDENT variables", font=("Arial", 36))
        self.choose_independent_variables_label.pack(side=tk.TOP)


        self.indedependent_variables_selection_frame = tk.Frame(self.independent_variable_options_frame, bg='beige')
        self.indedependent_variables_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)












        self.available_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='beige')
        self.available_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        self.available_independent_search_var = tk.StringVar()
        self.available_independent_search_var.trace("w", self.update_available_independent_variable_listbox)
        self.independent_var_search_entry = tk.Entry(self.available_independent_variables_frame, textvariable=self.available_independent_search_var, font=("Arial", 24))
        self.independent_var_search_entry.pack(side=tk.TOP, pady=10)


        self.available_independent_variable_listbox = tk.Listbox(self.available_independent_variables_frame, selectmode=tk.MULTIPLE, font=("Arial", 24))
        self.available_independent_variable_listbox.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)


        for column in sorted(self.df.columns, key=str.lower):
            self.available_independent_variable_listbox.insert(tk.END, column)


        self.available_independent_variable_listbox.update_idletasks()






        self.transfer_buttons_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='beige')
        self.transfer_buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        self.transfer_right_button = tk.Button(self.transfer_buttons_frame, text=">>>", command=self.transfer_right, font=("Arial", 60))
        self.transfer_right_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)


        self.transfer_left_button = tk.Button(self.transfer_buttons_frame, text="<<<", command=self.transfer_left, font=("Arial", 60))
        self.transfer_left_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)








        self.selected_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='beige')
        self.selected_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        self.selected_independent_variables_label = tk.Label(self.selected_independent_variables_frame, text="Selected Variables", font=("Arial", 24))
        self.selected_independent_variables_label.pack(side=tk.TOP, pady=10)




        self.selected_independent_variable_listbox = tk.Listbox(self.selected_independent_variables_frame, selectmode=tk.MULTIPLE, font=("Arial", 24))
        self.selected_independent_variable_listbox.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)


        self.available_independent_variable_listbox.update_idletasks()



        self.regression_type_selection_frame = tk.Frame(self.independent_variable_options_frame, bg='beige')
        self.regression_type_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)




        def on_radio_button_selected():
            self.selected_analysis = self.regression_type_radio_var.get()


        self.regression_type_radio_var = tk.IntVar(value=1)
        self.selected_analysis = self.regression_type_radio_var.get()


        self.random_forest_radiobutton = tk.Radiobutton(self.regression_type_selection_frame, text="Random Forest", variable=self.regression_type_radio_var, value=1, command=on_radio_button_selected, indicator = 0,font=("Arial", 40))
        self.random_forest_radiobutton.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)


        self.xgboost_radiobutton = tk.Radiobutton(self.regression_type_selection_frame, text="XGBoost", variable=self.regression_type_radio_var, value=2, command=on_radio_button_selected, indicator = 0, font=("Arial", 40))
        self.xgboost_radiobutton.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)




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


        for index in reversed(selections):
            self.available_independent_variable_listbox.delete(index)


    def transfer_left(self):
        selections = self.selected_independent_variable_listbox.curselection()
        selected_items = [self.selected_independent_variable_listbox.get(index) for index in selections]


        for item in selected_items:
            self.available_independent_variable_listbox.insert(tk.END, item)
            self.selected_independent_variables.remove(item)


        for index in reversed(selections):
            self.selected_independent_variable_listbox.delete(index)






    def create_variable_handling_frame(self):


        self.variable_handling_label_frame = tk.Frame(self.variable_handling_frame, bg='purple')
        self.variable_handling_label_frame.pack(side=tk.TOP)


        self.variable_handling_label = tk.Label(self.variable_handling_label_frame, text="Variable Handling", font=("Arial", 36))
        self.variable_handling_label.pack(side=tk.TOP)

        self.variable_handling_options_frame = tk.Frame(self.variable_handling_frame, bg='beige')
        self.variable_handling_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.variable_handling_menu_frame = tk.Frame(self.variable_handling_frame, bg='lightgray')
        self.variable_handling_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_independent_variable_frame_button = tk.Button(self.variable_handling_menu_frame, command=self.switch_to_independent_variables_frame, text='Back', font=("Arial", 36))
        self.return_to_independent_variable_frame_button.pack(side=tk.LEFT)

        self.view_results_button = tk.Button(self.variable_handling_menu_frame, command=self.switch_to_results_frame, text="View Results", font=("Arial", 36))
        self.view_results_button.pack(side=tk.RIGHT)

        self.variable_handling_frame_dependent_label = tk.Label(self.variable_handling_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.variable_handling_frame_dependent_label.pack(side=tk.RIGHT, expand=True)










    def create_results_frame(self):


        self.results_display_frame = tk.Frame(self.results_frame, bg='beige')
        self.results_display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.results_menu_frame = tk.Frame(self.results_frame, bg='lightgray')
        self.results_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)


        self.return_to_independent_variable_frame_button = tk.Button(self.results_menu_frame, command=self.switch_to_independent_variables_frame, text='Back', font=("Arial", 36))
        self.return_to_independent_variable_frame_button.pack(side=tk.LEFT)


        self.results_frame_dependent_label = tk.Label(self.results_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.results_frame_dependent_label.pack(side=tk.RIGHT, expand=True)





    def switch_to_dependent_variable_frame(self):


        self.variable_handling_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack(fill=tk.BOTH, expand=True)

        self.dependent_var_search_entry.focus_set()

        self.dependent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")



    def switch_to_independent_variables_frame(self):
        if self.selected_dependent_variable == "":
            return

        self.variable_handling_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.indedependent_variables_frame.pack(fill=tk.BOTH, expand=True)

        self.independent_var_search_entry.focus_set()

        self.independent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")



    def switch_to_variable_handling_frame(self):

        if self.selected_analysis not in [1,2]:
            return
        
        else:
            
            try:
                self.df[self.selected_dependent_variable] = self.df[self.selected_dependent_variable].dropna().astype(float)
            except:
                utils.show_message('dependent variable error', 'Dependent Variable not numeric for linear regression')
                return
            self.handle_variables_machine_learning()


    def handle_variables_machine_learning(self):
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.variable_handling_frame.pack(fill=tk.BOTH, expand=True)


        self.variable_handling_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.variable_handling_label.configure(text="Linear Regression Variable Settings")

        utils.forget_frame_widgets(self.variable_handling_options_frame)


        self.clean_df = self.df[self.selected_independent_variables + [self.selected_dependent_variable]].copy()
        self.clean_df.dropna(inplace=True)

        self.unique_values = list(self.clean_df[self.selected_independent_variables].columns)
        self.non_numeric_columns = []

        self.input_var = {}
        self.selected_options = {}
        self.selected_column_map = {}

        for column in self.unique_values:
            try:
                self.clean_df[column] = self.clean_df[column].astype(float)
            except:
                self.non_numeric_columns.append(column)

        for variable in self.non_numeric_columns:
            options_frame = tk.Frame(self.variable_handling_options_frame)
            options_frame.pack(side=tk.TOP)

            variable_label = tk.Label(options_frame, text=variable)
            variable_label.pack(side=tk.TOP)

            for value in self.clean_df[variable].unique():
                self.selected_column_map[value] = variable
                value_frame = tk.Frame(options_frame)
                value_frame.pack(side=tk.TOP)

                value_label = tk.Label(value_frame, text=value)
                value_label.pack(side=tk.LEFT)

                input_var = tk.StringVar()
                self.input_var[value] = input_var

                input_combobox = ttk.Combobox(value_frame, textvariable=input_var, state="readonly")
                values = list(range(len(self.clean_df[variable].unique())))

                input_combobox['values'] = values
                input_combobox.current(0)  # Set default selection to the first item
                # input_combobox.bind("<<ComboboxSelected>>", lambda event, combobox=input_combobox: self.on_combobox_select(combobox, value))
                input_combobox.bind("<<ComboboxSelected>>", lambda event, combobox=input_combobox, value=value: self.on_combobox_select(combobox, value))
                input_combobox.pack(side=tk.LEFT)


    def apply_machine_learning_selection(self):
        for value, input_var in self.input_var.items():
            selected_value = (input_var.get())
            column_to_update = self.selected_column_map[value]
            self.clean_df.loc[self.clean_df[column_to_update] == value, column_to_update] = int(selected_value)
        for column in self.non_numeric_columns:
            self.clean_df[column] = self.clean_df[column].astype(float)




    def on_combobox_select(self, combobox, value):
        selected_value = combobox.get()
        self.input_var[value].set(selected_value)



    def switch_to_results_frame(self):
        self.run_analysis()

        self.indedependent_variables_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.variable_handling_frame.pack_forget()
        self.results_frame.pack(fill=tk.BOTH, expand=True)


        self.results_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")


    def run_analysis(self):
        utils.remove_frame_widgets(self.results_display_frame)

        self.execute_model()




    def execute_model(self):
        self.apply_machine_learning_selection()

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




