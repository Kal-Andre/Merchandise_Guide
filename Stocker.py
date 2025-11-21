# 1. Stock tracking
# We're storing the data in json format for easy access and modification.
import json
# We're logging data to its added dates.
import datetime
# Exporting to CSV
import csv
class StockTracker:
    def __init__(self):
        self.stock = {}
        self.sales = {}
        self.targets = {}
        self.daily_log =[] # Temporary log for today's activities
        self.sales = {
            "BestBuy Bukoto": {},
            "Kenjoy Bukoto": {},
            "Carrefour Acacia": {}
        }
        self.weekly_sales = {} # Track last week's sold units per outlet
    # StockTracker manages stock & initialises an empty dictionary to store items

    def add_item(self, name, quantity):
        self.stock[name] = quantity
        self.sales[name] = 0
        self.daily_log.append(f"Added {quantity} units of {name}")
    # Add new items to the dictionary
    
    def update_stock(self, name, quantity):
        if name in self.stock:
            old_quantity = self.stock[name]
            self.stock[name] = quantity
            self.daily_log.append(f"Updated stock for {name}: {old_quantity} → {quantity}")
        else:
            print("Item not found")


    # Method to update existing stock quantities
    
    def get_stock(self):
        return self.stock

    # Method to retrieve entire stock dictionary.

    # Stage 2. Sales Tracker

    '''def record_sale(self, outlet, name, quantity_sold):
        if outlet not in self.sales:
            self.sales[outlet] = {}
        if name not in self.stock:
            print("ITEM NOT FOUND")
            return
        if self.stock[name] < quantity_sold:
            print("NOT ENOUGH STOCK.")
            return
        self.sales[outlet][name] = self.sales[outlet].get(name, 0) + quantity_sold
        self.stock[name] -= quantity_sold
        self.sales[name] += quantity_sold
        self.daily_log.append(f"Sold {quantity_sold} units of {name}")'''

    # We shall use record weekly stock balances other than daily sales. 
    def record_weekly_balance(self, outlet, item, balance):
        if outlet not in self.weekly_balances:
            self.weekly_balances[outlet] = {}
        if outlet not in self.sales:
            self.sales[outlet] = {}
        if outlet not in self.weekly_sales:
            self.weekly_sales[outlet] = {}

        prev_balance = self.weekly_balances[outlet].get(item, balance)
        sold = prev_balance - balance
        self.weekly_balances[outlet][item] = balance
        self.sales[outlet][item] = self.sales[outlet].get(item, 0) + sold
        self.weekly_sales[outlet][item] = sold # Store weekly sold separately

        self.stock[item] = balance
    # Another dictionary to store sales history
    def get_sales(self, name):
        return self.sales.get(name, 0)
    
    # Stage 3: Target Tracker

    def set_target(self, name, target_quantity):
        old_target = self.targets.get(name, 0)
        self.targets[name] = target_quantity
        self.daily_log.append(f"Set target for {name}: {old_target} → {target_quantity}")

    
    def check_progress(self, name):
        sold = self.sales.get(name, 0)
        target = self.targets.get(name, 0)
        if target == 0:
            print(f"No target set for {name}.")
            return
        percent =(sold /target) * 100
        print(f"{name}: {percent:.2f}% of target reached.")

    def update_sales(self, name, quantity_Sold):
        if name in self.stock:
            if not hasattr(self, 'sales'):
                self.sales = {}
            if name not in self.sales:
                self.sales[name] = 0
            self.sales[name] += quantity_Sold
        else:
            print("Item not found")
    
    # Stage 4. Saving to file
    def save_to_file(self, filename="StockData.json"):
        data = {
            'stock': self.stock,
            'sales': self.sales,
            'targets': self.targets
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    # Loading from file
    def load_from_file(self, filename="StockData.json"):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.stock = data.get('stock', {})
                self.sales = data.get('sales', {})
                self.targets = data.get('targets', {})
        except FileNotFoundError:
            print("No saved data found.")
            
    # Stage 5. Making a summary report that is tabular.
    def summary_report(self):
        headers = ["Item", "Stock", "Sold", "Target", "Progress"]
        col_widths = [20, 10, 10, 10, 10]
    
        # Print header
        for header, width in zip(headers, col_widths):
            print(header.ljust(width), end="")
        print()
        print("-" * sum(col_widths))
    
        # Print rows
        for name in self.stock:
            stock = str(self.stock.get(name, 0)).ljust(col_widths[1])
            sold = str(self.sales.get(name, 0)).ljust(col_widths[2])
            target = str(self.targets.get(name, 0)).ljust(col_widths[3])
            progress = f"{(self.sales.get(name, 0) / self.targets.get(name, 1) * 100):.2f}%" if self.targets.get(name, 0) else "0.00%"
            progress = progress.ljust(col_widths[4])
    
            print(name.ljust(col_widths[0]), stock, sold, target, progress)
    
    # Stage 6. Logging daily activities with dates
    def finalize_daily_log(self):
        today = datetime.today().date()
        dated_log = [f"{entry} on {today}" for entry in self.daily_log]
        self.history = self.history if hasattr(self, 'history') else []
        self.history.extend(dated_log)
        self.daily_log = []  # Clear for next day

    # Stage 7. Exporting to CSV
    def export_to_csv(self, filename="stock_report.csv"):
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Outlet", "Item", "Weekly Sold", "Daily Estimate",
                "Cumulative Sold", "Target", "Progress"
            ])

            for outlet in self.sales:
                for item in self.stock:
                    # Weekly sold (from weekly_sales dict)
                    weekly_sold = self.weekly_sales.get(outlet, {}).get(item, 0)

                    # Daily estimate = weekly ÷ 7
                    daily_est = weekly_sold / 7 if weekly_sold else 0

                    # Cumulative sold (from sales dict)
                    cumulative_sold = self.sales[outlet].get(item, 0)

                    # Target and progress
                    target = self.targets.get(item, 0)
                    progress = (cumulative_sold / target * 100) if target else 0

                    writer.writerow([
                        outlet, item, weekly_sold, f"{daily_est:.2f}",
                        cumulative_sold, target, f"{progress:.2f}%"
                    ])
    
    # Stage 8. Enable removing items
    def remove_item(self, name):
        if name in self.stock:
            del self.stock[name]
            del self.sales[name]
            if name in self.targets:
                del self.targets[name]
            self.daily_log.append(f"Removed item {name} from tracker")
        else:
            print("Item not found")

    # Stage 9. Finalize daily log at the end of the day
    def finalize_daily_log(self):
        today = datetime.today().date()
        dated_log = [f"{entry} on {today}" for entry in self.daily_log]
        self.history = self.history if hasattr(self, 'history') else []
        self.history.extend(dated_log)
        self.daily_log = []

    def export_monthly_summary(self, filename="monthly_summary.csv"):
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Item", "Total Weekly Sold", "Daily Estimate",
                "Cumulative Sold", "Target", "Progress"
            ])
    
            for item in self.stock:
                # Aggregate weekly sold across all outlets
                total_weekly_sold = sum(
                    self.weekly_sales.get(outlet, {}).get(item, 0)
                    for outlet in self.weekly_sales
                )
    
                # Daily estimate = weekly ÷ 7
                daily_est = total_weekly_sold / 7 if total_weekly_sold else 0
    
                # Aggregate cumulative sold across all outlets
                cumulative_sold = sum(
                    self.sales.get(outlet, {}).get(item, 0)
                    for outlet in self.sales
                )

            # Target and progress
            target = self.targets.get(item, 0)
            progress = (cumulative_sold / target * 100) if target else 0

            writer.writerow([
                item, total_weekly_sold, f"{daily_est:.2f}",
                cumulative_sold, target, f"{progress:.2f}%"
            ])
tracker = StockTracker()
        
# Ensures the app loads existing data on startup
tracker.load_from_file()