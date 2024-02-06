import tkinter as tk
from tkinter import Variable, filedialog, messagebox, simpledialog
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
import styles
from styles import color_dict


def setup_edit_tab(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame):

    df = data_manager.get_dataframe()
    if df is None:
        utils.show_message("Error", "Please open a file first.")
        return

    style.configure("file_button.TButton", background=color_dict["inactive_main_tab_bg"], foreground=color_dict["inactive_main_tab_txt"])
    style.configure("dataframe_view_button.TButton", background=color_dict["inactive_main_tab_bg"], foreground=color_dict["inactive_main_tab_txt"])
    style.configure("edit_button.TButton", background=color_dict["active_main_tab_bg"], foreground=color_dict["active_main_tab_txt"])
    style.configure("visualize_button.TButton", background=color_dict["inactive_main_tab_bg"], foreground=color_dict["inactive_main_tab_txt"])

    style.configure("edit_data_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"], borderwidth=0, padding=0, font=("Arial", 36, "bold"))
    style.configure("create_new_var_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"], borderwidth=0, padding=0, font=("Arial", 36, "bold"))

    for button_style in ["edit_data_button.TButton", "create_new_var_button.TButton"]:
        style.map(
            button_style,
            background=[("active", color_dict["hover_subtab_bg"])],
            foreground=[("active", color_dict["hover_subtab_txt"])]
        )


    # CHECK FOR CURRRENT TAB
    tab_dict = data_manager.get_tab_dict()
    try:
        current_tab = tab_dict["current_edit_tab"]
    except:
        current_tab = None

    # SET SUBTAB COLORS
    for tab in ["edit_data", "create_new_var"]:
        button_style = f"{tab}_button.TButton"
        if tab == current_tab:
            style.configure(button_style, background=color_dict["active_subtab_bg"], foreground=color_dict["active_subtab_txt"], borderwidth=0, padding=0, font=("Arial", 36, "bold"))
        else:
            style.configure(button_style, background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"], borderwidth=0, padding=0, font=("Arial", 36, "bold"))

        style.map(
            button_style,
            background=[("active", color_dict["hover_subtab_bg"])],
            foreground=[("active", color_dict["hover_subtab_txt"])]
        )

    utils.remove_frame_widgets(sub_button_frame)


    # SUBHEADING BUTTONS
    edit_data_button = ttk.Button(sub_button_frame, text="Edit Data", style="edit_data_button.TButton")
    edit_data_button.pack(side="left", fill="x", expand=True)
    edit_data_button.config(command=lambda: EditDataClass(editing_content_frame, dataframe_content_frame, sub_button_frame, style))

    create_new_var = ttk.Button(sub_button_frame, text="Create New Variable", style="create_new_var_button.TButton")
    create_new_var.pack(side="left", fill="x", expand=True)
    create_new_var.config(command=lambda: CreateNewVariableClass(editing_content_frame, dataframe_content_frame, sub_button_frame, style))



                

    # LOAD EDIT FRAME
    visualize_content_frame.pack_forget()
    file_handling_content_frame.pack_forget()
    dataframe_content_frame.pack_forget()
    editing_content_frame.pack(fill=tk.BOTH, expand=True)




    # UPDATE TAB IF DATAFRAME HAS BEEN CHANGED
    tab_update_status = data_manager.get_df_update_status_dict()
    if tab_update_status:
        if tab_update_status["edit_tab"] == True:
            if "current_edit_tab" in tab_dict:
                if tab_dict['current_edit_tab']:
                    if tab_dict['current_edit_tab'] == 'edit_data':
                        EditDataClass(editing_content_frame, dataframe_content_frame, sub_button_frame, style)
                    elif tab_dict['current_edit_tab'] == 'create_new_var':
                        CreateNewVariableClass(editing_content_frame, dataframe_content_frame, sub_button_frame, style)

                data_manager.add_df_update_status_to_dict("edit_tab", False)


    editing_content_frame.update_idletasks()





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
#                                               EDIT DATA                                                      #
#                                                                                                              #
################################################################################################################
################################################################################################################


class EditDataClass():
    def __init__(self, editing_content_frame, dataframe_content_frame, sub_button_frame, style):
        self.df = data_manager.get_dataframe()

        self.dataframe_content_frame = dataframe_content_frame
        self.sub_button_frame = sub_button_frame
        self.style = style

        style.configure("edit_data_button.TButton", background=color_dict["active_subtab_bg"], foreground=color_dict["active_subtab_txt"], borderwidth=0, padding=0, font=("Arial", 36, "bold"))
        style.configure("create_new_var_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"], borderwidth=0, padding=0, font=("Arial", 36, "bold"))

        data_manager.add_tab_to_tab_dict("current_edit_tab", "edit_data")

        self.editing_content_frame = editing_content_frame

        utils.remove_frame_widgets(self.editing_content_frame)

        # AVAILABLE COLUMNS FRAME
        self.column_options_frame = tk.Frame(self.editing_content_frame, bg='blue')
        self.column_options_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.create_column_options_list()


        # EDIT FRAME
        self.edit_frame = tk.Frame(self.editing_content_frame, bg='beige')
        self.edit_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.variable_type_choice_frame = tk.Frame(self.edit_frame, bg='beige')
        self.value_handling_frame = tk.Frame(self.edit_frame, bg='beige')
        self.data_display_frame = tk.Frame(self.edit_frame, bg='beige')

        self.create_variable_type_choice_frame()
        self.create_value_handling_frame()
        self.create_data_display_frame()



