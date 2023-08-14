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
df = pd.read_excel(r"/Users/spencersmith/Desktop/coding/OHSU_data.xlsx")
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


regression_button = tk.Button(visualize_content_frame, text="Regression", font=("Arial", 36), command=lambda: RegressionAnalysisClass(visualize_content_frame, df))
regression_button.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)




class RegressionAnalysisClass:
    def __init__(self, visualize_content_frame, df):
        self.df = df
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





# Start the GUI event loop
main_window.mainloop()




