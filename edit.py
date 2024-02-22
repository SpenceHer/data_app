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
            style.configure(button_style, background=color_dict["active_subtab_bg"], foreground=color_dict["active_subtab_txt"], borderwidth=0, padding=0, font=styles.sub_tabs_font)
        else:
            style.configure(button_style, background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"], borderwidth=0, padding=0, font=styles.sub_tabs_font)

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

        self.editing_content_frame = editing_content_frame
        self.dataframe_content_frame = dataframe_content_frame
        self.sub_button_frame = sub_button_frame

        self.style = style

        style.configure("edit_data_button.TButton", background=color_dict["active_subtab_bg"], foreground=color_dict["active_subtab_txt"])
        style.configure("create_new_var_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"])

        data_manager.add_tab_to_tab_dict("current_edit_tab", "edit_data")

        self.selected_column = None
        self.selected_variable_type = None
        
        utils.remove_frame_widgets(self.editing_content_frame)


        self.variable_selection_frame = tk.Frame(self.editing_content_frame, bg=color_dict["main_content_border"])
        self.variable_type_choice_frame = tk.Frame(self.editing_content_frame, bg=color_dict["main_content_border"])
        self.value_handling_frame = tk.Frame(self.editing_content_frame, bg=color_dict["main_content_border"])
        self.data_display_frame = tk.Frame(self.editing_content_frame, bg=color_dict["main_content_border"])


        self.create_variable_selection_frame()
        self.create_variable_type_choice_frame()
        self.create_value_handling_frame()
        self.create_data_display_frame()

        self.switch_to_variable_selection_frame()


################################################################################################################
################################################################################################################
################################################################################################################


    # CREATE VARIABLE SELECTION FRAME

    def create_variable_selection_frame(self):

        # MAIN CONTENT FRAME
        self.variable_selection_inner_frame = tk.Frame(self.variable_selection_frame, bg=color_dict["main_content_bg"])
        self.variable_selection_inner_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)


################################################################################################################


        # VARIABLE SELECTION

        self.variable_selection_subframe_border = tk.Frame(self.variable_selection_inner_frame, bg=color_dict["sub_frame_border"])
        self.variable_selection_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.variable_selection_subframe = tk.Frame(self.variable_selection_subframe_border, bg=color_dict["sub_frame_bg"])
        self.variable_selection_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.variable_frame_label = tk.Label(self.variable_selection_subframe, text="Select A Variable to Edit", font=styles.sub_frame_header_font, bg=color_dict["sub_frame_bg"], fg=color_dict["sub_frame_header"])
        self.variable_frame_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.variable_selection_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)

        # VARIABLE SELECTION FRAME
        self.column_choice_frame = tk.Frame(self.variable_selection_subframe, bg=color_dict["sub_frame_bg"])
        self.column_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

        self.column_search_var = tk.StringVar()
        self.column_search_var.trace("w", self.update_variable_listbox)
        self.column_var_search_entry = tk.Entry(self.column_choice_frame, textvariable=self.column_search_var, font=styles.listbox_font)
        self.column_var_search_entry.pack(side=tk.TOP, pady=10)

        self.variable_listbox = tk.Listbox(self.column_choice_frame, selectmode=tk.SINGLE, font=styles.listbox_font, exportselection=False, bg=color_dict["listbox_bg"],
                     fg=color_dict["listbox_fg"],
                     highlightbackground=color_dict["listbox_highlight_bg"],
                     highlightcolor=color_dict["listbox_highlight_color"],
                     selectbackground=color_dict["listbox_select_bg"],
                     selectforeground=color_dict["listbox_select_fg"])
        self.variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)

        for column in sorted(self.df.columns, key=str.lower):
            self.variable_listbox.insert(tk.END, column)

        self.variable_listbox.bind("<<ListboxSelect>>", self.on_variable_listbox_select)



################################################################################################################

        # NAVIGATION MENU
        self.variable_selection_menu_frame = tk.Frame(self.variable_selection_inner_frame, bg=color_dict["nav_banner_bg"])
        self.variable_selection_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.advance_to_variable_type_choice_frame = ttk.Button(self.variable_selection_menu_frame, text="Next", command=self.switch_to_variable_type_choice_frame, style='nav_menu_button.TButton')
        self.advance_to_variable_type_choice_frame.pack(side=tk.RIGHT)

        self.variable_selection_menu_label = tk.Label(self.variable_selection_menu_frame, text="", font=styles.nav_menu_label_font, bg=color_dict["nav_banner_bg"], fg=color_dict["nav_banner_txt"])
        self.variable_selection_menu_label.pack(side=tk.RIGHT, expand=True)



################################################################################################################

    def on_variable_listbox_select(self, event):
        if self.variable_listbox.curselection():
            self.selected_column = self.variable_listbox.get(self.variable_listbox.curselection()[0])
            self.variable_selection_menu_label.config(text=f"Selected Variable: {self.selected_column}")


    def update_variable_listbox(self, *args):
        search_term = self.column_search_var.get().lower()
        self.variable_listbox.delete(0, tk.END)

        # Check if the search term is empty
        if search_term == "":
            # If search term is empty, insert all columns sorted alphabetically
            for column in sorted(self.df.columns, key=str.lower):
                self.variable_listbox.insert(tk.END, column)
        else:
            # If there is a search term, filter and sort the columns based on the search term
            filtered_sorted_columns = sorted([column for column in self.df.columns if search_term in column.lower()], key=str.lower)
            # Populate the Listbox with the sorted list
            for column in filtered_sorted_columns:
                self.variable_listbox.insert(tk.END, column)




################################################################################################################
################################################################################################################
################################################################################################################


    def create_variable_type_choice_frame(self):

        # MAIN CONTENT FRAME
        self.variable_type_inner_frame = tk.Frame(self.variable_type_choice_frame, bg=color_dict["main_content_bg"])
        self.variable_type_inner_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

################################################################################################################


        self.variable_type_selection_subframe_border = tk.Frame(self.variable_type_inner_frame, bg=color_dict["sub_frame_border"])
        self.variable_type_selection_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.variable_type_selection_subframe = tk.Frame(self.variable_type_selection_subframe_border, bg=color_dict["sub_frame_bg"])
        self.variable_type_selection_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.variable_type_frame_label = tk.Label(self.variable_type_selection_subframe, text="Choose Variable Type", font=styles.sub_frame_header_font, bg=color_dict["sub_frame_bg"], fg=color_dict["sub_frame_header"])
        self.variable_type_frame_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.variable_type_selection_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)


################################################################################################################

        self.variable_type_choice_button_frame = tk.Frame(self.variable_type_selection_subframe, bg=color_dict["sub_frame_bg"])
        self.variable_type_choice_button_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # CATEGORICAL VARIABLE BUTTON
        self.categorical_variable_frame = tk.Frame(self.variable_type_choice_button_frame, bg=color_dict["sub_frame_bg"])
        self.categorical_variable_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.categorical_variable_button = ttk.Button(self.categorical_variable_frame, text='Categorical Variable', style="inactive_radio_button.TButton")
        self.categorical_variable_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # CONTINUOUS VARIABLE BUTTON
        self.continuous_variable_frame = tk.Frame(self.variable_type_choice_button_frame, bg=color_dict["sub_frame_bg"])
        self.continuous_variable_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.continuous_variable_button = ttk.Button(self.continuous_variable_frame,text='Continuous Variable', style="inactive_radio_button.TButton")
        self.continuous_variable_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)


        self.continuous_variable_button.configure(command=lambda cb=self.continuous_variable_button, catb=self.categorical_variable_button: self.toggle_variable_type_button_style("Continuous", cb, catb))
        self.categorical_variable_button.configure(command=lambda cb=self.continuous_variable_button, catb=self.categorical_variable_button: self.toggle_variable_type_button_style("Categorical", cb, catb))


