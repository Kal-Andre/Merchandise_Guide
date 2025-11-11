# 1. Stock tracking
class StockTracker:
    def __init__(self):
        self.stock = {}
        self.sales = {}
        self.targets = {}

    # StockTracker manages stock & initialises an empty dictionary to store items

    def add_item(self, name, quantity):
        self.stock[name] = quantity
        self.sales[name] = 0
    # Add new items to the dictionary
    
    def update_stock(self, name, quantity):
        if name in self.stock:
            self.stock[name] = quantity
        else:
            print("Item not found")

    # Method to update existing stock quantities
    
    def get_stock(self):
        return self.stock

    # Method to retrieve entire stock dictionary.

    # Stage 2. Sales Tracker

    def record_sale(self, name, quantity_sold):
        if name not in self.stock:
            print("ITEM NOT FOUND")
            return
        if self.stock[name] < quantity_sold:
            print("NOT ENOUGH STOCK.")
            return
        self.stock[name] -= quantity_sold
        self.sales[name] += quantity_sold


    # Another dictionary to store sales history
    def get_sales(self, name):
        return self.sales.get(name, 0)
    
    # Sets targets

    def set_target(self, name, target_quantity):
        self.targets[name] = target_quantity

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
            self.sales[name] += quantity_sold
        else:
            print("Item not found")
tracker = StockTracker()

while True:
    print("\n1. Add item\n2. Update Stock\n3. Get Stock\n4. Record Sale\n5. View Sales\n6. Set Target\n7. Check Progress\n8. Exit")
    choice = input("Choose an option: ")

    if choice == '1':
        name = input("Enter item name: ")
        quantity = int(input("Enter quantity: "))
        tracker.add_item(name, quantity)

    elif choice == '2':
        name = input("Enter item name: ")
        quantity = int(input("Enter new stock quantity: "))
        tracker.update_stock(name, quantity)

    elif choice == '3':
        print(tracker.get_stock())

    elif choice == '4':
        name = input("Enter item name: ")
        quantity_sold = int(input("Enter quantity sold: "))
        tracker.record_sale(name, quantity_sold)

    elif choice == '5':
        name = input("Enter item name: ")
        print(f"Total sold: {tracker.get_sales(name)}")

    elif choice == '6':
        name = input("Enter item name: ")
        target = int(input("Enter sales target: "))
        tracker.set_target(name, target)

    elif choice == '7':
        name = input("Enter item name: ")
        tracker.check_progress(name)

    elif choice == '8':
        break

    else:
        print("Invalid option!")