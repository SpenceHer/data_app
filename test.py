import tkinter as tk
from tkinter import ttk

# Function to update the slider's min and max values
def update_slider(event):
    selected_option = listbox.get(listbox.curselection())
    min_val, max_val = value_ranges[selected_option]
    slider.config(from_=min_val, to=max_val)
    slider.set(max_val)
    update_label(max_val)

# Function to update the label with the current slider value
def update_label(value):
    value_label.config(text=f"Current Value: {int(value)}")

# Initialize the main window
root = tk.Tk()
root.title("Dynamic Slider Example")

# Define the value ranges for different options
value_ranges = {
    "Option 1": (0, 10),
    "Option 2": (10, 50),
    "Option 3": (50, 100)
}

# Create and pack the Listbox
listbox = tk.Listbox(root)
for option in value_ranges.keys():
    listbox.insert(tk.END, option)
listbox.pack()

# Create and pack the Label to display the slider value
value_label = tk.Label(root, text="Current Value: 0")
value_label.pack()

# Create and pack the Slider (Scale)
slider = ttk.Scale(root, orient='horizontal', length=300, command=lambda x: update_label(slider.get()))
slider.pack()

# Bind the Listbox selection event to the update_slider function
listbox.bind('<<ListboxSelect>>', update_slider)

# Set initial slider values based on the first listbox item
listbox.select_set(0)  # Select the first item
update_slider(None)    # Update the slider

# Start the Tkinter event loop
root.mainloop()
