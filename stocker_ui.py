import tkinter as tk
from tkinter import ttk
from Stocker import StockTracker

# Initialize tracker
tracker = StockTracker()
tracker.load_from_file()

# Create main window
root = tk.Tk()
root.title("Soft Drink Stock Tracker")

# ========== Outlet Selection ==========
outlet_var = tk.StringVar()
tk.Label(root, text="Select Outlet").grid(row=0, column=0, padx=10, pady=10, sticky="w")
outlet_dropdown = ttk.Combobox(root, textvariable=outlet_var, width=30)
outlet_dropdown['values'] = ["BestBuy Bukoto", "Kenjoy Bukoto", "Carrefour Acacia"]
outlet_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")
outlet_var.set("BestBuy Bukoto")

# ========== Item Management ==========
item_frame = tk.LabelFrame(root, text="Item Management", padx=20, pady=10)
item_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

item_name_entry = tk.Entry(item_frame, width=20)
item_name_entry.grid(row=0, column=0, padx=5, pady=5)
stock_entry = tk.Entry(item_frame, width=10)
stock_entry.grid(row=0, column=1, padx=5, pady=5)

def add_item():
    name = item_name_entry.get().strip()
    qty = int(stock_entry.get()) if stock_entry.get().isdigit() else 0
    if name:
        tracker.add_item(name, qty)
        tracker.save_to_file()
        status_label.config(text=f"✅ Added {qty} units of {name}")
        refresh_dropdowns()

tk.Button(item_frame, text="Add Item", command=add_item).grid(row=0, column=2, padx=5)

remove_item_var = tk.StringVar()
tk.Entry(item_frame, textvariable=remove_item_var, width=20).grid(row=1, column=0, padx=5, pady=5)
tk.Button(item_frame, text="Remove Item", command=lambda: remove_item_ui()).grid(row=1, column=1, padx=5)

def remove_item_ui():
    name = remove_item_var.get().strip()
    if name:
        tracker.remove_item(name)
        tracker.save_to_file()
        status_label.config(text=f"🗑️ Removed {name} from tracker")
        refresh_dropdowns()
    else:
        status_label.config(text="⚠️ Please enter an item name to remove")

# ========== Set Target ==========
target_frame = tk.LabelFrame(root, text="Set Target", padx=20, pady=10)
target_frame.grid(row=1, column=1, padx=10, pady=10, sticky="w")

target_name_var = tk.StringVar()
target_name_dropdown = ttk.Combobox(target_frame, textvariable=target_name_var, width=20)
target_name_dropdown.grid(row=0, column=0, padx=5, pady=5)

target_quantity_entry = tk.Entry(target_frame, width=10)
target_quantity_entry.grid(row=0, column=1, padx=5, pady=5)

def set_target():
    name = target_name_var.get().strip()
    qty = int(target_quantity_entry.get()) if target_quantity_entry.get().isdigit() else 0
    if name:
        tracker.set_target(name, qty)
        tracker.save_to_file()
        status_label.config(text=f"🎯 Set target of {qty} for {name}")

tk.Button(target_frame, text="Set Target", command=set_target).grid(row=1, column=0, columnspan=2, pady=5)

# ========== Summary Frame ==========
summary_frame = tk.LabelFrame(root, text="Summary", padx=20, pady=10)
summary_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")

summary_outlet_var = tk.StringVar()
summary_outlet_dropdown = ttk.Combobox(summary_frame, textvariable=summary_outlet_var, width=30)
summary_outlet_dropdown['values'] = ["All Outlets", "BestBuy Bukoto", "Kenjoy Bukoto", "Carrefour Acacia"]
summary_outlet_dropdown.grid(row=0, column=1, padx=5)
summary_outlet_var.set("All Outlets")

def show_summary():
    selected_outlet = summary_outlet_var.get()
    summary_window = tk.Toplevel(root)
    summary_window.title(f"Summary Report - {selected_outlet}")
    text = tk.Text(summary_window, width=100, height=25)
    text.pack()

    headers = f"{'Item':<20}{'Weekly Sold':<15}{'Daily Est.':<15}{'Cumulative Sold':<15}{'Target':<10}{'Progress':<10}\n"
    text.insert(tk.END, headers + "-"*80 + "\n")

    if selected_outlet == "All Outlets":
        for item in tracker.stock:
            weekly_sold = sum(tracker.weekly_sales.get(outlet, {}).get(item, 0) for outlet in tracker.weekly_sales)
            cumulative_sold = sum(tracker.sales.get(outlet, {}).get(item, 0) for outlet in tracker.sales)
            daily_est = weekly_sold / 7 if weekly_sold else 0
            target = tracker.targets.get(item, 0)
            progress = (cumulative_sold / target * 100) if target else 0
            line = f"{item:<20}{weekly_sold:<15}{daily_est:<15.2f}{cumulative_sold:<15}{target:<10}{progress:.2f}%\n"
            text.insert(tk.END, line)
    else:
        outlet_sales = tracker.sales.get(selected_outlet, {})
        for item in tracker.stock:
            weekly_sold = tracker.weekly_sales.get(selected_outlet, {}).get(item, 0)
            cumulative_sold = outlet_sales.get(item, 0)
            daily_est = weekly_sold / 7 if weekly_sold else 0
            target = tracker.targets.get(item, 0)
            progress = (cumulative_sold / target * 100) if target else 0
            line = f"{item:<20}{weekly_sold:<15}{daily_est:<15.2f}{cumulative_sold:<15}{target:<10}{progress:.2f}%\n"
            text.insert(tk.END, line)

tk.Button(summary_frame, text="Show Summary", command=show_summary).grid(row=0, column=0, sticky="w", pady=5)
tk.Button(summary_frame, text="📁 Export Outlet Summary", command=lambda: export_outlet_summary()).grid(row=1, column=0, sticky="w", pady=5)
tk.Button(summary_frame, text="📊 Export Monthly Roll-Up", command=lambda: export_monthly_rollup()).grid(row=2, column=0, sticky="w", pady=5)
tk.Button(summary_frame, text="📊 Weekly Balance Entry", command=lambda: open_weekly_balance_entry()).grid(row=3, column=0, sticky="w", pady=5)

def export_outlet_summary():
    tracker.export_to_csv()
    status_label.config(text="📁 Exported outlet summary to CSV")

def export_monthly_rollup():
    tracker.export_monthly_summary()
    status_label.config(text="📊 Exported monthly roll-up to CSV")

def open_weekly_balance_entry():
    outlet = outlet_var.get()
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

# ========== Status Label ==========
status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=3, column=0, columnspan=2, pady=10, sticky="w")

def refresh_dropdowns():
    items = list(tracker.stock.keys())
    target_name_dropdown['values'] = items

refresh_dropdowns()
root.mainloop()