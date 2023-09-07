import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import utils
import pandas as pd
import data_manager
 
def setup_file_tab(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame):
    style.configure("file_button.TButton", background="white")
    style.configure("dataframe_view_button.TButton", background="gray")
    style.configure("edit_button.TButton", background="gray")
    style.configure("visualize_button.TButton", background="gray")
    def initialize_file_tab():
        file_handling_content_frame.pack(fill=tk.BOTH, expand=True)
        style.configure("open_file_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 72))
        open_file_button = ttk.Button(file_handling_content_frame, text="Open File", style="open_file_button.TButton")
        open_file_button.pack(side="left", fill="both", expand=True, padx=100, pady=100)  # Set expand=True to fill the horizontal space
        open_file_button.config(command=lambda: open_file(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame))
 
    def switch_to_file_tab():
        utils.remove_frame_widgets(sub_button_frame)
        dataframe_content_frame.pack_forget()
        editing_content_frame.pack_forget()
        visualize_content_frame.pack_forget()
        file_handling_content_frame.pack(fill=tk.BOTH, expand=True)
 
    df = data_manager.get_dataframe()
    if df is None:
        initialize_file_tab()
    else:
        switch_to_file_tab()









def setup_dataframe_view_tab(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame, initialize=False):
    df = data_manager.get_dataframe()
    if df is None:
        utils.show_message("Error", "Please open a file first.")
        return
    style.configure("file_button.TButton", background="gray")
    style.configure("dataframe_view_button.TButton", background="white")
    style.configure("edit_button.TButton", background="gray")
    style.configure("visualize_button.TButton", background="gray")
 
    utils.remove_frame_widgets(sub_button_frame)
 
    style.configure("save_file_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 36))
    save_file_button = ttk.Button(sub_button_frame, text="Save File", style="save_file_button.TButton")
    save_file_button.pack(side="left", fill="both", expand=True)  # Set expand=True to fill the horizontal space
    save_file_button.config(command=lambda: save_file(df))
 
    def initialize_dataframe_view_tab():
        utils.remove_frame_widgets(dataframe_content_frame)
 
        utils.create_table(dataframe_content_frame, df)
        summary_df = utils.create_summary_table(df)
        utils.create_table(dataframe_content_frame, summary_df, title="COLUMN SUMMARY TABLE")
 
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
 

def open_file(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame):
    # Specify the path of the specific dataframe file you want to load
    file_path = filedialog.askopenfilename()
    # file_path = "X:\OHSU Shared\Restricted\SOM\SURG\ORTH\Smith\Projects\YOO\OHSU Lumbar Fusions\master_8.1.23.xlsx"
    # file_path = "/Users/spencersmith/Desktop/coding/OHSU_data.xlsx"

    def fix_columns(df):
            df.columns = df.columns.str.replace(' ', '_')
            df.columns = df.columns.str.replace('__', '_')
            df.columns = df.columns.str.replace('___', '_')
            df.columns = df.columns.str.replace(r'\W+', '', regex=True)

    try:
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path, keep_default_na=False, na_values=[''])
        else:
            df = pd.read_csv(file_path, keep_default_na=False, na_values=[''])



        fix_columns(df)
        data_manager.set_dataframe(df)  # Set the df variable
 
        setup_dataframe_view_tab(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame, initialize=True)
    except Exception as e:
        utils.show_message("Error", str(e))
 

def save_file(df):
    if df is None:
        utils.show_message("Error", "Please open a file first.")
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv"), ("All files", "*.*")]
    )
 
    # Check if the user selected a file
    if file_path:
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
            print("Unsupported file format. Please choose either CSV or Excel.")
            return
 
        print(f"DataFrame saved to: {file_path}")








