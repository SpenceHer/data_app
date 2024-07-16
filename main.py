import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font
from tkinter import ttk

import pandas as pd
import numpy as np

from tkinter import font

# LOCAL FILES
import file_handling
import data_manager
import utils
import visualize
import edit
import styles
from styles import color_dict


# Create the main window
main_window = tk.Tk()
screen_width = main_window.winfo_screenwidth() // 3
screen_height = main_window.winfo_screenheight()
main_window.title("DataFrame Editor")

main_window.geometry(f"{screen_width}x{screen_height}+0+0")
# main_window.wm_state('zoomed')






style = ttk.Style()
style.theme_use("clam")


# Create frames
banner_frame = tk.Frame(main_window)
banner_frame.pack(side="top", fill=tk.X)

button_frame = tk.Frame(banner_frame)
button_frame.pack(fill=tk.X)  # Change to fill=tk.X to expand horizontally

sub_button_frame = tk.Frame(banner_frame)
sub_button_frame.pack(fill=tk.X)  # Change to fill=tk.X to expand horizontally
sub_button_frame.pack_propagate(True)

content_frame = tk.Frame(main_window)
content_frame.pack(side="top", fill=tk.BOTH, expand=True)

dataframe_content_frame = tk.Frame(content_frame, bg=color_dict["background_frame_bg"])
file_handling_content_frame = tk.Frame(content_frame, bg=color_dict["background_frame_bg"])
editing_content_frame = tk.Frame(content_frame, bg=color_dict["background_frame_bg"])
visualize_content_frame = tk.Frame(content_frame, bg=color_dict["background_frame_bg"])

# Add Buttons

# Banner Frame
style.configure("file_button.TButton", background="white", borderwidth=0, padding=0, font=styles.main_tabs_font)
file_button = ttk.Button(button_frame, text="File", style="file_button.TButton")
file_button.pack(side="left", fill="x", expand=True)
file_button.config(command=lambda: file_handling.setup_file_tab(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame))

style.configure("dataframe_view_button.TButton", background="gray", borderwidth=0, padding=0, font=styles.main_tabs_font)
dataframe_view_button = ttk.Button(button_frame, text="Dataframe View", style="dataframe_view_button.TButton")
dataframe_view_button.pack(side="left", fill="x", expand=True)
dataframe_view_button.config(command=lambda: file_handling.setup_dataframe_view_tab(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame, initialize=False))

style.configure("edit_button.TButton", background="gray", borderwidth=0, padding=0, font=styles.main_tabs_font)
edit_button = ttk.Button(button_frame, text="Edit Data", style="edit_button.TButton")
edit_button.pack(side="left", fill="x", expand=True)
edit_button.config(command=lambda: edit.setup_edit_tab(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame))

style.configure("visualize_button.TButton", background="gray", borderwidth=0, padding=0, font=styles.main_tabs_font)
visualize_button = ttk.Button(button_frame, text="Visualize Data", style="visualize_button.TButton")
visualize_button.pack(side="left", fill="x", expand=True)
visualize_button.config(command=lambda: visualize.setup_visualize_tab(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame))





for button in ["file_button.TButton", "dataframe_view_button.TButton", "edit_button.TButton", "visualize_button.TButton"]:
    style.map(button, background=[("active", "#3E2723")])


file_handling.setup_file_tab(style, sub_button_frame, dataframe_content_frame, file_handling_content_frame, editing_content_frame, visualize_content_frame)


################################################################################################################
################################################################################################################
################################################################################################################

# STYLING

################################################################################################################

style.configure("Separator.Separator", background=color_dict["separator"])

################################################################################################################

# RADIO BUTTONS
style.configure("inactive_radio_button.TButton", 
                    font=styles.large_button_font, 
                    foreground=color_dict["radio_button_inactive_text"],
                    background=color_dict["radio_button_inactive_background"],
                    bordercolor=color_dict["radio_button_inactive_border"],
                    relief="flat")

style.configure("active_radio_button.TButton", 
                    font=styles.large_button_font, 
                    foreground=color_dict["radio_button_active_text"],
                    background=color_dict["radio_button_active_background"],
                    bordercolor=color_dict["radio_button_active_border"],
                    relief="groove")

style.map("inactive_radio_button.TButton",
                foreground=[("pressed", color_dict["radio_button_pressed_text"]), ("active", color_dict["radio_button_pressed_text"])],
                background=[("pressed", color_dict["radio_button_pressed_background"]), ("active", color_dict["radio_button_pressed_background"])],
                bordercolor=[("pressed", color_dict["radio_button_pressed_border"]), ("active", color_dict["radio_button_pressed_border"])])

style.map("active_radio_button.TButton",
                foreground=[("pressed", color_dict["radio_button_hover_text"]), ("active", color_dict["radio_button_hover_text"])],
                background=[("pressed", color_dict["radio_button_hover_background"]), ("active", color_dict["radio_button_hover_background"])],
                bordercolor=[("pressed", color_dict["radio_button_hover_border"]), ("active", color_dict["radio_button_hover_border"])])

