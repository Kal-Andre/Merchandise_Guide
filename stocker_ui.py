from Stocker import StockTracker
import tkinter as tk
from tkinter import ttk

# Initialize tracker and load saved data
tracker = StockTracker()
tracker.load_from_file()

# Create main window
root = tk.Tk()
root.title("Soft Drink Stock Tracker")

# ========== Outlet Selection ==========
outlet_var = tk.StringVar()
outlet_dropdown = ttk.Combobox(root, textvariable=outlet_var)
outlet_dropdown['values'] = ["BestBuy Bukoto", "Kenjoy Bukoto", "Carrefour Acacia"]
outlet_dropdown.grid(row=0, column=1, padx=10, pady=10)
outlet_var.set("BestBuy Bukoto")  # default

# ========== Add Item Section ==========
add_frame = tk.LabelFrame(root, text="Add Item", padx=10, pady=10)
add_frame.grid(row=0, column=0, padx=10, pady=10)

tk.Label(add_frame, text="Item Name").grid(row=0, column=0)
item_name_entry = tk.Entry(add_frame)
item_name_entry.grid(row=0, column=1)

tk.Label(add_frame, text="Stock Quantity").grid(row=1, column=0)
stock_entry = tk.Entry(add_frame)
stock_entry.grid(row=1, column=1)

def add_item():
    name = item_name_entry.get()
    quantity = int(stock_entry.get())
    tracker.add_item(name, quantity)
    tracker.save_to_file()
    status_label.config(text=f"✅ Added {quantity} units of {name}")

tk.Button(add_frame, text="Add Item", command=add_item).grid(row=2, column=0, columnspan=2)

def refresh_dropdowns():
    items = list(tracker.stock.keys())
    sale_name_dropdown['values'] = items
    target_name_dropdown['values'] = items

# ========== Record Sale Section ==========
sale_frame = tk.LabelFrame(root, text="Record Sale", padx=10, pady=10)
sale_frame.grid(row=1, column=0, padx=10, pady=10)

tk.Label(sale_frame, text="Item Name").grid(row=0, column=0)
sale_name_entry = tk.Entry(sale_frame)
sale_name_entry.grid(row=0, column=1)

tk.Label(sale_frame, text="Quantity Sold").grid(row=1, column=0)
sale_quantity_entry = tk.Entry(sale_frame)
sale_quantity_entry.grid(row=1, column=1)

sale_name_var = tk.StringVar()
sale_name_dropdown = ttk.Combobox(sale_frame, textvariable=sale_name_var)
sale_name_dropdown.grid(row=0, column=1)

# Record sale function replaced.
'''def record_sale():
    outlet = outlet_var.get()
    name = sale_name_var.get()
    quantity = int(sale_quantity_entry.get())
    tracker.record_sale(outlet, name, quantity)
    tracker.save_to_file()
    status_label.config(text=f"📦 Recorded sale of {quantity} units of {name}")
tk.Button(sale_frame, text="Record Sale", command=record_sale).grid(row=2, column=0, columnspan=2)'''

def open_weekly_balance_entry():
    outlet = outlet_var.get()  # selected outlet from dropdown
    entry_window = tk.Toplevel(root)
    entry_window.title(f"Weekly Balance Entry - {outlet}")

    entries = {}
    row = 0
    for item in tracker.stock:
        tk.Label(entry_window, text=item).grid(row=row, column=0, padx=5, pady=2)
        balance_entry = tk.Entry(entry_window, width=10)
        balance_entry.grid(row=row, column=1, padx=5, pady=2)
        entries[item] = balance_entry
        row += 1

    def submit_balances():
        for item, entry in entries.items():
            val = entry.get()
            if val.strip().isdigit():
                balance = int(val)
                tracker.record_weekly_balance(outlet, item, balance)
        tracker.save_to_file()
        status_label.config(text=f"✅ Recorded weekly balances for {outlet}")
        entry_window.destroy()

    tk.Button(entry_window, text="Submit", command=submit_balances).grid(row=row, column=0, columnspan=2, pady=10)

tk.Button(sale_frame, text="📊 Weekly Balance Entry", command=open_weekly_balance_entry).grid(row=4, column=0, columnspan=2, pady=5)

# ========== Summary Section ==========
summary_frame = tk.LabelFrame(root, text="Summary", padx=10, pady=10)
summary_frame.grid(row=3, column=0, padx=10, pady=10)

