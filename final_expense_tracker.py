import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

FILE_NAME = "expenses.csv"

# If the CSV doesn't exist, create it
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Description"])

# Save an expense
def save_expense():
    date = entry_date.get()
    category = entry_category.get()
    amount = entry_amount.get()
    desc = entry_desc.get()

    if not (date and category and amount):
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number")
        return

    with open(FILE_NAME, "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, desc])

    messagebox.showinfo("Saved", "Expense saved successfully")
    clear_fields()

# Show pie chart
def show_pie_chart():
    try:
        data = defaultdict(float)
        with open(FILE_NAME, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data[row["Category"]] += float(row["Amount"])

        if not data:
            messagebox.showinfo("No Data", "No expense data to plot.")
            return

        plt.pie(data.values(), labels=data.keys(), autopct="%1.1f%%")
        plt.title("Expenses by Category")
        plt.axis("equal")
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

# Load all expenses
def load_expenses():
    text_output.delete("1.0", tk.END)
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            text_output.insert(tk.END, f"{', '.join(row)}\n")

# Clear the input fields
def clear_fields():
    entry_date.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_desc.delete(0, tk.END)

# GUI setup
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("600x400")

# Inputs
tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
entry_date = tk.Entry(root)
entry_date.grid(row=0, column=1)
entry_date.insert(0, datetime.now().strftime('%Y-%m-%d'))

tk.Label(root, text="Category:").grid(row=1, column=0)
entry_category = tk.Entry(root)
entry_category.grid(row=1, column=1)

tk.Label(root, text="Amount:").grid(row=2, column=0)
entry_amount = tk.Entry(root)
entry_amount.grid(row=2, column=1)

tk.Label(root, text="Description:").grid(row=3, column=0)
entry_desc = tk.Entry(root)
entry_desc.grid(row=3, column=1)

# Buttons
tk.Button(root, text="Save Expense", command=save_expense).grid(row=4, column=0, pady=10)
tk.Button(root, text="Load Expenses", command=load_expenses).grid(row=4, column=1)
tk.Button(root, text="Show Pie Chart", command=show_pie_chart).grid(row=4, column=2)

# Output area
text_output = tk.Text(root, width=70, height=10)
text_output.grid(row=5, column=0, columnspan=3)

# Start app
root.mainloop()
