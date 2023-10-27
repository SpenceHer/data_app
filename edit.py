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

    style.configure("edit_clean_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36))
    edit_clean_button = ttk.Button(sub_button_frame, text="Edit Data", style="edit_clean_button.TButton")
    edit_clean_button.pack(side="left", fill="x", expand=True)
    edit_clean_button.config(command=lambda: EditData(editing_content_frame, dataframe_content_frame, df, style))

    style.configure("create_new_var_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36))
    create_new_var = ttk.Button(sub_button_frame, text="Create New Variable", style="create_new_var_button.TButton")
    create_new_var.pack(side="left", fill="x", expand=True)
    create_new_var.config(command=lambda: CreateNewVariableClass(editing_content_frame, dataframe_content_frame, df, style))

    tab_dict = data_manager.get_tab_dict()
    try:
        if tab_dict['current_edit_tab']:
            for tab in ['edit_clean', 'create_new_var']:
                if tab_dict['current_edit_tab'] == tab:
                    style.configure(f"{tab_dict['current_edit_tab']}_button.TButton", background="white")
                else:
                    style.configure(f"{tab}_button.TButton", background="gray")
    except:
        pass


    visualize_content_frame.pack_forget()
    file_handling_content_frame.pack_forget()
    dataframe_content_frame.pack_forget()
    editing_content_frame.pack(fill=tk.BOTH, expand=True)





################################################################################################################################################################################################
################################################################################################################################################################################################
################################################################################################################################################################################################




################################################
################################################
 
                # EDIT DATA #
 
################################################
################################################

class EditData():
    def __init__(self, editing_content_frame, dataframe_content_frame, df, style):
        self.df = data_manager.get_dataframe()
        self.dataframe_content_frame = dataframe_content_frame

        self.style = style

        self.style.configure("edit_clean_button.TButton", background="white")
        self.style.configure("create_new_var_button.TButton", background="gray")

        data_manager.add_tab_to_dict("current_edit_tab", "edit_clean")

        self.editing_content_frame = editing_content_frame
        utils.remove_frame_widgets(self.editing_content_frame)
 
        self.column_options_frame = tk.Frame(self.editing_content_frame, bg='beige')
        self.column_options_frame.pack(side=tk.LEFT, fill=tk.BOTH)
 
        self.clean_settings_frame = tk.Frame(self.editing_content_frame, bg='beige')
        self.clean_settings_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        self.create_column_options_list()
   
    def update_column_listbox(self, *args):
        search_term = self.column_search_var.get().lower()
        self.column_choice_listbox.delete(0, tk.END)
        for column in self.df.columns:
            if search_term in column.lower():
                self.column_choice_listbox.insert(tk.END, column)

    def create_column_options_list(self):
        utils.remove_frame_widgets(self.column_options_frame)
 
        self.available_columns = self.df.columns
        self.selected_column = None
        self.selected_column = tk.StringVar(value=self.selected_column)
 
        self.choice_frame = tk.Frame(self.column_options_frame, bg='beige')
        self.choice_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        self.choice_frame_label = tk.Label(self.choice_frame, text="COLUMN SELECTION", font=("Arial", 30, "bold"))
        self.choice_frame_label.pack(side=tk.TOP)

        self.column_search_var = tk.StringVar()
        self.column_search_var.trace("w", self.update_column_listbox)
        self.column_search_entry = tk.Entry(self.choice_frame, textvariable=self.column_search_var, font=("Arial", 24))
        self.column_search_entry.pack(side=tk.TOP, pady=5)
        self.column_search_entry.focus_set()

        self.column_type_selection = tk.StringVar()
        self.column_choice_listbox = tk.Listbox(self.choice_frame, font=("Arial", 24))
        self.column_choice_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
 
        for column in sorted(self.available_columns):
            self.column_choice_listbox.insert(tk.END, column)
 
        self.column_choice_listbox.update_idletasks()
 
        def on_column_choice_listbox_selection(event):
            selected_index = self.column_choice_listbox.curselection()
            if selected_index:
                selected_column_type = self.column_choice_listbox.get(selected_index[0])
                self.column_type_selection.set(selected_column_type)
 

        self.column_choice_listbox.bind("<<ListboxSelect>>", on_column_choice_listbox_selection)
 
        self.column_options_button_frame = tk.Frame(self.column_options_frame, bg='beige')
        self.column_options_button_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        self.choose_column_button = tk.Button(self.column_options_button_frame, text="Edit Column", command=lambda: self.clean_column(), font=('Arial', 24))
        self.choose_column_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
 
    def clean_column(self):
        selected_index = self.column_choice_listbox.curselection()
        if selected_index:
            self.selected_column = self.column_choice_listbox.get(selected_index[0])
            self.choose_variable_type()
 
    def choose_variable_type(self):
        utils.remove_frame_widgets(self.clean_settings_frame)
 
        self.variable_type_choice_frame = tk.Frame(self.clean_settings_frame, bg='beige')
        self.variable_type_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
 
        self.categorical_variable_frame = tk.Frame(self.variable_type_choice_frame, bg='beige')
        self.categorical_variable_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 
        self.continuous_variable_frame = tk.Frame(self.variable_type_choice_frame, bg='beige')
        self.continuous_variable_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
 

        self.categorical_variable_button = tk.Button(self.categorical_variable_frame, text='Categorical Variable', command=self.clean_categorical_variable, font=('Arial', 30))
        self.categorical_variable_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
 
        self.continuous_variable_button = tk.Button(self.continuous_variable_frame,text='Continuous Variable', command=self.clean_continuous_variable, font=('Arial', 30))
        self.continuous_variable_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)



        self.menu_button_frame = tk.Frame(self.clean_settings_frame, bg='lightgray')
        self.menu_button_frame.pack(side=tk.BOTTOM, fill=tk.X)
 
        self.menu_column_choice = tk.Label(self.menu_button_frame, text=f"Cleaning Column: {self.selected_column}", font=("Arial", 36), bg="lightgray", fg='black')
        self.menu_column_choice.pack(side=tk.TOP, padx= 10, pady=10, fill=tk.BOTH, expand=True)




















    ################################################
            # CLEAN CONTINUOUS VARIABLE #
    ################################################
 
    def clean_continuous_variable(self):
        self.temp_df = self.df.copy()
        self.handle_non_numeric_values()
 

    def handle_non_numeric_values(self):
        utils.remove_frame_widgets(self.clean_settings_frame)
       
 
        self.handle_non_numerics_frame = tk.Frame(self.clean_settings_frame, bg='beige')
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
 
            self.value_choice_frame = tk.Frame(self.handle_non_numerics_frame, bg='beige')
            self.value_choice_frame.pack(side=tk.LEFT, fill=tk.BOTH)
 
            self.value_action_frame = tk.Frame(self.handle_non_numerics_frame, bg='beige')
            self.value_action_frame.pack(side=tk.LEFT)
 
            self.remove_button = tk.Button(self.value_action_frame, text="Remove Value", command=lambda: self.remove_non_numeric_value(), font=("Arial", 36))
            self.remove_button.grid(row=0, column=0, padx=5, pady=5)
 
            self.change_value_button = tk.Button(self.value_action_frame, text="Change Value To:", command=lambda: self.change_non_numeric_value(), font=("Arial", 36))
            self.change_value_button.grid(row=1, column=0, padx=5, pady=5)
 
            # Create the Entry widget
            self.new_value_entry = tk.Entry(self.value_action_frame, font=("Arial", 36))
            self.new_value_entry.grid(row=1, column=1, padx=5, pady=5)



            self.value_choice_frame_label = tk.Label(self.value_choice_frame, text="NON-NUMERIC VALUES", font=("Arial", 30, "bold"))
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
 

 
    def handle_other_numeric_values(self):
        self.handle_other_numerics_frame = tk.Frame(self.clean_settings_frame, bg='beige')
        self.handle_other_numerics_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
 
        self.histogram_frame = tk.Frame(self.handle_other_numerics_frame, bg='beige')
        self.histogram_frame.pack(side=tk.TOP, fill=tk.X)
 
        self.options_frame = tk.Frame(self.handle_other_numerics_frame, bg='beige')
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
        self.figure = self.create_histogram_figure()
 
        utils.remove_frame_widgets(self.histogram_frame)
        # Create a canvas to display the histogram in the frame
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.histogram_frame)
        self.canvas.draw()
 
        # Remove expand=True and add height=histogram_frame_height
        self.canvas.get_tk_widget().pack(pady=5, padx=5, ipadx=5, ipady=5, side=tk.TOP)
 
    def create_histogram_figure(self):
        self.temp_df[self.selected_column] = pd.to_numeric(self.temp_df[self.selected_column], errors='coerce')

        clean_df = self.temp_df.dropna(subset=[self.selected_column])


        # Create scatter plot with seaborn
        # sns.set(style="ticks")
        fig, ax = plt.subplots()


        # Create the histogram using Seaborn
        # sns.histplot(clean_df[self.selected_column], kde=True, color='skyblue', ax=ax)
        plt.hist(clean_df[self.selected_column], color='skyblue', edgecolor='black')


        # Set the title and labels
        plt.title('Histogram')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.tight_layout()
 
        return fig



















    def update_dataframe(self):
        self.df = self.temp_df.copy()
        def fix_columns(df):
            df.columns = df.columns.str.replace(' ', '_')
            df.columns = df.columns.str.replace('__', '_')
            df.columns = df.columns.str.replace('___', '_')
            df.columns = df.columns.str.replace(r'\W+', '', regex=True)

        fix_columns(self.df)


        data_manager.add_dataframe_to_dict(self.df, data_manager.get_dataframe_name())
        data_manager.set_dataframe(data_manager.get_dataframe_name())

        utils.remove_frame_widgets(self.dataframe_content_frame)
 
        utils.create_table(self.dataframe_content_frame, self.df)
        summary_df = utils.create_summary_table(self.df)
        utils.create_table(self.dataframe_content_frame, summary_df, title="COLUMN SUMMARY TABLE")

        utils.show_message("Dataframe Update Status", "Database Has Been Updated")








    ################################################
            # CLEAN CATEGORICAL VARIABLE #
    ################################################
 
    def clean_categorical_variable(self):
        self.temp_df = self.df.copy()
        self.handle_categorical_values()
 

    def handle_categorical_values(self):
        utils.remove_frame_widgets(self.clean_settings_frame)
 
        self.handle_categorical_values_frame = tk.Frame(self.clean_settings_frame, bg='beige')
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
 

        self.value_choice_frame = tk.Frame(self.handle_categorical_values_frame, bg='beige')
        self.value_choice_frame.pack(side=tk.LEFT, fill=tk.BOTH)
 
        self.value_action_frame = tk.Frame(self.handle_categorical_values_frame, bg='beige')
        self.value_action_frame.pack(side=tk.LEFT)
 
        self.remove_button = tk.Button(self.value_action_frame, text="Remove Value", command=lambda: self.remove_categorical_value(), font=("Arial", 36))
        self.remove_button.grid(row=0, column=0, padx=5, pady=5)
 
        self.change_value_button = tk.Button(self.value_action_frame, text="Change Value To:", command=lambda: self.change_categorical_value(), font=("Arial", 36))
        self.change_value_button.grid(row=1, column=0, padx=5, pady=5)
 
        # Create the Entry widget
        self.new_value_entry = tk.Entry(self.value_action_frame, font=("Arial", 36))
        self.new_value_entry.grid(row=1, column=1, padx=5, pady=5)
 

        self.value_choice_frame_label = tk.Label(self.value_choice_frame, text="UNIQUE VALUES", font=("Arial", 30, "bold"))
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
       
        self.barplot_frame = tk.Frame(self.clean_settings_frame, bg='beige')
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
        self.figure = self.create_barplot_figure()
 
        utils.remove_frame_widgets(self.barplot_frame)
        # Create a canvas to display the histogram in the frame
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.barplot_frame)
        self.canvas.draw()
 
        self.canvas.get_tk_widget().pack(pady=5, padx=5, ipadx=5, ipady=5, side=tk.TOP, fill=tk.BOTH, expand=True)
 
    def create_barplot_figure(self):
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



















