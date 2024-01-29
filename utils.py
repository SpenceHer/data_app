from email import message
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
import styles
from styles import color_dict

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








def create_scrollable_frame(root):
    def on_variable_handling_canvas_configure(event):
        canvas_width = event.width
        main_canvas.itemconfig(scrollable_frame_window, width=canvas_width)

    def on_variable_handling_mousewheel(event):
        if main_canvas.winfo_exists():
            if event.num == 4 or event.delta > 0:  # Scroll up
                main_canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:  # Scroll down
                main_canvas.yview_scroll(1, "units")

    # SCROLLABLE FRAME
    container_frame = tk.Frame(root)
    container_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=3, pady=3)

    # Canvas for scrollable content
    main_canvas = tk.Canvas(container_frame, bg=color_dict["main_content_bg"], highlightthickness=0)
    main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Scrollbar for the canvas
    scrollbar = tk.Scrollbar(container_frame, command=main_canvas.yview)
    main_canvas.configure(yscrollcommand=scrollbar.set)

    # Scrollable frame inside the canvas
    scrollable_frame = tk.Frame(main_canvas, bg=color_dict["main_content_bg"])
    scrollable_frame_window = main_canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)

    # Bind events
    main_canvas.bind("<Configure>", on_variable_handling_canvas_configure)
    scrollable_frame.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))

    # Cross-platform scroll event binding
    scrollable_frame.bind_all("<MouseWheel>", on_variable_handling_mousewheel)
    scrollable_frame.bind_all("<Button-4>", on_variable_handling_mousewheel)
    scrollable_frame.bind_all("<Button-5>", on_variable_handling_mousewheel)

    return scrollable_frame, main_canvas



def bind_mousewheel_to_frame(scrollable_frame, main_canvas, bind=True):
    def on_mousewheel(event):
        if main_canvas.winfo_exists():
            # Get the current view
            current_view = main_canvas.yview()

            # Scroll up
            if (event.num == 4 or event.delta > 0) and current_view[0] > 0:
                main_canvas.yview_scroll(-1, "units")

            # Scroll down
            elif (event.num == 5 or event.delta < 0) and current_view[1] < 1:
                main_canvas.yview_scroll(1, "units")

    if bind:
        scrollable_frame.bind_all("<MouseWheel>", on_mousewheel)
        scrollable_frame.bind_all("<Button-4>", on_mousewheel)
        scrollable_frame.bind_all("<Button-5>", on_mousewheel)
    else:
        scrollable_frame.unbind_all("<MouseWheel>")
        scrollable_frame.unbind_all("<Button-4>")
        scrollable_frame.unbind_all("<Button-5>")















def create_table(parent, df, show_index=True, table_name="", graph_name="", title=""):

    table_frame = tk.Frame(parent, bg='beige')
    table_frame.pack(fill=tk.Y, expand=True)

    if title != "":
        label = tk.Label(table_frame, text=title, font=('Arial', 32, 'bold'), bg='beige')
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
    # Preparing the columns for the summary dataframe
    describe_cols = ['mean', 'std', 'min', '25%', '50%', '75%', 'max']
    summary_cols = ['Column', 'Mode', 'Non-Missing Count', 'Missing Count', 'Non-Missing Unique Count'] + describe_cols
    summary_list = []  # Initialize a list to store DataFrames

    # Function to check if a column is numeric
    def is_numeric(col):
        return pd.api.types.is_numeric_dtype(df[col])

    # Iterating through each column to compute the statistics
    for column in df.columns:
        data = {
            'Column': column,
            'Mode': tuple(map(str, df[column].mode().values)),
            'Non-Missing Count': df[column].count(),
            'Missing Count': df[column].isnull().sum(),
            'Non-Missing Unique Count': df[column].nunique()
        }

        # Adding descriptive statistics for numeric columns
        if is_numeric(column):
            data.update(df[column].describe()[describe_cols].to_dict())

        # Filtering out empty or all-NA columns from the data dictionary
        data = {k: v for k, v in data.items() if v is not None and not pd.isna(v)}

        # Adding the computed data to the summary_list
        summary_list.append(pd.DataFrame([data]))

    # Concatenate all DataFrames in the summary_list
    summary = pd.concat(summary_list, ignore_index=True)

    return summary
