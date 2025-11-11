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
        if name in self.stock:
            if self.stock[name] >= quantity_sold:
                self.stock[name] -= quantity_sold
            else:
                print("NOT ENOUGH STOCK.")
        else:
            print("ITEM NOT FOUND")

    # Another dictionary to store sales history
    def get_sales(self, name):
        if not hasattr(self, 'sales'):
            self.sales = {}
        if name in self.stock:
            if name not in self.sales:
                self.sales[name] = 0
            return self.sales[name]
        else:
            print("Item not found")

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
    print("1. Add item \n 2. Update Stock \n 3. Get stock \n 4. Record sale \n 5. View sales \n 6. Exit")
    choice = input("Choose an option: ")
    if choice == '1':
        name = input("Enter item name: ")
        quantity = int(input("Enter Quantity: "))
        tracker.add_item(name, quantity)
    elif choice == '2':
        name = input("Enter item name: ")
        quantity = int(input("Enter Quantity: "))
        tracker.update_stock(name, quantity)
    elif choice == '3':
        print(tracker.get_stock())
    elif choice == '4':
        name = input("Enter item name: ")
        quantity_sold = int(input("Enter quantity sold: "))
        tracker.record_sale(name, quantity_sold)
        tracker.update_sales(name, quantity_sold)
    elif choice == '5':
        name = input("Enter item name: ")
        print(tracker.get_sales(name))
    elif choice == '6':
        break
    else:
        print("Invalid option!!")
    

        
