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
        self.add_widget(Label(text="Select Outlet"))
        self.outlet_spinner = Spinner(
            text="BestBuy Bukoto",
            values=["BestBuy Bukoto", "Kenjoy Bukoto", "Carrefour Acacia"],
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.outlet_spinner)

        # ---------- Item Management ----------
        item_layout = GridLayout(cols=3, spacing=5, size_hint_y=None, height=60)
        self.item_name = TextInput(hint_text="Item Name")
        self.item_qty = TextInput(hint_text="Stock Quantity", input_filter="int")
        add_btn = Button(text="Add Item", on_press=self.add_item)
        item_layout.add_widget(self.item_name)
        item_layout.add_widget(self.item_qty)
        item_layout.add_widget(add_btn)
        self.add_widget(Label(text="Item Management"))
        self.add_widget(item_layout)

        remove_layout = GridLayout(cols=2, spacing=5, size_hint_y=None, height=60)
        self.remove_spinner = Spinner(text="Select Item", values=list(tracker.stock.keys()))
        remove_btn = Button(text="Remove Item", on_press=self.remove_item)
        remove_layout.add_widget(self.remove_spinner)
        remove_layout.add_widget(remove_btn)
        self.add_widget(remove_layout)

        # ---------- Set Target ----------
        target_layout = GridLayout(cols=3, spacing=5, size_hint_y=None, height=60)
        self.target_spinner = Spinner(text="Select Item", values=list(tracker.stock.keys()))
        self.target_qty = TextInput(hint_text="Target Quantity", input_filter="int")
        target_btn = Button(text="Set Target", on_press=self.set_target)
        target_layout.add_widget(self.target_spinner)
        target_layout.add_widget(self.target_qty)
        target_layout.add_widget(target_btn)
        self.add_widget(Label(text="Set Target"))
        self.add_widget(target_layout)

        # ---------- Summary ----------
        summary_layout = GridLayout(cols=2, spacing=5, size_hint_y=None, height=160)
        self.summary_spinner = Spinner(
            text="All Outlets",
            values=["All Outlets", "BestBuy Bukoto", "Kenjoy Bukoto", "Carrefour Acacia"]
        )
        summary_btn = Button(text="Show Summary", on_press=self.show_summary)
        export_outlet_btn = Button(text="📁 Export Outlet Summary", on_press=lambda x: self.export_outlet_summary())
        export_monthly_btn = Button(text="📊 Export Monthly Roll-Up", on_press=lambda x: self.export_monthly_rollup())
        weekly_balance_btn = Button(text="📊 Weekly Balance Entry", on_press=self.open_weekly_balance_popup)

        summary_layout.add_widget(self.summary_spinner)
        summary_layout.add_widget(summary_btn)
        summary_layout.add_widget(export_outlet_btn)
        summary_layout.add_widget(export_monthly_btn)
        summary_layout.add_widget(weekly_balance_btn)
        self.add_widget(Label(text="Summary"))
        self.add_widget(summary_layout)

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
            self.item_name.text = ""
            self.item_qty.text = ""
            self.refresh_spinners()

    def remove_item(self, instance):
        name = self.remove_spinner.text.strip()
        if name and name in tracker.stock:
            # Confirmation popup
            layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
            layout.add_widget(Label(text=f"Remove '{name}'?"))
            btns = BoxLayout(spacing=10, size_hint_y=None, height=40)
            def confirm(btn):
                tracker.remove_item(name)
                tracker.save_to_file()
                self.status_label.text = f"🗑️ Removed {name} from tracker"
                self.refresh_spinners()
                popup.dismiss()
            def cancel(btn):
                popup.dismiss()
            btns.add_widget(Button(text="Yes", on_press=confirm))
            btns.add_widget(Button(text="Cancel", on_press=cancel))
            layout.add_widget(btns)
            popup = Popup(title="Confirm Removal", content=layout, size_hint=(0.6,0.4))
            popup.open()

    def set_target(self, instance):
        name = self.target_spinner.text.strip()
        qty = int(self.target_qty.text) if self.target_qty.text.isdigit() else 0
        if name:
            tracker.set_target(name, qty)
            tracker.save_to_file()
            self.status_label.text = f"🎯 Set target of {qty} for {name}"
            self.target_spinner.text = "Select Item"
            self.target_qty.text = ""

    def open_weekly_balance_popup(self, instance):
        outlet = self.outlet_spinner.text
        layout = GridLayout(cols=2, spacing=5, padding=10)
        entries = {}
        for item in tracker.stock:
            layout.add_widget(Label(text=item))
            entry = TextInput(input_filter="int")
            layout.add_widget(entry)
            entries[item] = entry

        def submit(btn):
            for item, entry in entries.items():
                if entry.text.isdigit():
                    tracker.record_weekly_balance(outlet, item, int(entry.text))
            tracker.save_to_file()
            self.status_label.text = f"✅ Recorded weekly balances for {outlet}"
            popup.dismiss()

        layout.add_widget(Button(text="Submit", on_press=submit))
        popup = Popup(title=f"Weekly Balance Entry - {outlet}", content=layout, size_hint=(0.8,0.8))
        popup.open()

    def show_summary(self, instance):
        selected_outlet = self.summary_spinner.text
        layout = BoxLayout(orientation="vertical", spacing=5, padding=10)
        for item in tracker.stock:
            weekly_sold = sum((tracker.weekly_sales.get(outlet) or {}).get(item, 0)
                              for outlet in (tracker.weekly_sales.keys() if isinstance(tracker.weekly_sales, dict) else []))
            cumulative = sum((tracker.sales.get(outlet) or {}).get(item, 0)
                             for outlet in (tracker.sales.keys() if isinstance(tracker.sales, dict) else []))
            daily_est = weekly_sold / 7 if weekly_sold else 0
            target = tracker.targets.get(item, 0)
            progress = (cumulative / target * 100) if target else 0
            layout.add_widget(Label(text=f"{item}: Weekly={weekly_sold}, Daily≈{daily_est:.2f}, Total={cumulative}, Target={target}, Progress={progress:.2f}%"))
        popup = Popup(title=f"Summary Report - {selected_outlet}", content=layout, size_hint=(0.9,0.9))
        popup.open()

    def export_outlet_summary(self):
        tracker.export_to_csv()
        self.status_label.text = "📁 Exported outlet summary to CSV"

    def export_monthly_rollup(self):
        tracker.export_monthly_summary()
        self.status_label.text = "📊 Exported monthly roll-up to CSV"

    def refresh_spinners(self):
        items = list(tracker.stock.keys())
        self.remove_spinner.values = items
        self.target_spinner.values = items

class StockApp(App):
    def build(self):
        return StockUI()

if __name__ == "__main__":
    StockApp().run()