import pandas as pd
import pickle
import os  # To check if the cart file exists

# Define the CartItem class for each product/item in the cart
class CartItem:
    def __init__(self, name, price, quantity):
        """
        Initialize a CartItem object with:
        - name: Name of the product/item (string)
        - price: Price of the product/item (float or int, assumed to be in INR)
        - quantity: Quantity of the product/item (int)
        """
        self.name = name
        self.price = price
        self.quantity = quantity
        self.next_item = None  # Points to the next item (None by default)

# Define the ShoppingCart class to manage multiple items using linked list style
class ShoppingCart:
    def __init__(self):
        """
        Initialize an empty shopping cart. The cart's head is set to None,
        indicating that the cart is currently empty.
        """
        self.head = None  # No items in the cart initially

    def add_item(self, name, price, quantity):
        """
        Adds a new item to the shopping cart:
        - name: Name of the item (string)
        - price: Price of the item (float or int, assumed to be in INR)
        - quantity: Quantity of the item (int)
        """
        # Create a new CartItem object
        new_item = CartItem(name, price, quantity)
        
        if self.head is None:
            # If the cart is empty, make the new item the head
            self.head = new_item
        else:
            # Otherwise, traverse the cart to add the new item at the end
            current = self.head
            while current.next_item is not None:
                current = current.next_item
            current.next_item = new_item
    
    def show_cart(self):
        """
        Displays the current contents of the cart in a tabular format.
        Uses pandas to show item details and total price.
        """
        if self.head is None:
            print("Shopping cart is empty.")
        else:
            # Traverse the linked list and collect all item details
            current = self.head
            items = []
            total = 0
            while current:
                items.append([current.name, f"₹{current.price}", current.quantity, f"₹{current.price * current.quantity}"])
                total += current.price * current.quantity
                current = current.next_item
            
            # Display the cart using pandas DataFrame
            df = pd.DataFrame(items, columns=["Item", "Price (INR)", "Quantity", "Total (INR)"])
            print(df)
            print(f"\nTotal Price: ₹{total}")

    def remove_item(self, name):
        """
        Removes an item by its name from the cart.
        - name: Name of the item to be removed (string)
        """
        if self.head is None:
            print("Cart is empty, nothing to remove.")
            return
        
        if self.head.name == name:
            # If the first item is the one to be removed
            self.head = self.head.next_item
            print(f"Removed {name} from the cart.")
        else:
            # Traverse the list to find and remove the item
            current = self.head
            while current.next_item is not None:
                if current.next_item.name == name:
                    current.next_item = current.next_item.next_item
                    print(f"Removed {name} from the cart.")
                    return
                current = current.next_item
            print(f"Item {name} not found in the cart.")

    def save_cart(self, filename):
        """
        Save the current cart state to a file using the pickle module.
        - filename: File path to save the cart (string)
        """
        try:
            with open(filename, 'wb') as f:
                pickle.dump(self, f)
            print("Cart saved successfully.")
        except Exception as e:
            print(f"Error saving cart: {e}")

    @staticmethod
    def load_cart(filename):
        """
        Load a saved cart from a file. If the file doesn't exist, return a new empty cart.
        - filename: File path to load the cart from (string)
        """
        if os.path.exists(filename):
            try:
                with open(filename, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Error loading cart: {e}")
        else:
            print("No saved cart found. Starting with an empty cart.")
            return ShoppingCart()

# Example usage
if __name__ == "__main__":
    cart = ShoppingCart.load_cart('shopping_cart.pkl')  # Load previous cart if available

    # Adding items to the cart
    cart.add_item("Laptop", 150000, 1)  # Prices in INR
    cart.add_item("Headphones", 2000, 2)
    cart.add_item("Keyboard", 1500, 1)

    cart.show_cart()  # Display the cart

    cart.remove_item("Headphones")  # Remove an item

    cart.show_cart()  # Display the cart again after removal

    cart.save_cart('shopping_cart.pkl')  # Save the cart state