################################################################################################################


        # NAVIGATION MENU
        self.variable_type_choice_menu_frame = tk.Frame(self.variable_type_choice_frame, bg=color_dict["nav_banner_bg"])
        self.variable_type_choice_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_variable_selection_frame_button = ttk.Button(self.variable_type_choice_menu_frame, text="Back", command=self.switch_to_variable_selection_frame, style='nav_menu_button.TButton')
        self.return_to_variable_selection_frame_button.pack(side=tk.LEFT)

        self.advance_to_value_handling_frame_button = ttk.Button(self.variable_type_choice_menu_frame, text="Next", command=self.switch_to_value_handling_frame, style='nav_menu_button.TButton')
        self.advance_to_value_handling_frame_button.pack(side=tk.RIGHT)

        self.variable_type_choice_menu_frame_label = tk.Label(self.variable_type_choice_menu_frame, text="", font=styles.nav_menu_label_font, bg=color_dict["nav_banner_bg"], fg=color_dict["nav_banner_txt"])
        self.variable_type_choice_menu_frame_label.pack(side=tk.RIGHT, expand=True)

################################################################################################################

    def toggle_variable_type_button_style(self, selection, continuous_button, categorical_button):
        styles = {"Continuous": ("active_radio_button.TButton", "inactive_radio_button.TButton"),
                  "Categorical": ("inactive_radio_button.TButton", "active_radio_button.TButton")
                  }

        cont_style, cat_style = styles[selection]
        continuous_button.configure(style=cont_style)
        categorical_button.configure(style=cat_style)

        self.selected_variable_type = selection


################################################################################################################
################################################################################################################
################################################################################################################


    def create_value_handling_frame(self):

        # MAIN CONTENT FRAME
        self.value_handling_inner_frame, self.value_handling_canvas = utils.create_scrollable_frame(self.value_handling_frame)

################################################################################################################

        self.value_handling_subframe_border = tk.Frame(self.value_handling_inner_frame, bg=color_dict["sub_frame_border"])
        self.value_handling_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.value_handling_subframe = tk.Frame(self.value_handling_subframe_border, bg=color_dict["sub_frame_bg"])
        self.value_handling_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.value_handling_frame_label = tk.Label(self.value_handling_subframe, text="", font=styles.sub_frame_header_font, bg=color_dict["sub_frame_bg"], fg=color_dict["sub_frame_header"])
        self.value_handling_frame_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.value_handling_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)

        self.options_frame = tk.Frame(self.value_handling_subframe, bg=color_dict["sub_frame_bg"])
        self.options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

################################################################################################################


        # NAVIGATION MENU
        self.value_handling_menu_frame = tk.Frame(self.value_handling_frame, bg=color_dict["nav_banner_bg"])
        self.value_handling_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_variable_type_selection_frame_button = ttk.Button(self.value_handling_menu_frame, text="Back", command=self.switch_to_variable_type_choice_frame, style='nav_menu_button.TButton')
        self.return_to_variable_type_selection_frame_button.pack(side=tk.LEFT)

        self.advance_to_data_display_frame_button = ttk.Button(self.value_handling_menu_frame, text="Next", command=self.switch_to_data_display_frame, style='nav_menu_button.TButton')
        self.advance_to_data_display_frame_button.pack(side=tk.RIGHT)

        self.value_handling_menu_frame_label = tk.Label(self.value_handling_menu_frame, text=f"Selected Variable: {self.selected_column}", font=styles.nav_menu_label_font, bg=color_dict["nav_banner_bg"], fg=color_dict["nav_banner_txt"])
        self.value_handling_menu_frame_label.pack(side=tk.RIGHT, expand=True)



