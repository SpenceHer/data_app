import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
import pandas as pd
import numpy as np
import data_manager
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import tkinter.font as tkfont

def show_message(title, message):
    messagebox.showinfo(title, message)
 
def prompt_yes_no(text_prompt):
    answer = messagebox.askyesno("Yes No Choice", text_prompt)
    return answer
 
def get_single_choice(parent, choices, text_prompt):
    selected_choice = None
    dialog = SingleChoiceSelectionDialog(parent, choices, selected_choice, text_prompt)
    parent.wait_window(dialog.top)
    return dialog.selected_choice.get()
 
def get_multiple_choices(parent, list_of_choices, text_prompt):
    selected_choices = []
    dialog = MultipleChoiceSelectionDialog(parent, list_of_choices, selected_choices, text_prompt)
    parent.wait_window(dialog.top)
    return dialog.selected_choices

























def remove_frame_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def forget_frame_widgets(frame):
    for widget in frame.winfo_children():
        widget.pack_forget()














def create_table(parent, df, show_index=True, table_name="", graph_name="", title=""):
 
    table_frame = tk.Frame(parent)
    table_frame.pack()
 
    if title != "":
        label = tk.Label(table_frame, text=title, font=('Arial', 32, 'bold'))
        label.pack(pady=10)
 
    treeview_frame = tk.Frame(table_frame)
    treeview_frame.pack(fill="both", expand=True)
 
    yscrollbar = ttk.Scrollbar(treeview_frame, orient="vertical")
    yscrollbar.pack(side="right", fill="y")
 
    xscrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
    xscrollbar.pack(side="bottom", fill="x")
 
    table_treeview = ttk.Treeview(
        treeview_frame, height=15, show="headings",
        yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set
    )
 
    yscrollbar.configure(command=table_treeview.yview)
    xscrollbar.configure(command=table_treeview.xview)
 
    columns = df.columns.tolist()
    table_treeview["columns"] = columns
 

    if show_index == True:
        table_treeview.heading("#0", text="Index")
 
    for column in columns:
 
        table_treeview.heading(column, text=column)
 
    for i, row in df.iterrows():
        try:
            values = ["" if pd.isnull(val) else val for val in row.tolist()]
            table_treeview.insert("", "end", values=values)
        except:
            print(row)
    for column in columns:
        table_treeview.column(column, width=160, anchor="center")
 
    table_treeview.pack(side="left", fill="both", expand=True)
 
    if not hasattr(parent, "table_frames"):
        parent.table_frames = {}
    parent.table_frames[table_name] = table_frame










def create_graph(content_frame, fig):
 
    remove_frame_widgets(content_frame)
 
    # Create a new graph frame
    graph_frame = tk.Frame(content_frame)
    graph_frame.pack()
 
    # Set the size of the figure
    fig.set_size_inches(10, 7)
 
    # Create a canvas for the graph
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    


def is_column_numeric(df, column_name):
    try:
        if df[column_name].dtype == 'O':
            return False
       
        numeric_values = pd.to_numeric(df[column_name], errors='coerce')
        non_null_numeric_values = numeric_values.nunique()
 
        if non_null_numeric_values > 2:
            return True
        else:
            return False
    except (TypeError, ValueError):
        return False

def create_summary_table(df):
    summary = pd.DataFrame(columns=['Column', 'Mode', 'Non-Null Count', 'Null Count', 'Non-Null Unique Count'] + list(df.describe().transpose().columns))
    
    for column in df.columns:
        
        mode = tuple(map(str, df[column].mode().values))
        non_null_count = df[column].count()
        null_count = df[column].isnull().sum()
        non_null_unique_count = df[column].nunique()
        describe_data = pd.Series(dtype='object')
        
        if is_column_numeric(df, column):
            describe_data = df[column].describe()
        
        summary = pd.concat([summary, pd.DataFrame({
            'Column': [column],
            'Mode': [mode],
            'Non-Null Count': [non_null_count],
            'Null Count': [null_count],
            'Non-Null Unique Count': [non_null_unique_count],
            **describe_data.to_dict()
        })])
    
    summary = summary.drop(columns={"count"})
    if "top" in summary.columns:
        summary = summary.drop(columns={"freq", 'top', 'unique'})
    return summary










































