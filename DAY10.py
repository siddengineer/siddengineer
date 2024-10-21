print("----------------------welcome to chalodrive----------------------")



import random
from googletrans import Translator, LANGUAGES

# Initialize the translator
translator = Translator()

# Rider class to represent a customer
class Rider:
    def __init__(self, name, location):
        self.name = name
        self.location = location

# Driver class to represent a driver
class Driver:
    def __init__(self, name, location, available=True):
        self.name = name
        self.location = location
        self.available = available

# RideService class to manage rides
class RideService:
    def __init__(self):
        self.drivers = []

    # Add driver to the system
    def add_driver(self, driver):
        self.drivers.append(driver)

    # Find nearest available driver
    def find_nearest_driver(self, rider_location):
        available_drivers = [driver for driver in self.drivers if driver.available]
        if not available_drivers:
            return None
        nearest_driver = min(available_drivers, key=lambda driver: abs(driver.location - rider_location))
        return nearest_driver

    # Calculate price based on distance
    def calculate_price(self, driver_location, rider_location):
        distance = abs(driver_location - rider_location)
        price = distance * 20  # Assume price is ₹20 per unit distance
        return price

    # Generate a random safety number
    def generate_safety_number(self):
        safety_number = random.randint(1000000000, 9999999999)
        return safety_number

    # Translate messages
    def translate_message(self, message, target_language='en'):
        try:
            print(f"Translating message: {message}")
            translated = translator.translate(message, dest=target_language)
            if translated and translated.text:
                print(f"Original: {message}")
                print(f"Translated: {translated.text}")
                return translated.text
            else:
                print(f"Translation result is None for message: {message}")
                return message
        except Exception as e:
            print(f"Translation error: {e}")
            return message

    # Book a ride
    def book_ride(self, rider, language='en'):
        if language not in LANGUAGES.keys():
            print("Unsupported language. Defaulting to English.")
            language = 'en'
        
        driver = self.find_nearest_driver(rider.location)
        if driver:
            price = self.calculate_price(driver.location, rider.location)
            message = (
                f"Driver {driver.name} is available at location {driver.location}.\n"
                f"The price for your ride is: ₹{price}"
            )
            translated_message = self.translate_message(message, language)
            print(translated_message)
            
            confirm_message = self.translate_message("Do you want to book this ride? (yes/no): ", language)
            confirm = input(confirm_message).strip().lower()
            if confirm == 'yes':
                driver.available = False
                safety_number = self.generate_safety_number()
                confirmation_message = (
                    f"Ride booked! Driver {driver.name} will pick you up soon.\n"
                    f"For any help, call our safety number: {safety_number}"
                )
                return self.translate_message(confirmation_message, language)
            else:
                return self.translate_message("Ride not booked.", language)
        else:
            return self.translate_message("No drivers available.", language)

# Simulate the app
if __name__ == "__main__":
    # Create ride service
    ride_service = RideService()

    # Create some drivers and add to service
    ride_service.add_driver(Driver("Alice", location=5))
    ride_service.add_driver(Driver("Bob", location=15))
    ride_service.add_driver(Driver("Charlie", location=10))

    # Input rider details
    rider_name = input("Enter your name: ")
    rider_location = int(input("Enter your location (number): "))
    print("Select your preferred language:")
    print("1. English (en)")
    print("2. Marathi (mr)")
    print("3. Hindi (hi)")
    language_choice = input("Enter your choice (1, 2, or 3): ").strip()
    if language_choice == '1':
        language = 'en'
    elif language_choice == '2':
        language = 'mr'
    elif language_choice == '3':
        language = 'hi'
    else:
        print("Invalid choice. Defaulting to English.")
        language = 'en'

    # Create rider object
    rider = Rider(rider_name, location=rider_location)

    # Book ride for the rider
    print(ride_service.book_ride(rider, language))
