from peewee import *

# Database setup
db = SqliteDatabase('inventory.db')

class InventoryItem(Model):
    item_id = AutoField(primary_key=True)
    name = CharField()
    category = CharField()
    price = FloatField()
    stock = IntegerField()

    class Meta:
        database = db

    @classmethod
    def create(cls, **query):
        if query['price'] < 0:
            print("Invalid price! Price must be greater than or equal to $0.")
            return # don't create a new row
        if query['stock'] >= 0 and query['stock'] % 10 != 0:
            print("Invalid stock! Stock must be 0 or in increments of 10.")
            return # don't create a new row
        new_item = super().create(**query) # store item in variable after being created
        print(f"Item '{query['name']}' added successfully.") 
        return new_item # return that item

    def update_stock_by_10(self):
        self.stock += 10
        self.save()
        print(f"Stock for '{self.name}' updated to {self.stock}.")

    def get_info(self):
        return f"ID: {self.item_id} | Name: {self.name} | Category: {self.category} | Price: ${self.price} | Stock: {self.stock}"

# create/connect to the database
db.connect()
db.create_tables([InventoryItem])

# just separating out logic into its own function. You could put this anywhere.
# You could also try converting things into lists and using built in average
# functions, but I like showing a solution that doesn't require knowing about
# any extra functions.
def view_average_price():
    items = InventoryItem.select()
    total_price = 0
    count = 0
    for item in items:
        total_price += item.price
        count += 1
    if count == 0:
        print("No items in the database.")
    else:
        avg_price = total_price / count
        print(f"Average price of all items: ${avg_price:.2f}")

while True:
    print("\nElectronics Store Inventory Manager:")
    print("1. Add an inventory item")
    print("2. View all items")
    print("3. View average price of all items")
    print("4. Delete an item by ID")
    print("5. Add stock to an item by ID")
    print("6. Exit")

    choice = input("Choose an option (1-6): ")
    if choice == "1":
        name = input("Enter the item name: ")
        category = input("Enter the category: ")
        price = float(input("Enter the price: "))
        stock = int(input("Enter the stock (in increments of 10): "))
        InventoryItem.create(name=name, category=category, price=price, stock=stock)
    
    elif choice == "2":
        items = InventoryItem.select()
        for item in items:
            print(item.get_info())
    
    elif choice == "3":
        view_average_price()
    
    elif choice == "4":
        item_id = int(input("Enter the ID of the item to delete: "))
        item = InventoryItem.get(InventoryItem.item_id == item_id)
        item_name = item.name
        item.delete_instance()
        print(f"Item '{item_name}' deleted successfully.")
    
    elif choice == "5":
        item_id = int(input("Enter the ID of the item to add stock to: "))
        # assume that id is always valid. Will get a single item.
        item = InventoryItem.get(InventoryItem.item_id == item_id)
        item.update_stock_by_10() # run method to update by 10
    
    elif choice == "6":
        print("Goodbye.")
        break
    
    else:
        print("Invalid choice. Please try again.")

