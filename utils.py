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


















def remove_frame_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def forget_frame_widgets(frame):
    for widget in frame.winfo_children():
        widget.pack_forget()














def create_table(parent, df, show_index=True, table_name="", graph_name="", title=""):
 
    table_frame = tk.Frame(parent)
    table_frame.pack(fill=tk.Y, expand=True)
 
    if title != "":
        label = tk.Label(table_frame, text=title, font=('Arial', 32, 'bold'))
        label.pack(pady=10)
 
    treeview_frame = tk.Frame(table_frame)
    treeview_frame.pack(fill=tk.BOTH, expand=True)
 
    yscrollbar = ttk.Scrollbar(treeview_frame, orient="vertical")
    yscrollbar.pack(side="right", fill="y")

    xscrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
    xscrollbar.pack(side="bottom", fill="x")

    table_treeview = ttk.Treeview(
        treeview_frame, show="headings",
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
    summary = pd.DataFrame(columns=['Column', 'Mode', 'Non-Missing Count', 'Missing Count', 'Non-Missing Unique Count'] + list(df.describe().transpose().columns))
    
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
            'Non-Missing Count': [non_null_count],
            'Missing Count': [null_count],
            'Non-Missing Unique Count': [non_null_unique_count],
            **describe_data.to_dict()
        })])
    
    summary = summary.drop(columns={"count"})
    if "top" in summary.columns:
        summary = summary.drop(columns={"freq", 'top', 'unique'})
    return summary

