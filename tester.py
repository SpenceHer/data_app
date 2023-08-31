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


main_window.wm_state('zoomed')


editing_content_frame = tk.Frame(main_window, bg="green")
editing_content_frame.pack(side="top", fill=tk.BOTH, expand=True)


regression_button = tk.Button(editing_content_frame, text="Comparison Table", font=("Arial", 36), command=lambda: CreateNewVariableClass(editing_content_frame, df))
regression_button.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)




class CreateNewVariableClass:
    def __init__(self, editing_content_frame, df):
        self.df = df
        self.editing_content_frame = editing_content_frame

        utils.remove_frame_widgets(self.editing_content_frame)

        self.column_selection_frame = tk.Frame(self.editing_content_frame, bg='hotpink')
        self.conditions_frame = tk.Frame(self.editing_content_frame, bg='purple')
        self.finalize_frame = tk.Frame(self.editing_content_frame, bg='red')

        self.create_column_selection_frame()
        self.create_conditions_frame()
        self.create_finalize_frame()

        self.switch_to_column_selection_frame()


    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    ###################################################################################################################################################################################################
    def create_column_selection_frame(self):

        self.selected_columns = []

        self.column_choice_frame = tk.Frame(self.column_selection_frame, bg='yellow')
        self.column_choice_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.choose_columns_label = tk.Label(self.column_choice_frame, text="Choose columns to use", font=("Arial", 36))
        self.choose_columns_label.pack(side=tk.TOP, fill=tk.X)

        self.selection_frame = tk.Frame(self.column_choice_frame, bg='blue')
        self.selection_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



        self.available_columns_frame = tk.Frame(self.selection_frame, bg='green')
        self.available_columns_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
        self.transfer_buttons_frame = tk.Frame(self.selection_frame, bg='red')
        self.transfer_buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.selected_columns_frame = tk.Frame(self.selection_frame, bg='pink')
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
        self.column_name_frame = tk.Frame(self.conditions_frame, bg='green')
        self.column_name_frame.pack(side=tk.TOP, fill=tk.X)

        self.column_name_frame_label = tk.Label(self.column_name_frame, text="Name of new variable:", font=('Arial', 42), background='orange')
        self.column_name_frame_label.pack(side=tk.TOP, fill=tk.X)

        self.column_name_entry = tk.Entry(self.column_name_frame, font=('Arial', 24))
        self.column_name_entry.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)


        # ADD/REMOVE CONDITIONS BUTTONS FRAME
        self.condition_buttons_frame = tk.Frame(self.conditions_frame, bg='yellow')
        self.condition_buttons_frame.pack(side=tk.TOP, fill=tk.X)

        self.add_new_value_button = tk.Button(self.condition_buttons_frame, text='Add New Value', command=self.add_value_frame, font=('Arial', 36))
        self.add_new_value_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.remove_value_button = tk.Button(self.condition_buttons_frame, text='Remove Value', command=self.remove_value_frame, font=('Arial', 36))
        self.remove_value_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)



        
        # CONDITIONS OPTIONS FRAME
        self.value_frames = []
        self.condition_frames = []
        self.condition_signs = ['Equals', 'Does Not Equal', 'Less Than', 'Greater Than', 'Less Than or Equal To', 'Greater Than or Equal To', 'Contains', 'Does Not Contain']
        self.condition_signs_dict = {'Equals':'==', 'Does Not Equal':'!=', 'Less Than':'<', 'Greater Than':'>', 'Less Than or Equal To':'<=', 'Greater Than or Equal To':'>=',
                                     'Contains':'Contains', 'Does Not Contain':'Does Not Contain'}

        self.condition_options_frame = tk.Frame(self.conditions_frame, bg='orange')
        self.condition_options_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        def on_mousewheel(event):
            self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

        self.canvas = tk.Canvas(self.condition_options_frame)
        self.scrollbar = ttk.Scrollbar(self.condition_options_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel event to the canvas
        self.canvas.bind("<MouseWheel>", on_mousewheel)

















        # MENU FRAME

        self.conditions_menu_frame = tk.Frame(self.conditions_frame, bg='lightgray')
        self.conditions_menu_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.return_to_column_selection_button = tk.Button(self.conditions_menu_frame, command=self.switch_to_column_selection_frame, text="Back", font=("Arial", 36))
        self.return_to_column_selection_button.pack(side=tk.LEFT)

        self.advance_to_conditions_button = tk.Button(self.conditions_menu_frame, command=self.switch_to_finalize_frame, text="Next", font=("Arial", 36))
        self.advance_to_conditions_button.pack(side=tk.RIGHT)








    def add_value_frame(self):
        condition_frames = []

        # REMOVE MOST RECENT CONDITION LINE
        def remove_condition():
            if len(condition_frames) > 1:
                frame = condition_frames.pop()
                next_frame = condition_frames[-1]
                print(next_frame.winfo_children()[0])
                print(condition_frames[-1].winfo_children()[0].cget("text"))
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
                value_list = ['USER CHOICE'] + list(self.df[column_selected].unique())
                column_values_dropdown["values"] = value_list

            selected_column_option = tk.StringVar()
            column_dropdown = ttk.Combobox(condition_frame, textvariable=selected_column_option, values=self.selected_columns)
            column_dropdown.pack(side=tk.LEFT)
            column_dropdown.bind("<<ComboboxSelected>>", on_combobox_select)

            # CONDITION SIGN DROPDOWN
            selected_condition_sign = tk.StringVar()
            selected_condition_sign_dropdown = ttk.Combobox(condition_frame, textvariable=selected_condition_sign, values=self.condition_signs)
            selected_condition_sign_dropdown.pack(side=tk.LEFT)

            # VALUE SELECTION DROPDOWN
            selected_value = tk.StringVar()
            value_list = ['USER CHOICE']
            column_values_dropdown = ttk.Combobox(condition_frame, textvariable=selected_value, values=value_list)
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

        add_major_and_button = tk.Button(condition_handling_frame, text='AND', command=lambda: add_condition(label='AND'))
        add_major_and_button.pack(side=tk.LEFT)

        add_major_or_button = tk.Button(condition_handling_frame, text='OR', command=lambda: add_condition(label='OR'))
        add_major_or_button.pack(side=tk.LEFT)

        add_remove_button = tk.Button(condition_handling_frame, text='Remove Condition', command=remove_condition)
        add_remove_button.pack(side=tk.LEFT)

        # FRAME WHERE THE USER EDITS THE CONDITIONS
        add_condition(label='Where')



        
        self.value_frames.append(new_value_frame)









    def remove_value_frame(self):
        print(self.value_frames)
        if self.value_frames:
            frame = self.value_frames.pop()
            frame.destroy()

    def get_values_from_frames(self):

        for idx, frame in enumerate(self.value_frames, start=1):
            condition_list_total = []
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
                print(condition_list)
                condition_list_total.append(condition_list)

            print('\n')
            print(f"Value: {condition_value}")
            print(condition_list_total)
            print('\n')

        



# self.df.loc[self.df.eval(condition_string), column_name] = condition_value

# data = {'A': [1, 2, 3, 4, 5]}
# df = pd.DataFrame(data)

# # Define condition strings
# condition_high = "A > 3"
# condition_low = "A <= 3"

# # Evaluate conditions and create a new column
# df['Category'] = 'Unknown'
# df.loc[df.eval(condition_high), 'Category'] = 'High'
# df.loc[df.eval(condition_low), 'Category'] = 'Low'

# # Define the complex condition string
# condition_string = "(A < 3) | (A == 5)"

# # Evaluate the condition and create a new column
# df['Category'] = 'Other'
# df.loc[df.eval(condition_string), 'Category'] = 'Selected'


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

        self.finalize_variable_name_label = tk.Label(self.finalize_menu_frame, text='Variable Name',font=("Arial", 36))
        self.finalize_variable_name_label.pack(side=tk.LEFT, fill=tk.X)


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
        self.get_values_from_frames()
        self.conditions_frame.pack_forget()
        self.column_selection_frame.pack_forget()
        self.finalize_frame.pack(fill=tk.BOTH, expand=True)


    def update_dataframe(self):
        return
















# Start the GUI event loop
main_window.mainloop()