################################################################################################################

# COMBOBOXES
style.map("TCombobox",
    fieldbackground=[("readonly", color_dict["active_combobox_background"]), ("disabled", color_dict["inactive_combobox_background"])],
    background=[("readonly", color_dict["active_combobox_background"]), ("disabled", color_dict["inactive_combobox_background"])],
    foreground = [("readonly", color_dict["listbox_fg"]), ("disabled", color_dict["inactive_combobox_text"])],
)

################################################################################################################

# NAV MENU
style.configure('nav_menu_button.TButton', font=styles.nav_menu_button_font, background=color_dict["nav_menu_button_bg"], foreground=color_dict["nav_menu_button_txt"])
style.map("nav_menu_button.TButton",
    background=[("active", color_dict["nav_menu_button_hover_bg"])],
    foreground=[("active", color_dict["nav_menu_button_hover_txt"])]
)

style.configure("nav_menu_label.TLabel",
               foreground=color_dict["nav_banner_txt"],
               background=color_dict["nav_banner_bg"],
               font=styles.nav_menu_label_font)


################################################################################################################

# LARGE BUTTONS
style.configure("large_button.TButton", 
                    font=styles.large_button_font,
                    foreground=color_dict["action_button_text_color"], 
                    background=color_dict["action_button_bg"],
                    borderwidth=1,
                    relief="raised",
                    padding=6)

style.map("large_button.TButton",
            foreground=[("pressed", color_dict["action_button_text_color"]), ("active", color_dict["action_button_text_color"])],
            background=[("pressed", color_dict["action_button_pressed_bg"]), ("active", color_dict["action_button_active_bg"])])

################################################################################################################

# SMALL BUTTONS
style.configure("small_button.TButton", 
                    font=styles.small_button_font,
                    foreground=color_dict["action_button_text_color"],
                    background=color_dict["action_button_bg"],
                    borderwidth=1,
                    relief="raised",
                    padding=6)

style.map("small_button.TButton",
            foreground=[("pressed", color_dict["action_button_text_color"]), ("active", color_dict["action_button_text_color"])],
            background=[("pressed", color_dict["action_button_pressed_bg"]), ("active", color_dict["action_button_active_bg"])]) 

################################################################################################################

# SUB FRAME HEADER LABELS
style.configure("sub_frame_header.TLabel", 
                foreground=color_dict["sub_frame_header"], 
                background=color_dict["sub_frame_bg"], 
                font=styles.sub_frame_header_font,
                )

################################################################################################################

# SUB FRAME SUB-HEADER LABELS
style.configure("sub_frame_sub_header.TLabel", 
                foreground=color_dict["sub_frame_sub_header"], 
                background=color_dict["sub_frame_bg"], 
                font=styles.sub_frame_sub_header_font
                )

################################################################################################################

# SUB FRAME TEXT FONT
style.configure("sub_frame_text.TLabel", 
                foreground=color_dict["sub_frame_sub_header"], 
                background=color_dict["sub_frame_bg"], 
                font=styles.sub_frame_text_font)

################################################################################################################

# TREE TABLES

style.configure("Treeview",
                background=color_dict["treeview_bg"],
                foreground=color_dict["treeview_fg"],
                rowheight=25,
                fieldbackground=color_dict["treeview_field_bg"])
style.map("Treeview",
            background=[('selected', color_dict["treeview_selected_bg"])],
            foreground=[('selected', color_dict["treeview_selected_fg"])])

# Treeview Heading style (for columns)
style.configure("Treeview.Heading",
                background=color_dict["treeview_heading_bg"],
                foreground=color_dict["treeview_heading_fg"],
                font=('Arial Rounded MT Bold', 12, 'bold'))
style.map("Treeview.Heading",
            background=[('active', color_dict["treeview_heading_active_bg"])],
            foreground=[('active', color_dict["treeview_heading_active_fg"])])

# Scrollbar style
style.configure("Vertical.TScrollbar", gripcount=0,
                background=color_dict["scrollbar_bg"], darkcolor=color_dict["scrollbar_bg"], lightcolor=color_dict["scrollbar_bg"],
                troughcolor=color_dict["scrollbar_troughcolor"], bordercolor=color_dict["scrollbar_bg"], arrowcolor=color_dict["scrollbar_arrowcolor"])
style.configure("Horizontal.TScrollbar", gripcount=0,
                background=color_dict["scrollbar_bg"], darkcolor=color_dict["scrollbar_bg"], lightcolor=color_dict["scrollbar_bg"],
                troughcolor=color_dict["scrollbar_troughcolor"], bordercolor=color_dict["scrollbar_bg"], arrowcolor=color_dict["scrollbar_arrowcolor"])


################################################################################################################
################################################################################################################
################################################################################################################

# Start the GUI event loop
main_window.mainloop()
