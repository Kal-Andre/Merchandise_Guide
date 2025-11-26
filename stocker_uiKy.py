from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup

from Stocker import StockTracker

tracker = StockTracker()
tracker.load_from_file()

class StockUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10

        # ---------- Outlet Selection ----------
        self.outlet_spinner = Spinner(
            text="BestBuy Bukoto",
            values=["BestBuy Bukoto", "Kenjoy Bukoto", "Carrefour Acacia"],
            size_hint=(1, None),
            height=40
        )
        self.add_widget(Label(text="Select Outlet"))
        self.add_widget(self.outlet_spinner)

        # ---------- Add Item ----------
        self.add_widget(Label(text="Add Item"))
        self.item_name = TextInput(hint_text="Item Name")
        self.item_qty = TextInput(hint_text="Stock Quantity", input_filter="int")
        self.add_btn = Button(text="Add Item", on_press=self.add_item)
        self.add_widget(self.item_name)
        self.add_widget(self.item_qty)
        self.add_widget(self.add_btn)

        # ---------- Remove Item ----------
        self.add_widget(Label(text="Remove Item"))
        self.remove_name = TextInput(hint_text="Item Name")
        self.remove_btn = Button(text="Remove Item", on_press=self.remove_item)
        self.add_widget(self.remove_name)
        self.add_widget(self.remove_btn)

        # ---------- Set Target ----------
        self.add_widget(Label(text="Set Target"))
        self.target_name = TextInput(hint_text="Item Name")
        self.target_qty = TextInput(hint_text="Target Quantity", input_filter="int")
        self.target_btn = Button(text="Set Target", on_press=self.set_target)
        self.add_widget(self.target_name)
        self.add_widget(self.target_qty)
        self.add_widget(self.target_btn)

        # ---------- Weekly Balance Entry ----------
        self.balance_btn = Button(text="📊 Weekly Balance Entry", on_press=self.open_weekly_balance_popup)
        self.add_widget(self.balance_btn)

        # ---------- Summary ----------
        self.summary_btn = Button(text="Show Summary", on_press=self.show_summary)
        self.export_outlet_btn = Button(text="📁 Export Outlet Summary", on_press=lambda x: self.export_outlet_summary())
        self.export_monthly_btn = Button(text="📊 Export Monthly Roll-Up", on_press=lambda x: self.export_monthly_rollup())
        self.add_widget(self.summary_btn)
        self.add_widget(self.export_outlet_btn)
        self.add_widget(self.export_monthly_btn)

        # ---------- Status Label ----------
        self.status_label = Label(text="", color=(0,1,0,1))
        self.add_widget(self.status_label)

    # ---------- Callbacks ----------
    def add_item(self, instance):
        name = self.item_name.text.strip()
        qty = int(self.item_qty.text) if self.item_qty.text.isdigit() else 0
        if name:
            tracker.add_item(name, qty)
            tracker.save_to_file()
            self.status_label.text = f"✅ Added {qty} units of {name}"

    def remove_item(self, instance):
        name = self.remove_name.text.strip()
        if name:
            tracker.remove_item(name)
            tracker.save_to_file()
            self.status_label.text = f"🗑️ Removed {name} from tracker"
        else:
            self.status_label.text = "⚠️ Please enter an item name to remove"

    def set_target(self, instance):
        name = self.target_name.text.strip()
        qty = int(self.target_qty.text) if self.target_qty.text.isdigit() else 0
        if name:
            tracker.set_target(name, qty)
            tracker.save_to_file()
            self.status_label.text = f"🎯 Set target of {qty} for {name}"

    def open_weekly_balance_popup(self, instance):
        outlet = self.outlet_spinner.text
        layout = GridLayout(cols=2, spacing=5, padding=10)
        entries = {}

        for item in tracker.stock:
            layout.add_widget(Label(text=item))
            entry = TextInput(input_filter="int")
            layout.add_widget(entry)
            entries[item] = entry

        def submit_balances(btn):
            for item, entry in entries.items():
                if entry.text.isdigit():
                    balance = int(entry.text)
                    tracker.record_weekly_balance(outlet, item, balance)
            tracker.save_to_file()
            self.status_label.text = f"✅ Recorded weekly balances for {outlet}"
            popup.dismiss()

        submit_btn = Button(text="Submit", on_press=submit_balances)
        layout.add_widget(submit_btn)

        popup = Popup(title=f"Weekly Balance Entry - {outlet}", content=layout, size_hint=(0.8, 0.8))
        popup.open()

    def show_summary(self, instance):
        layout = GridLayout(cols=1, spacing=5, padding=10)
        for item in tracker.stock:
            weekly_sold = sum(tracker.weekly_sales.get(outlet, {}).get(item, 0) for outlet in tracker.weekly_sales)
            daily_est = weekly_sold / 7 if weekly_sold else 0
            cumulative = sum(tracker.sales.get(outlet, {}).get(item, 0) for outlet in tracker.sales)
            target = tracker.targets.get(item, 0)
            progress = (cumulative / target * 100) if target else 0
            layout.add_widget(Label(text=f"{item}: Weekly={weekly_sold}, Daily≈{daily_est:.2f}, Total={cumulative}, Target={target}, Progress={progress:.2f}%"))

        popup = Popup(title="Summary Report", content=layout, size_hint=(0.9, 0.9))
        popup.open()

    def export_outlet_summary(self):
        tracker.export_to_csv()
        self.status_label.text = "📁 Exported outlet summary to CSV"

    def export_monthly_rollup(self):
        tracker.export_monthly_summary()
        self.status_label.text = "📊 Exported monthly roll-up to CSV"


class StockApp(App):
    def build(self):
        return StockUI()


if __name__ == "__main__":
    StockApp().run()