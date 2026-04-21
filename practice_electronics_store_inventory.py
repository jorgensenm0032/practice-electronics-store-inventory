# enter your code here

import peewee as p

db = p.SqliteDatabase("inventory.db")

class InventoryItem(p.Model):
    item_id = p.AutoField(primary_key = True)
    i_name = p.CharField()
    i_category = p.CharField()
    i_price = p.FloatField()
    i_stock = p.IntegerField()

    class Meta:
        database = db

    def get_info(self):
        print(f'\n{self.i_name} | {self.i_category} | Price per unit: {self.i_price} | Current stock: {self.i_stock}')

    @classmethod
    def create(cls, **query):
        check_price = query.get('i_price', 0)
        check_stock = query.get('i_stock', 0)

        create = True 

        if check_price < 0:
            print("Error: Price must be greater than or equal to 0.")
            create = False 

        if check_stock != 0 and check_stock % 10 != 0:
            print("Error: Stock must be 0 or in increments of 10.")
            create = False

        if create == True:
            return super(InventoryItem, cls).create(**query)
       
        else:
            return None
        
    
    def update_stock_by_10(self):
        self.i_stock += 10
        self.save()
        print(f"Stock for {self.i_name} is now: {self.i_stock}")


db.connect()
db.create_tables([InventoryItem]) 


while True:
    print("\nMenu")
    print("Option 1: Add an inventory item")
    print("Option 2: View all items")
    print("Option 3: View the average price of all items")
    print("Option 4: Delete an item by ID")
    print("Option 5: Add stock to an item by ID")
    print("Option 6: Exit")
    choice = input("Enter a number for the Menu option you would like to choose: ").strip()

    if choice == '1':
        name = input("\nEnter inventory item name: ").strip()
        category = input("Enter inventory item category: ").strip()
        price = float(input("Enter inventory item price: "))
        stock = int(input("Enter the current stock for this inventory item: "))

        inventory_obj = InventoryItem.create(i_name = name, i_category = category, i_price = price, i_stock = stock)

        if inventory_obj is not None:
            print("Item was successfully added.")
        
        else:
            continue 


    elif choice == "2":
        for item in InventoryItem.select():
            item.get_info()

    
    elif choice == "3":
        try: 
            total = 0 
            num_items = 0
            for item in InventoryItem.select():
                total += item.i_price
                num_items += 1

            price_avg = (total/num_items)
            print(f"Average price of all items: {price_avg}")

        except ZeroDivisionError:
            print("There are no items in your inventory, so we cannot print the average.")


    elif choice == "4":
        id_choice = int(input("Enter the ID of the item you would like to delete: "))
        item_to_delete = InventoryItem.get_or_none(InventoryItem.item_id == id_choice )

        if item_to_delete:
            item_to_delete.delete_instance()
            print('Item was successfully deleted. ')

        else:
            print("Invalid ID, please try again.")

    
    elif choice == "5":
        stock_id = int(input("Enter the ID of the item you would like to add stock to: "))
        item_to_add_to = InventoryItem.get_or_none(InventoryItem.item_id == stock_id)

        if item_to_add_to:
            item_to_add_to.update_stock_by_10()

        else:
            print("Invalid ID, please try again.")


    elif choice == "6":
        print("Goodbye")
        break

    else:
        print("Invalid choice. Please try again.")







        


        

    


