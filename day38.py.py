
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, 
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QLabel, 
    QInputDialog, QLineEdit, QHBoxLayout, QFileDialog
)
import sys
import json

class AutoExpoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main Window Configuration
        self.setWindowTitle("Auto Expo Management System")
        self.setGeometry(100, 100, 800, 400)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Label
        self.label = QLabel("Welcome to the Auto Expo Management System!")
        layout.addWidget(self.label)

        # Search Bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Vehicle Name")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_vehicle)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)

        # Table to Display Vehicles
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Vehicle Name", "Type", "Fuel Type"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # Add Buttons
        add_button = QPushButton("Add Vehicle")
        add_button.clicked.connect(self.add_vehicle)
        layout.addWidget(add_button)

        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_vehicle)
        layout.addWidget(delete_button)

        save_button = QPushButton("Save Vehicles")
        save_button.clicked.connect(self.save_vehicles)
        layout.addWidget(save_button)

        load_button = QPushButton("Load Vehicles")
        load_button.clicked.connect(self.load_vehicles)
        layout.addWidget(load_button)

        # Predefined vehicles
        self.vehicles = [
            {"name": "Maruti Suzuki Swift", "type": "Hatchback", "fuel": "Petrol"},
            {"name": "Hyundai Creta", "type": "SUV", "fuel": "Diesel"},
            {"name": "Tata Nexon", "type": "SUV", "fuel": "Electric"},
            {"name": "Honda City", "type": "Sedan", "fuel": "Petrol"},
            {"name": "Kia Seltos", "type": "SUV", "fuel": "Diesel"},
            {"name": "Ford EcoSport", "type": "SUV", "fuel": "Petrol"},
            {"name": "Toyota Innova Crysta", "type": "MPV", "fuel": "Diesel"},
            {"name": "MG Hector", "type": "SUV", "fuel": "Petrol"},
            {"name": "Mahindra Thar", "type": "SUV", "fuel": "Diesel"},
            {"name": "Skoda Octavia", "type": "Sedan", "fuel": "Petrol"}
        ]

        self.populate_table()

    def populate_table(self):
        """Populates the table with vehicles."""
        self.table.setRowCount(0)  # Clear existing rows
        for vehicle in self.vehicles:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(vehicle["name"]))
            self.table.setItem(row_position, 1, QTableWidgetItem(vehicle["type"]))
            self.table.setItem(row_position, 2, QTableWidgetItem(vehicle["fuel"]))

    def add_vehicle(self):
        """Add a new vehicle row to the table."""
        vehicle_name, ok1 = QInputDialog.getText(self, "Vehicle Name", "Enter Vehicle Name:")
        if not ok1 or not vehicle_name:
            return

        vehicle_type, ok2 = QInputDialog.getText(self, "Vehicle Type", "Enter Vehicle Type:")
        if not ok2 or not vehicle_type:
            return

        fuel_type, ok3 = QInputDialog.getText(self, "Fuel Type", "Enter Fuel Type (Petrol/Diesel/Electric):")
        if not ok3 or not fuel_type:
            return

        new_vehicle = {"name": vehicle_name, "type": vehicle_type, "fuel": fuel_type}
        self.vehicles.append(new_vehicle)
        self.populate_table()
        QMessageBox.information(self, "Vehicle Added", "Vehicle added successfully!")

    def delete_vehicle(self):
        """Delete the selected vehicle."""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a vehicle to delete.")
        else:
            del self.vehicles[selected_row]
            self.table.removeRow(selected_row)
            QMessageBox.information(self, "Vehicle Deleted", "Vehicle deleted successfully!")

    def search_vehicle(self):
        """Search for a vehicle by name."""
        search_text = self.search_input.text().strip().lower()
        if not search_text:
            QMessageBox.warning(self, "No Search Term", "Please enter a vehicle name to search.")
            return

        filtered_vehicles = [v for v in self.vehicles if search_text in v["name"].lower()]
        if not filtered_vehicles:
            QMessageBox.warning(self, "No Results", "No vehicles found matching your search.")
            return
        
        # Populate table with filtered vehicles
        self.table.setRowCount(0)  # Clear existing rows
        for vehicle in filtered_vehicles:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(vehicle["name"]))
            self.table.setItem(row_position, 1, QTableWidgetItem(vehicle["type"]))
            self.table.setItem(row_position, 2, QTableWidgetItem(vehicle["fuel"]))

    def save_vehicles(self):
        """Save the vehicles to a JSON file."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Vehicles", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as f:
                json.dump(self.vehicles, f)
            QMessageBox.information(self, "Saved", "Vehicles saved successfully!")

    def load_vehicles(self):
        """Load vehicles from a JSON file."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Vehicles", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as f:
                self.vehicles = json.load(f)
            self.populate_table()
            QMessageBox.information(self, "Loaded", "Vehicles loaded successfully!")

# Run the Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoExpoApp()
    window.show()
    sys.exit(app.exec())