################################################################################################################

    # EDIT CATEGORICAL VARIABLE

    def edit_categorical_variable(self):
        
        utils.remove_frame_widgets(self.options_frame)

        self.value_handling_frame_label.configure(text="Categorical Variable Options")

        # TEMPORARY DATAFRAME
        self.temp_df = self.df.copy()

        self.temp_df[self.selected_column] = self.temp_df[self.selected_column].astype(str)
        self.temp_df.loc[self.temp_df[self.selected_column]=="nan", self.selected_column] = "[MISSING VALUE]"
        


        
        self.handle_categorical_values_frame = tk.Frame(self.options_frame, bg=color_dict["sub_frame_bg"])
        self.handle_categorical_values_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.left_frame = tk.Frame(self.handle_categorical_values_frame, bg=color_dict["sub_frame_bg"])
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(self.handle_categorical_values_frame, bg=color_dict["sub_frame_bg"])
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


        # UNIQUE VALUE LISTBOX
        self.value_listbox_frame = tk.Frame(self.left_frame, bg=color_dict["sub_frame_bg"])
        self.value_listbox_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        self.unique_categorical_values = sorted(self.temp_df[self.selected_column].unique())
        self.unique_categorical_values = [value for value in self.unique_categorical_values if value != 'nan']

        # Listbox label
        self.value_listbox_frame_label = tk.Label(self.value_listbox_frame, text="Unique Values", font=styles.sub_frame_sub_header_font, bg=color_dict["sub_frame_bg"], fg=color_dict["main_content_sub_header"])
        self.value_listbox_frame_label.pack(side=tk.TOP)

        separator = ttk.Separator(self.value_listbox_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.value_selection = tk.StringVar()
        self.value_choice_listbox = tk.Listbox(self.value_listbox_frame, font=styles.listbox_font, exportselection=False)
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
        self.value_choice_listbox.bind("<Enter>",lambda e: utils.bind_mousewheel_to_frame(self.value_handling_inner_frame, self.value_handling_canvas, False))
        self.value_choice_listbox.bind("<Leave>",lambda e: utils.bind_mousewheel_to_frame(self.value_handling_inner_frame, self.value_handling_canvas, True))



        # VALUE ACTIONS
        self.value_action_frame = tk.Frame(self.right_frame, bg=color_dict["sub_frame_bg"])
        self.value_action_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=25)

        # REMOVE OR CHANGE VALUE
        self.remove_change_value_action_frame = tk.Frame(self.value_action_frame, bg=color_dict["sub_frame_bg"])
        self.remove_change_value_action_frame.pack(side=tk.TOP, fill=tk.X, pady=25)

        self.handle_non_numeric_value_label = tk.Label(self.remove_change_value_action_frame, text="Handle Selected Value", font=styles.sub_frame_sub_header_font, fg=color_dict["main_content_sub_header"], bg=color_dict["sub_frame_bg"])
        self.handle_non_numeric_value_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        separator = ttk.Separator(self.remove_change_value_action_frame, orient="horizontal", style="Separator.TSeparator")
        separator.grid(row=1, column=0, columnspan=2, padx=100, pady=10, sticky="nsew")

        # Remove Value
        self.remove_button = ttk.Button(self.remove_change_value_action_frame, text="Remove Value", command=lambda: self.remove_categorical_value(), style="large_button.TButton")
        self.remove_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        # Change Value
        self.change_value_button = ttk.Button(self.remove_change_value_action_frame, text="Change Value To:", command=lambda: self.change_categorical_value(), style="large_button.TButton")
        self.change_value_button.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        self.new_value_entry = tk.Entry(self.remove_change_value_action_frame, font=("Arial", 24))
        self.new_value_entry.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        self.remove_change_value_action_frame.columnconfigure(0, weight=1)
        self.remove_change_value_action_frame.columnconfigure(1, weight=1)


        # RENAME COLUMN
        self.rename_column_frame = tk.Frame(self.value_action_frame, bg=color_dict["sub_frame_bg"])
        self.rename_column_frame.pack(side=tk.TOP, fill=tk.X, pady=25)

        self.rename_column_label = tk.Label(self.rename_column_frame, text="Rename Column", font=styles.sub_frame_sub_header_font, fg=color_dict["main_content_sub_header"], bg=color_dict["sub_frame_bg"])
        self.rename_column_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        separator = ttk.Separator(self.rename_column_frame, orient="horizontal", style="Separator.TSeparator")
        separator.grid(row=1, column=0, columnspan=2, padx=100, pady=10, sticky="nsew")


        self.rename_column_yes_button = ttk.Button(self.rename_column_frame, text="Yes", style="inactive_radio_button.TButton", command=lambda: self.toggle_rename_button_style("Yes"))
        self.rename_column_yes_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        self.rename_column_no_button = ttk.Button(self.rename_column_frame, text="No", style="inactive_radio_button.TButton", command=lambda: self.toggle_rename_button_style("No"))
        self.rename_column_no_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        self.rename_column_entry = tk.Entry(self.rename_column_frame, font=("Arial", 24), state=tk.DISABLED)
        self.rename_column_entry.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.toggle_rename_button_style("No")

        self.rename_column_frame.columnconfigure(0, weight=1)
        self.rename_column_frame.columnconfigure(1, weight=1)



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


    def toggle_rename_button_style(self, selected):
        if selected == "Yes":
            self.rename_column_yes_button.configure(style="active_radio_button.TButton")
            self.rename_column_no_button.configure(style="inactive_radio_button.TButton")
            self.rename_column_selection = "Yes"
            self.enable_rename_column()

        elif selected == "No":
            self.rename_column_yes_button.configure(style="inactive_radio_button.TButton")
            self.rename_column_no_button.configure(style="active_radio_button.TButton")
            self.rename_column_selection = "No"
            self.disable_rename_column()




    ################################################################################################################

    # CLEAN CONTINUOUS VARIABLE


    def edit_continuous_variable(self):
        
        utils.remove_frame_widgets(self.options_frame)

        self.value_handling_frame_label.configure(text="Continuous Variable Options")

        def is_float(value):
            try:
                float(value)
                return True
            except ValueError:
                return False

        # TEMPORARY DATAFRAME
        self.temp_df = self.df.copy()

        self.temp_df[self.selected_column] = self.temp_df[self.selected_column].astype(str)
        self.temp_df.loc[self.temp_df[self.selected_column]=="nan", self.selected_column] = "[MISSING VALUE]"

        self.non_numeric_values = [value for value in self.temp_df[self.selected_column] if not is_float(value)]
        self.unique_non_numeric_values = list(set(self.non_numeric_values))



        self.handle_continuous_values_frame = tk.Frame(self.options_frame, bg=color_dict["sub_frame_bg"])
        self.handle_continuous_values_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.left_frame = tk.Frame(self.handle_continuous_values_frame, bg=color_dict["sub_frame_bg"])
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(self.handle_continuous_values_frame, bg=color_dict["sub_frame_bg"])
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


        # NON NUMERIC LISTBOX
        self.value_listbox_frame = tk.Frame(self.left_frame, bg=color_dict["sub_frame_bg"])
        self.value_listbox_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        
        # Listbox label
        self.value_listbox_frame_label = tk.Label(self.value_listbox_frame, text="Non-Numeric Values", font=styles.sub_frame_sub_header_font, bg=color_dict["sub_frame_bg"], fg=color_dict["main_content_sub_header"])
        self.value_listbox_frame_label.pack(side=tk.TOP)

        self.value_selection = tk.StringVar()
        self.value_choice_listbox = tk.Listbox(self.value_listbox_frame, font=styles.listbox_font, exportselection=False)
        self.value_choice_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        for value in self.unique_non_numeric_values:
            self.value_choice_listbox.insert(tk.END, value)

        # Default value is first value
        self.value_choice_listbox.select_set(0)
        if len(self.unique_non_numeric_values) > 0:
            self.selected_value = tk.StringVar(value=self.unique_non_numeric_values[0])

        def on_value_choice_listbox_selection(event):
            selected_index = self.value_choice_listbox.curselection()
            if selected_index:
                self.selected_value = self.value_choice_listbox.get(selected_index[0])

        self.value_choice_listbox.bind("<<ListboxSelect>>", on_value_choice_listbox_selection)
        self.value_choice_listbox.bind("<Enter>",lambda e: utils.bind_mousewheel_to_frame(self.value_handling_inner_frame, self.value_handling_canvas, False))
        self.value_choice_listbox.bind("<Leave>",lambda e: utils.bind_mousewheel_to_frame(self.value_handling_inner_frame, self.value_handling_canvas, True))









        # VALUE ACTIONS
        self.value_action_frame = tk.Frame(self.right_frame, bg=color_dict["sub_frame_bg"])
        self.value_action_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=25)

        # REMOVE OR CHANGE VALUE
        self.remove_change_value_action_frame = tk.Frame(self.value_action_frame, bg=color_dict["sub_frame_bg"])
        self.remove_change_value_action_frame.pack(side=tk.TOP, fill=tk.X, pady=25)

        self.handle_non_numeric_value_label = tk.Label(self.remove_change_value_action_frame, text="Handle Selected Value", font=styles.sub_frame_sub_header_font, fg=color_dict["main_content_sub_header"], bg=color_dict["sub_frame_bg"])
        self.handle_non_numeric_value_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        separator = ttk.Separator(self.remove_change_value_action_frame, orient="horizontal", style="Separator.TSeparator")
        separator.grid(row=1, column=0, columnspan=2, padx=100, pady=10, sticky="nsew")

        # Remove Value
        self.remove_button = ttk.Button(self.remove_change_value_action_frame, text="Remove Value", command=lambda: self.remove_non_numeric_value(), style="large_button.TButton")
        self.remove_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        # Change Value
        self.change_value_button = ttk.Button(self.remove_change_value_action_frame, text="Change Value To:", command=lambda: self.change_non_numeric_value(), style="large_button.TButton")
        self.change_value_button.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        self.new_value_entry = tk.Entry(self.remove_change_value_action_frame, font=("Arial", 24))
        self.new_value_entry.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
        self.new_value_entry.focus_set()


        self.remove_change_value_action_frame.columnconfigure(0, weight=1)
        self.remove_change_value_action_frame.columnconfigure(1, weight=1)


        # REMOVE NEGATIVE VALUES
        self.remove_negative_values_frame = tk.Frame(self.value_action_frame, bg=color_dict["sub_frame_bg"])
        self.remove_negative_values_frame.pack(side=tk.TOP, fill=tk.X, pady=25)

        self.remove_negative_values_label = tk.Label(self.remove_negative_values_frame, text="Remove Negative Values", font=styles.sub_frame_sub_header_font, bg=color_dict["sub_frame_bg"], fg=color_dict["main_content_sub_header"])
        self.remove_negative_values_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        separator = ttk.Separator(self.remove_negative_values_frame, orient="horizontal", style="Separator.TSeparator")
        separator.grid(row=1, column=0, columnspan=2, padx=100, pady=10, sticky="nsew")

        self.remove_negative_values_yes_button = ttk.Button(self.remove_negative_values_frame, text="Yes", style="inactive_radio_button.TButton", command=lambda: self.toggle_remove_negatives_button_style("Yes"))
        self.remove_negative_values_yes_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        self.remove_negative_values_no_button = ttk.Button(self.remove_negative_values_frame, text="No", style="inactive_radio_button.TButton", command=lambda: self.toggle_remove_negatives_button_style("No"))
        self.remove_negative_values_no_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        self.remove_negative_values_entry = tk.Entry(self.remove_negative_values_frame, font=("Arial", 24))

        self.remove_negative_values_frame.columnconfigure(0, weight=1)
        self.remove_negative_values_frame.columnconfigure(1, weight=1)

        self.toggle_remove_negatives_button_style("No")


        # REMOVE ZERO VALUES
        self.remove_values_of_zero_frame = tk.Frame(self.value_action_frame, bg=color_dict["sub_frame_bg"])
        self.remove_values_of_zero_frame.pack(side=tk.TOP, fill=tk.X, pady=25)

        self.remove_values_of_zero_label = tk.Label(self.remove_values_of_zero_frame, text="Remove Values of Zero", font=styles.sub_frame_sub_header_font, bg=color_dict["sub_frame_bg"], fg=color_dict["main_content_sub_header"])
        self.remove_values_of_zero_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        separator = ttk.Separator(self.remove_values_of_zero_frame, orient="horizontal", style="Separator.TSeparator")
        separator.grid(row=1, column=0, columnspan=2, padx=100, pady=10, sticky="nsew")

        self.remove_values_of_zero_yes_button = ttk.Button(self.remove_values_of_zero_frame, text="Yes", style="inactive_radio_button.TButton", command=lambda: self.toggle_remove_zeros_button_style("Yes"))
        self.remove_values_of_zero_yes_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        self.remove_values_of_zero_no_button = ttk.Button(self.remove_values_of_zero_frame, text="No", style="inactive_radio_button.TButton", command=lambda: self.toggle_remove_zeros_button_style("No"))
        self.remove_values_of_zero_no_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        self.remove_values_of_zero_entry = tk.Entry(self.remove_values_of_zero_frame, font=("Arial", 24))

        self.remove_values_of_zero_frame.columnconfigure(0, weight=1)
        self.remove_values_of_zero_frame.columnconfigure(1, weight=1)

        self.toggle_remove_zeros_button_style("No")



        # RENAME COLUMN
        self.rename_column_frame = tk.Frame(self.value_action_frame, bg=color_dict["sub_frame_bg"])
        self.rename_column_frame.pack(side=tk.TOP, fill=tk.X, pady=25)

        self.rename_column_label = tk.Label(self.rename_column_frame, text="Rename Column", font=styles.sub_frame_sub_header_font, bg=color_dict["sub_frame_bg"], fg=color_dict["main_content_sub_header"])
        self.rename_column_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

        separator = ttk.Separator(self.rename_column_frame, orient="horizontal", style="Separator.TSeparator")
        separator.grid(row=1, column=0, columnspan=2, padx=100, pady=10, sticky="nsew")

        self.rename_column_yes_button = ttk.Button(self.rename_column_frame, text="Yes", style="inactive_radio_button.TButton", command=lambda: self.toggle_rename_button_style("Yes"))
        self.rename_column_yes_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        self.rename_column_no_button = ttk.Button(self.rename_column_frame, text="No", style="inactive_radio_button.TButton", command=lambda: self.toggle_rename_button_style("No"))
        self.rename_column_no_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        self.rename_column_entry = tk.Entry(self.rename_column_frame, font=("Arial", 24), state=tk.DISABLED)
        self.rename_column_entry.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.toggle_rename_button_style("No")


        self.rename_column_frame.columnconfigure(0, weight=1)
        self.rename_column_frame.columnconfigure(1, weight=1)





    def enable_rename_column(self):
        self.rename_column_entry.configure(state=tk.NORMAL)
        self.rename_column_entry.focus_set()

    def disable_rename_column(self):
        self.rename_column_entry.configure(state=tk.DISABLED)


    def toggle_remove_negatives_button_style(self, selected):
        if selected == "Yes":
            self.remove_negative_values_yes_button.configure(style="active_radio_button.TButton")
            self.remove_negative_values_no_button.configure(style="inactive_radio_button.TButton")
            self.remove_negatives_selection = "Yes"

        elif selected == "No":
            self.remove_negative_values_yes_button.configure(style="inactive_radio_button.TButton")
            self.remove_negative_values_no_button.configure(style="active_radio_button.TButton")
            self.remove_negatives_selection = "No"

    def toggle_remove_zeros_button_style(self, selected):
        if selected == "Yes":
            self.remove_values_of_zero_yes_button.configure(style="active_radio_button.TButton")
            self.remove_values_of_zero_no_button.configure(style="inactive_radio_button.TButton")
            self.remove_zeros_selection = "Yes"

        elif selected == "No":
            self.remove_values_of_zero_yes_button.configure(style="inactive_radio_button.TButton")
            self.remove_values_of_zero_no_button.configure(style="active_radio_button.TButton")
            self.remove_zeros_selection = "No"






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
        self.data_display_inner_frame, self.data_display_canvas = utils.create_scrollable_frame(self.data_display_frame)

