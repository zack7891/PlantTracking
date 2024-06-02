import csv
import tkinter as tk
from tkinter import messagebox, Toplevel, Listbox, filedialog, PhotoImage
from pathlib import Path

# File path for the CSV
csv_file_path = 'plants.csv'

# Function to read plants from CSV
def read_plants():
    try:
        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return []

# Function to write plants to CSV
def write_plants(plants):
    with open(csv_file_path, mode='w', newline='') as file:
        fieldnames = ['plant_type', 'planting_date', 'amount_planted']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(plants)

# Function to insert a new plant into the CSV
def insert_plant(plant_type, planting_date, amount_planted):
    plants = read_plants()
    plants.append({'plant_type': plant_type, 'planting_date': planting_date, 'amount_planted': amount_planted})
    write_plants(plants)

# Function to display the plants in a new window
def view_plants():
    plants = read_plants()
    new_window = Toplevel(app)
    new_window.title("View Plants")
    listbox = Listbox(new_window, width=50, height=10)
    listbox.pack(padx=20, pady=20)
    for plant in plants:
        listbox.insert(tk.END, f"{plant['plant_type']} - Planted on: {plant['planting_date']} - Amount: {plant['amount_planted']}")
    # Download button that saves the currently displayed list
    download_button = tk.Button(new_window, text="Download CSV", command=lambda: download_csv(plants))
    download_button.pack(pady=10)

# Function to download CSV of plants
def download_csv(plants):
    filepath = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if filepath:
        with open(filepath, mode='w', newline='') as file:
            fieldnames = ['plant_type', 'planting_date', 'amount_planted']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(plants)
        messagebox.showinfo("Success", "File has been saved!")

# Function to handle the submit button click
def on_submit():
    plant_type = plant_type_entry.get()
    planting_date = planting_date_entry.get()
    amount_planted = amount_planted_entry.get()
    
    try:
        if plant_type and planting_date and amount_planted:
            amount_planted = int(amount_planted)
            insert_plant(plant_type, planting_date, amount_planted)
            messagebox.showinfo("Success", "Plant added successfully!")
            plant_type_entry.delete(0, tk.END)
            planting_date_entry.delete(0, tk.END)
            amount_planted_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Input Error", "Please fill in all fields correctly.")
    except ValueError:
        messagebox.showerror("Input Error", "Amount planted must be a number.")

# Ensure the CSV file exists and has the correct headers
if not Path(csv_file_path).exists():
    write_plants([])  # Create an empty file with headers

# Set up the main application window using tkinter
app = tk.Tk()
app.title("Plant Recorder")

# Change the application icon
app.iconbitmap('C:/Users/18137/Sprout-595b40b65ba036ed117d3411.png')  # Path to your icon file

# Application title label
tk.Label(app, text="Plant Recorder Application").grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky='we')

# Setup GUI elements using grid for precise placement
tk.Label(app, text="Plant Type:").grid(row=1, column=1, padx=10, pady=10, sticky='w')
plant_type_entry = tk.Entry(app)
plant_type_entry.grid(row=1, column=2, padx=10, pady=10, sticky='we')

tk.Label(app, text="Planting Date (YYYY-MM-DD):").grid(row=2, column=1, padx=10, pady=10, sticky='w')
planting_date_entry = tk.Entry(app)
planting_date_entry.grid(row=2, column=2, padx=10, pady=10, sticky='we')

tk.Label(app, text="Amount Planted (in acres):").grid(row=3, column=1, padx=10, pady=10, sticky='w')
amount_planted_entry = tk.Entry(app)
amount_planted_entry.grid(row=3, column=2, padx=10, pady=10, sticky='we')

submit_button = tk.Button(app, text="Submit", command=on_submit)
submit_button.grid(row=4, column=1, padx=10, pady=10, sticky='w')

view_button = tk.Button(app, text="View Plants", command=view_plants)
view_button.grid(row=4, column=2, padx=10, pady=10, sticky='w')

# Load and add a static picture of a plant
plant_image = PhotoImage(file='C:/Users/18137/Sprout-595b40b65ba036ed117d3411.png')
image_label = tk.Label(app, image=plant_image)
image_label.grid(row=0, column=0, rowspan=4, padx=10, pady=10, sticky='ns')  # Span multiple rows to align with the input fields

# Ensure the window displays all columns correctly
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=3)  # Give more weight to the input column

# Run the tkinter event loop
app.mainloop()
