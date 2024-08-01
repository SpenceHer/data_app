
theme = "Barbie"


################################################################################################################
################################################################################################################
################################################################################################################


if theme == "Barbie":
    color_dict = {
        # Main Tabs
        "active_main_tab_bg": "#E91E63",  # Barbie Pink for active main tabs
        "active_main_tab_txt": "#FFFFFF",  # White text for contrast
        "inactive_main_tab_bg": "#F8BBD0",  # Lighter pink for inactive main tabs
        "inactive_main_tab_txt": "#4A2C4E",  # Dark purple for text
        "hover_main_tab_bg": "#AD1457",  # Deeper pink for hover states
        "hover_main_tab_txt": "#FFFFFF",  # White text for hover states

        # Sub Tabs
        "active_subtab_bg": "#F06292",  # Bright pink for active subtabs
        "active_subtab_txt": "#FFFFFF",  # White text for active subtabs
        "inactive_subtab_bg": "#FCE4EC",  # Very light pink for inactive subtabs
        "inactive_subtab_txt": "#4A2C4E",  # Dark purple for inactive subtabs text
        "hover_subtab_bg": "#EC407A",  # Medium pink for hover states on subtabs
        "hover_subtab_txt": "#FFFFFF",  # White text for hover states

        # Background Frame
        "background_frame_bg": "#FCE4EC",  # Very light pink for the background frame. Match with inactive subtabs

        # Main Content Frame
        "main_content_bg": "#FAFAFA",  # Off-white for main content background
        "main_content_border": "#F8BBD0",  # Light pink for borders

        # Sub Content Frame - Several within every Main Content Frame
        "sub_frame_bg": "#FADCE6",  # Pastel pink for sub-frame backgrounds, providing a soft, thematic contrast
        "sub_frame_border": "#E1BEE7",  # Pastel purple for sub-frame borders, adding a pop of color and definition

        "sub_frame_header": "#AD1457",  # A deeper shade of pink for main headers, providing contrast and emphasis
        "sub_frame_sub_header": "#E91E63",  # A slightly lighter Barbie pink for sub-headers to differentiate from the main headers but maintain the theme
        "sub_frame_text": "#4A2C4E",  # A dark purple or almost black for regular text, ensuring readability against lighter backgrounds

        # Navigation Banner - at the bottom of every main_content frame
        "nav_banner_bg": "#E91E63",  # Barbie Pink for navigation banner
        "nav_banner_txt": "#FFFFFF",  # White for navigation text
        "nav_banner_hover_bg": "#C2185B",  # Darker pink for hover states
        "nav_banner_hover_txt": "#FFFFFF",  # White for hover state text

        # Navigation Menu Buttons
        "nav_menu_button_bg": "#F06292",  # Bright pink for menu buttons
        "nav_menu_button_txt": "#FFFFFF",  # White text for buttons
        "nav_menu_button_hover_bg": "#E91E63",  # Barbie Pink for button hover states
        "nav_menu_button_hover_txt": "#FFFFFF",  # White text for hover states

        # Listboxes
        "listbox_bg": "#FAFAFA",  # Off-white for listbox background
        "listbox_fg": "#AD1457",  # Deep pink for listbox foreground text
        "listbox_highlight_bg": "#F8BBD0",  # Light pink for listbox highlight background
        "listbox_highlight_color": "#EC407A",  # Medium pink for highlight color
        "listbox_select_bg": "#FCE4EC",  # Very light pink for selected item background
        "listbox_select_fg": "#4A2C4E",  # Dark purple for selected item text

        # Radio Buttons
        "radio_button_inactive_text": "#4A2C4E",
        "radio_button_inactive_background": "#FAFAFA",
        "radio_button_inactive_border": "#E91E63",
        "radio_button_active_text": "#FFFFFF",
        "radio_button_active_background": "#E91E63",
        "radio_button_active_border": "#AD1457",
        "radio_button_pressed_text": "#4A2C4E",
        "radio_button_pressed_background": "#F8BBD0",
        "radio_button_pressed_border": "#C2185B",
        "radio_button_hover_text": "#FFFFFF",
        "radio_button_hover_background": "#AD1457",
        "radio_button_hover_border": "#991846",

        # Large Buttons
        "action_button_text_color": "#FFFFFF",
        "action_button_bg": "#E91E63",
        "action_button_pressed_bg": "#C2185B",
        "action_button_active_bg": "#AD1457",

        # Comboboxes
        "active_combobox_background": "#FFB6C1",  # Light Pink
        "active_combobox_text": "#FF69B4",        # Hot Pink
        "inactive_combobox_background": "#E6E6E6", # Light Gray
        "inactive_combobox_text": "#E6E6E6",       # Light Gray

        # Tree Tables
        "treeview_bg": "#FCE4EC",  # Very light pink for Treeview background
        "treeview_fg": "#4A2C4E",  # Dark purple for Treeview foreground text
        "treeview_field_bg": "#FCE4EC",  # Matching the Treeview background for consistency
        "treeview_selected_bg": "#E91E63",  # Barbie Pink for selected item background
        "treeview_selected_fg": "#FFFFFF",  # White for selected item text

        "treeview_heading_bg": "#AD1457",  # Deeper pink for Treeview Heading background
        "treeview_heading_fg": "#FFFFFF",  # White for Treeview Heading text
        "treeview_heading_active_bg": "#EC407A",  # Medium pink for active heading background
        "treeview_heading_active_fg": "#FFFFFF",  # White for active heading text

        "scrollbar_bg": "#E91E63",  # Barbie Pink for Scrollbar background and elements
        "scrollbar_troughcolor": "#FADCE6",  # Pastel pink for Scrollbar trough
        "scrollbar_arrowcolor": "#FFFFFF",  # White for Scrollbar arrows

        # Separator
        "separator": "#E91E63"

    }

    # FONTS
    main_tabs_font = ("Brush Script MT", 22, "bold")  # Playful script font for main tabs
    sub_tabs_font = ("Comic Sans MS", 20)  # Fun and casual font for sub tabs

    nav_menu_label_font = ("Brush Script MT", 18)  # A playful, cursive font that's still legible for menu labels
    nav_menu_button_font = ("Comic Sans MS", 18, "bold")  # A casual, friendly font for button text to keep the interface light-hearted

    sub_frame_header_font = ("American Typewriter", 22, "bold")  # A stylish, impactful font for main headers to draw attention
    sub_frame_sub_header_font = ("Chalkboard SE", 20, "bold")  # A more playful, yet readable font for sub-headers
    sub_frame_text_font = ("Arial Rounded MT Bold", 18)  # A clean, modern font that's versatile and readable

    listbox_font = ("Arial Rounded MT Bold", 18, "bold")
    entrybox_small_font = ("Arial Rounded MT Bold", 18, "bold")
    entrybox_large_font = ("Arial Rounded MT Bold", 22, "bold")


    large_button_font = ("Arial Rounded MT Bold", 20)  # Bold and fun for standout buttons
    small_button_font = ("Arial Rounded MT Bold", 18)  # Bold and fun for standout buttons


