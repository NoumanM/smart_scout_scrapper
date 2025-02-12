import tkinter as tk
from tkinter import MULTIPLE, Listbox
from main import process_data

categories = {
    "3": "Home & Kitchen",
    "17": "Health & Household",
    "21": "Appliances",
    "2": "Arts, Crafts & Sewing",
    "13": "Automotive",
    "6": "Baby Products",
    "4": "Beauty & Personal Care",
    "31": "Books",
    "27": "CDs & Vinyl",
    "62": "Camera & Photo",

}
def submit():
    selected_categories = [category_listbox.get(i) for i in category_listbox.curselection()]
    min_fba = min_entry.get()
    max_fba = max_entry.get()
    country = country_entry.get()
    print(f"Selected Categories: {selected_categories}")
    print(f"FBA Percent - Min: {min_fba}, Max: {max_fba}")
    print(f"Country: {country}")
    process_data(selected_categories, min_fba, max_fba, country)

# Create main window
root = tk.Tk()
root.title("Smart Scout Scraper")
root.geometry("300x400")

# Category Label & Listbox
category_label = tk.Label(root, text="Category")
category_label.pack()

categories = categories.values()
category_listbox = Listbox(root, selectmode=MULTIPLE)
for category in categories:
    category_listbox.insert(tk.END, category)
category_listbox.pack()

# FBA Percent Min & Max Entry
min_label = tk.Label(root, text="FBA Percent (Min)")
min_label.pack()
min_entry = tk.Entry(root)
min_entry.pack()

max_label = tk.Label(root, text="FBA Percent (Max)")
max_label.pack()
max_entry = tk.Entry(root)
max_entry.pack()

# Country Entry
country_label = tk.Label(root, text="Country")
country_label.pack()
country_entry = tk.Entry(root)
country_entry.pack()

# Submit Button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

# Run the main loop
root.mainloop()