class CleanCategoricalSelectionDialog:
    def __init__(self, parent, unique_values, selected_options, change_dict):
        self.top = tk.Toplevel(parent)
        self.top.title("Value Selection")

        self.change_dict = change_dict
        self.unique_values = unique_values
        self.selected_options = selected_options

        self.radio_var = {}
        self.input_var = {}

        self.label = tk.Label(self.top, text="Select options for each value:")
        self.label.pack(pady=5)

        for value in self.unique_values:
            frame = tk.Frame(self.top)
            frame.pack(anchor=tk.W)

            value_label = tk.Label(frame, text=value)
            value_label.pack(side=tk.LEFT)

            options_frame = tk.Frame(frame)
            options_frame.pack(side=tk.LEFT)

            var = tk.StringVar(value="keep")  # Set default value to "keep"
            self.radio_var[value] = var

            input_var = tk.StringVar()
            self.input_var[value] = input_var

            radio1 = ttk.Radiobutton(options_frame, text="Keep", variable=var, value="keep")
            radio1.pack(side=tk.LEFT)

            radio2 = ttk.Radiobutton(options_frame, text="Remove", variable=var, value="remove")
            radio2.pack(side=tk.LEFT)

            radio3 = ttk.Radiobutton(options_frame, text="Change", variable=var, value="change")
            radio3.pack(side=tk.LEFT)

            input_entry = tk.Entry(frame, textvariable=input_var, state=tk.DISABLED)
            input_entry.pack(side=tk.LEFT)

            # Bind the state of the input_entry to the selection of 'Change' radio button
            radio3.bind("<Button-1>", lambda event, entry=input_entry: entry.configure(state=tk.NORMAL))
            radio1.bind("<Button-1>", lambda event, entry=input_entry: entry.configure(state=tk.DISABLED))
            radio2.bind("<Button-1>", lambda event, entry=input_entry: entry.configure(state=tk.DISABLED))

        self.button = tk.Button(self.top, text="Apply", command=self.apply_selection)
        self.button.pack(pady=5)


    def apply_selection(self):
        self.selected_options.clear()
        for value, var in self.radio_var.items():
            option = var.get()
            self.selected_options[value] = option

            if option == 'change':
                input_value = self.input_var[value].get()
                self.change_dict[value] = input_value

        self.top.destroy()

class MultipleChoiceSelectionDialog:
    def __init__(self, parent, list_of_choices, selected_choices, text_prompt):
        self.top = tk.Toplevel(parent)
        self.top.title("Multiple Choice Selection")

        self.text_prompt = tk.Label(self.top, text=text_prompt)
        self.text_prompt.pack(pady=10)

        self.search_frame = tk.Frame(self.top)
        self.search_frame.pack(pady=10)

        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT)

        self.listbox_frame = tk.Frame(self.top)
        self.listbox_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.arrow_frame = tk.Frame(self.top)
        self.arrow_frame.pack(side=tk.LEFT)

        self.selected_frame = tk.Frame(self.top)
        self.selected_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.available_listbox = tk.Listbox(self.listbox_frame, selectmode=tk.MULTIPLE)
        self.available_listbox.pack(fill=tk.BOTH, expand=True)

        self.arrow_right_button = tk.Button(self.arrow_frame, text=">>", command=self.transfer_right)
        self.arrow_right_button.pack(pady=5)

        self.arrow_left_button = tk.Button(self.arrow_frame, text="<<", command=self.transfer_left)
        self.arrow_left_button.pack(pady=5)

        self.selected_listbox = tk.Listbox(self.selected_frame, selectmode=tk.MULTIPLE)
        self.selected_listbox.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self.top)
        self.button_frame.pack(side=tk.BOTTOM, pady=10)

        self.submit_button = tk.Button(self.button_frame, text="Submit", command=self.submit_selections)
        self.submit_button.pack()

        self.text_prompt = text_prompt
        self.list_of_choices = list_of_choices
        self.selected_choices = selected_choices

        self.search_entry.bind("<KeyRelease>", self.search_choices)

        self.populate_listboxes()

    def populate_listboxes(self):
        for choice in self.list_of_choices:
            self.available_listbox.insert(tk.END, choice)

        for selected_choice in self.selected_choices:
            self.selected_listbox.insert(tk.END, selected_choice)

    def search_choices(self, event):
        search_text = self.search_entry.get().lower()
        self.available_listbox.delete(0, tk.END)

        for choice in self.list_of_choices:
            if search_text in choice.lower():
                self.available_listbox.insert(tk.END, choice)

    def transfer_right(self):
        selections = self.available_listbox.curselection()
        selected_items = [self.available_listbox.get(index) for index in selections]

        for item in selected_items:
            if item not in self.selected_choices:
                self.selected_listbox.insert(tk.END, item)
                self.selected_choices.append(item)

        for index in reversed(selections):
            self.available_listbox.delete(index)

    def transfer_left(self):
        selections = self.selected_listbox.curselection()
        selected_items = [self.selected_listbox.get(index) for index in selections]

        for item in selected_items:
            self.available_listbox.insert(tk.END, item)
            self.selected_choices.remove(item)

        for index in reversed(selections):
            self.selected_listbox.delete(index)

    def submit_selections(self):
        self.top.destroy()