################################################################################################################

        self.display_frame_subframe_border = tk.Frame(self.data_display_inner_frame, bg=color_dict["sub_frame_border"])
        self.display_frame_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.display_frame_subframe = tk.Frame(self.display_frame_subframe_border, bg=color_dict["sub_frame_bg"])
        self.display_frame_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.display_frame_subframe_label = tk.Label(self.display_frame_subframe, text="", font=styles.sub_frame_header_font, bg=color_dict["sub_frame_bg"], fg=color_dict["sub_frame_header"])
        self.display_frame_subframe_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.display_frame_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)

        self.display_frame = tk.Frame(self.display_frame_subframe, bg=color_dict["sub_frame_bg"])
        self.display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

################################################################################################################

        # NAVIGATION MENU
        self.data_display_menu_frame = tk.Frame(self.data_display_frame, bg=color_dict["nav_banner_bg"])
        self.data_display_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_value_handling_frame_button = ttk.Button(self.data_display_menu_frame, text="Back", command=self.switch_to_value_handling_frame, style='nav_menu_button.TButton')
        self.return_to_value_handling_frame_button.pack(side=tk.LEFT)

        self.update_dataframe_button = ttk.Button(self.data_display_menu_frame, text="Update Dataframe", command=self.update_dataframe, style='nav_menu_button.TButton')
        self.update_dataframe_button.pack(side=tk.RIGHT)

        self.data_display_menu_frame_label = tk.Label(self.data_display_menu_frame, text="", font=styles.nav_menu_label_font, bg=color_dict["nav_banner_bg"], fg=color_dict["nav_banner_txt"])
        self.data_display_menu_frame_label.pack(side=tk.RIGHT, expand=True)





    ################################################################################################################

    # CATEGORICAL BAR PLOT
    def create_categorical_variable_barplot(self):
        self.display_frame_subframe_label.configure(text="Updated Data Display")
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
        plt.title('')
        plt.xlabel('Categories')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
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
        if self.rename_column_selection == "Yes":

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

        utils.create_table(self.dataframe_content_frame, self.df, self.style)
        summary_df = utils.create_summary_table(self.df)
        utils.create_table(self.dataframe_content_frame, summary_df, self.style, title="COLUMN SUMMARY TABLE")

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

        self.style.configure("save_dataframe_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"], borderwidth=0, padding=0, font=styles.sub_tabs_font)
        self.style.map(
            "save_dataframe_button.TButton",
            background=[("active", color_dict["hover_subtab_bg"])],
            foreground=[("active", color_dict["hover_subtab_txt"])]
        )
        save_dataframe_button = ttk.Button(self.sub_button_frame, text="Save Dataframe", style="save_dataframe_button.TButton")
        save_dataframe_button.pack(side="left", fill="both", expand=True)  # Set expand=True to fill the horizontal space
        save_dataframe_button.config(command=lambda: file_handling.save_file(df))

        def initialize_dataframe_view_tab():
            utils.remove_frame_widgets(self.dataframe_content_frame)


            data_frame_border = tk.Frame(self.dataframe_content_frame, bg=color_dict["main_content_border"])
            data_frame_border.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

            data_inner_frame = tk.Frame(data_frame_border, bg=color_dict["main_content_bg"])
            data_inner_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

            # RAW DATA TABLE
            
            raw_data_table_subframe_border = tk.Frame(data_inner_frame, bg=color_dict["sub_frame_border"])
            raw_data_table_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

            raw_data_table_subframe = tk.Frame(raw_data_table_subframe_border, bg=color_dict["sub_frame_bg"])
            raw_data_table_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

            raw_data_table_subframe_label = tk.Label(raw_data_table_subframe, text="Raw Data", font=styles.sub_frame_header_font, bg=color_dict["sub_frame_bg"], fg=color_dict["sub_frame_header"])
            raw_data_table_subframe_label.pack(side=tk.TOP, pady=10)

            separator = ttk.Separator(raw_data_table_subframe, orient="horizontal", style="Separator.TSeparator")
            separator.pack(side=tk.TOP, fill=tk.X, padx=200)

            utils.create_table(raw_data_table_subframe, df, self.style)


            # SUMMARY DATA TABLE

            summary_df = utils.create_summary_table(df)

            summary_data_table_subframe_border = tk.Frame(data_inner_frame, bg=color_dict["sub_frame_border"])
            summary_data_table_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

            summary_data_table_subframe = tk.Frame(summary_data_table_subframe_border, bg=color_dict["sub_frame_bg"])
            summary_data_table_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

            summary_data_table_subframe_label = tk.Label(summary_data_table_subframe, text="Summary Data", font=styles.sub_frame_header_font, bg=color_dict["sub_frame_bg"], fg=color_dict["sub_frame_header"])
            summary_data_table_subframe_label.pack(side=tk.TOP, pady=10)

            separator = ttk.Separator(summary_data_table_subframe, orient="horizontal", style="Separator.TSeparator")
            separator.pack(side=tk.TOP, fill=tk.X, padx=200)

            utils.create_table(summary_data_table_subframe, summary_df, self.style)

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

    def switch_to_variable_selection_frame(self):
        self.variable_type_choice_frame.pack_forget()
        self.value_handling_frame.pack_forget()
        self.data_display_frame.pack_forget()
        self.variable_selection_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        self.editing_content_frame.update_idletasks()


    def switch_to_variable_type_choice_frame(self):
        if self.selected_column == None:
            utils.show_message("Error", "Please select a variable")
            return

        self.variable_type_choice_menu_frame_label.configure(text=f"Selected Variable: {self.selected_column}")
        self.value_handling_menu_frame_label.configure(text=f"Selected Variable: {self.selected_column}")


        
        self.variable_selection_frame.pack_forget()
        self.value_handling_frame.pack_forget()
        self.data_display_frame.pack_forget()
        self.variable_type_choice_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        self.editing_content_frame.update_idletasks()

    def switch_to_value_handling_frame(self):

        if self.selected_variable_type == None:
            utils.show_message("Error", "Please select a variable type")
            return

        if self.selected_variable_type == "Categorical":
            self.edit_categorical_variable()

        if self.selected_variable_type == "Continuous":
            self.edit_continuous_variable()

        self.variable_type_choice_frame.pack_forget()
        self.data_display_frame.pack_forget()
        self.value_handling_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        if self.new_value_entry:
            self.new_value_entry.focus_set()

        utils.bind_mousewheel_to_frame(self.value_handling_inner_frame, self.value_handling_canvas, True)
        self.editing_content_frame.update_idletasks()


    def switch_to_data_display_frame(self):
        if self.rename_column_selection == "Yes":
            if not self.is_valid_column_name(self.rename_column_entry.get()):
                utils.show_message("Error", "Invalid Column Name")
                return
            self.data_display_menu_frame_label.configure(text=f"New Column Name: {self.rename_column_entry.get()}")
        else:
            self.data_display_menu_frame_label.configure(text=f"Selected Variable: {self.selected_column}")

        self.new_df = self.temp_df.copy()


        if self.selected_variable_type == "Continuous":

            try:
                self.new_df[self.selected_column] = self.new_df[self.selected_column].astype(float)
            except:
                utils.show_message("error", "Please make sure all values are numerical")
                return
        
            if self.remove_zeros_selection == "Yes":
                self.remove_values_of_zero()
            if self.remove_negatives_selection == "Yes":
                self.remove_negative_values()
                
            self.create_continuous_variable_histogram()

        elif self.selected_variable_type == "Categorical":
            self.create_categorical_variable_barplot()

        self.variable_type_choice_frame.pack_forget()
        self.value_handling_frame.pack_forget()
        self.data_display_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        utils.bind_mousewheel_to_frame(self.data_display_inner_frame, self.data_display_canvas, True)
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

        style.configure("edit_data_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"])
        style.configure("create_new_var_button.TButton", background=color_dict["active_subtab_bg"], foreground=color_dict["active_subtab_txt"])

        data_manager.add_tab_to_tab_dict("current_edit_tab", "create_new_var")

        self.selected_variables = data_manager.get_create_var_tab_var_list()

        utils.remove_frame_widgets(self.editing_content_frame)

        self.variable_selection_frame = tk.Frame(self.editing_content_frame, bg=color_dict["main_content_border"])
        self.conditions_frame = tk.Frame(self.editing_content_frame, bg=color_dict["main_content_border"])
        self.finalize_frame = tk.Frame(self.editing_content_frame, bg=color_dict["main_content_border"])

        self.create_variable_selection_frame()
        self.create_conditions_frame()
        self.create_finalize_frame()


        self.switch_to_variable_selection_frame()


    ################################################################################################################
    ################################################################################################################
    ################################################################################################################

    # CREATE VARIABLE SELECTION FRAME

    def create_variable_selection_frame(self):

        # MAIN CONTENT FRAME
        self.variable_selection_inner_frame = tk.Frame(self.variable_selection_frame, bg=color_dict["main_content_bg"])
        self.variable_selection_inner_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

