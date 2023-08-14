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
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
 
def setup_edit_tab(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame):
    df = data_manager.get_dataframe()
    if df is None:
        utils.show_message("Error", "Please open a file first.")
        return
    style.configure("file_button.TButton", background="gray")
    style.configure("dataframe_view_button.TButton", background="gray")
    style.configure("edit_button.TButton", background="white")
    style.configure("visualize_button.TButton", background="gray")
    utils.remove_frame_widgets(sub_button_frame)
 

    style.configure("clean_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36))
    clean_button = ttk.Button(sub_button_frame, text="Clean Data", style="clean_button.TButton")
    clean_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    clean_button.config(command=lambda: CleanData(editing_content_frame, dataframe_content_frame, df))
 
    style.configure("fix_columns_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36))
    fix_columns_button = ttk.Button(sub_button_frame, text="Fix Columns", style="fix_columns_button.TButton", command=fix_columns(editing_content_frame, dataframe_content_frame, df))
    fix_columns_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    # fix_columns_button.config(command=lambda: fix_columns(df, editing_content_frame))
 
    style.configure("create_cat_var_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36))
    create_cat_var_button = ttk.Button(sub_button_frame, text="Create Categorical Variable", style="create_cat_var_button.TButton")
    create_cat_var_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    # create_cat_var_button.config(command=lambda: create_cat_var(editing_content_frame, df))
 

    editing_content_frame.pack(fill=tk.BOTH, expand=True)
    visualize_content_frame.pack_forget()
    file_handling_content_frame.pack_forget()
    dataframe_content_frame.pack_forget()








################################################
################################################
 
                # CLEAN DATA #
 
################################################
################################################
 
class CleanData():
    def __init__(self, editing_content_frame, dataframe_content_frame, df):
        self.df = df
        self.dataframe_content_frame = dataframe_content_frame
 

        self.editing_content_frame = editing_content_frame
        utils.remove_frame_widgets(self.editing_content_frame)
 
        self.column_options_frame = tk.Frame(self.editing_content_frame, bg='yellow')
        self.column_options_frame.pack(side=tk.LEFT, fill=tk.BOTH)
 
        self.clean_settings_frame = tk.Frame(self.editing_content_frame, bg='pink')
        self.clean_settings_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        self.create_column_options_list()
   
    def create_column_options_list(self):
        utils.remove_frame_widgets(self.column_options_frame)
 
        self.available_columns = self.df.columns
        self.selected_column = None
        self.selected_column = tk.StringVar(value=self.selected_column)
 
        self.choice_frame = tk.Frame(self.column_options_frame, bg='orange')
        self.choice_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        self.choice_frame_label = tk.Label(self.choice_frame, text="COLUMN SELECTION", font=("Arial", 30, "bold"))
        self.choice_frame_label.pack(side=tk.TOP)
 

        self.column_type_selection = tk.StringVar()
        self.column_choice_listbox = tk.Listbox(self.choice_frame, font=("Arial", 18))
        self.column_choice_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
 
        for column in self.available_columns:
            self.column_choice_listbox.insert(tk.END, column)
 
        self.column_choice_listbox.update_idletasks()
 
        def on_column_choice_listbox_selection(event):
            selected_index = self.column_choice_listbox.curselection()
            if selected_index:
                selected_column_type = self.column_choice_listbox.get(selected_index[0])
                self.column_type_selection.set(selected_column_type)
 

        self.column_choice_listbox.bind("<<ListboxSelect>>", on_column_choice_listbox_selection)
 
        self.column_options_button_frame = tk.Frame(self.column_options_frame, bg='yellow')
        self.column_options_button_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        self.choose_column_button = tk.Button(self.column_options_button_frame, text="Clean Column", bg='orange', command=lambda: self.clean_column())
        self.choose_column_button.pack(side=tk.LEFT)
 
    def clean_column(self):
        selected_index = self.column_choice_listbox.curselection()
        if selected_index:
            self.selected_column = self.column_choice_listbox.get(selected_index[0])
            self.choose_variable_type()
 
    def choose_variable_type(self):
        utils.remove_frame_widgets(self.clean_settings_frame)
 
        self.variable_type_choice_frame = tk.Frame(self.clean_settings_frame, bg='purple')
        self.variable_type_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
 
        self.categorical_variable_frame = tk.Frame(self.variable_type_choice_frame, bg='purple')
        self.categorical_variable_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        self.continuous_variable_frame = tk.Frame(self.variable_type_choice_frame, bg='beige')
        self.continuous_variable_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 

        self.categorical_variable_button = tk.Button(self.categorical_variable_frame, text='Categorical Variable', command=self.clean_categorical_variable, font=('Arial', 30))
        self.categorical_variable_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
 
        self.continuous_variable_button = tk.Button(self.continuous_variable_frame,text='Continuous Variable', command=self.clean_continuous_variable, font=('Arial', 30))
        self.continuous_variable_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)



        self.menu_button_frame = tk.Frame(self.clean_settings_frame, bg='lightgray')
        self.menu_button_frame.pack(side=tk.BOTTOM, fill=tk.X)
 
        self.menu_column_choice = tk.Label(self.menu_button_frame, text=f"Cleaning Column: {self.selected_column}", font=("Arial", 36), bg="lightgray")
        self.menu_column_choice.pack(side=tk.TOP, padx= 10, pady=10, fill=tk.BOTH, expand=True)




















    ################################################
            # CLEAN CONTINUOUS VARIABLE #
    ################################################
 
    def clean_continuous_variable(self):
        self.temp_df = self.df.copy()
        self.handle_non_numeric_values()
 

    def handle_non_numeric_values(self):
        utils.remove_frame_widgets(self.clean_settings_frame)
       
 
        self.handle_non_numerics_frame = tk.Frame(self.clean_settings_frame, bg='purple')
        self.handle_non_numerics_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
 
        self.menu_button_frame = tk.Frame(self.clean_settings_frame, bg='lightgray')
        self.menu_button_frame.pack(side=tk.BOTTOM, fill=tk.X)
 
        self.advance_buton = tk.Button(self.menu_button_frame, text="Next", command=self.check_for_other_numeric_values, font=("Arial", 36))
        self.advance_buton.pack(side=tk.RIGHT, padx= 10, pady=10)
 
        self.return_button = tk.Button(self.menu_button_frame, text="Back", command=self.choose_variable_type, font=("Arial", 36))
        self.return_button.pack(side=tk.LEFT, padx= 10, pady=10)
 
        self.menu_column_choice = tk.Label(self.menu_button_frame, text=f"Cleaning Column: {self.selected_column}", font=("Arial", 36), bg="lightgray")
        self.menu_column_choice.pack(side=tk.LEFT, padx= 10, pady=10, fill=tk.BOTH, expand=True)
 
        try:
            self.temp_df[self.selected_column] = self.temp_df[self.selected_column].astype(float)
 
            no_non_numerics_label = tk.Label(self.handle_non_numerics_frame, text="No Non-Numeric Values. Click Next", font=("Arial", 36))
            no_non_numerics_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
 
        except:
            self.non_numeric_values = self.temp_df[self.selected_column].loc[~self.temp_df[self.selected_column].apply(lambda x: isinstance(x, (int, float)))]
            self.unique_non_numeric_values = self.non_numeric_values.unique()
 
            self.value_choice_frame = tk.Frame(self.handle_non_numerics_frame, bg='orange')
            self.value_choice_frame.pack(side=tk.LEFT, fill=tk.BOTH)
 
            self.value_action_frame = tk.Frame(self.handle_non_numerics_frame, bg='yellow')
            self.value_action_frame.pack(side=tk.LEFT)
 
            self.remove_button = tk.Button(self.value_action_frame, text="Remove Value", command=lambda: self.remove_non_numeric_value())
            self.remove_button.grid(row=0, column=0, padx=5, pady=5)
 
            self.change_value_button = tk.Button(self.value_action_frame, text="Change Value To:", command=lambda: self.change_non_numeric_value())
            self.change_value_button.grid(row=1, column=0, padx=5, pady=5)
 
            # Create the Entry widget
            self.new_value_entry = tk.Entry(self.value_action_frame, font=("Arial", 18))
            self.new_value_entry.grid(row=1, column=1, padx=5, pady=5)



            self.value_choice_frame_label = tk.Label(self.value_choice_frame, text="NON-NUMERIC VALUE SELECTION", font=("Arial", 30, "bold"))
            self.value_choice_frame_label.pack(side=tk.TOP)
 
            self.value_selection = tk.StringVar()
            self.value_choice_listbox = tk.Listbox(self.value_choice_frame, font=("Arial", 18))
            self.value_choice_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
 
            for value in self.unique_non_numeric_values:
                self.value_choice_listbox.insert(tk.END, value)
 
            self.value_choice_listbox.select_set(0)
            self.value_choice_frame.update_idletasks()
 
            self.selected_value = tk.StringVar(value=self.unique_non_numeric_values[0])
 
            def on_value_choice_listbox_selection(event):
                selected_index = self.value_choice_listbox.curselection()
                if selected_index:
                    self.selected_value = self.value_choice_listbox.get(selected_index[0])
 

            self.value_choice_listbox.bind("<<ListboxSelect>>", on_value_choice_listbox_selection)
 

   
    def remove_non_numeric_value(self):
        if type(self.selected_value) == str:
            self.temp_df.loc[self.temp_df[self.selected_column] == self.selected_value, self.selected_column] = np.nan
            self.update_non_numeric_listbox()
        else:
            self.temp_df.loc[self.temp_df[self.selected_column] == self.selected_value.get(), self.selected_column] = np.nan
            self.update_non_numeric_listbox()
 
    def change_non_numeric_value(self):
 
        if type(self.selected_value) == str:
            try:
                self.temp_df.loc[self.temp_df[self.selected_column] == self.selected_value, self.selected_column] = float(self.new_value_entry.get())
            except:
                self.numberic_error_label = tk.Label(self.value_action_frame, text="Value must be a number", font=("Arial", 18), foreground='red')
                self.numberic_error_label.grid(row=1, column=3, padx=5, pady=5)
        else:
            try:
                self.temp_df.loc[self.temp_df[self.selected_column] == self.selected_value.get(), self.selected_column] = float(self.new_value_entry.get())
            except:
                self.numberic_error_label = tk.Label(self.value_action_frame, text="Value must be a number", font=("Arial", 18), foreground='red')
                self.numberic_error_label.grid(row=1, column=3, padx=5, pady=5)



       
        self.update_non_numeric_listbox()
 

    def update_non_numeric_listbox(self):
        self.non_numeric_values = self.temp_df[self.selected_column].loc[~self.temp_df[self.selected_column].apply(lambda x: isinstance(x, (int, float)))]
        self.unique_non_numeric_values = self.non_numeric_values.unique()
 
        # Clear the listbox and insert the updated values
        self.value_choice_listbox.delete(0, tk.END)
        for value in self.unique_non_numeric_values:
            self.value_choice_listbox.insert(tk.END, value)
 
        self.value_choice_listbox.update_idletasks()
        self.value_choice_listbox.select_set(0)
        try:
            self.selected_value = tk.StringVar(value=self.unique_non_numeric_values[0])
        except:
            print('')
 

    def check_for_other_numeric_values(self):
        try:
            self.temp_df[self.selected_column] = self.temp_df[self.selected_column].astype(float)
            utils.remove_frame_widgets(self.clean_settings_frame)
            self.handle_other_numeric_values()
        except:
            return
 
    def create_histogram(self):
        clean_df = self.temp_df[self.selected_column].dropna()
 
        # Create scatter plot with seaborn
        sns.set(style="ticks")
        fig, ax = plt.subplots(figsize=(10,4))
 
        # Create the histogram using Seaborn
        sns.histplot(clean_df, kde=True, color='skyblue', ax=ax)
 
        # Set the title and labels
        plt.title('Histogram')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.tight_layout()
 
        return fig
 
    def handle_other_numeric_values(self):
        self.handle_other_numerics_frame = tk.Frame(self.clean_settings_frame, bg='pink')
        self.handle_other_numerics_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
 
        self.histogram_frame = tk.Frame(self.handle_other_numerics_frame, bg='pink')
        self.histogram_frame.pack(side=tk.TOP, fill=tk.X)
 
        self.options_frame = tk.Frame(self.handle_other_numerics_frame, bg='green')
        self.options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
 

        self.remove_negative_values_button = tk.Button(self.options_frame, text="Remove Negative Values", font=("Arial", 36), command=self.remove_negative_values)
        self.remove_negative_values_button.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
 
        self.remove_zero_values_button = tk.Button(self.options_frame, text="Remove Values of Zero", font=("Arial", 36), command=self.remove_zero_values)
        self.remove_zero_values_button.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
 

        self.menu_button_frame = tk.Frame(self.clean_settings_frame, bg='lightgray')
        self.menu_button_frame.pack(side=tk.BOTTOM, fill=tk.X)
 
        self.update_dataframe_button = tk.Button(self.menu_button_frame, text="Update Dataframe", command=self.update_dataframe, font=("Arial", 36))
        self.update_dataframe_button.pack(side=tk.RIGHT, padx= 10, pady=10)
 
        self.return_button = tk.Button(self.menu_button_frame, text="Back", command=self.handle_non_numeric_values, font=("Arial", 36))
        self.return_button.pack(side=tk.LEFT, padx= 10, pady=10)
 
        self.menu_column_choice = tk.Label(self.menu_button_frame, text=f"Cleaning Column: {self.selected_column}", font=("Arial", 36), bg="lightgray")
        self.menu_column_choice.pack(side=tk.LEFT, padx= 10, pady=10, fill=tk.BOTH, expand=True)
 

        self.create_continuous_variable_histogram()
 
    def remove_negative_values(self):
        self.temp_df.loc[self.temp_df[self.selected_column] < 0, self.selected_column] = np.nan
        self.create_continuous_variable_histogram()
       
 
    def remove_zero_values(self):
        self.temp_df.loc[self.temp_df[self.selected_column] == 0, self.selected_column] = np.nan
        self.create_continuous_variable_histogram()
       
 
    def create_continuous_variable_histogram(self):
        self.figure = self.create_histogram()
 
        utils.remove_frame_widgets(self.histogram_frame)
        # Create a canvas to display the histogram in the frame
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.histogram_frame)
        self.canvas.draw()
 
        # Remove expand=True and add height=histogram_frame_height
        self.canvas.get_tk_widget().pack(pady=5, padx=5, ipadx=5, ipady=5, side=tk.TOP)
 

    def update_dataframe(self):
        self.df = self.temp_df.copy()
        data_manager.set_dataframe(self.df)
 
        utils.remove_frame_widgets(self.dataframe_content_frame)
 
        utils.create_table(self.dataframe_content_frame, self.df)
        summary_df = utils.create_summary_table(self.df)
        utils.create_table(self.dataframe_content_frame, summary_df, title="COLUMN SUMMARY TABLE")













    ################################################
            # CLEAN CATEGORICAL VARIABLE #
    ################################################
 
    def clean_categorical_variable(self):
        self.temp_df = self.df.copy()
        self.handle_categorical_values()
 

    def handle_categorical_values(self):
        utils.remove_frame_widgets(self.clean_settings_frame)
 
        self.handle_categorical_values_frame = tk.Frame(self.clean_settings_frame, bg='purple')
        self.handle_categorical_values_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
 
        self.menu_button_frame = tk.Frame(self.clean_settings_frame, bg='lightgray')
        self.menu_button_frame.pack(side=tk.BOTTOM, fill=tk.X)
 
        self.advance_buton = tk.Button(self.menu_button_frame, text="Next", command=self.view_categorical_value_counts, font=("Arial", 36))
        self.advance_buton.pack(side=tk.RIGHT, padx= 10, pady=10)
 
        self.return_button = tk.Button(self.menu_button_frame, text="Back", command=self.choose_variable_type, font=("Arial", 36))
        self.return_button.pack(side=tk.LEFT, padx= 10, pady=10)
 
        self.menu_column_choice = tk.Label(self.menu_button_frame, text=f"Cleaning Column: {self.selected_column}", font=("Arial", 36), bg="lightgray")
        self.menu_column_choice.pack(side=tk.LEFT, padx= 10, pady=10, fill=tk.BOTH, expand=True)
 

       
        self.temp_df[self.selected_column] = self.temp_df[self.selected_column].astype(str)
 
        self.unique_categorical_values = self.temp_df[self.selected_column].unique()
        self.unique_categorical_values = [value for value in self.unique_categorical_values if value != 'nan']
 

        self.value_choice_frame = tk.Frame(self.handle_categorical_values_frame, bg='orange')
        self.value_choice_frame.pack(side=tk.LEFT, fill=tk.BOTH)
 
        self.value_action_frame = tk.Frame(self.handle_categorical_values_frame, bg='yellow')
        self.value_action_frame.pack(side=tk.LEFT)
 
        self.remove_button = tk.Button(self.value_action_frame, text="Remove Value", command=lambda: self.remove_categorical_value())
        self.remove_button.grid(row=0, column=0, padx=5, pady=5)
 
        self.change_value_button = tk.Button(self.value_action_frame, text="Change Value To:", command=lambda: self.change_categorical_value())
        self.change_value_button.grid(row=1, column=0, padx=5, pady=5)
 
        # Create the Entry widget
        self.new_value_entry = tk.Entry(self.value_action_frame, font=("Arial", 18))
        self.new_value_entry.grid(row=1, column=1, padx=5, pady=5)
 

        self.value_choice_frame_label = tk.Label(self.value_choice_frame, text="NON-NUMERIC VALUE SELECTION", font=("Arial", 30, "bold"))
        self.value_choice_frame_label.pack(side=tk.TOP)
 
        self.value_selection = tk.StringVar()
        self.value_choice_listbox = tk.Listbox(self.value_choice_frame, font=("Arial", 18))
        self.value_choice_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
 
        for value in self.unique_categorical_values:
            self.value_choice_listbox.insert(tk.END, value)
 
        self.value_choice_listbox.select_set(0)
        self.value_choice_frame.update_idletasks()
 
        self.selected_value = tk.StringVar(value=self.unique_categorical_values[0])
 
        def on_value_choice_listbox_selection(event):
            selected_index = self.value_choice_listbox.curselection()
            if selected_index:
                self.selected_value = self.value_choice_listbox.get(selected_index[0])
 

        self.value_choice_listbox.bind("<<ListboxSelect>>", on_value_choice_listbox_selection)
 

    def remove_categorical_value(self):
        if type(self.selected_value) == str:
            self.temp_df.loc[self.temp_df[self.selected_column] == self.selected_value, self.selected_column] = np.nan
            self.update_categorical_value_listbox()
        else:
            self.temp_df.loc[self.temp_df[self.selected_column] == self.selected_value.get(), self.selected_column] = np.nan
            self.update_categorical_value_listbox()
 

    def change_categorical_value(self):
        if type(self.selected_value) == str:
            self.temp_df.loc[self.temp_df[self.selected_column] == self.selected_value, self.selected_column] = self.new_value_entry.get()
 
        else:
            self.temp_df.loc[self.temp_df[self.selected_column] == self.selected_value.get(), self.selected_column] = self.new_value_entry.get()
        self.update_categorical_value_listbox()
 
    def update_categorical_value_listbox(self):
        self.temp_df[self.selected_column] = self.temp_df[self.selected_column].astype(str)
        self.unique_categorical_values = self.temp_df[self.selected_column].unique()
        self.unique_categorical_values = [value for value in self.unique_categorical_values if value != 'nan']
       
        # Clear the listbox and insert the updated values
        self.value_choice_listbox.delete(0, tk.END)
        for value in self.unique_categorical_values:
            self.value_choice_listbox.insert(tk.END, value)
 
        self.value_choice_listbox.update_idletasks()
        self.value_choice_listbox.select_set(0)
        try:
            self.selected_value = tk.StringVar(value=self.unique_categorical_values[0])
        except:
            print('')
 
    def view_categorical_value_counts(self):
        utils.remove_frame_widgets(self.clean_settings_frame)
       
        self.barplot_frame = tk.Frame(self.clean_settings_frame, bg='pink')
        self.barplot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
 

        self.menu_button_frame = tk.Frame(self.clean_settings_frame, bg='lightgray')
        self.menu_button_frame.pack(side=tk.BOTTOM, fill=tk.X)
 
        self.update_dataframe_button = tk.Button(self.menu_button_frame, text="Update Dataframe", command=self.update_dataframe, font=("Arial", 36))
        self.update_dataframe_button.pack(side=tk.RIGHT, padx= 10, pady=10)
 
        self.return_button = tk.Button(self.menu_button_frame, text="Back", command=self.handle_categorical_values, font=("Arial", 36))
        self.return_button.pack(side=tk.LEFT, padx= 10, pady=10)
 
        self.menu_column_choice = tk.Label(self.menu_button_frame, text=f"Cleaning Column: {self.selected_column}", font=("Arial", 36), bg="lightgray")
        self.menu_column_choice.pack(side=tk.LEFT, padx= 10, pady=10, fill=tk.BOTH, expand=True)
 

        self.create_categorical_variable_barplot()
 

    def create_categorical_variable_barplot(self):
        self.figure = self.create_categorical_barplot()
 
        utils.remove_frame_widgets(self.barplot_frame)
        # Create a canvas to display the histogram in the frame
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.barplot_frame)
        self.canvas.draw()
 
        self.canvas.get_tk_widget().pack(pady=5, padx=5, ipadx=5, ipady=5, side=tk.TOP, fill=tk.BOTH, expand=True)
 
    def create_categorical_barplot(self):
        self.temp_df[self.selected_column] = self.temp_df[self.selected_column].replace('nan', np.nan)
 
        # Drop rows containing NaN values in the selected column
        clean_df = self.temp_df.dropna(subset=[self.selected_column])
 
        # Create scatter plot with seaborn
        sns.set(style="ticks")
        fig, ax = plt.subplots()
 
        # Create the histogram using Seaborn
        ordered_categories = clean_df[self.selected_column].value_counts().sort_index().index
        sns.countplot(x=clean_df[self.selected_column], color='skyblue', ax=ax, order=ordered_categories)
 
        # Set the title and labels
        plt.title('Count Plot')
        plt.xlabel('Categories')
        plt.ylabel('Frequency')
        plt.xticks(rotation=90)
        plt.tight_layout()
 
        return fig










