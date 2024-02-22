from math import exp
import tkinter as tk
from tkinter import LEFT, ttk
from tkinter import filedialog, messagebox
import utils
import pandas as pd
import data_manager
import os
import styles
from styles import color_dict

def setup_file_tab(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame, initialize=True):

    for button_style in ["file_button.TButton", "dataframe_view_button.TButton", "edit_button.TButton", "visualize_button.TButton"]:
        style.map(
            button_style,
            background=[("active", color_dict["hover_main_tab_bg"])],
            foreground=[("active", color_dict["hover_main_tab_txt"])]
        )
    
    style.configure("file_button.TButton", background=color_dict["active_main_tab_bg"], foreground=color_dict["active_main_tab_txt"])
    style.configure("dataframe_view_button.TButton", background=color_dict["inactive_main_tab_bg"], foreground=color_dict["inactive_main_tab_txt"])
    style.configure("edit_button.TButton", background=color_dict["inactive_main_tab_bg"], foreground=color_dict["inactive_main_tab_txt"])
    style.configure("visualize_button.TButton", background=color_dict["inactive_main_tab_bg"], foreground=color_dict["inactive_main_tab_txt"])

    utils.remove_frame_widgets(sub_button_frame)



    manage_dataframes_button = ttk.Button(sub_button_frame, text="Comparison Table", style="comparison_table_button.TButton")
    manage_dataframes_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    manage_dataframes_button.config(command=lambda: ComparisonTableClass(file_handling_content_frame, style))

    create_dataframe_button = ttk.Button(sub_button_frame, text="Regression", style="regression_button.TButton")
    create_dataframe_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
    create_dataframe_button.config(command=lambda: RegressionAnalysisClass(file_handling_content_frame, style))


    dataframe_content_frame.pack_forget()
    editing_content_frame.pack_forget()
    visualize_content_frame.pack_forget()
    file_handling_content_frame.pack(fill=tk.BOTH, expand=True)

    if initialize==True:
        SetupFileTabClass(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame, initialize)

    def switch_to_file_tab():
        utils.remove_frame_widgets(sub_button_frame)

        if data_manager.get_dataframe_name():
            sub_button_frame_label = tk.Label(sub_button_frame, text=f"Current Dataframe: {data_manager.get_dataframe_name()}", font=("Arial", 36), bg="white")
            sub_button_frame_label.pack(fill=tk.BOTH, expand=True)

        dataframe_content_frame.pack_forget()
        editing_content_frame.pack_forget()
        visualize_content_frame.pack_forget()
        file_handling_content_frame.pack(fill=tk.BOTH, expand=True)

    df = data_manager.get_dataframe()

    if df is None:
        return
    else:
        switch_to_file_tab()

    







###################################################################################################################################################################################################
###################################################################################################################################################################################################
###################################################################################################################################################################################################



