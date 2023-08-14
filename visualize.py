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
    comparison_table_button.config(command=lambda: ComparisonTableClass(visualize_content_frame, df))
 
    style.configure("multi_log_reg_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36))
    multi_log_reg_button = ttk.Button(sub_button_frame, text="Regression", style="multi_log_reg_button.TButton")
    multi_log_reg_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    multi_log_reg_button.config(command=lambda: RegressionAnalysisClass(visualize_content_frame, df))
 
    style.configure("create_plot_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36))
    create_plot_button = ttk.Button(sub_button_frame, text="Create Plot", style="create_plot_button.TButton")
    create_plot_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    create_plot_button.config(command=lambda: CreatePlotClass(visualize_content_frame, df))
 
    style.configure("machine_learning_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36))
    machine_learning_button = ttk.Button(sub_button_frame, text="Machine Learning", style="machine_learning_button.TButton")
    machine_learning_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    machine_learning_button.config(command=lambda: create_machine_learing(visualize_content_frame, df))
 
    editing_content_frame.pack_forget()
    visualize_content_frame.pack(fill=tk.BOTH, expand=True)
    file_handling_content_frame.pack_forget()
    dataframe_content_frame.pack_forget()















def summarize_column(column, df):
 
    return





################################################################################################################################################################################################
################################################################################################################################################################################################
################################################################################################################################################################################################



################################################
################################################
 
        # CREATE COMPARISON TABLE #
 
################################################
################################################
 
class ComparisonTableClass():
    def __init__(self, visualize_content_frame, df):
        self.df = data_manager.get_dataframe()
        self.visualize_content_frame = visualize_content_frame


        self.selected_dependent_variable = ""
        self.selected_independent_variables = []
        self.selected_analysis = ""


        utils.remove_frame_widgets(self.visualize_content_frame)


        self.dependent_variable_frame = tk.Frame(self.visualize_content_frame, bg='hotpink')
        self.indedependent_variables_frame = tk.Frame(self.visualize_content_frame, bg='red')
        self.variable_handling_frame = tk.Frame(self.visualize_content_frame, bg='green')
        self.results_frame = tk.Frame(self.visualize_content_frame, bg='blue')



        self.create_dependent_variable_frame()
        self.create_independent_variables_frame()
        self.create_variable_handling_frame()
        self.create_results_frame()


        self.switch_to_dependent_variable_frame()


    def create_dependent_variable_frame(self):


        self.dependent_variable_options_frame = tk.Frame(self.dependent_variable_frame, bg='yellow')
        self.dependent_variable_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.dependent_variable_menu_frame = tk.Frame(self.dependent_variable_frame, bg='lightgray')
        self.dependent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)


        self.advance_to_independent_variables_button = tk.Button(self.dependent_variable_menu_frame, text="Next", command=self.switch_to_independent_variables_frame, font=("Arial", 36))
        self.advance_to_independent_variables_button.pack(side=tk.RIGHT)


        self.dependent_frame_dependent_label = tk.Label(self.dependent_variable_menu_frame, text="", font=("Arial", 36), bg='lightgray')
        self.dependent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)










        self.dependent_column_choice_frame = tk.Frame(self.dependent_variable_options_frame, bg='hotpink')
        self.dependent_column_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.choose_dependent_variable_label = tk.Label(self.dependent_column_choice_frame, text="Choose your DEPENDENT variable", font=("Arial", 36))
        self.choose_dependent_variable_label.pack(side=tk.TOP)


        self.dependent_search_var = tk.StringVar()
        self.dependent_search_var.trace("w", self.update_dependent_variable_listbox)
        self.search_entry = tk.Entry(self.dependent_column_choice_frame, textvariable=self.dependent_search_var, font=("Arial", 24))
        self.search_entry.pack(side=tk.TOP, pady=10)


        self.dependent_variable_listbox = tk.Listbox(self.dependent_column_choice_frame, selectmode=tk.SINGLE, font=("Arial", 24))
        self.dependent_variable_listbox.pack(side=tk.TOP, pady=10)


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


        self.independent_variable_options_frame = tk.Frame(self.indedependent_variables_frame, bg='hotpink')
        self.independent_variable_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.independent_variable_menu_frame = tk.Frame(self.indedependent_variables_frame, bg='lightgray')
        self.independent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)


        self.return_to_dependent_variable_frame_button = tk.Button(self.independent_variable_menu_frame, command=self.switch_to_dependent_variable_frame, text='Back', font=("Arial", 36))
        self.return_to_dependent_variable_frame_button.pack(side=tk.LEFT)


        self.advance_to_variable_handling_frame_button = tk.Button(self.independent_variable_menu_frame, command=self.switch_to_variable_handling_frame, text="Next", font=("Arial", 36))
        self.advance_to_variable_handling_frame_button.pack(side=tk.RIGHT)


        self.independent_frame_dependent_label = tk.Label(self.independent_variable_menu_frame, text="", font=("Arial", 36), bg='lightgray')
        self.independent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)










        self.choose_independent_variables_label = tk.Label(self.independent_variable_options_frame, text="Choose your INDEPENDENT variables", font=("Arial", 36))
        self.choose_independent_variables_label.pack(side=tk.TOP)


        self.indedependent_variables_selection_frame = tk.Frame(self.independent_variable_options_frame, bg='orange')
        self.indedependent_variables_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)












        self.available_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='yellow')
        self.available_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        self.available_independent_search_var = tk.StringVar()
        self.available_independent_search_var.trace("w", self.update_available_independent_variable_listbox)
        self.search_entry = tk.Entry(self.available_independent_variables_frame, textvariable=self.available_independent_search_var, font=("Arial", 24))
        self.search_entry.pack(side=tk.TOP, pady=10)


        self.available_independent_variable_listbox = tk.Listbox(self.available_independent_variables_frame, selectmode=tk.MULTIPLE, font=("Arial", 24))
        self.available_independent_variable_listbox.pack(side=tk.TOP, pady=10)


        for column in sorted(self.df.columns, key=str.lower):
            self.available_independent_variable_listbox.insert(tk.END, column)


        self.available_independent_variable_listbox.update_idletasks()






        self.transfer_buttons_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='purple')
        self.transfer_buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        self.transfer_right_button = tk.Button(self.transfer_buttons_frame, text=">>", command=self.transfer_right, font=("Arial", 30))
        self.transfer_right_button.pack(pady=20)


        self.transfer_left_button = tk.Button(self.transfer_buttons_frame, text="<<", command=self.transfer_left, font=("Arial", 30))
        self.transfer_left_button.pack(pady=5)








        self.selected_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='brown')
        self.selected_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        self.selected_independent_variables_label = tk.Label(self.selected_independent_variables_frame, text="Selected Variables", font=("Arial", 24))
        self.selected_independent_variables_label.pack(side=tk.TOP, pady=10)




        self.selected_independent_variable_listbox = tk.Listbox(self.selected_independent_variables_frame, selectmode=tk.MULTIPLE, font=("Arial", 24))
        self.selected_independent_variable_listbox.pack(side=tk.TOP, pady=10)


        self.available_independent_variable_listbox.update_idletasks()



        self.regression_type_selection_frame = tk.Frame(self.independent_variable_options_frame, bg='green')
        self.regression_type_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)




        def on_radio_button_selected():
            self.selected_analysis = self.regression_type_radio_var.get()


        self.regression_type_radio_var = tk.IntVar()


        self.logistic_regression_radiobutton = tk.Radiobutton(self.regression_type_selection_frame, text="Logistic Regression", variable=self.regression_type_radio_var, value=1, command=on_radio_button_selected, font=("Arial", 24))
        self.logistic_regression_radiobutton.pack(side=tk.TOP)


        self.linear_regression_radiobutton = tk.Radiobutton(self.regression_type_selection_frame, text="Linear Regression", variable=self.regression_type_radio_var, value=2, command=on_radio_button_selected, font=("Arial", 24))
        self.linear_regression_radiobutton.pack(side=tk.TOP)




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


        self.variable_handling_options_frame = tk.Frame(self.variable_handling_frame, bg='green')
        self.variable_handling_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.variable_handling_menu_frame = tk.Frame(self.variable_handling_frame, bg='lightgray')
        self.variable_handling_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)


        self.return_to_independent_variable_frame_button = tk.Button(self.variable_handling_menu_frame, command=self.switch_to_independent_variables_frame, text='Back', font=("Arial", 36))
        self.return_to_independent_variable_frame_button.pack(side=tk.LEFT)


        self.view_results_button = tk.Button(self.variable_handling_menu_frame, command=self.switch_to_results_frame, text="View Results", font=("Arial", 36))
        self.view_results_button.pack(side=tk.RIGHT)


        self.variable_handling_frame_dependent_label = tk.Label(self.variable_handling_menu_frame, text="", font=("Arial", 36), bg='lightgray')
        self.variable_handling_frame_dependent_label.pack(side=tk.RIGHT, expand=True)






















