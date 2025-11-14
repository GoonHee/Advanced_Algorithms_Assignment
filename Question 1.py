import time
import random


# --- 1. Product Entity Class ---
class Product:
    """
    Represents a single product in the Baby Shop inventory.
    The primary key for hashing is 'product_id'.
    """

    def __init__(self, product_id, name, category, price, quantity):
        # We use a unique integer ID as the key for hashing.
        self.product_id = product_id
        self.name = name
        self.category = category  # e.g., 'Diapers', 'Strollers', 'Toys'
        self.price = price
        self.quantity = quantity

    def __str__(self):
        """Returns a user-friendly string representation of the product."""
        return (f"| ID: {self.product_id:<4} | Name: {self.name:<25} | Category: {self.category:<12} | "
                f"Price: ${self.price:>6.2f} | Qty: {self.quantity:>4} |")

    def to_tuple(self):
        """Returns a tuple (key, value) for use in the array comparison."""
        return (self.product_id, self)


# --- 2. Chaining Hash Table Implementation (Separate Chaining) ---
class ChainingHashTable:
    """
    Implements a Hash Table using Separate Chaining for collision resolution.
    The underlying structure is a list of lists (buckets).
    Each bucket (inner list) stores (key, value) tuples.
    """

    def __init__(self, size=10):
        # Initialize the table with 'size' empty buckets (lists)
        self.size = size
        self.table = [[] for _ in range(self.size)]
        self.count = 0  # To keep track of the number of items

    def _hash_function(self, key):
        """Simple division method hash function."""
        return key % self.size

    def insert(self, key, value):
        """Inserts a (key, value) pair into the hash table."""
        # Calculate the bucket index
        index = self._hash_function(key)
        bucket = self.table[index]

        # Check if the key already exists (update logic)
        for i, (existing_key, existing_value) in enumerate(bucket):
            if existing_key == key:
                # Update the existing value
                bucket[i] = (key, value)
                print(f"--> Key {key} updated in bucket {index}.")
                return

        # If key does not exist, append the new (key, value) tuple to the bucket
        bucket.append((key, value))
        self.count += 1
        print(f"--> Key {key} inserted at bucket {index}.")

    def search(self, key):
        """Searches for a key and returns its value (Product object) or None."""
        #Calculate the bucket index
        index = self._hash_function(key)
        bucket = self.table[index]

        #Linearly search within the bucket (chain)
        for existing_key, value in bucket:
            if existing_key == key:
                return value
        return None

    def delete(self, key):
        """Deletes a (key, value) pair from the hash table."""
        index = self._hash_function(key)
        bucket = self.table[index]

        #Iterate through the bucket to find and delete the item
        for i, (existing_key, value) in enumerate(bucket):
            if existing_key == key:
                del bucket[i]
                self.count -= 1
                print(f"--> Product with ID {key} deleted successfully.")
                return

        print(f"--> Error: Product with ID {key} not found for deletion.")

    def display_all(self):
        """Prints all items in the hash table, bucket by bucket."""
        print("\n--- Current Inventory (Hash Table Contents) ---")
        if self.count == 0:
            print("The inventory is empty.")
            return

        for i in range(self.size):
            bucket = self.table[i]
            print(f"Bucket {i}: ", end="")
            if not bucket:
                print("[]")
            else:
                # Print all (key, value) pairs in the bucket's chain
                print(" -> ".join([f"(ID: {k}, {v.name})" for k, v in bucket]))
        print(f"Total Items: {self.count}\n")


#Inventory System Functions

def generate_sample_data(hash_table, array_list):
    """
    Generates and inserts sample data into both the hash table and the array.
    Returns the next available product ID.
    """
    products_data = [
        (1, "Infant Car Seat", "Safety", 199.99, 15),
        (2, "Organic Cotton Onesie", "Apparel", 19.50, 150),
        (3, "Diaper Bag (Multi)", "Accessories", 65.00, 30),
        (4, "Wooden Stacking Rings", "Toys", 15.99, 85),
        (5, "Electric Breast Pump", "Feeding", 189.00, 10),
        (6, "Travel Stroller", "Strollers", 249.99, 22),
        (7, "Bamboo Swaddle Set", "Bedding", 35.00, 60),
        (8, "Waterproof Mattress Pad", "Bedding", 29.95, 45),
        (9, "Portable High Chair", "Feeding", 99.99, 18),
        (10, "Teething Toy Set", "Toys", 12.50, 110),
    ]

    next_id = 10001  # Start ID for user input to avoid collisions with sample data

    print("--- Initializing Inventory ---")
    for prod_id, name, category, price, quantity in products_data:
        product = Product(prod_id, name, category, price, quantity)
        # Insert into Hash Table
        hash_table.insert(prod_id, product)
        # Store in Array (list of (key, value) tuples) for comparison
        array_list.append(product.to_tuple())

    print("\nInitialization complete. 10 products added.")
    return next_id


