import tkinter as tk
from tkinter import ttk

def update_scale_range(event):
    selected_var = variable_combobox.get()
    
    if selected_var == "Variable 1":
        min_value, max_value = 0, 50
    elif selected_var == "Variable 2":
        min_value, max_value = 20, 100
    elif selected_var == "Variable 3":
        min_value, max_value = 10, 200
    else:
        min_value, max_value = 0, 100
    
    scale.config(from_=min_value, to=max_value)
    scale.set((min_value + max_value) / 2)  # Optionally reset the scale to the middle of the new range

def on_value_change(value):
    # This function will be called whenever the slider value changes
    value_label.config(text=f"Slider value: {float(value):.2f}")

# Create the main window
root = tk.Tk()
root.title("Tkinter Dynamic Scale Example")

# Create a label to display the current value
value_label = ttk.Label(root, text="Select a value")
value_label.pack(pady=10)

# Create a combobox to select the variable
variable_combobox = ttk.Combobox(root, values=["Variable 1", "Variable 2", "Variable 3"])
variable_combobox.set("Select Variable")
variable_combobox.pack(pady=10)

# Create the scale
scale = ttk.Scale(root, orient='horizontal', command=on_value_change)
scale.pack(pady=20)

# Bind the combobox selection event to update the scale range
variable_combobox.bind("<<ComboboxSelected>>", update_scale_range)

# Create a button to get the current value of the scale
def get_value():
    current_value = scale.get()
    value_label.config(text=f"Current value: {current_value:.2f}")

get_value_button = ttk.Button(root, text="Get Value", command=get_value)
get_value_button.pack(pady=10)

# Run the main event loop
root.mainloop()