def create_comparison_table(visualize_content_frame, df):
 

    outcome_variable = utils.get_single_choice(visualize_content_frame, df.columns, 'Choose your OUTCOME VARIABLE')
    if not outcome_variable:
        utils.show_message("No Columns Selected", "No columns selected for OUTCOME VARIABLE.")
        return
    independent_variables = utils.get_multiple_choices(visualize_content_frame, df.columns, "Choose your INDEPENDENT VARIABLES")
    if outcome_variable in independent_variables:
        utils.show_message("Wrong Column Selected", "Can't have OUTCOME VARIABLE as INDEPENDENT VARIABLE")
        return
    if not independent_variables:
        utils.show_message("No Columns Selected", "No columns selected for INDEPENDENT VARIABLES.")
        return
    # text_prompt = "Use all data? If no, only rows with complete data will be used"
    # full_data_yesno = utils.prompt_yes_no(text_prompt)
    full_data_yesno = False
    if full_data_yesno == True:
        clean_df = df[independent_variables + [outcome_variable]].copy()
        clean_df.dropna(subset=[outcome_variable], inplace=True)
    elif full_data_yesno == False:
        clean_df = df[independent_variables + [outcome_variable]].copy()
        clean_df.dropna(inplace=True)
 

    selected_options = {}
 
    dialog = utils.ComparisonTableSelectionDialog(visualize_content_frame, clean_df, independent_variables, selected_options)
    visualize_content_frame.wait_window(dialog.top)  
 

    summary_table = []
 
    for independent_variable, option in selected_options.items():
        if option == 'Continuous':
            try:
                clean_df[independent_variable] = clean_df[independent_variable].astype(float)
                # Independent variable is continuous
 
                row1 = []
                row2 = []
                row3 = []
                unique_values = sorted(clean_df[outcome_variable].unique())
                row1.append(f"{independent_variable}")
                row1.extend([np.nan] * len(unique_values))
 
                f_values = []
                if len(unique_values) > 2:
                    # More than two unique values, perform ANOVA
                    for value in unique_values:
                        group = clean_df.loc[clean_df[outcome_variable] == value, independent_variable]
                        f_values.append(group)
                    _, p_value = stats.f_oneway(*f_values)
                    if p_value < 0.0001:
                        p_value = '< 0.0001'
                        row1.append(p_value)
                    else:
                        row1.append(f"{p_value:.4f}")
                else:
                    # Two unique values, perform t-test
                    _, p_value = stats.ttest_ind(*[clean_df[independent_variable][clean_df[outcome_variable] == value] for value in unique_values])
                    if p_value < 0.0001:
                        p_value = '< 0.0001'
                        row1.append(p_value)
                    else:
                        row1.append(f"{p_value:.4f}")
                row2.append("  Mean (SD)")
                for value in unique_values:
                    row2.append(f"{clean_df.loc[clean_df[outcome_variable] == value, independent_variable].mean():.1f} ({clean_df.loc[clean_df[outcome_variable] == value, independent_variable].std():.1f})")
                row2.append(np.nan)
 
                row3.append("  Range")
                for value in unique_values:
                    row3.append(f"{clean_df.loc[clean_df[outcome_variable] == value, independent_variable].min():.1f} - {clean_df.loc[clean_df[outcome_variable] == value, independent_variable].max():.1f}")
 
                row3.append(np.nan)
 
                summary_table.append(row1)
                summary_table.append(row2)
                summary_table.append(row3)
                summary_table.append([np.nan] * len(row1))
            except:
                data_error = True
                pass
 
        elif option == 'Categorical':
            # Independent variable is categorical
            row1 =[]
            observed = pd.crosstab(clean_df[independent_variable], clean_df[outcome_variable])
            _, p_value, _, _ = stats.chi2_contingency(observed)
 
            row1.append(f"{independent_variable}")
            unique_values = sorted(clean_df[outcome_variable].unique())
            row1.extend([np.nan] * len(unique_values))
 
            if p_value < 0.0001:
                p_value = '< 0.0001'
                row1.append(p_value,)
            else:
                row1.append(f"{p_value:.4f}")
            summary_table.append(row1)
 
            for index, row in observed.iterrows():
                new_row = [index]
 
                row_sum = row.sum()
                percent_selection = "column"
                if percent_selection == 'row':
                    for value in row:
                        new_row.append(f"{value} ({int(round(value/row_sum*100,0))}%)")
                if percent_selection == 'column':
                    column_sums = observed.sum(axis=0)
                    for value, column_sum in zip(row, column_sums):
                        new_row.append(f"{value} ({int(round(value / column_sum * 100, 0))}%)")
                new_row.append(np.nan)
                summary_table.append(new_row)
            summary_table.append([np.nan] * len(row1))



    # Create the summary dataframe
    columns = ['Characteristic']
    for value in unique_values:
        count_of_value = len(clean_df.loc[clean_df[outcome_variable] == value])
 

        columns.append(f"{value} (N = {count_of_value})")
    columns.append('p-value')
 
    summary_df = pd.DataFrame(summary_table, columns=columns)
 
    utils.remove_frame_widgets(visualize_content_frame)
 
    utils.create_table(visualize_content_frame, summary_df, show_index=False, table_name="visualize_table", graph_name="visualize_graph")
 
    summary_text = tk.Text(visualize_content_frame.table_frames["visualize_table"], height=5, width=120, font=("Arial", 20))
    summary_text.pack(fill=tk.BOTH, expand=True)
    summary_text.insert(tk.END, f"TABLE OUTCOME VARIABLE: {outcome_variable}")
 
    save_summary_button = tk.Button(visualize_content_frame.table_frames["visualize_table"], text="Save Table", command=lambda: file_handling.save_file(summary_df))
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
    def __init__(self, visualize_content_frame, df):
        self.df = data_manager.get_dataframe()
        self.visualize_content_frame = visualize_content_frame


        self.selected_dependent_variable = ""
        self.selected_independent_variables = []
        self.selected_analysis = ""


        utils.remove_frame_widgets(self.visualize_content_frame)


        self.dependent_variable_frame = tk.Frame(self.visualize_content_frame, bg='hotpink')
        self.indedependent_variables_frame = tk.Frame(self.visualize_content_frame, bg='red')
        self.variable_handling_frame = tk.Frame(self.visualize_content_frame, bg='green')
        self.results_frame = tk.Frame(self.visualize_content_frame, bg='blue')




        self.create_dependent_variable_frame()
        self.create_independent_variables_frame()
        self.create_variable_handling_frame()
        self.create_results_frame()


        self.switch_to_dependent_variable_frame()






    def create_dependent_variable_frame(self):


        self.dependent_variable_options_frame = tk.Frame(self.dependent_variable_frame, bg='yellow')
        self.dependent_variable_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.dependent_variable_menu_frame = tk.Frame(self.dependent_variable_frame, bg='lightgray')
        self.dependent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)


        self.advance_to_independent_variables_button = tk.Button(self.dependent_variable_menu_frame, text="Next", command=self.switch_to_independent_variables_frame, font=("Arial", 36))
        self.advance_to_independent_variables_button.pack(side=tk.RIGHT)


        self.dependent_frame_dependent_label = tk.Label(self.dependent_variable_menu_frame, text="", font=("Arial", 36), bg='lightgray')
        self.dependent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)










        self.dependent_column_choice_frame = tk.Frame(self.dependent_variable_options_frame, bg='hotpink')
        self.dependent_column_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.choose_dependent_variable_label = tk.Label(self.dependent_column_choice_frame, text="Choose your DEPENDENT variable", font=("Arial", 36))
        self.choose_dependent_variable_label.pack(side=tk.TOP)


        self.dependent_search_var = tk.StringVar()
        self.dependent_search_var.trace("w", self.update_dependent_variable_listbox)
        self.search_entry = tk.Entry(self.dependent_column_choice_frame, textvariable=self.dependent_search_var, font=("Arial", 24))
        self.search_entry.pack(side=tk.TOP, pady=10)


        self.dependent_variable_listbox = tk.Listbox(self.dependent_column_choice_frame, selectmode=tk.SINGLE, font=("Arial", 24))
        self.dependent_variable_listbox.pack(side=tk.TOP, pady=10)


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


        self.independent_variable_options_frame = tk.Frame(self.indedependent_variables_frame, bg='hotpink')
        self.independent_variable_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.independent_variable_menu_frame = tk.Frame(self.indedependent_variables_frame, bg='lightgray')
        self.independent_variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)


        self.return_to_dependent_variable_frame_button = tk.Button(self.independent_variable_menu_frame, command=self.switch_to_dependent_variable_frame, text='Back', font=("Arial", 36))
        self.return_to_dependent_variable_frame_button.pack(side=tk.LEFT)


        self.advance_to_variable_handling_frame_button = tk.Button(self.independent_variable_menu_frame, command=self.switch_to_variable_handling_frame, text="Next", font=("Arial", 36))
        self.advance_to_variable_handling_frame_button.pack(side=tk.RIGHT)


        self.independent_frame_dependent_label = tk.Label(self.independent_variable_menu_frame, text="", font=("Arial", 36), bg='lightgray')
        self.independent_frame_dependent_label.pack(side=tk.RIGHT, expand=True)










        self.choose_independent_variables_label = tk.Label(self.independent_variable_options_frame, text="Choose your INDEPENDENT variables", font=("Arial", 36))
        self.choose_independent_variables_label.pack(side=tk.TOP)


        self.indedependent_variables_selection_frame = tk.Frame(self.independent_variable_options_frame, bg='orange')
        self.indedependent_variables_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)












        self.available_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='yellow')
        self.available_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        self.available_independent_search_var = tk.StringVar()
        self.available_independent_search_var.trace("w", self.update_available_independent_variable_listbox)
        self.search_entry = tk.Entry(self.available_independent_variables_frame, textvariable=self.available_independent_search_var, font=("Arial", 24))
        self.search_entry.pack(side=tk.TOP, pady=10)


        self.available_independent_variable_listbox = tk.Listbox(self.available_independent_variables_frame, selectmode=tk.MULTIPLE, font=("Arial", 24))
        self.available_independent_variable_listbox.pack(side=tk.TOP, pady=10)


        for column in sorted(self.df.columns, key=str.lower):
            self.available_independent_variable_listbox.insert(tk.END, column)


        self.available_independent_variable_listbox.update_idletasks()






        self.transfer_buttons_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='purple')
        self.transfer_buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        self.transfer_right_button = tk.Button(self.transfer_buttons_frame, text=">>", command=self.transfer_right, font=("Arial", 30))
        self.transfer_right_button.pack(pady=20)


        self.transfer_left_button = tk.Button(self.transfer_buttons_frame, text="<<", command=self.transfer_left, font=("Arial", 30))
        self.transfer_left_button.pack(pady=5)








        self.selected_independent_variables_frame = tk.Frame(self.indedependent_variables_selection_frame, bg='brown')
        self.selected_independent_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        self.selected_independent_variables_label = tk.Label(self.selected_independent_variables_frame, text="Selected Variables", font=("Arial", 24))
        self.selected_independent_variables_label.pack(side=tk.TOP, pady=10)




        self.selected_independent_variable_listbox = tk.Listbox(self.selected_independent_variables_frame, selectmode=tk.MULTIPLE, font=("Arial", 24))
        self.selected_independent_variable_listbox.pack(side=tk.TOP, pady=10)


        self.available_independent_variable_listbox.update_idletasks()



        self.regression_type_selection_frame = tk.Frame(self.independent_variable_options_frame, bg='green')
        self.regression_type_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)




        def on_radio_button_selected():
            self.selected_analysis = self.regression_type_radio_var.get()


        self.regression_type_radio_var = tk.IntVar()


        self.logistic_regression_radiobutton = tk.Radiobutton(self.regression_type_selection_frame, text="Logistic Regression", variable=self.regression_type_radio_var, value=1, command=on_radio_button_selected, font=("Arial", 24))
        self.logistic_regression_radiobutton.pack(side=tk.TOP)


        self.linear_regression_radiobutton = tk.Radiobutton(self.regression_type_selection_frame, text="Linear Regression", variable=self.regression_type_radio_var, value=2, command=on_radio_button_selected, font=("Arial", 24))
        self.linear_regression_radiobutton.pack(side=tk.TOP)




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


        self.variable_handling_options_frame = tk.Frame(self.variable_handling_frame, bg='green')
        self.variable_handling_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.variable_handling_menu_frame = tk.Frame(self.variable_handling_frame, bg='lightgray')
        self.variable_handling_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)


        self.return_to_independent_variable_frame_button = tk.Button(self.variable_handling_menu_frame, command=self.switch_to_independent_variables_frame, text='Back', font=("Arial", 36))
        self.return_to_independent_variable_frame_button.pack(side=tk.LEFT)


        self.view_results_button = tk.Button(self.variable_handling_menu_frame, command=self.switch_to_results_frame, text="View Results", font=("Arial", 36))
        self.view_results_button.pack(side=tk.RIGHT)


        self.variable_handling_frame_dependent_label = tk.Label(self.variable_handling_menu_frame, text="", font=("Arial", 36), bg='lightgray')
        self.variable_handling_frame_dependent_label.pack(side=tk.RIGHT, expand=True)










    def create_results_frame(self):


        self.results_display_frame = tk.Frame(self.results_frame, bg='blue')
        self.results_display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.results_menu_frame = tk.Frame(self.results_frame, bg='lightgray')
        self.results_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)


        self.return_to_independent_variable_frame_button = tk.Button(self.results_menu_frame, command=self.switch_to_independent_variables_frame, text='Back', font=("Arial", 36))
        self.return_to_independent_variable_frame_button.pack(side=tk.LEFT)


        self.results_frame_dependent_label = tk.Label(self.results_menu_frame, text="", font=("Arial", 36), bg='lightgray')
        self.results_frame_dependent_label.pack(side=tk.RIGHT, expand=True)





    def switch_to_dependent_variable_frame(self):


        self.variable_handling_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack(fill=tk.BOTH, expand=True)


        self.dependent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")








    def switch_to_independent_variables_frame(self):
        if self.selected_dependent_variable == "":
            return
   
        self.variable_handling_frame.pack_forget()
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.indedependent_variables_frame.pack(fill=tk.BOTH, expand=True)


        self.independent_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")
        self.available_independent_variable_listbox.update_idletasks()






    def switch_to_variable_handling_frame(self):

        if self.selected_analysis not in [1,2]:
            return
       
        if self.selected_analysis == 1:
            self.handle_variables_logistic_regression()


        if self.selected_analysis == 2:
            self.handle_variables_linear_regression()


    def handle_variables_linear_regression(self):
        self.results_frame.pack_forget()
        self.dependent_variable_frame.pack_forget()
        self.indedependent_variables_frame.pack_forget()
        self.variable_handling_frame.pack(fill=tk.BOTH, expand=True)


        self.variable_handling_frame_dependent_label.configure(text=f"Dependent Variable: {self.selected_dependent_variable}")


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


        utils.forget_frame_widgets(self.variable_handling_options_frame)


        self.clean_df = self.df[self.selected_independent_variables + [self.selected_dependent_variable]].copy()
        self.clean_df.dropna(inplace=True)




        self.unique_values = list(self.clean_df[self.selected_independent_variables].columns)
        self.selected_options = {}
        self.reference_value_dict = {}


        self.variable_type_radio_var = {}
        self.input_var = {}


        for value in self.unique_values:


            options_frame = tk.Frame(self.variable_handling_options_frame)
            options_frame.pack(side=tk.TOP)


            value_label = tk.Label(options_frame, text=value)
            value_label.pack(side=tk.LEFT)


            var = tk.StringVar(value="Continuous")  # Set default value to "Continuous"
            self.variable_type_radio_var[value] = var


            input_var = tk.StringVar()
            self.input_var[value] = input_var


            radio1 = ttk.Radiobutton(options_frame, text="Continuous", variable=var, value="Continuous")
            radio1.pack(side=tk.LEFT)


            radio3 = ttk.Radiobutton(options_frame, text="Categorical", variable=var, value="Categorical")
            radio3.pack(side=tk.LEFT)


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
 
    def __init__(self, visualize_content_frame, df):
        self.df = df
 
        self.visualize_content_frame = visualize_content_frame
        utils.remove_frame_widgets(self.visualize_content_frame)
 
        self.plot_options_frame = tk.Frame(self.visualize_content_frame, bg='yellow')
        self.plot_options_frame.pack(side=tk.LEFT, fill=tk.BOTH)
 
        self.figure_settings_frame = tk.Frame(self.visualize_content_frame, bg='blue')
        self.figure_settings_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        self.figure_display_frame = tk.Frame(self.visualize_content_frame, bg='orange')
        self.figure_display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.figure_display_frame.pack_forget()
 

        self.create_plot_options_list()
 

    def create_plot_options_list(self):
 
        self.available_plots = ["Scatter Plot", "Histogram", "Box and Whisker"]
        self.selected_plot = None
        self.selected_plot = tk.StringVar(value=self.selected_plot)
 
        self.radiobuttons = []
 
        self.choice_frame = tk.Frame(self.plot_options_frame, bg='orange')
        self.choice_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        self.choice_frame_label = tk.Label(self.choice_frame, text="PLOT SELECTION", font=("Arial", 30, "bold"))
        self.choice_frame_label.pack(side=tk.TOP)
 

        self.plot_type_selection = tk.StringVar()
        self.plot_choice_listbox = tk.Listbox(self.choice_frame)
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
 

        self.plot_options_button_frame = tk.Frame(self.plot_options_frame, bg='yellow')
        self.plot_options_button_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        self.choose_plot_button = tk.Button(self.plot_options_button_frame, text="Choose Plot", bg='orange', command=lambda: self.choose_plot())
        self.choose_plot_button.pack(side=tk.LEFT)












    def choose_plot(self):
        selected_index = self.plot_choice_listbox.curselection()
        if selected_index:
            self.selected_plot = self.plot_choice_listbox.get(selected_index[0])
 
            print(self.selected_plot)
 
            self.display_plot_settings()
            # fig=None
            # self.fig = self.create_virtual_figure()
 
            # if self.fig is not None:
            #     self.create_graph()
 

    def display_plot_settings(self):
 
        if self.selected_plot == "Scatter Plot":
            self.display_scatter_plot_settings()



    def display_scatter_plot_settings(self):
        self.column_choice_frame = tk.Frame(self.figure_settings_frame, bg='pink')
        self.column_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
 
        self.submit_settings_button_frame = tk.Frame(self.figure_settings_frame, bg='red')
        self.submit_settings_button_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
 
        self.x_axis_selection = tk.StringVar()
        self.y_axis_selection = tk.StringVar()
 
        ###################### X AXIS ######################
        self.x_axis_frame = tk.Frame(self.column_choice_frame, bg='orange')
        self.x_axis_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        self.x_axis_frame_label = tk.Label(self.x_axis_frame, text="X-AXIS SELECTION", font=("Arial", 30, "bold"))
        self.x_axis_frame_label.pack(side=tk.TOP)
 
        self.x_axis_listbox = tk.Listbox(self.x_axis_frame)
        self.x_axis_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        for column in self.df.columns:
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
        ###################### X AXIS ######################
 
        ###################### Y AXIS ######################
        self.y_axis_frame = tk.Frame(self.column_choice_frame, bg='orange')
        self.y_axis_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        self.y_axis_frame_label = tk.Label(self.y_axis_frame, text="Y-AXIS SELECTION", font=("Arial", 30, "bold"))
        self.y_axis_frame_label.pack(side=tk.TOP)
 
        self.y_axis_listbox = tk.Listbox(self.y_axis_frame)
        self.y_axis_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        for column in self.df.columns:
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
 
        # Force update the Listboxes after the frame becomes visible
        self.x_axis_listbox.update()
        self.y_axis_listbox.update()
        ###################### Y AXIS ######################
 
        # Add the Submit button
        self.submit_button = tk.Button(
            self.submit_settings_button_frame,
            text="Submit",
            command=self.submit_plot_settings
        )
        self.submit_button.pack(pady=10)
 

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
 

       






# def create_plot():
 
#     utils.remove_frame_widgets(visualize_content_frame)
   
#     CreatePlotClass(visualize_content_frame, df)
   
 
    # available_plots = ["Scatter Plot", "Histogram"]
    # text_prompt = "Choose a PLOT you want to make"
    # plot_choice = utils.get_single_choice(visualize_content_frame, available_plots, text_prompt)
    # if not plot_choice:
    #     utils.show_message("No plot Selected", "No plot selected.")
    #     return
   
 
    # if plot_choice == "Scatter Plot":
    #     fig = create_scatter_plot(visualize_content_frame, df)
 
    # if plot_choice == "Histogram":
    #     fig = create_histogram(visualize_content_frame, df)



    # if fig is not None:
    #     utils.create_graph(visualize_content_frame, fig)




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












def create_machine_learing(visualize_content_frame, df):
    return