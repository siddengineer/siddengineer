import sqlite3

# Path to SQLite database
DATABASE = 'vegetable_platform.db'

# Function to get the database connection
def get_db():
    try:
        conn = sqlite3.connect(DATABASE)
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")

# Function to initialize the database and create tables
def init_db():
    conn = get_db()
    if conn:
        cursor = conn.cursor()
        try:
            # Create sellers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sellers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            ''')

            # Create vegetables table with unique constraint on name
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vegetables (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    seller_id INTEGER,
                    name TEXT NOT NULL UNIQUE,
                    price REAL NOT NULL,
                    FOREIGN KEY (seller_id) REFERENCES sellers(id)
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
        finally:
            conn.close()

# Function to add a seller only if not exists
def add_seller(name):
    conn = get_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO sellers (name) VALUES (?)", (name,))
            conn.commit()
            print(f"Seller '{name}' added successfully.")
        except sqlite3.IntegrityError:
            print(f"Seller '{name}' already exists.")
        except sqlite3.Error as e:
            print(f"Error adding seller: {e}")
        finally:
            conn.close()

# Function to log in a seller
def login_seller(name):
    conn = get_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM sellers WHERE name=?", (name,))
            seller = cursor.fetchone()
            return seller[0] if seller else None
        except sqlite3.Error as e:
            print(f"Error logging in: {e}")
        finally:
            conn.close()
    return None

# Function to update vegetables and prices for a seller
def update_vegetables(seller_id, veg_name, price):
    conn = get_db()
    if conn:
        cursor = conn.cursor()
        try:
            if not veg_name or price < 0:
                print("Invalid vegetable name or price.")
                return

            # First try to update the vegetable
            cursor.execute('''
                UPDATE vegetables
                SET price = ?
                WHERE seller_id = ? AND name = ?
            ''', (price, seller_id, veg_name))

            # Check if the update was successful
            if cursor.rowcount == 0:
                # If no rows were updated, insert the vegetable
                cursor.execute('''
                    INSERT INTO vegetables (seller_id, name, price)
                    VALUES (?, ?, ?)
                ''', (seller_id, veg_name, price))

            conn.commit()
            print(f"Vegetable '{veg_name}' updated with price {price}.")
        except sqlite3.Error as e:
            print(f"Error updating vegetables: {e}")
        finally:
            conn.close()

# Function to view vegetables and their prices
def view_vegetables():
    conn = get_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT sellers.name, vegetables.name, vegetables.price
                FROM vegetables
                JOIN sellers ON vegetables.seller_id = sellers.id
            ''')
            vegetables = cursor.fetchall()
            if vegetables:
                print("Vegetables available:")
                for seller_name, veg_name, price in vegetables:
                    print(f"Seller: {seller_name}, Vegetable: {veg_name}, Price: {price}")
            else:
                print("No vegetables available.")
        except sqlite3.Error as e:
            print(f"Error retrieving vegetables: {e}")
        finally:
            conn.close()

# Command-line interface to interact with the platform
def main():
    init_db()  # Initialize the database (create tables if not exists)

    # Add sellers only once
    sellers = ["anil", "harshwardhan", "chandu"]  # Example sellers
    for seller in sellers:
        add_seller(seller)

    while True:
        print("\nLocal Vegetable Sellers Platform:")
        print("1. Login as seller")
        print("2. View all vegetables and prices")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            seller_name = input("Enter the seller's name: ")
            seller_id = login_seller(seller_name)
            if seller_id:
                while True:
                    print(f"\nWelcome {seller_name}!")
                    print("1. Update vegetables and prices")
                    print("2. Logout")
                    option = input("Choose an option: ")
                    
                    if option == '1':
                        veg_name = input("Enter the vegetable name: ")
                        try:
                            price = float(input("Enter the price: "))
                            print(f"Updating vegetable for seller_id: {seller_id}, vegetable: {veg_name}, price: {price}")
                            update_vegetables(seller_id, veg_name, price)
                        except ValueError:
                            print("Invalid price entered. Please enter a numeric value.")
                    elif option == '2':
                        print("Logging out.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Seller not found. Please ensure you're registered.")
        
        elif choice == '2':
            view_vegetables()
        elif choice == '3':
            print("Exiting the platform.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