# Outlet selection for summary
summary_outlet_var = tk.StringVar()
summary_outlet_dropdown = ttk.Combobox(summary_frame, textvariable=summary_outlet_var)
summary_outlet_dropdown['values'] = ["All Outlets", "BestBuy Bukoto", "Kenjoy Bukoto", "Carrefour Acacia"]
summary_outlet_dropdown.grid(row=0, column=1, padx=5)
summary_outlet_var.set("All Outlets")

def show_summary():
    selected_outlet = summary_outlet_var.get()
    summary_window = tk.Toplevel(root)
    summary_window.title(f"Summary Report - {selected_outlet}")
    text = tk.Text(summary_window, width=80, height=20)
    text.pack()
    headers = f"{'Item':<20}{'Stock':<10}{'Sold':<10}{'Target':<10}{'Progress':<10}\n"
    text.insert(tk.END, headers + "-"*60 + "\n")

    if selected_outlet == "All Outlets":
        for name in tracker.stock:
            total_sold = sum(tracker.sales[outlet].get(name, 0) for outlet in tracker.sales)
            stock = tracker.stock[name]
            target = tracker.targets.get(name, 0)
            progress = (total_sold / target * 100) if target else 0
            line = f"{name:<20}{stock:<10}{total_sold:<10}{target:<10}{progress:.2f}%\n"
            text.insert(tk.END, line)
    else:
        outlet_sales = tracker.sales.get(selected_outlet, {})
        for name in tracker.stock:
            sold = outlet_sales.get(name, 0)
            stock = tracker.stock[name]
            target = tracker.targets.get(name, 0)
            progress = (sold / target * 100) if target else 0
            line = f"{name:<20}{stock:<10}{sold:<10}{target:<10}{progress:.2f}%\n"
            text.insert(tk.END, line)

tk.Button(summary_frame, text="Show Summary", command=show_summary).grid(row=0, column=0, sticky="w")

# ========== Status Label ==========
status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=4, column=0, pady=10)

# ========== Set Target Section ==========
target_frame = tk.LabelFrame(root, text="Set Target", padx=10, pady=10)
target_frame.grid(row=2, column=0, padx=10, pady=10)

tk.Label(target_frame, text="Item Name").grid(row=0, column=0)
target_name_var = tk.StringVar()
target_name_dropdown = ttk.Combobox(target_frame, textvariable=target_name_var)
target_name_dropdown.grid(row=0, column=1)

tk.Label(target_frame, text="Target Quantity").grid(row=1, column=0)
target_quantity_entry = tk.Entry(target_frame)
target_quantity_entry.grid(row=1, column=1)

def set_target():
    name = target_name_var.get()
    quantity = int(target_quantity_entry.get())
    tracker.set_target(name, quantity)
    tracker.save_to_file()
    status_label.config(text=f"🎯 Set target of {quantity} for {name}")

tk.Button(target_frame, text="Set Target", command=set_target).grid(row=2, column=0, columnspan=2)

def finalize_day():
    tracker.finalize_daily_log()
    tracker.save_to_file()
    status_label.config(text="📘 Finalized today's log")


def export_csv():
    tracker.export_to_csv()
    status_label.config(text="📁 Exported data to CSV")

def open_daily_entry_sheet():
    outlet = outlet_var.get()
    entry_window = tk.Toplevel(root)
    entry_window.title(f"Daily Entry - {outlet}")

    entries = {}
    row = 0
    for item in tracker.stock:
        tk.Label(entry_window, text=item).grid(row=row, column=0)
        qty_entry = tk.Entry(entry_window, width=10)
        qty_entry.grid(row=row, column=1)
        entries[item] = qty_entry
        row += 1

    def submit_sales():
        for item, entry in entries.items():
            val = entry.get()
            if val.strip().isdigit():
                tracker.record_sale(outlet, item, int(val))
        tracker.save_to_file()
        status_label.config(text=f"✅ Recorded daily sales for {outlet}")
        entry_window.destroy()

    tk.Button(entry_window, text="Submit", command=submit_sales).grid(row=row, column=0, columnspan=2)
tk.Button(sale_frame, text="📋 Daily Entry Sheet", command=open_daily_entry_sheet).grid(row=3, column=0, columnspan=2)
tk.Button(summary_frame, text="📘 Finalize Day", command=finalize_day).grid(row=1, column=0, sticky="w")
tk.Button(summary_frame, text="Export to CSV", command=export_csv).grid(row=2, column=0, sticky="w")
tracker.load_from_file()
refresh_dropdowns()
# ========== Launch App ==========

root.mainloop()