class SingleChoiceSelectionDialog:
    def __init__(self, parent, choices, selected_choice, text_prompt):
        self.top = tk.Toplevel(parent)
        self.top.title("Choice Selection")
        self.top.geometry("300x300")  # Set the window size here

        self.choices = choices
        self.selected_choice = tk.StringVar(value=selected_choice)

        self.radiobuttons = []

        self.label = tk.Label(self.top, text=text_prompt)
        self.label.pack(pady=5)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_choices)

        self.search_entry = tk.Entry(self.top, textvariable=self.search_var)
        self.search_entry.pack(pady=5)

        self.choice_frame = ttk.Frame(self.top)
        self.choice_frame.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.choice_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.choice_listbox = tk.Listbox(
            self.choice_frame,
            yscrollcommand=self.scrollbar.set,
            selectmode=tk.SINGLE
        )
        self.choice_listbox.pack(fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.choice_listbox.yview)

        for choice in self.choices:
            self.choice_listbox.insert(tk.END, choice)
            self.radiobuttons.append(choice)

        self.button = tk.Button(self.top, text="Submit", command=self.clean)
        self.button.pack(pady=5)

    def filter_choices(self, *args):
        search_text = self.search_var.get().lower()
        self.choice_listbox.delete(0, tk.END)
        for choice in self.choices:
            if search_text in choice.lower():
                self.choice_listbox.insert(tk.END, choice)

    def clean(self):
        selected_index = self.choice_listbox.curselection()
        if selected_index:
            selected_choice = self.choice_listbox.get(selected_index[0])
            self.selected_choice.set(selected_choice)
        self.top.destroy()





class LogisticRegressionVariableDialog:
    def __init__(self, parent, clean_df, independent_variables, selected_options, reference_value_dict):
        self.top = tk.Toplevel(parent)
        self.top.title("Value Selection")

        self.df = clean_df
        self.reference_value_dict = reference_value_dict
        self.unique_values = clean_df[independent_variables].columns
        self.selected_options = selected_options

        self.radio_var = {}
        self.input_var = {}

        self.label = tk.Label(self.top, text="Choose the types of variable and reference value if applicable")
        self.label.pack(pady=5)

        for value in self.unique_values:
            frame = tk.Frame(self.top)
            frame.pack(anchor=tk.W)

            value_label = tk.Label(frame, text=value)
            value_label.pack(side=tk.LEFT)

            options_frame = tk.Frame(frame)
            options_frame.pack(side=tk.LEFT)

            var = tk.StringVar(value="Continuous")  # Set default value to "Continuous"
            self.radio_var[value] = var

            input_var = tk.StringVar()
            self.input_var[value] = input_var

            radio1 = ttk.Radiobutton(options_frame, text="Continuous", variable=var, value="Continuous")
            radio1.pack(side=tk.LEFT)

            radio3 = ttk.Radiobutton(options_frame, text="Categorical", variable=var, value="Categorical")
            radio3.pack(side=tk.LEFT)

            input_combobox = ttk.Combobox(frame, textvariable=input_var, state="readonly")
            values = [str(val) for val in clean_df[value].unique()]
            input_combobox['values'] = values
            input_combobox.current(0)  # Set default selection to the first item
            # input_combobox.bind("<<ComboboxSelected>>", lambda event, combobox=input_combobox: self.on_combobox_select(combobox, value))
            input_combobox.bind("<<ComboboxSelected>>", lambda event, combobox=input_combobox, value=value: self.on_combobox_select(combobox, value))

            input_combobox.pack(side=tk.LEFT)

            # Bind the state of the input_combobox to the selection of 'Categorical' radio button
            radio3.bind("<Button-1>", lambda event, combobox=input_combobox: combobox.configure(state="readonly"))
            radio1.bind("<Button-1>", lambda event, combobox=input_combobox: combobox.configure(state=tk.DISABLED))

        self.button = tk.Button(self.top, text="Apply", command=self.apply_selection)
        self.button.pack(pady=5)


    def on_combobox_select(self, combobox, value):
        
        selected_value = combobox.get()
        self.input_var[value].set(selected_value)

    def apply_selection(self):
        self.selected_options.clear()
        for value, var in self.radio_var.items():
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
                
        self.top.destroy()