################################################################################################################
################################################################################################################
################################################################################################################


    def create_column_options_list(self):

        self.available_columns = self.df.columns
        self.selected_column = None
        self.selected_column = tk.StringVar(value=self.selected_column)

        self.choice_frame = tk.Frame(self.column_options_frame, bg='beige')
        self.choice_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.choice_frame_label = tk.Label(self.choice_frame, text="Select A Column", font=("Arial", 30, "bold"), bg='beige')
        self.choice_frame_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.choice_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.column_search_var = tk.StringVar()
        self.column_search_var.trace("w", self.update_column_listbox)
        self.column_search_entry = tk.Entry(self.choice_frame, textvariable=self.column_search_var, font=("Arial", 24))
        self.column_search_entry.pack(side=tk.TOP, pady=5)
        self.column_search_entry.focus_set()

        self.column_type_selection = tk.StringVar()
        self.column_choice_listbox = tk.Listbox(self.choice_frame, font=("Arial", 24), exportselection=False)
        self.column_choice_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        for column in sorted(self.df.columns, key=str.lower):
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

        self.choose_column_button = tk.Button(self.column_options_button_frame, text="Edit\nColumn", command=lambda: self.edit_column(), font=('Arial', 36))
        self.choose_column_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def update_column_listbox(self, *args):
        search_term = self.column_search_var.get().lower()
        self.column_choice_listbox.delete(0, tk.END)
        for column in self.df.columns:
            if search_term in column.lower():
                self.column_choice_listbox.insert(tk.END, column)


    def edit_column(self):
        selected_index = self.column_choice_listbox.curselection()
        if selected_index:

            utils.remove_frame_widgets(self.edit_frame)

            self.variable_type_choice_frame = tk.Frame(self.edit_frame, bg='beige')
            self.value_handling_frame = tk.Frame(self.edit_frame, bg='beige')
            self.data_display_frame = tk.Frame(self.edit_frame, bg='beige')

            self.create_variable_type_choice_frame()
            self.create_value_handling_frame()
            self.create_data_display_frame()


            self.selected_column = self.column_choice_listbox.get(selected_index[0])

            self.variable_type_choice_menu_frame_label.configure(text=f"Selected Column: {self.selected_column}")
            self.value_handling_menu_frame_label.configure(text=f"Selected Column: {self.selected_column}")
            self.data_display_menu_frame_label.configure(text=f"Selected Column: {self.selected_column}")


            self.switch_to_variable_type_choice_frame()
        else:
            utils.show_message("Error", "Please select a column first")




################################################################################################################
################################################################################################################
################################################################################################################


    def create_variable_type_choice_frame(self):

        self.variable_type_choice_label = tk.Label(self.variable_type_choice_frame, text="Choose Variable Type", font=("Arial", 36, "bold"),  bg='beige')
        self.variable_type_choice_label.pack(side=tk.TOP, fill=tk.X)

        separator = ttk.Separator(self.variable_type_choice_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)


        # MAIN CONTENT FRAME
        self.variable_type_choice_button_frame = tk.Frame(self.variable_type_choice_frame, bg='beige')
        self.variable_type_choice_button_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        # CATEGORICAL VARIABLE BUTTON
        self.categorical_variable_frame = tk.Frame(self.variable_type_choice_button_frame, bg='beige')
        self.categorical_variable_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.categorical_variable_button = tk.Button(self.categorical_variable_frame, text='Categorical Variable', command=self.edit_categorical_variable, font=('Arial', 30))
        self.categorical_variable_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)


        # CONTINUOUS VARIABLE BUTTON
        self.continuous_variable_frame = tk.Frame(self.variable_type_choice_button_frame, bg='beige')
        self.continuous_variable_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.continuous_variable_button = tk.Button(self.continuous_variable_frame,text='Continuous Variable', command=self.edit_continuous_variable, font=('Arial', 30))
        self.continuous_variable_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)


        # MENU
        self.variable_type_choice_menu_frame = tk.Frame(self.variable_type_choice_frame, bg='lightgray')
        self.variable_type_choice_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.variable_type_choice_menu_frame_label = tk.Label(self.variable_type_choice_menu_frame, text=f"Selected Column: {self.selected_column}", font=("Arial", 36), bg="lightgray", fg='black')
        self.variable_type_choice_menu_frame_label.pack(side=tk.TOP, padx= 10, pady=10, fill=tk.BOTH, expand=True)


