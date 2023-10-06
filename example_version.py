import json
import datetime

class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.promotions = []

    def add_promotion(self, start_date, end_date, promo_price):
        self.promotions.append({"start_date": start_date, "end_date": end_date, "promo_price": promo_price})

    def is_on_promotion(self, date):
        for promo in self.promotions:
            if promo["start_date"] <= date <= promo["end_date"]:
                return promo["promo_price"]
        return self.price

class Supermarket:
    def __init__(self):
        self.products = {}
        self.receipt_number = 1

    def add_product(self, product_id, name, price):
        product = Product(product_id, name, price)
        self.products[product_id] = product

    def update_product(self, product_id, name, price):
        if product_id in self.products:
            product = self.products[product_id]
            product.name = name
            product.price = price

    def add_promotion_to_product(self, product_id, start_date, end_date, promo_price):
        if product_id in self.products:
            product = self.products[product_id]
            product.add_promotion(start_date, end_date, promo_price)

    def remove_promotion_from_product(self, product_id, start_date, end_date):
        if product_id in self.products:
            product = self.products[product_id]
            product.promotions = [promo for promo in product.promotions if promo["start_date"] != start_date or promo["end_date"] != end_date]

    def generate_receipt(self, cart):
        date = datetime.date.today().strftime("%Y%m%d")
        receipt_filename = f"RECEIPT_{date}.txt"
        
        with open(receipt_filename, "a") as receipt_file:
            receipt_file.write(f"Receipt #{self.receipt_number}\n")
            self.receipt_number += 1
            total_price = 0
            for item in cart:
                product_id, quantity = item
                if product_id in self.products:
                    product = self.products[product_id]
                    price = product.is_on_promotion(date)
                    total_item_price = price * quantity
                    receipt_file.write(f"{product.name} x{quantity}: {total_item_price} SEK\n")
                    total_price += total_item_price
            receipt_file.write(f"Total: {total_price} SEK\n")
            receipt_file.write("=" * 20 + "\n")

def main():
    supermarket = Supermarket()

    # Load products from a JSON file if it exists
    try:
        with open("products.json", "r") as product_file:
            data = json.load(product_file)
            for product_id, product_data in data.items():
                supermarket.add_product(product_id, product_data["name"], product_data["price"])
    except FileNotFoundError:
        pass

    while True:
        print("Retail Cashout System Menu:")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Add Promotion to Product")
        print("4. Remove Promotion from Product")
        print("5. Generate Receipt")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            product_id = input("Enter product ID: ")
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            supermarket.add_product(product_id, name, price)
        elif choice == "2":
            product_id = input("Enter product ID to update: ")
            name = input("Enter updated product name: ")
            price = float(input("Enter updated product price: "))
            supermarket.update_product(product_id, name, price)
        elif choice == "3":
            product_id = input("Enter product ID to add promotion: ")
            start_date = input("Enter promotion start date (YYYY-MM-DD): ")
            end_date = input("Enter promotion end date (YYYY-MM-DD): ")
            promo_price = float(input("Enter promotion price: "))
            supermarket.add_promotion_to_product(product_id, start_date, end_date, promo_price)
        elif choice == "4":
            product_id = input("Enter product ID to remove promotion from: ")
            start_date = input("Enter promotion start date to remove (YYYY-MM-DD): ")
            end_date = input("Enter promotion end date to remove (YYYY-MM-DD): ")
            supermarket.remove_promotion_from_product(product_id, start_date, end_date)
        elif choice == "5":
            cart = []
            while True:
                product_id_quantity = input("Enter product ID and quantity (e.g., '100 2', Enter 'done' to finish): ")
                if product_id_quantity.lower() == "done":
                    break
                else:
                    product_id, quantity = product_id_quantity.split()
                    cart.append((product_id, int(quantity)))
            supermarket.generate_receipt(cart)
            print("Receipt generated.")
        elif choice == "6":
            # Save the products to a JSON file before exiting
            data = {product_id: {"name": product.name, "price": product.price} for product_id, product in supermarket.products.items()}
            with open("products.json", "w") as product_file:
                json.dump(data, product_file, indent=4)
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
