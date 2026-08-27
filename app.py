import tkinter as tk
from tkinter import ttk, messagebox
import csv
from pathlib import Path

data_folder = Path.home() / "Documents" / "ResellerProfitAnalyzer"
data_folder.mkdir(parents=True, exist_ok=True)
sales_file = data_folder / "sales_history.csv"

current_sale = None

def calculate_profit():
    global current_sale

    try:
        item_name = item_entry.get().strip()

        if not item_name:
            messagebox.showerror("Missing Item", "Enter an item name.")
            return

        sale_price = float(sale_entry.get())
        item_cost = float(cost_entry.get())
        shipping = float(shipping_entry.get())
        fee_percent = float(fee_entry.get())

        if sale_price <= 0:
            raise ValueError

        if item_cost < 0 or shipping < 0 or fee_percent < 0:
            raise ValueError

        platform_fee = sale_price * (fee_percent / 100)
        net_profit = sale_price - item_cost - shipping - platform_fee
        profit_margin = (net_profit / sale_price) * 100

        fee_result.config(text=f"Platform fee: ${platform_fee:.2f}")
        profit_result.config(text=f"Net profit: ${net_profit:.2f}")
        margin_result.config(text=f"Profit margin: {profit_margin:.1f}%")

        current_sale = {
            "Item": item_name,
            "Sale Price": sale_price,
            "Item Cost": item_cost,
            "Shipping": shipping,
            "Fee Percent": fee_percent,
            "Platform Fee": platform_fee,
            "Net Profit": net_profit,
            "Profit Margin": profit_margin
        }

    except ValueError:
        messagebox.showerror(
            "Invalid Entry",
            "Enter valid positive numbers in all number fields."
        )

def save_sale():
    global current_sale

    if current_sale is None:
         messagebox.showwarning(
        "Nothing to Save",
        "Calculate a sale before saving."
        )
         return

    fieldnames = [
        "Item", "Sale Price", "Item Cost", "Shipping",
        "Fee Percent", "Platform Fee", "Net Profit",
        "Profit Margin"
    ]

    new_file = not sales_file.exists()

    with sales_file.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if new_file:
            writer.writeheader()

        writer.writerow(current_sale)

    messagebox.showinfo("Sale Saved", "The sale was saved successfully.")
    current_sale = None

    clear_form()

def show_summary():
    if not sales_file.exists():
        messagebox.showinfo("Sales Summary", "No saved sales found.")
        return

    total_revenue = 0
    total_costs = 0
    total_fees = 0
    total_profit = 0
    total_margin = 0
    sale_count = 0

    with sales_file.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            total_revenue += float(row["Sale Price"])
            total_costs += float(row["Item Cost"]) + float(row["Shipping"])
            total_fees += float(row["Platform Fee"])
            total_profit += float(row["Net Profit"])
            total_margin += float(row["Profit Margin"])
            sale_count += 1

    if sale_count == 0:
        messagebox.showinfo("Sales Summary", "No saved sales found.")
        return

    average_margin = total_margin / sale_count

    summary = (
        f"Number of sales: {sale_count}\n"
        f"Total revenue: ${total_revenue:.2f}\n"
        f"Total costs: ${total_costs:.2f}\n"
        f"Total platform fees: ${total_fees:.2f}\n"
        f"Total profit: ${total_profit:.2f}\n"
        f"Average profit margin: {average_margin:.1f}%"
    )

    messagebox.showinfo("Sales Summary", summary)

def clear_form():
    item_entry.delete(0, tk.END)
    sale_entry.delete(0, tk.END)
    cost_entry.delete(0, tk.END)
    shipping_entry.delete(0, tk.END)
    fee_entry.delete(0, tk.END)

    fee_result.config(text="Platform fee: $0.00")
    profit_result.config(text="Net profit: $0.00")
    margin_result.config(text="Profit margin: 0.0%")

    item_entry.focus()

window = tk.Tk()
window.title("Reseller Profit Analyzer")
window.geometry("500x500")
window.resizable(False, False)

title = ttk.Label(
    window,
    text="Reseller Profit Analyzer",
    font=("Arial", 18, "bold")
)
title.pack(pady=20)

form = ttk.Frame(window)
form.pack(pady=10)

ttk.Label(form, text="Item name:").grid(row=0, column=0, padx=10, pady=8, sticky="e")
item_entry = ttk.Entry(form, width=25)
item_entry.grid(row=0, column=1, padx=10, pady=8)

ttk.Label(form, text="Sale price: $").grid(row=1, column=0, padx=10, pady=8, sticky="e")
sale_entry = ttk.Entry(form, width=25)
sale_entry.grid(row=1, column=1, padx=10, pady=8)

ttk.Label(form, text="Item cost: $").grid(row=2, column=0, padx=10, pady=8, sticky="e")
cost_entry = ttk.Entry(form, width=25)
cost_entry.grid(row=2, column=1, padx=10, pady=8)

ttk.Label(form, text="Shipping cost: $").grid(row=3, column=0, padx=10, pady=8, sticky="e")
shipping_entry = ttk.Entry(form, width=25)
shipping_entry.grid(row=3, column=1, padx=10, pady=8)

ttk.Label(form, text="Platform fee: %").grid(row=4, column=0, padx=10, pady=8, sticky="e")
fee_entry = ttk.Entry(form, width=25)
fee_entry.grid(row=4, column=1, padx=10, pady=8)

calculate_button = ttk.Button(
    window,
    text="Calculate Profit",
    command=calculate_profit
)
calculate_button.pack(pady=20)

summary_button = ttk.Button(
    window,
    text="View Summary",
    command=show_summary
)
summary_button.pack(pady=5)
save_button = ttk.Button(
    window,
    text="Save Sale",
    command=save_sale
)
save_button.pack(pady=5)

fee_result = ttk.Label(window, text="Platform fee: $0.00")
fee_result.pack(pady=4)

profit_result = ttk.Label(window, text="Net profit: $0.00")
profit_result.pack(pady=4)

margin_result = ttk.Label(window, text="Profit margin: 0.0%")
margin_result.pack(pady=4)

window.mainloop()