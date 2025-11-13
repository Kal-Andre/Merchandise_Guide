# tracker_cli.py
from Stocker import StockTracker

tracker = StockTracker()
tracker.load_from_file()

while True:
    while True:
        print("\n1. Add item\n2. Update Stock\n3. Get Stock\n4. Record Sale\n5. View Sales\n6. Set Target\n7. Check Progress\n8. Summary Report\n9. Export to CSV\n10. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter item name: ")
            quantity = int(input("Enter quantity: "))
            tracker.add_item(name, quantity)
            tracker.save_to_file()

        elif choice == '2':
            name = input("Enter item name: ")
            quantity = int(input("Enter new stock quantity: "))
            tracker.update_stock(name, quantity)
            tracker.save_to_file()

        elif choice == '3':
            print(tracker.get_stock())

        elif choice == '4':
            name = input("Enter item name: ")
            quantity_sold = int(input("Enter quantity sold: "))
            tracker.record_sale(name, quantity_sold)
            tracker.save_to_file()

        elif choice == '5':
            name = input("Enter item name: ")
            print(f"Total sold: {tracker.get_sales(name)}")

        elif choice == '6':
            name = input("Enter item name: ")
            target = int(input("Enter sales target: "))
            tracker.set_target(name, target)
            tracker.save_to_file()

        elif choice == '7':
            name = input("Enter item name: ")
            tracker.check_progress(name)

        elif choice == '8':
            tracker.summary_report()

        elif choice == '9':
            tracker.export_to_csv()
        elif choice == '10':
            break

        else:
            print("Invalid option!")