class SetupFileTabClass():
    def __init__(self, style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame, initialize):
        self.sub_button_frame = sub_button_frame
        self.dataframe_content_frame = dataframe_content_frame
        self.file_handling_content_frame = file_handling_content_frame
        self.editing_content_frame = editing_content_frame
        self.visualize_content_frame = visualize_content_frame
        self.style = style

        self.selected_dataframe = None


        self.create_main_frame()




    def create_main_frame(self):

        self.file_handling_content_frame.pack(fill=tk.BOTH, expand=True)
        self.style.configure("open_file_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 48))

        # LEFT FRAME
        self.left_file_menu_frame = tk.Frame(self.file_handling_content_frame, bg='beige')
        self.left_file_menu_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.open_file_button = tk.Button(self.left_file_menu_frame, text="Open New File", font=("Arial", 48))
        self.open_file_button.pack(side=tk.TOP, padx=10, pady=10)  # Set expand=True to fill the horizontal space
        self.open_file_button.config(command=self.open_file)

        separator = ttk.Separator(self.left_file_menu_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=50, pady=5)

        self.dataframe_list_label = tk.Label(self.left_file_menu_frame, text="List of Dataframes", font=("Arial", 36, "bold"), bg="beige")
        self.dataframe_list_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        separator = ttk.Separator(self.left_file_menu_frame, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=50, pady=5)

        self.dataframe_choice_submit_button = tk.Button(self.left_file_menu_frame, text="Change Dataframe", font=("Arial", 28), command=self.update_dataframe)
        self.dataframe_choice_submit_button.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        self.dataframe_listbox = tk.Listbox(self.left_file_menu_frame, font=("Arial", 36))
        self.dataframe_listbox.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)
        self.dataframe_listbox.bind("<<ListboxSelect>>", self.on_dataframe_listbox_select)





        # RIGHT FRAME
        self.right_file_menu_frame = tk.Frame(self.file_handling_content_frame, bg=color_dict["background_frame_bg"])
        self.right_file_menu_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_new_dataframe_button_frame = tk.Frame(self.right_file_menu_frame)
        self.create_new_dataframe_button_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_new_dataframe_button = tk.Button(self.create_new_dataframe_button_frame, text="Create New Custom Dataframe\n\n(Select from available dataframes)", font=("Arial", 48), command=self.create_new_dataframe)
        self.create_new_dataframe_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def on_dataframe_listbox_select(self, event):
        if self.dataframe_listbox.curselection():
            self.selected_dataframe = self.dataframe_listbox.get(self.dataframe_listbox.curselection()[0])
        else:
            return

    def update_dataframe(self):
        # CHECK TO MAKE SURE USER ACTUALLY WANTS TO CHANGE THE DATAFRAME
        result = messagebox.askyesno("Confirmation", "WARNING: changing dataframes will reset all other tabs. Are you sure you want to continue?")

        if result:
            data_manager.set_dataframe_name(self.selected_dataframe)
            data_manager.set_dataframe(data_manager.get_dataframe_name())


            utils.remove_frame_widgets(self.dataframe_content_frame)

            utils.create_table(self.dataframe_content_frame, data_manager.get_dataframe(), self.style)
            summary_df = utils.create_summary_table(data_manager.get_dataframe())
            utils.create_table(self.dataframe_content_frame, summary_df, self.style, title="COLUMN SUMMARY TABLE")
            setup_dataframe_view_tab(self.style, self.sub_button_frame, self.dataframe_content_frame, self.file_handling_content_frame, self.editing_content_frame, self.visualize_content_frame, initialize=False)
            utils.remove_frame_widgets(self.editing_content_frame)
            utils.remove_frame_widgets(self.visualize_content_frame)
        else:
            return















    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################




    def open_file(self):
        # Specify the path of the specific dataframe file you want to load
        # self.file_path = filedialog.askopenfilename()
        self.file_path = "/Users/spencersmith/Desktop/coding/OHSU_data.xlsx"

        try:
            if self.file_path.endswith('.xlsx'):
                self.df = pd.read_excel(self.file_path)
                # self.df.fillna("[MISSING VALUE]", inplace=True)
            else:
                self.df = pd.read_csv(self.file_path)
                # self.df.fillna("[MISSING VALUE]", inplace=True)
        except:
            utils.show_message('error loading', 'Error Reading File')
            raise

        def fix_columns(df):
                df.columns = df.columns.str.replace(' ', '_')
                df.columns = df.columns.str.replace('__', '_')
                df.columns = df.columns.str.replace('___', '_')
                df.columns = df.columns.str.replace(r'\W+', '', regex=True)

        fix_columns(self.df)

        dataframe_name = os.path.basename(self.file_path)

        data_manager.set_dataframe_name(dataframe_name)
        data_manager.add_dataframe_to_dict(self.df, dataframe_name)
        data_manager.set_dataframe(dataframe_name)  # Set the df variable




        self.update_dataframe_listbox()

        setup_dataframe_view_tab(self.style, self.sub_button_frame, self.dataframe_content_frame, self.file_handling_content_frame, self.editing_content_frame, self.visualize_content_frame, initialize=True)
        utils.remove_frame_widgets(self.editing_content_frame)
        utils.remove_frame_widgets(self.visualize_content_frame)


    def update_dataframe_listbox(self):
        self.dataframe_listbox.delete(0, tk.END)
        for key, value in data_manager.get_df_dict().items():
            self.dataframe_listbox.insert(tk.END, key)













    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################

    def create_new_dataframe(self):
        self.df = data_manager.get_dataframe()
        if self.df is None:
            utils.show_message("Error", "Please open a file first.")
            return
        if self.selected_dataframe is None:
            utils.show_message("Error", "Select A Dataframe from the Left First")
            return

        self.df = data_manager.get_df_dict()[self.selected_dataframe]



        self.column_selection_frame = tk.Frame(self.right_file_menu_frame, bg='beige')
        self.dataframe_settings_frame = tk.Frame(self.right_file_menu_frame, bg='beige')

        self.create_column_selection_frame()
        self.create_dataframe_settings_frame()



        self.df_in_use_column_selection_menu_label.configure(text=f"USING: {self.selected_dataframe}")
        self.df_in_use_dataframe_settings_menu_label.configure(text=f"USING: {self.selected_dataframe}")

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
        self.search_entry = tk.Entry(self.available_columns_frame, textvariable=self.available_column_search_var, font=("Arial", 24))
        self.search_entry.pack(side=tk.TOP, pady=5)


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

        self.return_to_create_new_dataframe_button = tk.Button(self.column_selection_menu_frame, command=self.switch_to_create_new_dataframe_button_frame, text="Back", font=("Arial", 36))
        self.return_to_create_new_dataframe_button.pack(side=tk.LEFT)

        self.advance_to_dataframe_settings_button = tk.Button(self.column_selection_menu_frame, command=self.switch_to_dataframe_settings_frame, text="Next", font=("Arial", 36))
        self.advance_to_dataframe_settings_button.pack(side=tk.RIGHT)

        self.df_in_use_column_selection_menu_label = tk.Label(self.column_selection_menu_frame, text="", font=("Arial", 36), bg='lightgray')
        self.df_in_use_column_selection_menu_label.pack(side=tk.RIGHT, expand=True)


        self.search_entry.focus_set()

        print(self.column_selection_frame.focus_get())






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


    def create_dataframe_settings_frame(self):

        # VARIABLE NAME FRAME
        self.dataframe_name_frame = tk.Frame(self.dataframe_settings_frame, bg='beige')
        self.dataframe_name_frame.pack(side=tk.TOP, fill=tk.X)

        self.dataframe_name_frame_label = tk.Label(self.dataframe_name_frame, text="Name of New Dataframe:", font=('Arial', 42), background='beige', foreground='black')
        self.dataframe_name_frame_label.pack(side=tk.TOP, fill=tk.X)

        self.dataframe_name_entry = tk.Entry(self.dataframe_name_frame, font=('Arial', 24))
        self.dataframe_name_entry.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.dataframe_name_entry.focus_set()


        # CONDITIONS OPTIONS FRAME
        self.condition_frames = []
        self.condition_signs = ['Equals', 'Does Not Equal', 'Less Than', 'Greater Than', 'Less Than or Equal To', 'Greater Than or Equal To', 'Contains', 'Does Not Contain']
        self.condition_signs_dict = {'Equals':'==',
                                     'Does Not Equal':'!=',
                                     'Less Than':'<',
                                     'Greater Than':'>',
                                     'Less Than or Equal To':'<=',
                                     'Greater Than or Equal To':'>='}

        self.condition_options_frame = tk.Frame(self.dataframe_settings_frame, bg='beige')
        self.condition_options_frame.pack(side=tk.TOP)


        # FRAME WHERE THE USER CAN ADD OR REMOVE MORE CONDITIONS
        self.condition_handling_frame = tk.Frame(self.condition_options_frame)
        self.condition_handling_frame.pack(side=tk.TOP)

        add_simple_and_button = tk.Button(self.condition_handling_frame, text='and', command=lambda: self.add_condition(label='and'))
        add_simple_and_button.pack(side=tk.LEFT)

        add_simple_or_button = tk.Button(self.condition_handling_frame, text='or', command=lambda: self.add_condition(label='or'))
        add_simple_or_button.pack(side=tk.LEFT)

        add_remove_button = tk.Button(self.condition_handling_frame, text='Remove Condition', command=self.remove_condition)
        add_remove_button.pack(side=tk.LEFT)


        # FRAME WHERE THE CONDITIONS GO
        self.conditions_frame = tk.Frame(self.condition_options_frame)
        self.conditions_frame.pack(side=tk.TOP)


        # SUBMIT SETTINGS BUTTON
        self.submit_settings_button = tk.Button(self.condition_options_frame, text="SUBMIT AND CREATE NEW DATAFRAME", font=("Arial", 36), command=self.submit_dataframe_settings)
        self.submit_settings_button.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=30, pady=30)


        # MENU FRAME
        self.dataframe_settings_menu = tk.Frame(self.dataframe_settings_frame, bg='lightgray')
        self.dataframe_settings_menu.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_column_selection_button = tk.Button(self.dataframe_settings_menu, command=self.switch_to_column_selection_frame, text="Back", font=("Arial", 36))
        self.return_to_column_selection_button.pack(side=tk.LEFT)

        self.df_in_use_dataframe_settings_menu_label = tk.Label(self.dataframe_settings_menu, text="", font=("Arial", 36), bg='lightgray')
        self.df_in_use_dataframe_settings_menu_label.pack(side=tk.RIGHT, expand=True)






    # REMOVE MOST RECENT CONDITION LINE
    def remove_condition(self):
        if len(self.condition_frames) > 1:
            frame = self.condition_frames.pop()

            if self.condition_frames and self.condition_frames[-1].winfo_children()[0].cget("text") in {'AND', 'OR'}:
                separation_frame = self.condition_frames.pop()
                separation_frame.destroy()
            frame.destroy()

        else:
            return

    # ADD NEW CONDITION LINE
    def add_condition(self, label=''):

        condition_frame = tk.Frame(self.conditions_frame)
        condition_frame.pack(side=tk.TOP)

        self.condition_frames.append(condition_frame)

        condition_label = tk.Label(condition_frame, text=label)
        condition_label.pack(side=tk.LEFT)


        # COLUMN DROPDOWN FOR CONDITION
        def on_combobox_select(event):
            column_selected = column_dropdown.get()
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



    def submit_dataframe_settings(self):

        if self.dataframe_name_entry.get() == "":
            utils.show_message("No Dataframe Name", "Please input a DATAFRAME NAME")
            return


        self.dataframe_name = self.dataframe_name_entry.get()
        condition_list_total = []
        condition_strings = []
        condition_syntax = {}

        for idx, frame in enumerate(self.condition_frames, start=1):

            condition_list = []

            if idx == 0:
                continue

            for widget in frame.winfo_children():
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
                    self.df[condition[1]] = self.df[condition[1]].astype(float)
                    condition_string = condition_string + str(float(condition[3]))
                except:
                    self.df[condition[1]] = self.df[condition[1]].astype(object)
                    condition_string = condition_string + "'" + condition[3] + "'"

            condition_string = condition_string + ')'
            condition_strings.append(condition_string)



        final_condition_string = ''.join(condition_strings)


        self.new_df = self.df.loc[self.df.eval(final_condition_string)]

        data_manager.add_dataframe_to_dict(self.new_df, self.dataframe_name_entry.get())
        self.update_dataframe_listbox()



    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################

    def switch_to_create_new_dataframe_button_frame(self):
        self.column_selection_frame.pack_forget()
        self.dataframe_settings_frame.pack_forget()
        self.create_new_dataframe_button_frame.pack(fill=tk.BOTH, expand=True)



    def switch_to_column_selection_frame(self):
        self.create_new_dataframe_button_frame.pack_forget()
        self.dataframe_settings_frame.pack_forget()
        self.column_selection_frame.pack(fill=tk.BOTH, expand=True)

        self.dataframe_name_entry.focus_set()


    def switch_to_dataframe_settings_frame(self):
        if not self.selected_columns:
            return

        utils.remove_frame_widgets(self.conditions_frame)
        self.condition_frames = []
        self.add_condition(label='Where')

        self.create_new_dataframe_button_frame.pack_forget()
        self.column_selection_frame.pack_forget()
        self.dataframe_settings_frame.pack(fill=tk.BOTH, expand=True)