################################################################################################################
################################################################################################################
################################################################################################################


    def create_value_handling_frame(self):

        # MAIN CONTENT FRAME
        self.options_frame = tk.Frame(self.value_handling_frame, bg='beige')
        self.options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        # NAVIGATION MENU
        self.value_handling_menu_frame = tk.Frame(self.value_handling_frame, bg='lightgray')
        self.value_handling_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_variable_type_choice_frame_button = tk.Button(self.value_handling_menu_frame, command=self.edit_column, text='Back', font=("Arial", 36))
        self.return_to_variable_type_choice_frame_button.pack(side=tk.LEFT)

        self.advance_to_display_frame_button = tk.Button(self.value_handling_menu_frame, text="Next", command=self.switch_to_data_display_frame, font=("Arial", 36), bg='blue', fg='black')
        self.advance_to_display_frame_button.pack(side=tk.RIGHT)

        self.value_handling_menu_frame_label = tk.Label(self.value_handling_menu_frame, text="Back", font=("Arial", 36), bg='lightgray', fg='black')
        self.value_handling_menu_frame_label.pack(side=tk.RIGHT, expand=True)


    ################################################################################################################

    # EDIT CATEGORICAL VARIABLE

    def edit_categorical_variable(self):
        self.selected_variable_type = "Categorical"

        self.temp_df = self.df.copy()

        self.handle_categorical_values()

        self.switch_to_value_handling_frame()


    def handle_categorical_values(self):

        self.categorical_variable_handling_label = tk.Label(self.options_frame, text='Categorical Variable Options', bg='beige', font=("Arial", 36, "bold"))
        self.categorical_variable_handling_label.pack(side=tk.TOP, fill=tk.X)

        separator = ttk.Separator(self.options_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)

        # TEMPORARY DATAFRAME
        self.temp_df.loc[self.temp_df[self.selected_column].isnull(), self.selected_column] = "[MISSING VALUES]"
        self.temp_df[self.selected_column] = self.temp_df[self.selected_column].astype(str)


        self.handle_categorical_values_frame = tk.Frame(self.options_frame, bg='beige')
        self.handle_categorical_values_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)




        # UNIQUE VALUE LISTBOX
        self.value_choice_frame = tk.Frame(self.handle_categorical_values_frame, bg='beige')
        self.value_choice_frame.pack(side=tk.LEFT, fill=tk.BOTH)




        self.unique_categorical_values = sorted(self.temp_df[self.selected_column].unique())
        self.unique_categorical_values = [value for value in self.unique_categorical_values if value != 'nan']

        # Listbox label
        self.value_choice_frame_label = tk.Label(self.value_choice_frame, text="Unique Values", font=("Arial", 30, "bold"), bg='beige')
        self.value_choice_frame_label.pack(side=tk.TOP)

        self.value_selection = tk.StringVar()
        self.value_choice_listbox = tk.Listbox(self.value_choice_frame, font=("Arial", 36), exportselection=False)
        self.value_choice_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        for value in self.unique_categorical_values:
            self.value_choice_listbox.insert(tk.END, value)

        # Default value is first value
        self.value_choice_listbox.select_set(0)
        self.selected_value = tk.StringVar(value=self.unique_categorical_values[0])

        def on_value_choice_listbox_selection(event):
            selected_index = self.value_choice_listbox.curselection()
            if selected_index:
                self.selected_value = self.value_choice_listbox.get(selected_index[0])

        self.value_choice_listbox.bind("<<ListboxSelect>>", on_value_choice_listbox_selection)





        # VALUE ACTIONS
        self.value_action_frame = tk.Frame(self.handle_categorical_values_frame, bg='beige')
        self.value_action_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # REMOVE OR CHANGE VALUE
        self.remove_change_value_action_frame = tk.Frame(self.value_action_frame, bg='beige')
        self.remove_change_value_action_frame.pack(side=tk.TOP, fill=tk.X, pady=25)

        self.handle_non_numeric_value_label = tk.Label(self.remove_change_value_action_frame, text="Handle Selected Value", font=("Arial", 24, "bold"), bg="beige")
        self.handle_non_numeric_value_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        # Remove Value
        self.remove_button = tk.Button(self.remove_change_value_action_frame, text="Remove Value", command=lambda: self.remove_categorical_value(), font=("Arial", 24))
        self.remove_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Change Value
        self.change_value_button = tk.Button(self.remove_change_value_action_frame, text="Change Value To:", command=lambda: self.change_categorical_value(), font=("Arial", 24))
        self.change_value_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        self.new_value_entry = tk.Entry(self.remove_change_value_action_frame, font=("Arial", 24))
        self.new_value_entry.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        separator = ttk.Separator(self.value_action_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=50, pady=5)

        self.remove_change_value_action_frame.columnconfigure(0, weight=1)
        self.remove_change_value_action_frame.columnconfigure(1, weight=1)


        # RENAME COLUMN
        self.rename_column_frame = tk.Frame(self.value_action_frame, bg='beige')
        self.rename_column_frame.pack(side=tk.TOP, fill=tk.X, pady=25)

        self.rename_column_label = tk.Label(self.rename_column_frame, text="Rename Column", font=("Arial", 24, "bold"), bg="beige")
        self.rename_column_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        self.rename_column_var = tk.StringVar(value="No")

        self.rename_column_yes_button = tk.Radiobutton(self.rename_column_frame, text="Yes", variable=self.rename_column_var, value="Yes", command=lambda: self.enable_rename_column(), indicator=0, font=("Arial", 24), borderwidth=10)
        self.rename_column_yes_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.rename_column_no_button = tk.Radiobutton(self.rename_column_frame, text="No", variable=self.rename_column_var, value="No", command=lambda: self.disable_rename_column(), indicator=0, font=("Arial", 24), borderwidth=10)
        self.rename_column_no_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.rename_column_entry = tk.Entry(self.rename_column_frame, font=("Arial", 24))

        self.rename_column_frame.columnconfigure(0, weight=1)
        self.rename_column_frame.columnconfigure(1, weight=1)

        separator = ttk.Separator(self.value_action_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=50, pady=5)

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
        self.unique_categorical_values = sorted(self.temp_df[self.selected_column].unique())
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
            pass


    ################################################################################################################

    # CLEAN CONTINUOUS VARIABLE

    def edit_continuous_variable(self):
        self.selected_variable_type = "Continuous"

        self.temp_df = self.df.copy()

        self.handle_continuous_values()

        self.switch_to_value_handling_frame()


    def handle_continuous_values(self):

        def is_float(value):
            try:
                float(value)
                return True
            except ValueError:
                return False

        self.continuous_variable_handling_label = tk.Label(self.options_frame, text='Continuous Variable Options', bg='beige', font=("Arial", 36, "bold"))
        self.continuous_variable_handling_label.pack(side=tk.TOP, fill=tk.X)

        separator = ttk.Separator(self.options_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)

        self.handle_continuous_values_frame = tk.Frame(self.options_frame, bg='beige')
        self.handle_continuous_values_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.temp_df.loc[self.temp_df[self.selected_column].isnull(), self.selected_column] = "[MISSING VALUES]"

        self.non_numeric_values = [value for value in self.temp_df[self.selected_column] if not is_float(value)]
        self.unique_non_numeric_values = list(set(self.non_numeric_values))

        # NON NUMERIC LISTBOX
        self.value_choice_frame = tk.Frame(self.handle_continuous_values_frame, bg='beige')
        self.value_choice_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.value_choice_frame_label = tk.Label(self.value_choice_frame, text="Non-Numeric Values", font=("Arial", 30, "bold"), bg='beige')
        self.value_choice_frame_label.pack(side=tk.TOP)

        self.value_selection = tk.StringVar()
        self.value_choice_listbox = tk.Listbox(self.value_choice_frame, font=("Arial", 36), exportselection=False)
        self.value_choice_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        for value in self.unique_non_numeric_values:
            self.value_choice_listbox.insert(tk.END, value)

        if len(self.non_numeric_values) > 0:
            self.value_choice_listbox.select_set(0)

            self.selected_value = tk.StringVar(value=self.unique_non_numeric_values[0])

        def on_value_choice_listbox_selection(event):
            selected_index = self.value_choice_listbox.curselection()
            if selected_index:
                self.selected_value = self.value_choice_listbox.get(selected_index[0])

        self.value_choice_listbox.bind("<<ListboxSelect>>", on_value_choice_listbox_selection)









        # VALUE ACTIONS
        self.value_action_frame = tk.Frame(self.handle_continuous_values_frame, bg='beige')
        self.value_action_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        # REMOVE OR CHANGE VALUE
        self.remove_change_value_action_frame = tk.Frame(self.value_action_frame, bg='beige')
        self.remove_change_value_action_frame.pack(side=tk.TOP, fill=tk.X, pady=25)

        self.handle_non_numeric_value_label = tk.Label(self.remove_change_value_action_frame, text="Handle Selected Value", font=("Arial", 24, "bold"), bg="beige")
        self.handle_non_numeric_value_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        # Remove Value
        self.remove_button = tk.Button(self.remove_change_value_action_frame, text="Remove Value", command=lambda: self.remove_non_numeric_value(), font=("Arial", 24))
        self.remove_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Change Value
        self.change_value_button = tk.Button(self.remove_change_value_action_frame, text="Change Value To:", command=lambda: self.change_non_numeric_value(), font=("Arial", 24))
        self.change_value_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        self.new_value_entry = tk.Entry(self.remove_change_value_action_frame, font=("Arial", 24))
        self.new_value_entry.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        self.new_value_entry.focus_set()

        separator = ttk.Separator(self.value_action_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=50, pady=5)

        self.remove_change_value_action_frame.columnconfigure(0, weight=1)
        self.remove_change_value_action_frame.columnconfigure(1, weight=1)


        # REMOVE NEGATIVE VALUES
        self.remove_negative_values_frame = tk.Frame(self.value_action_frame, bg='beige')
        self.remove_negative_values_frame.pack(side=tk.TOP, fill=tk.X, pady=25)

        self.remove_negative_values_label = tk.Label(self.remove_negative_values_frame, text="Remove Negative Values", font=("Arial", 24, "bold"), bg="beige")
        self.remove_negative_values_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        self.remove_negative_values_var = tk.StringVar(value="No")

        self.remove_negative_values_yes_button = tk.Radiobutton(self.remove_negative_values_frame, text="Yes", variable=self.remove_negative_values_var, value="Yes", indicator=0, font=("Arial", 24), borderwidth=10)
        self.remove_negative_values_yes_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.remove_negative_values_no_button = tk.Radiobutton(self.remove_negative_values_frame, text="No", variable=self.remove_negative_values_var, value="No", indicator=0, font=("Arial", 24), borderwidth=10)
        self.remove_negative_values_no_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.remove_negative_values_entry = tk.Entry(self.remove_negative_values_frame, font=("Arial", 24))

        self.remove_negative_values_frame.columnconfigure(0, weight=1)
        self.remove_negative_values_frame.columnconfigure(1, weight=1)

        separator = ttk.Separator(self.value_action_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=50, pady=5)


        # REMOVE ZERO VALUES
        self.remove_values_of_zero_frame = tk.Frame(self.value_action_frame, bg='beige')
        self.remove_values_of_zero_frame.pack(side=tk.TOP, fill=tk.X, pady=25)

        self.remove_values_of_zero_label = tk.Label(self.remove_values_of_zero_frame, text="Remove Values of Zero", font=("Arial", 24, "bold"), bg="beige")
        self.remove_values_of_zero_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        self.remove_values_of_zero_var = tk.StringVar(value="No")

        self.remove_values_of_zero_yes_button = tk.Radiobutton(self.remove_values_of_zero_frame, text="Yes", variable=self.remove_values_of_zero_var, value="Yes", indicator=0, font=("Arial", 24), borderwidth=10)
        self.remove_values_of_zero_yes_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.remove_values_of_zero_no_button = tk.Radiobutton(self.remove_values_of_zero_frame, text="No", variable=self.remove_values_of_zero_var, value="No", indicator=0, font=("Arial", 24), borderwidth=10)
        self.remove_values_of_zero_no_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.remove_values_of_zero_entry = tk.Entry(self.remove_values_of_zero_frame, font=("Arial", 24))

        self.remove_values_of_zero_frame.columnconfigure(0, weight=1)
        self.remove_values_of_zero_frame.columnconfigure(1, weight=1)

        separator = ttk.Separator(self.value_action_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=50, pady=5)



        # RENAME COLUMN
        self.rename_column_frame = tk.Frame(self.value_action_frame, bg='beige')
        self.rename_column_frame.pack(side=tk.TOP, fill=tk.X, pady=25)

        self.rename_column_label = tk.Label(self.rename_column_frame, text="Rename Column", font=("Arial", 24, "bold"), bg="beige")
        self.rename_column_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        self.rename_column_var = tk.StringVar(value="No")

        self.rename_column_yes_button = tk.Radiobutton(self.rename_column_frame, text="Yes", variable=self.rename_column_var, value="Yes", command=lambda: self.enable_rename_column(), indicator=0, font=("Arial", 24), borderwidth=10)
        self.rename_column_yes_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.rename_column_no_button = tk.Radiobutton(self.rename_column_frame, text="No", variable=self.rename_column_var, value="No", command=lambda: self.disable_rename_column(), indicator=0, font=("Arial", 24), borderwidth=10)
        self.rename_column_no_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.rename_column_entry = tk.Entry(self.rename_column_frame, font=("Arial", 24))

        self.rename_column_frame.columnconfigure(0, weight=1)
        self.rename_column_frame.columnconfigure(1, weight=1)

        separator = ttk.Separator(self.value_action_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=50, pady=5)





    def enable_rename_column(self):
        self.rename_column_entry.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.rename_column_entry.focus_set()

    def disable_rename_column(self):
        self.rename_column_entry.grid_remove()


    def remove_non_numeric_value(self):
        try:
            if type(self.selected_value) == str:
                self.temp_df.loc[self.temp_df[self.selected_column] == self.selected_value, self.selected_column] = np.nan
                self.update_non_numeric_listbox()
            else:
                self.temp_df.loc[self.temp_df[self.selected_column] == self.selected_value.get(), self.selected_column] = np.nan
                self.update_non_numeric_listbox()
        except:
            return

    def change_non_numeric_value(self):
        try:
            if type(self.selected_value) == str:
                try:
                    self.temp_df.loc[self.temp_df[self.selected_column] == self.selected_value, self.selected_column] = float(self.new_value_entry.get())
                except:
                    utils.show_message("Error", "New value must be numeric")

            else:
                try:
                    self.temp_df.loc[self.temp_df[self.selected_column] == self.selected_value.get(), self.selected_column] = float(self.new_value_entry.get())
                except:
                    utils.show_message("Error", "New value must be numeric")
        except:
            return




        self.update_non_numeric_listbox()


    def update_non_numeric_listbox(self):

        def is_float(value):
            try:
                float(value)
                return True
            except ValueError:
                return False
        self.non_numeric_values = [value for value in self.temp_df[self.selected_column] if not is_float(value)]
        self.unique_non_numeric_values = list(set(self.non_numeric_values))

        # Clear the listbox and insert the updated values
        self.value_choice_listbox.delete(0, tk.END)
        for value in self.unique_non_numeric_values:
            self.value_choice_listbox.insert(tk.END, value)

        self.value_choice_listbox.update_idletasks()
        self.value_choice_listbox.select_set(0)
        try:
            self.selected_value = tk.StringVar(value=self.unique_non_numeric_values[0])
        except:
            pass


    def is_valid_column_name(self, column_name):
        # Define a regular expression pattern for a valid column name
        pattern = r'^[a-zA-Z0-9_\-]+$'

        if re.match(pattern, column_name):
            try:
                df = pd.DataFrame(columns=[column_name])
                return True
            except ValueError:
                return False
        else:
            return False

    def remove_negative_values(self):
        self.new_df.loc[self.new_df[self.selected_column] < 0, self.selected_column] = np.nan
        self.create_continuous_variable_histogram()

    def remove_values_of_zero(self):
        self.new_df.loc[self.new_df[self.selected_column] == 0, self.selected_column] = np.nan
        self.create_continuous_variable_histogram()