################################################################################################################

        self.variable_selection_subframe_border = tk.Frame(self.variable_selection_inner_frame, bg=color_dict["sub_frame_border"])
        self.variable_selection_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.variable_selection_subframe = tk.Frame(self.variable_selection_subframe_border, bg=color_dict["sub_frame_bg"])
        self.variable_selection_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.variable_selection_frame_label = tk.Label(self.variable_selection_subframe, text="Choose Variables to Use for New Variable", font=styles.sub_frame_header_font, bg=color_dict["sub_frame_bg"], fg=color_dict["sub_frame_header"])
        self.variable_selection_frame_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.variable_selection_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)

        self.variable_options_frame = tk.Frame(self.variable_selection_subframe, bg=color_dict["sub_frame_bg"])
        self.variable_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

################################################################################################################


        # AVAILABLE VARIABLES SELECTION FRAME
        self.variables_selection_frame = tk.Frame(self.variable_options_frame, bg=color_dict["sub_frame_bg"])
        self.variables_selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.available_variables_frame = tk.Frame(self.variables_selection_frame, bg=color_dict["sub_frame_bg"])
        self.available_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.available_variables_search_var = tk.StringVar()
        self.available_variables_search_var.trace("w", self.update_available_variables_listbox)
        self.variable_search_entry = tk.Entry(self.available_variables_frame, textvariable=self.available_variables_search_var, font=("Arial", 24))
        self.variable_search_entry.pack(side=tk.TOP, pady=10)

        self.available_variable_listbox = tk.Listbox(self.available_variables_frame, selectmode=tk.MULTIPLE, font=styles.listbox_font,
                                                                bg=color_dict["listbox_bg"],
                                                                fg=color_dict["listbox_fg"],
                                                                highlightbackground=color_dict["listbox_highlight_bg"],
                                                                highlightcolor=color_dict["listbox_highlight_color"],
                                                                selectbackground=color_dict["listbox_select_bg"],
                                                                selectforeground=color_dict["listbox_select_fg"]
                                                                )
        self.available_variable_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)

        for column in sorted(self.df.columns, key=str.lower):
            self.available_variable_listbox.insert(tk.END, column)



        # TRANSFER BUTTONS
        self.buttons_frame = tk.Frame(self.variables_selection_frame, bg=color_dict["sub_frame_bg"])
        self.buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Larger buttons with ">>>" and "<<<" symbols
        self.transfer_right_button = ttk.Button(self.buttons_frame, text="Transfer Right >>>", command=self.transfer_right, style="large_button.TButton")
        self.transfer_right_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.transfer_left_button = ttk.Button(self.buttons_frame, text="<<< Transfer Left", command=self.transfer_left, style="large_button.TButton")
        self.transfer_left_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)

        separator = ttk.Separator(self.buttons_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, pady=10)

        # Text buttons "Move All Right" and "Clear Selection"
        self.transfer_all_right_button = ttk.Button(self.buttons_frame, text="Select All", command=self.transfer_all_right, style="large_button.TButton")
        self.transfer_all_right_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)

        self.transfer_all_left_button = ttk.Button(self.buttons_frame, text="Clear Selection", command=self.transfer_all_left, style="large_button.TButton")
        self.transfer_all_left_button.pack(side=tk.TOP, pady=10, padx=10, fill=tk.X)



        # SELECTED VARIABLES FRAME
        self.selected_variables_frame = tk.Frame(self.variables_selection_frame, bg=color_dict["sub_frame_bg"])
        self.selected_variables_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.selected_variables_label = tk.Label(self.selected_variables_frame, text="Selected Variables", font=styles.sub_frame_sub_header_font, bg=color_dict["sub_frame_bg"], fg=color_dict["main_content_sub_header"])
        self.selected_variables_label.pack(side=tk.TOP, pady=10)

        self.selected_variables_listbox = tk.Listbox(self.selected_variables_frame, selectmode=tk.MULTIPLE, font=styles.listbox_font,
                                                                bg=color_dict["listbox_bg"],
                                                                fg=color_dict["listbox_fg"],
                                                                highlightbackground=color_dict["listbox_highlight_bg"],
                                                                highlightcolor=color_dict["listbox_highlight_color"],
                                                                selectbackground=color_dict["listbox_select_bg"],
                                                                selectforeground=color_dict["listbox_select_fg"]
                                                                )
        self.selected_variables_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=100, pady=10)

        if len(self.selected_variables) > 0:
            for var in self.selected_variables:
                self.selected_variables_listbox.insert(tk.END, var)
                self.available_variable_listbox.selection_set(sorted(self.df.columns, key=str.lower).index(var))
            selections = self.available_variable_listbox.curselection()
            for index in reversed(selections):
                self.available_variable_listbox.delete(index)