################################################################################################################
################################################################################################################
################################################################################################################
    

if theme == "Professional":
    color_dict = {
        # Main Tabs
        "active_main_tab_bg": "#005A9E",  # Deep Blue for active main tabs
        "active_main_tab_txt": "#FFFFFF",  # White text for contrast
        "inactive_main_tab_bg": "#D9E2EC",  # Light Gray for inactive main tabs
        "inactive_main_tab_txt": "#333333",  # Dark Gray for text
        "hover_main_tab_bg": "#004B8D",  # Slightly darker blue for hover states
        "hover_main_tab_txt": "#FFFFFF",  # White text for hover states

        # Sub Tabs
        "active_subtab_bg": "#007BFF",  # Bright Blue for active subtabs
        "active_subtab_txt": "#FFFFFF",  # White text for active subtabs
        "inactive_subtab_bg": "#E9ECEF",  # Very Light Gray for inactive subtabs
        "inactive_subtab_txt": "#495057",  # Medium Gray for inactive subtabs text
        "hover_subtab_bg": "#0056B3",  # Medium Blue for hover states on subtabs
        "hover_subtab_txt": "#FFFFFF",  # White text for hover states

        # Background Frame
        "background_frame_bg": "#F1F4F8",  # Very light gray for the background frame, clean and unobtrusive

        # Main Content Frame
        "main_content_bg": "#FFFFFF",  # Pure White for main content background, offering a clean slate
        "main_content_border": "#D9E2EC",  # Light Gray for borders, subtle and professional

        # Sub Content Frame
        "sub_frame_bg": "#E9ECEF",  # Very Light Gray for sub-frame backgrounds, for a subtle distinction from the main content
        "sub_frame_border": "#ADB5BD",  # Medium Gray for sub-frame borders, providing a crisp delineation

        "sub_frame_header": "#005A9E",  # Deep Blue for main headers, commanding attention with professionalism
        "sub_frame_sub_header": "#007BFF",  # Bright Blue for sub-headers, maintaining hierarchy with a vibrant contrast
        "sub_frame_text": "#495057",  # Medium Gray for regular text, ensuring excellent readability

        # Navigation Banner
        "nav_banner_bg": "#005A9E",  # Deep Blue for navigation banner, consistent with main tab active state
        "nav_banner_txt": "#FFFFFF",  # White for navigation text, ensuring legibility
        "nav_banner_hover_bg": "#004B8D",  # Darker Blue for hover states, subtly indicating interactivity
        "nav_banner_hover_txt": "#FFFFFF",  # White for hover state text, maintaining clarity

        # Navigation Menu Buttons
        "nav_menu_button_bg": "#007BFF",  # Bright Blue for menu buttons, making them stand out invitingly
        "nav_menu_button_txt": "#FFFFFF",  # White text for buttons, for clear visibility
        "nav_menu_button_hover_bg": "#0056B3",  # Medium Blue for button hover states, a subtle hint at interactivity
        "nav_menu_button_hover_txt": "#FFFFFF",  # White text for hover states, consistent with other hover state designs

        # Listboxes
        "listbox_bg": "#FFFFFF",  # Pure White for listbox background, clean and straightforward
        "listbox_fg": "#005A9E",  # Deep Blue for listbox foreground text, ensuring readability and visual harmony
        "listbox_highlight_bg": "#D9E2EC",  # Light Gray for listbox highlight background, subtle and professional
        "listbox_highlight_color": "#007BFF",  # Bright Blue for highlight color, drawing attention without overwhelming
        "listbox_select_bg": "#E9ECEF",  # Very Light Gray for selected item background, softly highlighting selection
        "listbox_select_fg": "#333333",  # Dark Gray for selected item text, maintaining legibility and contrast

        # Radio Buttons
        "radio_button_inactive_text": "#495057",  # Medium Gray for inactive text, clear and professional
        "radio_button_inactive_background": "#FFFFFF",  # White for inactive background, clean and unobtrusive
        "radio_button_inactive_border": "#ADB5BD",  # Medium Gray for inactive border, subtle and defining
        "radio_button_active_text": "#FFFFFF",  # White for active text, ensuring legibility against colored backgrounds
        "radio_button_active_background": "#005A9E",  # Deep Blue for active background, visually striking and consistent with the theme
        "radio_button_active_border": "#004B8D",  # Slightly darker blue for active border, adding depth
        "radio_button_pressed_text": "#495057",  # Medium Gray for pressed text, maintaining readability
        "radio_button_pressed_background": "#D9E2EC",  # Light Gray for pressed background, soft and unassuming
        "radio_button_pressed_border": "#0056B3",  # Medium Blue for pressed border, indicating interaction
        "radio_button_hover_text": "#FFFFFF",  # White for hover text, standing out against hover background
        "radio_button_hover_background": "#004B8D",  # Darker Blue for hover background, subtle hint at interactivity
        "radio_button_hover_border": "#003D7A",  # Even darker blue for hover border, adding a layer of depth

        # Large Buttons
        "action_button_text_color": "#FFFFFF",  # White for button text, ensuring visibility
        "action_button_bg": "#005A9E",  # Deep Blue for button background, consistent and bold
        "action_button_pressed_bg": "#004B8D",  # Slightly darker blue for pressed state, indicating interaction
        "action_button_active_bg": "#007BFF",  # Bright Blue for active state, vibrant and engaging

        # Comboboxes
        "active_combobox_background": "#FFFFFF",  # White for active combobox background, clean and straightforward
        "active_combobox_text": "#005A9E",  # Deep Blue for active combobox text, for easy reading and consistency
        "inactive_combobox_background": "#E9ECEF",  # Very Light Gray for inactive combobox, subtle and professional
        "inactive_combobox_text": "#ADB5BD",  # Medium Gray for inactive combobox text, muted and sophisticated

        # Tree Tables
        "treeview_bg": "#FFFFFF",  # White for Treeview background, offering a stark, clean canvas
        "treeview_fg": "#495057",  # Medium Gray for Treeview foreground text, ensuring excellent readability
        "treeview_field_bg": "#F1F4F8",  # Very light gray for field background, almost blending with the overall background
        "treeview_selected_bg": "#005A9E",  # Deep Blue for selected item background, highlighting selections vividly
        "treeview_selected_fg": "#FFFFFF",  # White for selected item text, for stark contrast and visibility

        "treeview_heading_bg": "#004B8D",  # Slightly darker blue for Treeview Heading background, setting apart the headings
        "treeview_heading_fg": "#FFFFFF",  # White for Treeview Heading text, ensuring legibility
        "treeview_heading_active_bg": "#007BFF",  # Bright Blue for active heading background, drawing attention
        "treeview_heading_active_fg": "#FFFFFF",  # White for active heading text, maintaining readability

        "scrollbar_bg": "#005A9E",  # Deep Blue for Scrollbar background, consistent with other primary elements
        "scrollbar_troughcolor": "#D9E2EC",  # Light Gray for Scrollbar trough, unobtrusive and blending with the interface
        "scrollbar_arrowcolor": "#FFFFFF",  # White for Scrollbar arrows, standing out for easy navigation

        # Separator
        "separator": "#ADB5BD"  # Medium Gray for separators, subtle yet effective in dividing sections
    }