################################################################################################################
################################################################################################################
################################################################################################################


    def create_data_display_frame(self):

        # MAIN CONTENT FRAME
        self.display_frame = tk.Frame(self.data_display_frame, bg='beige')
        self.display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # NAVIGATION MENU
        self.data_display_menu_frame = tk.Frame(self.data_display_frame, bg='lightgray')
        self.data_display_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_value_handling_frame_button = tk.Button(self.data_display_menu_frame, command=self.switch_to_value_handling_frame, text='Back', font=("Arial", 36))
        self.return_to_value_handling_frame_button.pack(side=tk.LEFT)

        self.update_dataframe_button = tk.Button(self.data_display_menu_frame, text="Update Dataframe", command=self.update_dataframe, font=("Arial", 36))
        self.update_dataframe_button.pack(side=tk.RIGHT)

        self.data_display_menu_frame_label = tk.Label(self.data_display_menu_frame, text="", font=("Arial", 36), bg='lightgray', fg='black')
        self.data_display_menu_frame_label.pack(side=tk.RIGHT, expand=True)


    ################################################################################################################

    # CATEGORICAL BAR PLOT
    def create_categorical_variable_barplot(self):
        self.figure = self.create_barplot_figure()

        utils.remove_frame_widgets(self.display_frame)
        # Create a canvas to display the histogram in the frame
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.display_frame)
        self.canvas.draw()

        self.canvas.get_tk_widget().pack(pady=5, padx=5, ipadx=5, ipady=5, side=tk.TOP, fill=tk.BOTH, expand=True)

    def create_barplot_figure(self):
        self.new_df[self.selected_column] = self.new_df[self.selected_column].replace('nan', np.nan)

        # Drop rows containing NaN values in the selected column
        clean_df = self.new_df.dropna(subset=[self.selected_column])

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








    def create_continuous_variable_histogram(self):
        self.figure = self.create_histogram_figure()

        utils.remove_frame_widgets(self.display_frame)
        # Create a canvas to display the histogram in the frame
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.display_frame)
        self.canvas.draw()

        # Remove expand=True and add height=histogram_frame_height
        self.canvas.get_tk_widget().pack(pady=5, padx=5, side=tk.TOP, fill=tk.BOTH, expand=True)

    def create_histogram_figure(self):
        self.new_df[self.selected_column] = pd.to_numeric(self.new_df[self.selected_column], errors='coerce')

        clean_df = self.new_df.dropna(subset=[self.selected_column])


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