class ComparisonTableSelectionDialog:
    def __init__(self, parent, clean_df, independent_variables, selected_options):
        self.top = tk.Toplevel(parent)
        self.top.title("Value Selection")

        self.df = clean_df
        self.unique_values = clean_df[independent_variables].columns
        self.selected_options = selected_options

        self.radio_var = {}

        self.label = tk.Label(self.top, text="Choose the types of variables")
        self.label.pack(pady=5)

        for row, value in enumerate(self.unique_values):
            frame = tk.Frame(self.top)
            frame.pack(anchor=tk.W)

            value_label = tk.Label(frame, text=value)
            value_label.grid(row=row, column=0, sticky="w")

            var = tk.StringVar(value="Continuous")  # Set default value to "Continuous"
            self.radio_var[value] = var

            radio1 = ttk.Radiobutton(frame, text="Continuous", variable=var, value="Continuous")
            radio1.grid(row=row, column=1, sticky="w")

            radio2 = ttk.Radiobutton(frame, text="Categorical", variable=var, value="Categorical")
            radio2.grid(row=row, column=2, sticky="w")

        self.button = tk.Button(self.top, text="Apply", command=self.apply_selection)
        self.button.pack(pady=5)

    def apply_selection(self):
        self.selected_options.clear()
        for value, var in self.radio_var.items():
            option = var.get()
            self.selected_options[value] = option

        self.top.destroy()

























class MultipleChoiceSelectionFrame(tk.Frame):
    def __init__(self, parent, list_of_choices, selected_choices, text_prompt):
        super().__init__(parent)

        self.text_prompt = tk.Label(self, text=text_prompt)
        self.text_prompt.pack(pady=10)

        self.search_frame = tk.Frame(self)
        self.search_frame.pack(pady=10)

        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.insert(0, "Search")
        self.search_entry.pack(side=tk.LEFT)
        self.search_entry.bind("<FocusIn>", self.clear_search_entry)

        self.listbox_frame = tk.Frame(self)
        self.listbox_frame.pack(side=tk.LEFT, padx=0, pady=10)

        self.arrow_frame = tk.Frame(self)
        self.arrow_frame.pack(side=tk.LEFT)

        self.selected_frame = tk.Frame(self)
        self.selected_frame.pack(side=tk.LEFT, padx=0, pady=10)

        # Increase the width of the Listbox widgets
        self.available_listbox = tk.Listbox(self.listbox_frame, selectmode=tk.MULTIPLE, width=40, font=("Arial", 16))
        self.available_listbox.pack(fill=tk.BOTH, expand=True)

        self.arrow_right_button = tk.Button(self.arrow_frame, text=">>", command=self.transfer_right)
        self.arrow_right_button.pack(pady=5)

        self.arrow_left_button = tk.Button(self.arrow_frame, text="<<", command=self.transfer_left)
        self.arrow_left_button.pack(pady=5)

        # Increase the width of the Listbox widgets
        self.selected_listbox = tk.Listbox(self.selected_frame, selectmode=tk.MULTIPLE, width=40, font=("Arial", 16))
        self.selected_listbox.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.BOTTOM, pady=10)

        self.list_of_choices = list_of_choices
        self.selected_choices = selected_choices

        self.search_entry.bind("<KeyRelease>", self.search_choices)

        self.populate_listboxes()

    def populate_listboxes(self):
        for choice in self.list_of_choices:
            self.available_listbox.insert(tk.END, choice)

        for selected_choice in self.selected_choices:
            self.selected_listbox.insert(tk.END, selected_choice)

    def clear_search_entry(self, event):
        self.search_entry.delete(0, tk.END)

    def search_choices(self, event):
        search_text = self.search_entry.get().lower()
        self.available_listbox.delete(0, tk.END)

        for choice in self.list_of_choices:
            if search_text in choice.lower():
                self.available_listbox.insert(tk.END, choice)

    def transfer_right(self):
        selections = self.available_listbox.curselection()
        selected_items = [self.available_listbox.get(index) for index in selections]

        for item in selected_items:
            if item not in self.selected_choices:
                self.selected_listbox.insert(tk.END, item)
                self.selected_choices.append(item)

        for index in reversed(selections):
            self.available_listbox.delete(index)

    def transfer_left(self):
        selections = self.selected_listbox.curselection()
        selected_items = [self.selected_listbox.get(index) for index in selections]

        for item in selected_items:
            self.available_listbox.insert(tk.END, item)
            self.selected_choices.remove(item)

        for index in reversed(selections):
            self.selected_listbox.delete(index)

























