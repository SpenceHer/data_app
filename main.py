import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font
from tkinter import ttk
import utils
import visualize
import edit
import pandas as pd
import numpy as np
import file_handling
import data_manager
 

# Create the main window
main_window = tk.Tk()
main_window.title("DataFrame Editor")
main_window.wm_state('zoomed')

 
style = ttk.Style()
style.theme_use("clam")



# Create frames
banner_frame = tk.Frame(main_window, bg="gray")
banner_frame.pack(side="top", fill=tk.X)
 
button_frame = tk.Frame(banner_frame, bg='gray')
button_frame.pack(fill=tk.X)  # Change to fill=tk.X to expand horizontally
 
sub_button_frame = tk.Frame(banner_frame)
sub_button_frame.pack(fill=tk.X)  # Change to fill=tk.X to expand horizontally
sub_button_frame.pack_propagate(True)
 
content_frame = tk.Frame(main_window, bg="beige")
content_frame.pack(side="top", fill=tk.BOTH, expand=True)
 
dataframe_content_frame = tk.Frame(content_frame, bg="beige")
file_handling_content_frame = tk.Frame(content_frame, bg="beige")
editing_content_frame = tk.Frame(content_frame, bg="beige")
visualize_content_frame = tk.Frame(content_frame, bg="beige")
 
# Add Buttons
 
# Banner Frame
style.configure("file_button.TButton", background="white", borderwidth=0, padding=0, font=("Arial", 48))
file_button = ttk.Button(button_frame, text="File", style="file_button.TButton")
file_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
file_button.config(command=lambda: file_handling.setup_file_tab(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame))
 
style.configure("dataframe_view_button.TButton", background="gray", borderwidth=0, padding=0, font=("Arial", 48))
dataframe_view_button = ttk.Button(button_frame, text="Dataframe View", style="dataframe_view_button.TButton")
dataframe_view_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
dataframe_view_button.config(command=lambda: file_handling.setup_dataframe_view_tab(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame, initialize=False))
 
style.configure("edit_button.TButton", background="gray", borderwidth=0, padding=0, font=("Arial", 48))
edit_button = ttk.Button(button_frame, text="Edit/Clean Data", style="edit_button.TButton")
edit_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
edit_button.config(command=lambda: edit.setup_edit_tab(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame))
 
style.configure("visualize_button.TButton", background="gray", borderwidth=0, padding=0, font=("Arial", 48))
visualize_button = ttk.Button(button_frame, text="Visualize Data", style="visualize_button.TButton")
visualize_button.pack(side="left", fill="x", expand=True)  # Set expand=True to fill the horizontal space
visualize_button.config(command=lambda: visualize.setup_visualize_tab(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame))
 

file_handling.setup_file_tab(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame)
 

# Start the GUI event loop
main_window.mainloop()