################################################################################################################
################################################################################################################
################################################################################################################

    # UPDATE DATAFRAME

    def update_dataframe(self):
        if self.rename_column_var.get() == "Yes":

            self.new_df.rename(columns={self.selected_column:self.rename_column_entry.get()}, inplace=True)

        self.df = self.new_df.copy()
        def fix_columns(df):
            df.columns = df.columns.str.replace(' ', '_')
            df.columns = df.columns.str.replace('__', '_')
            df.columns = df.columns.str.replace('___', '_')
            df.columns = df.columns.str.replace(r'\W+', '', regex=True)

        fix_columns(self.df)


        data_manager.add_dataframe_to_dict(self.df, data_manager.get_dataframe_name())
        data_manager.set_dataframe(data_manager.get_dataframe_name())
        data_manager.add_df_update_status_to_dict("edit_tab", True)
        data_manager.add_df_update_status_to_dict("visualize_tab", True)

        utils.remove_frame_widgets(self.dataframe_content_frame)

        utils.create_table(self.dataframe_content_frame, self.df)
        summary_df = utils.create_summary_table(self.df)
        utils.create_table(self.dataframe_content_frame, summary_df, title="COLUMN SUMMARY TABLE")

        utils.show_message("Dataframe Update Status", "Database Has Been Updated")

        self.setup_dataframe_view_tab()





    def setup_dataframe_view_tab(self, initialize=True):
        df = data_manager.get_dataframe()
        if df is None:
            utils.show_message("Error", "Please open a file first.")
            return
        self.style.configure("file_button.TButton", background=color_dict["inactive_main_tab_bg"], foreground=color_dict["inactive_main_tab_txt"])
        self.style.configure("dataframe_view_button.TButton", background=color_dict["active_main_tab_bg"], foreground=color_dict["active_main_tab_txt"])
        self.style.configure("edit_button.TButton", background=color_dict["inactive_main_tab_bg"], foreground=color_dict["inactive_main_tab_txt"])
        self.style.configure("visualize_button.TButton", background=color_dict["inactive_main_tab_bg"], foreground=color_dict["inactive_main_tab_txt"])

        utils.remove_frame_widgets(self.sub_button_frame)

        self.style.configure("save_file_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36))
        save_file_button = ttk.Button(self.sub_button_frame, text="Save File", style="save_file_button.TButton")
        save_file_button.pack(side="left", fill="both", expand=True)  # Set expand=True to fill the horizontal space
        save_file_button.config(command=lambda: file_handling.save_file(df))

        def initialize_dataframe_view_tab():
            utils.remove_frame_widgets(self.dataframe_content_frame)

            utils.create_table(self.dataframe_content_frame, df)
            summary_df = utils.create_summary_table(df)
            utils.create_table(self.dataframe_content_frame, summary_df, title="COLUMN SUMMARY TABLE")

            self.editing_content_frame.pack_forget()
            self.dataframe_content_frame.pack(fill=tk.BOTH, expand=True)

        def switch_to_dataframe_view_tab():
            self.editing_content_frame.pack_forget()
            self.dataframe_content_frame.pack(fill=tk.BOTH, expand=True)


        if initialize == True:
            initialize_dataframe_view_tab()
        if initialize == False:
            switch_to_dataframe_view_tab()

        self.dataframe_content_frame.update_idletasks()




################################################################################################################
################################################################################################################
################################################################################################################

    # NAVIGATION HANDLING FUNCTIONS

    def switch_to_variable_type_choice_frame(self):
        self.value_handling_frame.pack_forget()
        self.data_display_frame.pack_forget()
        self.variable_type_choice_frame.pack(fill=tk.BOTH, expand=True)

        self.editing_content_frame.update_idletasks()

    def switch_to_value_handling_frame(self):
        self.variable_type_choice_frame.pack_forget()
        self.data_display_frame.pack_forget()
        self.value_handling_frame.pack(fill=tk.BOTH, expand=True)

        if self.new_value_entry:
            self.new_value_entry.focus_set()

        self.editing_content_frame.update_idletasks()

    def switch_to_data_display_frame(self):
        if self.rename_column_var.get() == "Yes":
            if not self.is_valid_column_name(self.rename_column_entry.get()):
                utils.show_message("Error", "Invalid Column Name")
                return
            self.data_display_menu_frame_label.configure(text=f"New Column Name:{self.rename_column_entry.get()}")

        self.new_df = self.temp_df.copy()
        if self.selected_variable_type == "Continuous":
            if self.remove_values_of_zero_var.get() == "Yes":
                self.remove_values_of_zero()
            if self.remove_negative_values_var.get() == "Yes":
                self.remove_negative_values()


            self.create_continuous_variable_histogram()
        elif self.selected_variable_type == "Categorical":
            self.create_categorical_variable_barplot()

        self.variable_type_choice_frame.pack_forget()
        self.value_handling_frame.pack_forget()
        self.data_display_frame.pack(fill=tk.BOTH, expand=True)


        self.editing_content_frame.update_idletasks()



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
#                                           CREATE NEW VARIABLE                                                #
#                                                                                                              #
################################################################################################################
################################################################################################################


class CreateNewVariableClass:
    def __init__(self, editing_content_frame, dataframe_content_frame, sub_button_frame, style):
        self.df = data_manager.get_dataframe()
        self.editing_content_frame = editing_content_frame
        self.dataframe_content_frame = dataframe_content_frame
        self.sub_button_frame = sub_button_frame
        self.style = style

        style.configure("edit_data_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"], borderwidth=0, padding=0, font=("Arial", 36, "bold"))
        style.configure("create_new_var_button.TButton", background=color_dict["active_subtab_bg"], foreground=color_dict["active_subtab_txt"], borderwidth=0, padding=0, font=("Arial", 36, "bold"))

        data_manager.add_tab_to_tab_dict("current_edit_tab", "create_new_var")

        self.selected_variables = data_manager.get_create_var_tab_var_list()

        utils.remove_frame_widgets(self.editing_content_frame)

        self.variable_selection_frame = tk.Frame(self.editing_content_frame, bg='beige')
        self.conditions_frame = tk.Frame(self.editing_content_frame, bg='beige')
        self.finalize_frame = tk.Frame(self.editing_content_frame, bg='beige')

        self.create_variable_selection_frame()
        self.create_conditions_frame()
        self.create_finalize_frame()


        self.switch_to_variable_selection_frame()


    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################

    # CREATE VARIABLE SELECTION FRAME

    def create_variable_selection_frame(self):

        # MAIN CONTENT FRAME
        self.variable_options_frame = tk.Frame(self.variable_selection_frame, bg='beige')
        self.variable_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # TITLE LABEL
        self.choose_variables_label = tk.Label(self.variable_options_frame, text="Choose Variables to Create New Variable", font=("Arial", 36, "bold"), bg='beige')
        self.choose_variables_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.variable_options_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)


        # AVAILABLE VARIABLES SELECTION FRAME
        self.variables_selection_frame = tk.Frame(self.variable_options_frame, bg='beige')
        self.variables_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.available_variables_frame = tk.Frame(self.variables_selection_frame, bg='beige')
        self.available_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.available_variables_search_var = tk.StringVar()
        self.available_variables_search_var.trace("w", self.update_available_variables_listbox)
        self.variable_search_entry = tk.Entry(self.available_variables_frame, textvariable=self.available_variables_search_var, font=("Arial", 24))
        self.variable_search_entry.pack(side=tk.TOP, pady=10)

        self.available_variable_listbox = tk.Listbox(self.available_variables_frame, selectmode=tk.MULTIPLE, font=("Arial", 24))
        self.available_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)

        for column in sorted(self.df.columns, key=str.lower):
            self.available_variable_listbox.insert(tk.END, column)


        # TRANSFER BUTTONS
        self.transfer_buttons_frame = tk.Frame(self.variables_selection_frame, bg='beige')
        self.transfer_buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.transfer_right_button = tk.Button(self.transfer_buttons_frame, text=">>>", command=self.transfer_right, font=("Arial", 48))
        self.transfer_right_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.transfer_left_button = tk.Button(self.transfer_buttons_frame, text="<<<", command=self.transfer_left, font=("Arial", 48))
        self.transfer_left_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.transfer_all_right_button = tk.Button(self.transfer_buttons_frame, text="Move All Right", command=self.transfer_all_right, font=("Arial", 36))
        self.transfer_all_right_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)

        self.transfer_all_left_button = tk.Button(self.transfer_buttons_frame, text="Clear Selection", command=self.transfer_all_left, font=("Arial", 36))
        self.transfer_all_left_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)



        # SELECTED VARIABLES FRAME
        self.selected_variables_frame = tk.Frame(self.variables_selection_frame, bg='beige')
        self.selected_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.selected_variables_label = tk.Label(self.selected_variables_frame, text="Selected Variables", font=("Arial", 24), bg='beige')
        self.selected_variables_label.pack(side=tk.TOP, pady=10)

        self.selected_variables_listbox = tk.Listbox(self.selected_variables_frame, selectmode=tk.MULTIPLE, font=("Arial", 24))
        self.selected_variables_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)

        if len(self.selected_variables) > 0:
            for var in self.selected_variables:
                self.selected_variables_listbox.insert(tk.END, var)
                self.available_variable_listbox.selection_set(sorted(self.df.columns, key=str.lower).index(var))
            selections = self.available_variable_listbox.curselection()
            for index in reversed(selections):
                self.available_variable_listbox.delete(index)



        # NAVIGATION MENU
        self.variable_menu_frame = tk.Frame(self.variable_selection_frame, bg='lightgray')
        self.variable_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.advance_to_conditions_button = tk.Button(self.variable_menu_frame, command=self.switch_to_conditions_frame, text="Next", font=("Arial", 36))
        self.advance_to_conditions_button.pack(side=tk.RIGHT)



    def update_available_variables_listbox(self, *args):
        search_term = self.available_variables_search_var.get().lower()
        self.available_variable_listbox.delete(0, tk.END)
        for column in sorted(self.df.columns, key=str.lower):
            if search_term in column.lower():
                self.available_variable_listbox.insert(tk.END, column)


    def transfer_right(self):
        selections = self.available_variable_listbox.curselection()
        selected_items = [self.available_variable_listbox.get(index) for index in selections]

        for item in selected_items:
            if item not in self.selected_variables:
                self.selected_variables_listbox.insert(tk.END, item)
                self.selected_variables.append(item)


        for index in reversed(selections):
            self.available_variable_listbox.delete(index)


    def transfer_all_right(self):

        for i in range(self.available_variable_listbox.size()):
            self.available_variable_listbox.selection_set(i)

        selections = self.available_variable_listbox.curselection()
        selected_items = [self.available_variable_listbox.get(index) for index in selections]

        for item in selected_items:
            self.selected_variables_listbox.insert(tk.END, item)
            self.selected_variables.append(item)

        for index in reversed(selections):
            self.available_variable_listbox.delete(index)


    def transfer_left(self):
        selections = self.selected_variables_listbox.curselection()
        selected_items = [self.selected_variables_listbox.get(index) for index in selections]

        for item in selected_items:
            self.available_variable_listbox.insert(tk.END, item)
            self.selected_variables.remove(item)

        self.reorder_available_variables_listbox_alphabetically()

        for index in reversed(selections):
            self.selected_variables_listbox.delete(index)


    def transfer_all_left(self):

        for i in range(self.selected_variables_listbox.size()):
            self.selected_variables_listbox.selection_set(i)

        selections = self.selected_variables_listbox.curselection()
        selected_items = [self.selected_variables_listbox.get(index) for index in selections]

        for item in selected_items:
            self.available_variable_listbox.insert(tk.END, item)
            self.selected_variables.remove(item)

        self.reorder_available_variables_listbox_alphabetically()

        for index in reversed(selections):
            self.selected_variables_listbox.delete(index)


    def reorder_available_variables_listbox_alphabetically(self):
        top_visible_index = self.available_variable_listbox.nearest(0)
        top_visible_item = self.available_variable_listbox.get(top_visible_index)

        items = list(self.available_variable_listbox.get(0, tk.END))
        items = sorted(items, key=lambda x: x.lower())

        self.available_variable_listbox.delete(0, tk.END)  # Clear the Listbox
        for item in items:
            self.available_variable_listbox.insert(tk.END, item)

        if top_visible_index >= 0:
            index = items.index(top_visible_item)
            self.available_variable_listbox.yview(index)




    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################

    # CREATE CONDITIONS SELECTION FRAME

    def create_conditions_frame(self):

        # VARIABLE NAME FRAME
        self.column_name_frame = tk.Frame(self.conditions_frame, bg='beige')
        self.column_name_frame.pack(side=tk.TOP, fill=tk.X)

        self.column_name_frame_label = tk.Label(self.column_name_frame, text="Name of new variable:", font=('Arial', 42, "bold"), background='beige', foreground='black')
        self.column_name_frame_label.pack(side=tk.TOP, fill=tk.X)


        self.column_name_entry = tk.Entry(self.column_name_frame, font=('Arial', 24))
        self.column_name_entry.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        separator = ttk.Separator(self.variable_options_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)


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

        self.condition_canvas = tk.Canvas(self.condition_options_frame, bg='yellow')
        self.scrollbar = tk.Scrollbar(self.condition_options_frame, orient="vertical", command=self.condition_canvas.yview)
        self.scrollable_frame = tk.Frame(self.condition_canvas, bg='yellow')



        self.condition_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.condition_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.condition_canvas.pack(side=tk.LEFT, fill="both", expand=True, padx=200, pady=50)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.scrollable_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)

        # Bind mouse wheel event to the canvas
        self.condition_canvas.bind("<MouseWheel>", on_mousewheel)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.condition_canvas.configure(
                scrollregion=self.condition_canvas.bbox("all")
            )
        )


        # NAVIGATION MENU

        self.conditions_menu_frame = tk.Frame(self.conditions_frame, bg='lightgray')
        self.conditions_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_column_selection_button = tk.Button(self.conditions_menu_frame, command=self.switch_to_variable_selection_frame, text="Back", font=("Arial", 36))
        self.return_to_column_selection_button.pack(side=tk.LEFT)

        self.advance_to_finalize_frame_button = tk.Button(self.conditions_menu_frame, command=self.switch_to_finalize_frame, text="Next", font=("Arial", 36))
        self.advance_to_finalize_frame_button.pack(side=tk.RIGHT)

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

                temp_df = self.df.copy().dropna(subset=[column_selected])

                is_numeric = pd.to_numeric(temp_df[column_selected], errors='coerce').notna().all()

                if is_numeric:

                    temp_df[column_selected] = temp_df[column_selected].astype(float)
                    self.q1 = np.percentile(temp_df[column_selected], 25)
                    self.q2 = np.percentile(temp_df[column_selected], 50)  # Median (Q2)
                    self.q3 = np.percentile(temp_df[column_selected], 75)

                    self.q1_string = f"q1-{self.q1}"
                    self.q2_string = f"q2-{self.q2}"
                    self.q3_string = f"q3-{self.q3}"


                    value_list = ['USER CHOICE'] + [self.q1_string, self.q2_string, self.q3_string] + list(self.df[column_selected].unique())
                else:
                    value_list = ['USER CHOICE'] + list(self.df[column_selected].unique())

                column_values_dropdown["values"] = value_list

            selected_column_option = tk.StringVar()
            column_dropdown = ttk.Combobox(condition_frame, textvariable=selected_column_option, values=self.selected_variables, state="readonly")
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
        new_value_frame.pack(pady=10, side=tk.TOP)

        # FRAME WHERE USER INPUTS WHAT THE VALUE WILL BE BASED ON THE CONDITIONS BELOW
        value_entry_frame = tk.Frame(new_value_frame)
        value_entry_frame.pack(side=tk.TOP)

        label = tk.Label(value_entry_frame, text="Value:")
        label.pack(side=tk.LEFT)

        value_entry = tk.Entry(value_entry_frame)
        value_entry.pack(side=tk.LEFT)
        value_entry.focus_set()

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
        self.new_df = self.df.copy()

        self.column_name = self.column_name_entry.get()

        for idx, frame in enumerate(self.value_frames, start=1):
            condition_list_total = []
            condition_strings = []


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
                        self.new_df[condition[1]] = self.new_df[condition[1]].astype(float)
                        condition_string = condition_string + str(float(condition[4]))
                    except:
                        self.new_df[condition[1]] = self.new_df[condition[1]].astype(object)
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
                            self.new_df[condition[1]] = self.new_df[condition[1]].astype(float)
                            condition_string = condition_string + str(float(condition[3]))

                    except:

                        self.new_df[condition[1]] = self.new_df[condition[1]].astype(object)
                        condition_string = condition_string + "'" + condition[3] + "'"

                condition_string = condition_string + ')'
                condition_strings.append(condition_string)


            final_condition_string = ''.join(condition_strings)
            self.new_df.loc[self.new_df.eval(final_condition_string), self.column_name] = condition_value


    def is_valid_column_name(self, column_name):
        def fix_columns(column_name):
            column_name = column_name.replace(' ', '_')
            column_name = column_name.replace('__', '_')
            column_name = column_name.replace('___', '_')
            return column_name

        column_name = fix_columns(column_name)

        # Define a regular expression pattern for a valid column name
        pattern = r'^[a-zA-Z0-9_\-]+$'

        if re.match(pattern, column_name):
            try:
                df = pd.DataFrame(columns=[column_name])
                return True
            except ValueError:
                return False
        else:
            return False

    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################

    # CREATE FINALIZE FRAME #

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

        self.new_df.loc[(self.new_df[self.column_name]=='n') | (self.new_df[self.column_name]=='nan'), self.column_name] = np.nan
        category_counts = self.new_df[self.column_name].value_counts()
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


    def update_dataframe(self):
        self.df = self.new_df.copy()

        def fix_columns(df):
            df.columns = df.columns.str.replace(' ', '_')
            df.columns = df.columns.str.replace('__', '_')
            df.columns = df.columns.str.replace('___', '_')
            df.columns = df.columns.str.replace(r'\W+', '', regex=True)

        fix_columns(self.df)

        data_manager.add_dataframe_to_dict(self.df, data_manager.get_dataframe_name())
        data_manager.set_dataframe(data_manager.get_dataframe_name())
        data_manager.add_df_update_status_to_dict("edit_tab", True)
        data_manager.add_df_update_status_to_dict("visualize_tab", True)

        utils.remove_frame_widgets(self.dataframe_content_frame)

        utils.create_table(self.dataframe_content_frame, self.df)
        summary_df = utils.create_summary_table(self.df)
        utils.create_table(self.dataframe_content_frame, summary_df, title="COLUMN SUMMARY TABLE")

        utils.show_message("Dataframe Update Status", "Database Has Been Updated")

        self.setup_dataframe_view_tab()


    def setup_dataframe_view_tab(self, initialize=True):
        df = data_manager.get_dataframe()
        if df is None:
            utils.show_message("Error", "Please open a file first.")
            return
        self.style.configure("file_button.TButton", background="gray")
        self.style.configure("dataframe_view_button.TButton", background="white")
        self.style.configure("edit_button.TButton", background="gray")
        self.style.configure("visualize_button.TButton", background="gray")

        utils.remove_frame_widgets(self.sub_button_frame)

        self.style.configure("save_file_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36))
        save_file_button = ttk.Button(self.sub_button_frame, text="Save File", style="save_file_button.TButton")
        save_file_button.pack(side="left", fill="both", expand=True)  # Set expand=True to fill the horizontal space
        save_file_button.config(command=lambda: file_handling.save_file(df))

        def initialize_dataframe_view_tab():
            utils.remove_frame_widgets(self.dataframe_content_frame)

            utils.create_table(self.dataframe_content_frame, df)
            summary_df = utils.create_summary_table(df)
            utils.create_table(self.dataframe_content_frame, summary_df, title="COLUMN SUMMARY TABLE")

            self.editing_content_frame.pack_forget()
            self.dataframe_content_frame.pack(fill=tk.BOTH, expand=True)

        def switch_to_dataframe_view_tab():
            self.editing_content_frame.pack_forget()
            self.dataframe_content_frame.pack(fill=tk.BOTH, expand=True)


        if initialize == True:
            initialize_dataframe_view_tab()
        if initialize == False:
            switch_to_dataframe_view_tab()

        self.dataframe_content_frame.update_idletasks()

    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################

    # NAVIGATION MENU HANDLING FUNCTIONS

    def switch_to_variable_selection_frame(self):
        self.conditions_frame.pack_forget()
        self.finalize_frame.pack_forget()
        self.variable_selection_frame.pack(fill=tk.BOTH, expand=True)

        self.variable_search_entry.focus_set()



    def switch_to_conditions_frame(self):
        if not self.selected_variables:
            return
        self.finalize_frame.pack_forget()
        self.variable_selection_frame.pack_forget()
        self.conditions_frame.pack(fill=tk.BOTH, expand=True)

        self.column_name_entry.focus_set()


    def switch_to_finalize_frame(self):
        if not self.column_name_entry.get():
            utils.show_message("Error", "Invalid Variable Name")
            return
        if self.column_name_entry.get().lower() in self.df.columns:
            same_column_name = utils.prompt_yes_no(f"CAUTION: The column, '{self.column_name_entry.get().lower()}' is already in the dataframe. Do you want to replace the old column?")
            if same_column_name:
                self.df = self.df.drop(self.column_name_entry.get(), axis=1)
            else:
                return
        if not self.is_valid_column_name(self.column_name_entry.get()):
            utils.show_message("Error", "Invalid Column Name")
            return
        try:
            self.get_values_from_frames()
            self.plot_new_column()

        except:
            utils.show_message("value error", "Error with conditions")
            raise

        self.conditions_frame.pack_forget()
        self.variable_selection_frame.pack_forget()
        self.finalize_frame.pack(fill=tk.BOTH, expand=True)

        self.editing_content_frame.update_idletasks()