def setup_dataframe_view_tab(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame, initialize=False):
    df = data_manager.get_dataframe()
    if df is None:
        utils.show_message("Error", "Please open a file first.")
        return


    style.configure("file_button.TButton", background=color_dict["inactive_main_tab_bg"], foreground=color_dict["inactive_main_tab_txt"])
    style.configure("dataframe_view_button.TButton", background=color_dict["active_main_tab_bg"], foreground=color_dict["active_main_tab_txt"])
    style.configure("edit_button.TButton", background=color_dict["inactive_main_tab_bg"], foreground=color_dict["inactive_main_tab_txt"])
    style.configure("visualize_button.TButton", background=color_dict["inactive_main_tab_bg"], foreground=color_dict["inactive_main_tab_txt"])

    utils.remove_frame_widgets(sub_button_frame)

    style.configure("save_dataframe_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"], borderwidth=0, padding=0, font=styles.sub_tabs_font)
    style.map(
        "save_dataframe_button.TButton",
        background=[("active", color_dict["hover_subtab_bg"])],
        foreground=[("active", color_dict["hover_subtab_txt"])]
    )
    save_dataframe_button = ttk.Button(sub_button_frame, text="Save Dataframe", style="save_dataframe_button.TButton")
    save_dataframe_button.pack(side="left", fill="both", expand=True)  # Set expand=True to fill the horizontal space
    save_dataframe_button.config(command=lambda: save_file(df))

    def initialize_dataframe_view_tab():
        utils.remove_frame_widgets(dataframe_content_frame)

        data_frame_border = tk.Frame(dataframe_content_frame, bg=color_dict["main_content_border"])
        data_frame_border.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        data_inner_frame = tk.Frame(data_frame_border, bg=color_dict["main_content_bg"])
        data_inner_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)

        # RAW DATA TABLE
        
        raw_data_table_subframe_border = tk.Frame(data_inner_frame, bg=color_dict["sub_frame_border"])
        raw_data_table_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        raw_data_table_subframe = tk.Frame(raw_data_table_subframe_border, bg=color_dict["sub_frame_bg"])
        raw_data_table_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        raw_data_table_subframe_label = tk.Label(raw_data_table_subframe, text="Raw Data", font=styles.main_content_header_font, bg=color_dict["sub_frame_bg"], fg=color_dict["main_content_header"])
        raw_data_table_subframe_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(raw_data_table_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)

        utils.create_table(raw_data_table_subframe, df, style)


        # SUMMARY DATA TABLE

        summary_df = utils.create_summary_table(df)

        summary_data_table_subframe_border = tk.Frame(data_inner_frame, bg=color_dict["sub_frame_border"])
        summary_data_table_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        summary_data_table_subframe = tk.Frame(summary_data_table_subframe_border, bg=color_dict["sub_frame_bg"])
        summary_data_table_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        summary_data_table_subframe_label = tk.Label(summary_data_table_subframe, text="Summary Data", font=styles.main_content_header_font, bg=color_dict["sub_frame_bg"], fg=color_dict["main_content_header"])
        summary_data_table_subframe_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(summary_data_table_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)

        utils.create_table(summary_data_table_subframe, summary_df, style)




        editing_content_frame.pack_forget()
        visualize_content_frame.pack_forget()
        file_handling_content_frame.pack_forget()
        dataframe_content_frame.pack(fill=tk.BOTH, expand=True)

    def switch_to_dataframe_view_tab():
        editing_content_frame.pack_forget()
        visualize_content_frame.pack_forget()
        file_handling_content_frame.pack_forget()
        dataframe_content_frame.pack(fill=tk.BOTH, expand=True)


    if initialize == True:
        initialize_dataframe_view_tab()
    if initialize == False:
        switch_to_dataframe_view_tab()

    dataframe_content_frame.update_idletasks()



def save_file(df):
    if df is None:
        utils.show_message("Error", "Please open a file first.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv"), ("All files", "*.*")]
    )

    # Check if the user canceled the file dialog
    if not file_path:
        return

    # Get the selected file name and extension
    file_name = file_path.split('/')[-1]

    # Get the file extension
    file_extension = file_name.split('.')[-1]

    # Save the DataFrame to the chosen file path based on the selected file extension
    if file_extension == 'csv':
        df.to_csv(file_path, index=False)
    elif file_extension == 'xlsx':
        df.to_excel(file_path, index=False)
    else:
        return
