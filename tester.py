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
df = pd.read_excel(r"C:\Users\smithsp\OneDrive - Oregon Health & Science University\Desktop\application\master_8.8.23.xlsx")
# Create the main window
main_window = tk.Tk()
main_window.title("DataFrame Editor")


# screen_width = main_window.winfo_screenwidth()
# screen_height = main_window.winfo_screenheight()
# TASKBAR_HEIGHT = 40
# main_window.geometry(f"{screen_width}x{screen_height - TASKBAR_HEIGHT}")
main_window.wm_state('zoomed')


visualize_content_frame = tk.Frame(main_window, bg="green")
visualize_content_frame.pack(side="top", fill=tk.BOTH, expand=True)


regression_button = tk.Button(visualize_content_frame, text="Comparison Table", font=("Arial", 36), command=lambda: ComparisonTableClass(visualize_content_frame, df))
regression_button.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)




class ComparisonTableClass:
    def __init__(self, visualize_content_frame, df):
        self.df = df
        self.visualize_content_frame = visualize_content_frame


        self.selected_dependent_variable = ""
        self.selected_independent_variables = []
        self.selected_percent_type = ""
        self.selected_data = ""


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



    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################

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





        self.table_options_frame = tk.Frame(self.independent_variable_options_frame, bg='green')
        self.table_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.percentage_type_selection_frame = tk.Frame(self.table_options_frame, bg='blue')
        self.percentage_type_selection_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        def on_percentage_radio_button_selected():
            self.selected_percent_type = self.percentage_type_radio_var.get()

        self.percentage_type_radio_var = tk.IntVar()

        self.row_percentage_radiobutton = tk.Radiobutton(self.percentage_type_selection_frame, text="Row Percentages", variable=self.percentage_type_radio_var, value=1, command=on_percentage_radio_button_selected, font=("Arial", 24))
        self.row_percentage_radiobutton.pack(side=tk.TOP)

        self.column_percentage_radiobutton = tk.Radiobutton(self.percentage_type_selection_frame, text="Column Percentages", variable=self.percentage_type_radio_var, value=2, command=on_percentage_radio_button_selected, font=("Arial", 24))
        self.column_percentage_radiobutton.pack(side=tk.TOP)




        self.data_choice_frame = tk.Frame(self.table_options_frame, bg='purple')
        self.data_choice_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        def on_data_choice_radio_button_selected():
            self.selected_data = self.data_choice_radio_var.get()

        self.data_choice_radio_var = tk.IntVar()

        self.independent_data_radiobutton = tk.Radiobutton(self.data_choice_frame, text="All Data", variable=self.data_choice_radio_var, value=1, command=on_data_choice_radio_button_selected, font=("Arial", 24))
        self.independent_data_radiobutton.pack(side=tk.TOP)

        self.dependent_data_radiobutton = tk.Radiobutton(self.data_choice_frame, text="Only Data-Complete Subjects", variable=self.data_choice_radio_var, value=2, command=on_data_choice_radio_button_selected, font=("Arial", 24))
        self.dependent_data_radiobutton.pack(side=tk.TOP)




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


    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################

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

        utils.forget_frame_widgets(self.variable_handling_options_frame)



        self.unique_values = list(self.df[self.selected_independent_variables].columns)
        self.selected_options = {}
        self.variable_type_radio_var = {}

        for value in self.unique_values:

            options_frame = tk.Frame(self.variable_handling_options_frame)
            options_frame.pack(side=tk.TOP)

            value_label = tk.Label(options_frame, text=value)
            value_label.pack(side=tk.LEFT)

            var = tk.StringVar(value="Continuous")  # Set default value to "Continuous"
            self.variable_type_radio_var[value] = var

            radio1 = ttk.Radiobutton(options_frame, text="Continuous", variable=var, value="Continuous")
            radio1.pack(side=tk.LEFT)

            radio2 = ttk.Radiobutton(options_frame, text="Categorical", variable=var, value="Categorical")
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
            count_of_value = len(self.table_df.loc[self.table_df[self.selected_dependent_variable] == value])
            columns.append(f"{value} (N = {count_of_value})")
            
        columns.append('p-value')
        if len(self.unique_dependent_variable_values) == 2:
            columns.append("Odds ratio")
        
        self.summary_df = pd.DataFrame(self.summary_table, columns=columns)
        print(self.summary_df)




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
        print(self.summary_df)






# Start the GUI event loop
main_window.mainloop()