# FONTS
    main_tabs_font = ("Helvetica", 22, "bold")  # Professional and clean font for main tabs
    sub_tabs_font = ("Helvetica", 20)  # Clear and neutral font for sub tabs

    nav_menu_label_font = ("Helvetica", 18)  # Clean and simple font for menu labels, enhancing legibility
    nav_menu_button_font = ("Helvetica", 18, "bold")  # Strong, bold Helvetica for button text to ensure clarity and visibility

    sub_frame_header_font = ("Helvetica", 22, "bold")  # Bold and impactful Helvetica for main headers to draw attention
    sub_frame_sub_header_font = ("Helvetica", 20, "bold")  # Bold yet slightly smaller Helvetica for sub-headers, maintaining hierarchy
    sub_frame_text_font = ("Helvetica", 18)  # Clean and versatile Helvetica for readable text throughout the interface

    listbox_font = ("Helvetica", 18, "bold")  # Bold Helvetica for list items, ensuring they are prominently displayed
    entrybox_small_font = ("Helvetica", 18, "bold")  # Bold Helvetica for small text entry, enhancing interaction
    entrybox_large_font = ("Helvetica", 22, "bold")  # Larger, bold Helvetica for more important or prominent text entries

    large_button_font = ("Helvetica", 20)  # Bold and clear Helvetica for important buttons, ensuring visibility
    small_button_font = ("Helvetica", 18)  # Standard Helvetica, bold for general button usage, maintaining functionality



################################################################################################################
################################################################################################################
################################################################################################################