################################################################################################################


        # NAVIGATION MENU
        self.variable_selection_menu_frame = tk.Frame(self.variable_selection_frame, bg=color_dict["nav_banner_bg"])
        self.variable_selection_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.advance_to_conditions_button = ttk.Button(self.variable_selection_menu_frame, text="Next", command=self.switch_to_conditions_frame, style='nav_menu_button.TButton')
        self.advance_to_conditions_button.pack(side=tk.RIGHT)


################################################################################################################

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

        # MAIN CONTENT FRAME
        self.conditions_inner_frame, self.conditions_canvas = utils.create_scrollable_frame(self.conditions_frame)

################################################################################################################

        self.variable_name_frame_subframe_border = tk.Frame(self.conditions_inner_frame, bg=color_dict["sub_frame_border"])
        self.variable_name_frame_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.variable_name_frame_subframe = tk.Frame(self.variable_name_frame_subframe_border, bg=color_dict["sub_frame_bg"])
        self.variable_name_frame_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.variable_name_frame_subframe_label = tk.Label(self.variable_name_frame_subframe, text="Name of New Variable:", font=styles.sub_frame_header_font, bg=color_dict["sub_frame_bg"], fg=color_dict["sub_frame_header"])
        self.variable_name_frame_subframe_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.variable_name_frame_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)

        self.variable_name_frame = tk.Frame(self.variable_name_frame_subframe, bg=color_dict["sub_frame_bg"])
        self.variable_name_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.variable_name_entry = tk.Entry(self.variable_name_frame, font=('Arial', 24))
        self.variable_name_entry.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