################################################################################################################################################################################################
################################################################################################################################################################################################
################################################################################################################################################################################################



################################################
################################################
 
                # CREATE NEW VARIABLE #
 
################################################
################################################


class CreateNewVariableClass:
    def __init__(self, editing_content_frame, dataframe_content_frame, df, style):
        self.df = data_manager.get_dataframe()
        self.editing_content_frame = editing_content_frame
        self.dataframe_content_frame = dataframe_content_frame

        self.style = style

        self.style.configure("edit_clean_button.TButton", background="gray")
        self.style.configure("create_new_var_button.TButton", background="white")

        data_manager.add_tab_to_dict("current_edit_tab", "create_new_var")

        utils.remove_frame_widgets(self.editing_content_frame)

        self.column_selection_frame = tk.Frame(self.editing_content_frame, bg='beige')
        self.conditions_frame = tk.Frame(self.editing_content_frame, bg='beige')
        self.finalize_frame = tk.Frame(self.editing_content_frame, bg='beige')

        self.create_column_selection_frame()
        self.create_conditions_frame()
        self.create_finalize_frame()

        self.switch_to_column_selection_frame()


    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    
    def create_column_selection_frame(self):

        self.selected_columns = []

        self.column_choice_frame = tk.Frame(self.column_selection_frame, bg='beige')
        self.column_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.choose_columns_label = tk.Label(self.column_choice_frame, text="Choose columns to use", font=("Arial", 36))
        self.choose_columns_label.pack(side=tk.TOP, fill=tk.X)

        self.selection_frame = tk.Frame(self.column_choice_frame, bg='beige')
        self.selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



        self.available_columns_frame = tk.Frame(self.selection_frame, bg='beige')
        self.available_columns_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
        self.transfer_buttons_frame = tk.Frame(self.selection_frame, bg='beige')
        self.transfer_buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.selected_columns_frame = tk.Frame(self.selection_frame, bg='beige')
        self.selected_columns_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)




        # AVAILABLE COLUMNS FRAME
        self.available_column_search_var = tk.StringVar()
        self.available_column_search_var.trace("w", self.update_available_columns_listbox)
        self.column_search_entry = tk.Entry(self.available_columns_frame, textvariable=self.available_column_search_var, font=("Arial", 24))
        self.column_search_entry.pack(side=tk.TOP, pady=5)
        self.column_search_entry.focus_set()

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

        self.column_selection_frame.update_idletasks()




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

        # VARIABLE NAME FRAME
        self.column_name_frame = tk.Frame(self.conditions_frame, bg='beige')
        self.column_name_frame.pack(side=tk.TOP, fill=tk.X)

        self.column_name_frame_label = tk.Label(self.column_name_frame, text="Name of new variable:", font=('Arial', 42), background='beige', foreground='black')
        self.column_name_frame_label.pack(side=tk.TOP, fill=tk.X)

        self.column_name_entry = tk.Entry(self.column_name_frame, font=('Arial', 24))
        self.column_name_entry.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)


        # ADD/REMOVE CONDITIONS BUTTONS FRAME
        self.condition_buttons_frame = tk.Frame(self.conditions_frame, bg='beige')
        self.condition_buttons_frame.pack(side=tk.TOP, fill=tk.X)

        self.add_new_value_button = tk.Button(self.condition_buttons_frame, text='Add New Value', command=self.add_value_frame, font=('Arial', 36))
        self.add_new_value_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.remove_value_button = tk.Button(self.condition_buttons_frame, text='Remove Value', command=self.remove_value_frame, font=('Arial', 36))
        self.remove_value_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)



        
        # CONDITIONS OPTIONS FRAME
        self.value_frames = []
        self.condition_frames = []
        self.condition_signs = ['Equals', 'Does Not Equal', 'Less Than', 'Greater Than', 'Less Than or Equal To', 'Greater Than or Equal To']
        self.condition_signs_dict = {'Equals':'==',
                                     'Does Not Equal':'!=',
                                     'Less Than':'<',
                                     'Greater Than':'>',
                                     'Less Than or Equal To':'<=',
                                     'Greater Than or Equal To':'>='}
        
        self.condition_options_frame = tk.Frame(self.conditions_frame, bg='beige')
        self.condition_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        def on_mousewheel(event):
            self.condition_canvas.yview_scroll(-1 * (event.delta // 120), "units")

        self.condition_canvas = tk.Canvas(self.condition_options_frame)
        self.scrollbar = ttk.Scrollbar(self.condition_options_frame, orient="vertical", command=self.condition_canvas.yview)
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

















        # MENU FRAME

        self.conditions_menu_frame = tk.Frame(self.conditions_frame, bg='beige')
        self.conditions_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_column_selection_button = tk.Button(self.conditions_menu_frame, command=self.switch_to_column_selection_frame, text="Back", font=("Arial", 36))
        self.return_to_column_selection_button.pack(side=tk.LEFT)

        self.advance_to_conditions_button = tk.Button(self.conditions_menu_frame, command=self.switch_to_finalize_frame, text="Next", font=("Arial", 36))
        self.advance_to_conditions_button.pack(side=tk.RIGHT)

        self.conditions_frame.update_idletasks()








    def add_value_frame(self):
        condition_frames = []

        # REMOVE MOST RECENT CONDITION LINE
        def remove_condition():
            if len(condition_frames) > 1:
                frame = condition_frames.pop()

                if condition_frames and condition_frames[-1].winfo_children()[0].cget("text") in {'AND', 'OR'}:
                    separation_frame = condition_frames.pop()
                    separation_frame.destroy()
                frame.destroy()

            else:
                return
        
        # ADD NEW CONDITION LINE
        def add_condition(label=''):
            if label == 'AND' or label == 'OR':
                separation_frame = tk.Frame(new_value_frame)
                separation_frame.pack(side=tk.TOP)

                condition_frames.append(separation_frame)
                if label == 'AND':
                    separation_label = tk.Label(separation_frame, text=label)
                    separation_label.pack(side=tk.TOP)
                    label = 'Where'

                if label == 'OR':
                    separation_label = tk.Label(separation_frame, text=label)
                    separation_label.pack(side=tk.TOP)
                    label = 'Where'



            condition_frame = tk.Frame(new_value_frame)
            condition_frame.pack(side=tk.TOP)

            condition_frames.append(condition_frame)
            
            condition_label = tk.Label(condition_frame, text=label)
            condition_label.pack(side=tk.LEFT)


            # COLUMN DROPDOWN FOR CONDITION
            def on_combobox_select(event):
                column_selected = column_dropdown.get()

                clean_df = self.df.dropna(subset=[column_selected])
                
                is_numeric = pd.to_numeric(clean_df[column_selected], errors='coerce').notna().all()

                if is_numeric:

                    clean_df[column_selected] = clean_df[column_selected].astype(float)
                    self.q1 = np.percentile(clean_df[column_selected], 25)
                    self.q2 = np.percentile(clean_df[column_selected], 50)  # Median (Q2)
                    self.q3 = np.percentile(clean_df[column_selected], 75)

                    self.q1_string = f"q1-{self.q1}"
                    self.q2_string = f"q2-{self.q2}"
                    self.q3_string = f"q3-{self.q3}"


                    value_list = ['USER CHOICE'] + [self.q1_string, self.q2_string, self.q3_string] + list(self.df[column_selected].unique())
                else:
                    value_list = ['USER CHOICE'] + list(self.df[column_selected].unique())

                column_values_dropdown["values"] = value_list

            selected_column_option = tk.StringVar()
            column_dropdown = ttk.Combobox(condition_frame, textvariable=selected_column_option, values=self.selected_columns, state="readonly")
            column_dropdown.pack(side=tk.LEFT)
            column_dropdown.bind("<<ComboboxSelected>>", on_combobox_select)

            # CONDITION SIGN DROPDOWN
            selected_condition_sign = tk.StringVar()
            selected_condition_sign_dropdown = ttk.Combobox(condition_frame, textvariable=selected_condition_sign, values=self.condition_signs, state="readonly")
            selected_condition_sign_dropdown.pack(side=tk.LEFT)

            # VALUE SELECTION DROPDOWN
            selected_value = tk.StringVar()
            value_list = ['USER CHOICE']
            column_values_dropdown = ttk.Combobox(condition_frame, textvariable=selected_value, values=value_list, state="readonly")
            column_values_dropdown.pack(side=tk.LEFT)

            # USER ENTRY VALUE
            user_entry_value = tk.Entry(condition_frame)
            user_entry_value.pack(side=tk.LEFT)







        # NEW VALUE FRAME
        new_value_frame = tk.Frame(self.scrollable_frame, relief=tk.RAISED, borderwidth=2)
        new_value_frame.pack(pady=10)

        # FRAME WHERE USER INPUTS WHAT THE VALUE WILL BE BASED ON THE CONDITIONS BELOW
        value_entry_frame = tk.Frame(new_value_frame)
        value_entry_frame.pack(side=tk.TOP)

        label = tk.Label(value_entry_frame, text="Value:")
        label.pack(side=tk.LEFT)

        value_entry = tk.Entry(value_entry_frame)
        value_entry.pack(side=tk.LEFT)

        # FRAME WHERE THE USER CAN ADD OR REMOVE MORE CONDITIONS
        condition_handling_frame = tk.Frame(new_value_frame)
        condition_handling_frame.pack(side=tk.TOP)

        add_simple_and_button = tk.Button(condition_handling_frame, text='and', command=lambda: add_condition(label='and'))
        add_simple_and_button.pack(side=tk.LEFT)

        add_simple_or_button = tk.Button(condition_handling_frame, text='or', command=lambda: add_condition(label='or'))
        add_simple_or_button.pack(side=tk.LEFT)

        # add_major_and_button = tk.Button(condition_handling_frame, text='AND', command=lambda: add_condition(label='AND'))
        # add_major_and_button.pack(side=tk.LEFT)

        # add_major_or_button = tk.Button(condition_handling_frame, text='OR', command=lambda: add_condition(label='OR'))
        # add_major_or_button.pack(side=tk.LEFT)

        add_remove_button = tk.Button(condition_handling_frame, text='Remove Condition', command=remove_condition)
        add_remove_button.pack(side=tk.LEFT)

        # FRAME WHERE THE USER EDITS THE CONDITIONS
        add_condition(label='Where')



        
        self.value_frames.append(new_value_frame)









    def remove_value_frame(self):

        if self.value_frames:
            frame = self.value_frames.pop()
            frame.destroy()

    def get_values_from_frames(self):
        self.column_name = self.column_name_entry.get()
        for idx, frame in enumerate(self.value_frames, start=1):
            condition_list_total = []
            condition_strings = []
            condition_syntax = {}

            for subframe_number, subframe in enumerate(frame.winfo_children(), start=1):
                condition_list = []

                if subframe_number == 1:
                    condition_value = subframe.winfo_children()[1].get()

                    continue

                if subframe_number == 2:
                    continue

                for widget in subframe.winfo_children():
                    try:
                        condition_list.append(widget.get())
                    except:
                        condition_list.append(widget.cget("text"))


                condition_list_total.append(condition_list)

            for condition in condition_list_total:
                if len(condition) == 1:
                    if condition[0] == 'AND':
                        condition_strings.append("&")
                    elif condition[0] == 'OR':
                        condition_strings.append("&")
                    continue

                condition_string = ''
                if condition[0] == 'or':
                    condition_string = "|"
                if condition[0] == 'and':
                    condition_string = "&"

                condition_string = condition_string + "("
                condition_string = condition_string + condition[1]
                condition_string = condition_string + self.condition_signs_dict[condition[2]]

                if condition[3] == 'USER CHOICE':
                    
                    try:
                        self.df[condition[1]] = self.df[condition[1]].astype(float)
                        condition_string = condition_string + str(float(condition[4]))
                    except:
                        self.df[condition[1]] = self.df[condition[1]].astype(object)
                        condition_string = condition_string + "'" + condition[4] + "'"
                else:
                    
                    try:

                        if condition[3] == self.q1_string:
                            condition_string = condition_string + str(float(self.q1))
                        elif condition[3] == self.q2_string:
                            condition_string = condition_string + str(float(self.q2))
                        elif condition[3] == self.q3_string:
                            condition_string = condition_string + str(float(self.q3))
                        else:
                            self.df[condition[1]] = self.df[condition[1]].astype(float)
                            condition_string = condition_string + str(float(condition[3]))

                    except:

                        self.df[condition[1]] = self.df[condition[1]].astype(object)
                        condition_string = condition_string + "'" + condition[3] + "'"
                
                condition_string = condition_string + ')'
                condition_strings.append(condition_string)


            final_condition_string = ''.join(condition_strings)
            self.df.loc[self.df.eval(final_condition_string), self.column_name] = condition_value



        


    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################

    def create_finalize_frame(self):
        # GRAPH DISPLAY FRAME
        self.finalize_display_frame = tk.Frame(self.finalize_frame, bg='purple')
        self.finalize_display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)












        # MENU FRAME
        self.finalize_menu_frame = tk.Frame(self.finalize_frame, bg='lightgray')
        self.finalize_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_conditions_button = tk.Button(self.finalize_menu_frame, command=self.switch_to_conditions_frame, text="Back", font=("Arial", 36))
        self.return_to_conditions_button.pack(side=tk.LEFT)

        self.update_dataframe_button = tk.Button(self.finalize_menu_frame, command=self.update_dataframe, text="Update Dataframe", font=("Arial", 36))
        self.update_dataframe_button.pack(side=tk.RIGHT)



    def plot_new_column(self):
        for widget in self.finalize_display_frame.winfo_children():
            widget.destroy()
        category_counts = self.df[self.column_name].value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))
        category_counts.plot(kind='bar', color='skyblue', ax=ax)

        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        ax.set_title(f'Frequency Bar Chart of {self.column_name}')

        plt.xticks(rotation=90)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.finalize_display_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    
    def switch_to_column_selection_frame(self):
        self.conditions_frame.pack_forget()
        self.finalize_frame.pack_forget()
        self.column_selection_frame.pack(fill=tk.BOTH, expand=True)


    def switch_to_conditions_frame(self):
        if not self.selected_columns:
            return
        self.finalize_frame.pack_forget()
        self.column_selection_frame.pack_forget()
        self.conditions_frame.pack(fill=tk.BOTH, expand=True)


    def switch_to_finalize_frame(self):
        if not self.column_name_entry.get():
            return
        if self.column_name_entry.get() in self.df.columns:
            self.df = self.df.drop(self.column_name_entry.get(), axis=1)
        self.get_values_from_frames()
        self.plot_new_column()
        self.conditions_frame.pack_forget()
        self.column_selection_frame.pack_forget()
        self.finalize_frame.pack(fill=tk.BOTH, expand=True)




    def update_dataframe(self):

        def fix_columns(df):
            df.columns = df.columns.str.replace(' ', '_')
            df.columns = df.columns.str.replace('__', '_')
            df.columns = df.columns.str.replace('___', '_')
            df.columns = df.columns.str.replace(r'\W+', '', regex=True)

        fix_columns(self.df)

        data_manager.add_dataframe_to_dict(self.df, data_manager.get_dataframe_name())
        data_manager.set_dataframe(data_manager.get_dataframe_name())


        utils.remove_frame_widgets(self.dataframe_content_frame)
 
        utils.create_table(self.dataframe_content_frame, self.df)
        summary_df = utils.create_summary_table(self.df)
        utils.create_table(self.dataframe_content_frame, summary_df, title="COLUMN SUMMARY TABLE")

        utils.show_message("Dataframe Update Status", "Database Has Been Updated")