def inventory_menu(hash_table, next_id):
    """
    Menu-driven interface for the inventory system.
    """
    while True:
        print("\n=== Baby Shop Inventory Management ===")
        print("1. Insert New Product")
        print("2. Search Product by ID")
        print("3. Delete Product by ID")
        print("4. Display All Products")
        print("5. Run Performance Comparison (Search)")
        print("6. Exit")
        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                name = input("Enter Product Name: ")
                category = input("Enter Category: ")
                price = float(input("Enter Price: $"))
                quantity = int(input("Enter Quantity: "))

                new_product = Product(next_id, name, category, price, quantity)
                hash_table.insert(next_id, new_product)

                print(f"Product '{name}' inserted with ID: {next_id}")
                next_id += 1

            elif choice == '2':
                search_id = int(input("Enter Product ID to search: "))
                product = hash_table.search(search_id)
                if product:
                    print("\n--- Search Result ---")
                    print(product)
                else:
                    print(f"\nProduct with ID {search_id} not found.")

            elif choice == '3':
                delete_id = int(input("Enter Product ID to delete: "))
                hash_table.delete(delete_id)

            elif choice == '4':
                hash_table.display_all()

            elif choice == '5':
                # Run the performance test using the initial, static data set
                run_performance_comparison(hash_table, initial_array_data)

            elif choice == '6':
                print("Exiting Inventory Management System. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 6.")

        except ValueError:
            print("Invalid input. Please ensure you enter the correct data type (e.g., number for ID/price/quantity).")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break


# --- 4. Performance Comparison ---

def search_array(key, array):
    """
    Linearly searches for a key in a one-dimensional array (list of tuples).
    This function is used for the performance comparison baseline.
    """
    for existing_key, value in array:
        if existing_key == key:
            return value
    return None


def run_performance_comparison(hash_table, array_data):
    """
    Compares the search performance between the Hash Table and a standard array.
    """
    print("\n=== Running Search Performance Comparison ===")

    # 1. Identify the keys to search (use all existing keys for a fair test)
    search_keys = [key for key, _ in array_data]
    if not search_keys:
        print("Cannot run comparison: No data available in the array.")
        return

    # Shuffle the keys to ensure we are not only testing sequential access
    random.shuffle(search_keys)

    num_searches = len(search_keys)
    num_runs = 1000  # Number of times to repeat the search loop for timing

    # --- Hash Table Timing ---
    start_time_hash = time.perf_counter()
    for _ in range(num_runs):
        for key in search_keys:
            hash_table.search(key)
    end_time_hash = time.perf_counter()

    hash_time = (end_time_hash - start_time_hash) * 1e6  # Convert to microseconds
    avg_hash_time = hash_time / (num_searches * num_runs)

    # --- Array Timing ---
    start_time_array = time.perf_counter()
    for _ in range(num_runs):
        for key in search_keys:
            search_array(key, array_data)
    end_time_array = time.perf_counter()

    array_time = (end_time_array - start_time_array) * 1e6  # Convert to microseconds
    avg_array_time = array_time / (num_searches * num_runs)

    # --- Results ---
    print(f"\nTotal items searched: {num_searches}")
    print(f"Total loop repetitions: {num_runs}\n")

    print("-" * 50)
    print(f"| {'Algorithm':<20} | {'Total Time (µs)':<20} |")
    print("-" * 50)
    print(f"| {'Hash Table (Chaining)':<20} | {hash_time:<20.4f} |")
    print(f"| {'Array (Linear Search)':<20} | {array_time:<20.4f} |")
    print("-" * 50)

    print(f"\n| {'Algorithm':<20} | {'Avg Time Per Search (ns)':<20} |")
    print("-" * 50)
    # Convert average time from microseconds to nanoseconds (x 1000)
    print(f"| {'Hash Table (Chaining)':<20} | {avg_hash_time * 1000:<20.4f} |")
    print(f"| {'Array (Linear Search)':<20} | {avg_array_time * 1000:<20.4f} |")
    print("-" * 50)

    # Conclusion for the Report
    if avg_hash_time < avg_array_time:
        print("\nAnalysis: The Hash Table (Chaining) demonstrated superior search performance.")
        print("This is expected as Hash Table search approaches O(1) complexity (average case),")
        print("while Array search is O(N) (worst/average case).")
    else:
        print("\nAnalysis: The Array demonstrated superior search performance.")
        print("This suggests the dataset is too small, and the overhead of hashing/collision")
        print("resolution is greater than the O(N) linear search on the small list.")


#Main Execution Block

# Initialize the data structures
INVENTORY_SIZE = 15  # Define the size of the Hash Table
inventory_hash_table = ChainingHashTable(size=INVENTORY_SIZE)
initial_array_data = []  # Stores (key, Product) tuples for the array comparison

# 1. Generate and insert initial data
next_product_id = generate_sample_data(inventory_hash_table, initial_array_data)

# 2. Start the menu-driven inventory system
inventory_menu(inventory_hash_table, next_product_id)