################################################################################################################


        self.conditions_subframe_border = tk.Frame(self.conditions_inner_frame, bg=color_dict["sub_frame_border"])
        self.conditions_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.conditions_subframe = tk.Frame(self.conditions_subframe_border, bg=color_dict["sub_frame_bg"])
        self.conditions_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.conditions_subframe_label = tk.Label(self.conditions_subframe, text="Add Values to New Variable", font=styles.sub_frame_header_font, bg=color_dict["sub_frame_bg"], fg=color_dict["sub_frame_header"])
        self.conditions_subframe_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.conditions_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)

        # ADD/REMOVE CONDITIONS BUTTONS FRAME
        self.condition_buttons_frame = tk.Frame(self.conditions_subframe, bg=color_dict["sub_frame_bg"])
        self.condition_buttons_frame.pack(side=tk.TOP, fill=tk.X)

        self.add_new_value_button = ttk.Button(self.condition_buttons_frame, text='Add New Value', command=self.add_value_frame, style="large_button.TButton")
        self.add_new_value_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.remove_value_button = ttk.Button(self.condition_buttons_frame, text='Remove Value', command=self.remove_value_frame, style="large_button.TButton")
        self.remove_value_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        separator = ttk.Separator(self.conditions_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200, pady=5)


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




################################################################################################################

        # NAVIGATION MENU

        self.conditions_menu_frame = tk.Frame(self.conditions_frame, bg=color_dict["nav_banner_bg"])
        self.conditions_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_column_selection_button = ttk.Button(self.conditions_menu_frame, command=self.switch_to_variable_selection_frame, text="Back", style='nav_menu_button.TButton')
        self.return_to_column_selection_button.pack(side=tk.LEFT)

        self.advance_to_finalize_frame_button = ttk.Button(self.conditions_menu_frame, command=self.switch_to_finalize_frame, text="Next", style='nav_menu_button.TButton')
        self.advance_to_finalize_frame_button.pack(side=tk.RIGHT)

        self.conditions_frame.update_idletasks()