################################################
################################################
 
                # CLEAN DATA #
 
################################################
################################################
 
class fix_columns():
    def __init__(self, editing_content_frame, dataframe_content_frame, df):
        self.df = df
        self.dataframe_content_frame = dataframe_content_frame
        self.editing_content_frame = editing_content_frame
        self.fix_columns()
 
    def fix_columns(self):
        utils.remove_frame_widgets(self.editing_content_frame)
        self.df.columns = self.df.columns.str.replace(' ', '_')
        self.df.columns = self.df.columns.str.replace('__', '_')
        self.df.columns = self.df.columns.str.replace('___', '_')
        self.df.columns = self.df.columns.str.replace(r'\W+', '', regex=True)
        self.update_dataframe()
 
    def update_dataframe(self):
        data_manager.set_dataframe(self.df)
 
        utils.create_table(self.dataframe_content_frame, self.df, table_name="main_table")
        summary_df = utils.create_summary_table(self.df)
        utils.create_table(self.dataframe_content_frame, summary_df, table_name="summary_table", title="COLUMN SUMMARY TABLE")





















































def finalize_variable(df):
 
    return




def create_cat_variable(df, editing_content_frame, style):
 
    utils.remove_frame_widgets(editing_content_frame)
 
    left_frame = tk.Frame(editing_content_frame, bg="lightblue")  # Set the background color
    left_frame.pack(side="left", fill=tk.BOTH)
 
    left_top_frame = tk.Frame(left_frame, bg='yellow')
    left_top_frame.pack(side="top", fill="both")
   
    left_bottom_frame = tk.Frame(left_frame, bg='orange')
    left_bottom_frame.pack(side="top", fill="both", expand=True)
 
    style.configure("finalize_variable_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36))
    finalize_variable_button = ttk.Button(left_bottom_frame, text="Finalize Variable", style="finalize_variable.TButton")
    finalize_variable_button.pack(side="left", fill="both", expand=True, padx=100, pady=100)  # Set expand=True to fill the horizontal space
    finalize_variable_button.config(command=lambda: finalize_variable(df, right_frame))
 

    text_prompt = 'Choose which variables will be used to create your new variable:'
    selected_choices = []
    column_selection_frame = utils.MultipleChoiceSelectionFrame(left_top_frame, df.columns, selected_choices, text_prompt)
    column_selection_frame.pack(side="top", pady=5, padx=5)
 

    variable_name_label = tk.Label(left_top_frame, text="NAME of New Variable:")
    variable_name_label.pack(side="top", pady=5, padx=5)
 
    variable_name_entry = tk.Entry(left_top_frame)
    variable_name_entry.pack(side="top")
 
    set_variable_parameters_button = tk.Button(left_top_frame, text="Set Variable Parameters", font=("Arial", 18))
    set_variable_parameters_button.pack(side="top", pady=5, padx=5)
    set_variable_parameters_button.config(command=lambda: set_variable_parameters(right_frame, selected_choices, df))
 

    # Create the right frame
    right_frame = tk.Frame(editing_content_frame, bg="lightgreen")  # Set the background color
    right_frame.pack(side="left", fill=tk.BOTH, expand=True)
 
class App:
    def __init__(self, categories_frame, selected_choices, df):
        self.df = df
        self.categories_frame = categories_frame
        self.selected_choices = selected_choices
        self.category_frame_list = []
        self.condition_frames = []
        self.create_category_frame()
        self.create_button_frame()
 

    def create_category_frame(self):
        # Create the initial frame
        category_frame = tk.Frame(self.categories_frame, bd=1)
        category_frame.pack(side=tk.TOP, pady=5)
 
        self.category_frame_list.append(category_frame)
 
        category_value_frame = tk.Frame(category_frame, bd=1)
        category_value_frame.pack(side=tk.TOP)
 
        # Category Name Label and Entry
        category_name_label = tk.Label(category_value_frame, text=f"Category {len(self.category_frame_list)} Value:")
        category_name_label.pack(side=tk.LEFT)
 
        category_name_entry = tk.Entry(category_value_frame)
        category_name_entry.pack(side=tk.LEFT)
   
 
        condition_frame = tk.Frame(category_frame, bd=1, relief=tk.SOLID)
        condition_frame.pack(side=tk.TOP)
 
        self.create_condition_line(condition_frame)
 
        condition_button_frame = tk.Frame(category_frame, relief=tk.SOLID)
        condition_button_frame.pack(side=tk.BOTTOM)
 
        and_button = tk.Button(condition_button_frame, text="simple AND", command=lambda: self.add_simple_AND_condition(condition_frame))
        and_button.pack(side=tk.LEFT)
 
        or_button = tk.Button(condition_button_frame, text="simple OR", command=lambda: self.add_simple_OR_condition(condition_frame))
        or_button.pack(side=tk.LEFT)
 
        and_button = tk.Button(condition_button_frame, text=" major AND", command=lambda: self.add_major_AND_condition(condition_frame))
        and_button.pack(side=tk.LEFT)
 
        or_button = tk.Button(condition_button_frame, text="major OR", command=lambda: self.add_major_OR_condition(condition_frame))
        or_button.pack(side=tk.LEFT)
 
        remove_button = tk.Button(condition_button_frame, text="Remove Condition", command=self.remove_condition)
        remove_button.pack(side=tk.LEFT)



    def create_condition_line(self, condition_frame, option=None):
        condition_line_frame = tk.Frame(condition_frame)
        condition_line_frame.pack(side=tk.TOP)
 
        if option is None:
            condition_label = tk.Label(condition_line_frame, text="")
            condition_label.pack(side="left")
        elif option == "simple AND":
            condition_label = tk.Label(condition_line_frame, text="and")
            condition_label.pack(side="left")
        elif option == "simple OR":
            condition_label = tk.Label(condition_line_frame, text="or")
            condition_label.pack(side="left")
        elif option == "major AND":
            condition_label = tk.Label(condition_line_frame, text="AND")
            condition_label.pack(side="left")
        elif option == "major OR":
            condition_label = tk.Label(condition_line_frame, text="OR")
            condition_label.pack(side="left")
 
        # Selected Variable Dropdown
        choice_var = tk.StringVar(condition_line_frame)
        choice_var.set(self.selected_choices[0])
        column_dropdown = tk.OptionMenu(condition_line_frame, choice_var, *self.selected_choices)
        column_dropdown.pack(side=tk.LEFT, padx=10)
        def update_column_values(*args):
            column_values = ["user_choice"] + list(self.df[choice_var.get()].unique())
            values_var.set(column_values[0])
            column_values_dropdown['menu'].delete(0, 'end')
            for value in column_values:
                column_values_dropdown['menu'].add_command(label=value, command=tk._setit(values_var, value))
        choice_var.trace('w', update_column_values)
 
        # Comparison Operator Dropdown
        operator_options = ['==', '!=', '>', '>=', '<', '<=']
        operator_var = tk.StringVar(condition_line_frame)
        operator_var.set(operator_options[0])
        operator_dropdown = tk.OptionMenu(condition_line_frame, operator_var, *operator_options)
        operator_dropdown.pack(side=tk.LEFT, padx=10)
 
        # Column Values Dropdown or Entry
        column_values = ["user_choice"] + list(self.df[choice_var.get()].unique())
        values_var = tk.StringVar(condition_line_frame)
        values_var.set(column_values[0])
        column_values_dropdown = tk.OptionMenu(condition_line_frame, values_var, *column_values)
        column_values_dropdown.pack(side=tk.LEFT, padx=10)
 
        # Value Entry
        value_label = tk.Label(condition_line_frame, text="User Choice:")
        value_label.pack(side=tk.LEFT, pady=5)
        value_entry = tk.Entry(condition_line_frame)
        value_entry.pack(side=tk.LEFT)
 
        self.condition_frames.append(condition_line_frame)
 

    def remove_condition(self):
        if len(self.condition_frames) > 1:
            condition_frame = self.condition_frames.pop()
            condition_frame.destroy()



    def add_simple_AND_condition(self, condition_frame):
        self.create_condition_line(condition_frame, option="simple AND")
 
    def add_simple_OR_condition(self, condition_frame):
        self.create_condition_line(condition_frame, option="simple OR")
 
    def add_major_AND_condition(self, condition_frame):
        self.create_condition_line(condition_frame, option="major AND")
 
    def add_major_OR_condition(self, condition_frame):
        self.create_condition_line(condition_frame, option="major OR")
 

    def create_button_frame(self):
        self.button_frame = tk.Frame(self.categories_frame, bd=5)
        self.button_frame.pack(side=tk.BOTTOM, pady=5)
 
        add_button = tk.Button(self.button_frame, text="Add", command=self.add_new_frame)
        add_button.pack(side=tk.LEFT)
 
        remove_button = tk.Button(self.button_frame, text="Remove", command=self.delete_previous_frame)
        remove_button.pack(side=tk.LEFT)
 
    def add_new_frame(self):
        self.create_category_frame()
 

    def delete_previous_frame(self):
        # If there is more than one frame, remove the most recent frame
        if len(self.category_frame_list) > 1:
            last_frame = self.category_frame_list.pop()
            last_frame.pack_forget()
            self.button_frame.pack_forget()
 
            # Recreate the button_frame at the bottom after removing the frame
            self.create_button_frame()
        else:
            print("Cannot remove the initial frame.")




def set_variable_parameters(right_frame, selected_choices, df):
    if len(selected_choices) < 1:
        return
 
    # Destroy the previous categories_frame if it exists
    if hasattr(right_frame, 'categories_frame'):
        right_frame.categories_frame.destroy()
 
    # Create the new categories_frame
    categories_frame = tk.Frame(right_frame, bg='yellow')
    categories_frame.pack(fill=tk.BOTH)
    right_frame.categories_frame = categories_frame
   
 
    # Create the App instance and pass the categories_frame and app_instance to it
    app = App(categories_frame, selected_choices, df)