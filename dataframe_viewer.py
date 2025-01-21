from math import exp
import tkinter as tk
from tkinter import LEFT, ttk
from tkinter import filedialog, messagebox

import pandas as pd

import os

import numpy as np

# LOCAL FILES
import data_library
import styles
from styles import color_dict
import utils





def setup_dataframe_viewer_tab(style, sub_button_frame, dataframe_management_content_frame, dataframe_viewer_content_frame, column_editor_content_frame, data_visualization_content_frame, reset_tables=False):
    df = data_library.get_dataframe()

    if df is None:
        utils.show_message("Error", "Please open a file first.")
        return

    style.configure("dataframe_management_button.TButton", background=color_dict["inactive_main_tab_bg"], foreground=color_dict["inactive_main_tab_txt"])
    style.configure("dataframe_viewer_button.TButton", background=color_dict["active_main_tab_bg"], foreground=color_dict["active_main_tab_txt"])
    style.configure("column_editor_button.TButton", background=color_dict["inactive_main_tab_bg"], foreground=color_dict["inactive_main_tab_txt"])
    style.configure("data_visualization_button.TButton", background=color_dict["inactive_main_tab_bg"], foreground=color_dict["inactive_main_tab_txt"])

    utils.remove_frame_widgets(sub_button_frame)

    style.configure("save_dataframe_button.TButton", background=color_dict["inactive_subtab_bg"], foreground=color_dict["inactive_subtab_txt"], borderwidth=0, padding=0, font=styles.sub_tabs_font)
    style.map(
        "save_dataframe_button.TButton",
        background=[("active", color_dict["hover_subtab_bg"])],
        foreground=[("active", color_dict["hover_subtab_txt"])]
    )




    if reset_tables:
        utils.remove_frame_widgets(dataframe_viewer_content_frame)

        dataframe_viewer_frame = tk.Frame(dataframe_viewer_content_frame, bg=color_dict["main_content_border"])
        dataframe_viewer_frame.pack(fill=tk.BOTH, expand=True, padx=17, pady=17)

        dataframe_viewer_inner_frame, dataframe_viewer_canvas = utils.create_scrollable_frame(dataframe_viewer_frame)
        utils.bind_mousewheel_to_frame(dataframe_viewer_inner_frame, dataframe_viewer_canvas, True)


        # CREATE RAW DATA TABLE

        raw_data_table_subframe_border = tk.Frame(dataframe_viewer_inner_frame, bg=color_dict["sub_frame_border"])
        raw_data_table_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        raw_data_table_subframe = tk.Frame(raw_data_table_subframe_border, bg=color_dict["sub_frame_bg"])
        raw_data_table_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        raw_data_table_subframe_label = ttk.Label(raw_data_table_subframe, text="Raw Data", style="sub_frame_header.TLabel")
        raw_data_table_subframe_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(raw_data_table_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)

        # utils.create_dataframe_table(raw_data_table_subframe, df, style)
        table, columns = utils.create_editable_table(raw_data_table_subframe, df, style)

        data_library.set_df_treeview(table)
        data_library.set_df_columns(columns)



        # CREATE SUMMARY DATA TABLE

        summary_df = utils.create_summary_table(df)

        summary_data_table_subframe_border = tk.Frame(dataframe_viewer_inner_frame, bg=color_dict["sub_frame_border"])
        summary_data_table_subframe_border.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=8, pady=8)

        summary_data_table_subframe = tk.Frame(summary_data_table_subframe_border, bg=color_dict["sub_frame_bg"])
        summary_data_table_subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)

        summary_data_table_subframe_label = ttk.Label(summary_data_table_subframe, text="Summary Data", style="sub_frame_header.TLabel")
        summary_data_table_subframe_label.pack(side=tk.TOP, pady=10)

        separator = ttk.Separator(summary_data_table_subframe, orient="horizontal", style="Separator.TSeparator")
        separator.pack(side=tk.TOP, fill=tk.X, padx=200)

        utils.create_dataframe_table(summary_data_table_subframe, summary_df, style)



        save_dataframe_button = ttk.Button(sub_button_frame, text="Save Dataframe", style="save_dataframe_button.TButton")
        save_dataframe_button.pack(side="left", fill="both", expand=True)  # Set expand=True to fill the horizontal space
        save_dataframe_button.config(command=lambda: utils.save_editable_table(table, columns))

        column_editor_content_frame.pack_forget()
        data_visualization_content_frame.pack_forget()
        dataframe_management_content_frame.pack_forget()
        dataframe_viewer_content_frame.pack(fill=tk.BOTH, expand=True)

        dataframe_viewer_content_frame.focus_set()

    else:
        treeview = data_library.get_df_treeview()
        columns = data_library.get_df_columns()

        save_dataframe_button = ttk.Button(sub_button_frame, text="Save Dataframe", style="save_dataframe_button.TButton")
        save_dataframe_button.pack(side="left", fill="both", expand=True)  # Set expand=True to fill the horizontal space
        save_dataframe_button.config(command=lambda: utils.save_editable_table(treeview, columns))

        dataframe_management_content_frame.pack_forget()
        column_editor_content_frame.pack_forget()
        data_visualization_content_frame.pack_forget()
        dataframe_viewer_content_frame.pack(fill=tk.BOTH, expand=True)

        dataframe_viewer_content_frame.focus_set()