################################################################################################################

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
                separation_frame = tk.Frame(new_value_frame, bg=color_dict["sub_frame_bg"])
                separation_frame.pack(side=tk.TOP)

                condition_frames.append(separation_frame)
                if label == 'AND':
                    separation_label = tk.Label(separation_frame, text=label, bg=color_dict["sub_frame_bg"])
                    separation_label.pack(side=tk.TOP)
                    label = 'Where'

                if label == 'OR':
                    separation_label = tk.Label(separation_frame, text=label, bg=color_dict["sub_frame_bg"])
                    separation_label.pack(side=tk.TOP)
                    label = 'Where'


            condition_frame = tk.Frame(new_value_frame, bg=color_dict["sub_frame_bg"])
            condition_frame.pack(side=tk.TOP)

            condition_frames.append(condition_frame)

            condition_label = tk.Label(condition_frame, text=label, bg=color_dict["sub_frame_bg"])
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


                    value_list = ["USER CHOICE", "[MISSING VALUE]"] + [self.q1_string, self.q2_string, self.q3_string] + list(temp_df[column_selected].unique())
                else:
                    value_list = ["USER CHOICE", "[MISSING VALUE]"] + list(temp_df[column_selected].unique())

                column_values_dropdown["values"] = value_list

            selected_column_option = tk.StringVar()
            column_dropdown = ttk.Combobox(condition_frame, textvariable=selected_column_option, values=self.selected_variables, state="readonly")
            column_dropdown.pack(side=tk.LEFT)
            column_dropdown.bind("<<ComboboxSelected>>", on_combobox_select)
            column_dropdown.bind("<Enter>",lambda e: utils.bind_mousewheel_to_frame(self.conditions_inner_frame, self.conditions_canvas, False))
            column_dropdown.bind("<Leave>",lambda e: utils.bind_mousewheel_to_frame(self.conditions_inner_frame, self.conditions_canvas, True))


            # CONDITION SIGN DROPDOWN
            selected_condition_sign = tk.StringVar()
            selected_condition_sign_dropdown = ttk.Combobox(condition_frame, textvariable=selected_condition_sign, values=self.condition_signs, state="readonly")
            selected_condition_sign_dropdown.pack(side=tk.LEFT)
            selected_condition_sign_dropdown.bind("<Enter>",lambda e: utils.bind_mousewheel_to_frame(self.conditions_inner_frame, self.conditions_canvas, False))
            selected_condition_sign_dropdown.bind("<Leave>",lambda e: utils.bind_mousewheel_to_frame(self.conditions_inner_frame, self.conditions_canvas, True))



            # VALUE SELECTION DROPDOWN
            selected_value = tk.StringVar()
            value_list = []
            column_values_dropdown = ttk.Combobox(condition_frame, textvariable=selected_value, values=value_list, state="readonly")
            column_values_dropdown.pack(side=tk.LEFT)
            column_values_dropdown.bind("<Enter>",lambda e: utils.bind_mousewheel_to_frame(self.conditions_inner_frame, self.conditions_canvas, False))
            column_values_dropdown.bind("<Leave>",lambda e: utils.bind_mousewheel_to_frame(self.conditions_inner_frame, self.conditions_canvas, True))


            # USER ENTRY VALUE
            user_entry_value = tk.Entry(condition_frame)
            user_entry_value.pack(side=tk.LEFT)






        # NEW VALUE FRAME
        new_value_frame = tk.Frame(self.conditions_subframe, bg=color_dict["sub_frame_bg"])
        new_value_frame.pack(pady=10, side=tk.TOP)

        # FRAME WHERE USER INPUTS WHAT THE VALUE WILL BE BASED ON THE CONDITIONS BELOW
        value_entry_frame = tk.Frame(new_value_frame, bg=color_dict["sub_frame_bg"])
        value_entry_frame.pack(side=tk.TOP)

        label = tk.Label(value_entry_frame, text="New Value:", bg=color_dict["sub_frame_bg"], font=styles.main_content_regular_text_font)
        label.pack(side=tk.LEFT)

        value_entry = tk.Entry(value_entry_frame)
        value_entry.pack(side=tk.LEFT)
        value_entry.focus_set()

        # FRAME WHERE THE USER CAN ADD OR REMOVE MORE CONDITIONS
        condition_handling_frame = tk.Frame(new_value_frame, bg=color_dict["sub_frame_bg"])
        condition_handling_frame.pack(side=tk.TOP)

        add_simple_and_button = ttk.Button(condition_handling_frame, text='and', command=lambda: add_condition(label='and'), style="small_button.TButton")
        add_simple_and_button.pack(side=tk.LEFT)

        add_simple_or_button = ttk.Button(condition_handling_frame, text='or', command=lambda: add_condition(label='or'), style="small_button.TButton")
        add_simple_or_button.pack(side=tk.LEFT)

        # add_major_and_button = tk.Button(condition_handling_frame, text='AND', command=lambda: add_condition(label='AND'))
        # add_major_and_button.pack(side=tk.LEFT)

        # add_major_or_button = tk.Button(condition_handling_frame, text='OR', command=lambda: add_condition(label='OR'))
        # add_major_or_button.pack(side=tk.LEFT)

        add_remove_button = ttk.Button(condition_handling_frame, text='Remove Condition', command=remove_condition, style="small_button.TButton")
        add_remove_button.pack(side=tk.LEFT)

        # FRAME WHERE THE USER EDITS THE CONDITIONS
        add_condition(label='Where')

        separator = ttk.Separator(new_value_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.value_frames.append(new_value_frame)





    def remove_value_frame(self):

        if self.value_frames:
            frame = self.value_frames.pop()
            frame.destroy()


    def get_values_from_frames(self):
        self.new_df = self.df.copy()

        self.column_name = self.variable_name_entry.get()

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

                if subframe_number == 4:
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

                elif condition[3] == "[MISSING VALUE]":
                    
                    if self.condition_signs_dict[condition[2]] == "==":
                        condition_string = condition_string[:-2] + ".isnull()==True"
                    elif self.condition_signs_dict[condition[2]] == "!=":
                        condition_string = condition_string[:-2] + ".isnull()==False"


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

        # MAIN CONTENT FRAME
        self.data_display_inner_frame, self.data_display_canvas = utils.create_scrollable_frame(self.finalize_frame)

################################################################################################################


        # RESULTS TABLE DISPLAY FRAME
        self.finalize_display_subframe_border = tk.Frame(self.data_display_inner_frame, bg=color_dict["sub_frame_border"])
        self.finalize_display_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        self.finalize_display_subframe = tk.Frame(self.finalize_display_subframe_border, bg=color_dict["sub_frame_bg"])
        self.finalize_display_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.finalize_display_label = tk.Label(self.finalize_display_subframe, text="", font=styles.sub_frame_header_font, fg=color_dict["sub_frame_header"], bg=color_dict["sub_frame_bg"])
        self.finalize_display_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(self.finalize_display_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)


        self.results_display_frame = tk.Frame(self.finalize_display_subframe, bg=color_dict["sub_frame_bg"])
        self.results_display_frame.pack(side=tk.TOP, pady=10)




################################################################################################################

        # MENU FRAME
        self.finalize_menu_frame = tk.Frame(self.finalize_frame, bg=color_dict["nav_banner_bg"])
        self.finalize_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_conditions_button = ttk.Button(self.finalize_menu_frame, command=self.switch_to_conditions_frame, text='Back', style='nav_menu_button.TButton')
        self.return_to_conditions_button.pack(side=tk.LEFT)

        self.return_to_conditions_button = ttk.Button(self.finalize_menu_frame, command=self.update_dataframe, text='Update Dataframe', style='nav_menu_button.TButton')
        self.return_to_conditions_button.pack(side=tk.RIGHT)







################################################################################################################


    def plot_new_column(self):
        for widget in self.results_display_frame.winfo_children():
            widget.destroy()

        self.new_df.loc[(self.new_df[self.column_name]=='n') | (self.new_df[self.column_name]=='nan'), self.column_name] = np.nan
        category_counts = self.new_df[self.column_name].value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))
        category_counts.plot(kind='bar', color='skyblue', ax=ax)

        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')

        

        plt.xticks(rotation=90)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.results_display_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.X)


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

        utils.create_table(self.dataframe_content_frame, self.df, self.style)
        summary_df = utils.create_summary_table(self.df)
        utils.create_table(self.dataframe_content_frame, summary_df, self.style, title="COLUMN SUMMARY TABLE")

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

        self.style.configure("save_dataframe_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"], borderwidth=0, padding=0, font=styles.sub_tabs_font)
        self.style.map(
            "save_dataframe_button.TButton",
            background=[("active", color_dict["hover_subtab_bg"])],
            foreground=[("active", color_dict["hover_subtab_txt"])]
        )
        save_dataframe_button = ttk.Button(self.sub_button_frame, text="Save Dataframe", style="save_dataframe_button.TButton")
        save_dataframe_button.pack(side="left", fill="both", expand=True)  # Set expand=True to fill the horizontal space
        save_dataframe_button.config(command=lambda: file_handling.save_file(df))

        def initialize_dataframe_view_tab():
            utils.remove_frame_widgets(self.dataframe_content_frame)


            data_frame_border = tk.Frame(self.dataframe_content_frame, bg=color_dict["main_content_border"])
            data_frame_border.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

            data_inner_frame = tk.Frame(data_frame_border, bg=color_dict["main_content_bg"])
            data_inner_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

            # RAW DATA TABLE
            
            raw_data_table_subframe_border = tk.Frame(data_inner_frame, bg=color_dict["sub_frame_border"])
            raw_data_table_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

            raw_data_table_subframe = tk.Frame(raw_data_table_subframe_border, bg=color_dict["sub_frame_bg"])
            raw_data_table_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

            raw_data_table_subframe_label = tk.Label(raw_data_table_subframe, text="Raw Data", font=styles.sub_frame_header_font, bg=color_dict["sub_frame_bg"], fg=color_dict["sub_frame_header"])
            raw_data_table_subframe_label.pack(side=tk.TOP, pady=10)

            separator = ttk.Separator(raw_data_table_subframe, orient="horizontal", style="Separator.TSeparator")
            separator.pack(side=tk.TOP, fill=tk.X, padx=200)

            utils.create_table(raw_data_table_subframe, df, self.style)


            # SUMMARY DATA TABLE

            summary_df = utils.create_summary_table(df)

            summary_data_table_subframe_border = tk.Frame(data_inner_frame, bg=color_dict["sub_frame_border"])
            summary_data_table_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

            summary_data_table_subframe = tk.Frame(summary_data_table_subframe_border, bg=color_dict["sub_frame_bg"])
            summary_data_table_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

            summary_data_table_subframe_label = tk.Label(summary_data_table_subframe, text="Summary Data", font=styles.sub_frame_header_font, bg=color_dict["sub_frame_bg"], fg=color_dict["sub_frame_header"])
            summary_data_table_subframe_label.pack(side=tk.TOP, pady=10)

            separator = ttk.Separator(summary_data_table_subframe, orient="horizontal", style="Separator.TSeparator")
            separator.pack(side=tk.TOP, fill=tk.X, padx=200)

            utils.create_table(summary_data_table_subframe, summary_df, self.style)

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
        self.variable_selection_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        self.variable_search_entry.focus_set()



    def switch_to_conditions_frame(self):
        if not self.selected_variables:
            return
        self.finalize_frame.pack_forget()
        self.variable_selection_frame.pack_forget()
        self.conditions_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        utils.bind_mousewheel_to_frame(self.conditions_inner_frame, self.conditions_canvas, True)
        self.editing_content_frame.update_idletasks()

        self.variable_name_entry.focus_set()


    def switch_to_finalize_frame(self):

        if not self.variable_name_entry.get():
            utils.show_message("Error", "Invalid Variable Name")
            return
        if self.variable_name_entry.get().lower() in self.df.columns:
            same_column_name = utils.prompt_yes_no(f"CAUTION: The column, '{self.variable_name_entry.get().lower()}' is already in the dataframe. Do you want to replace the old column?")
            if same_column_name:
                self.df = self.df.drop(self.variable_name_entry.get(), axis=1)
            else:
                return
        if not self.is_valid_column_name(self.variable_name_entry.get()):
            utils.show_message("Error", "Invalid Column Name")
            return
        try:
            self.get_values_from_frames()
            self.finalize_display_label.configure(text=f"Frequency Bar Chart of {self.column_name}")
            self.plot_new_column()

        except:
            utils.show_message("value error", "Error with conditions")
            raise

        self.conditions_frame.pack_forget()
        self.variable_selection_frame.pack_forget()
        self.finalize_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        utils.bind_mousewheel_to_frame(self.data_display_inner_frame, self.data_display_canvas, True)

        self.editing_content_frame.update_idletasks()
