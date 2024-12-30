#1 part
import matplotlib.pyplot as plt


#2 part
transport_modes = ['Cabs', 'Local Trains', 'Rickshaws']
daily_users = [5_000_000, 1_500_000, 30_000_000]  # in millions
cab_count = 53_000
cab_increase = 9_000



#3 part
def display_reasons():
    reasons = [
        "Traffic congestion",
        "Limited parking spaces",
        "Difficulty in finding other forms of transportation",
        "Rickshaw drivers switching to cabs"
    ]
    print("\nReasons for Increased Cab Usage in Pune:")
    for reason in reasons:
        print(f"- {reason}")



#4 part
def display_benefits():
    benefits = [
        "Reduced waiting time",
        "More options to choose from",
        "Cabs are readily available"
    ]
    print("\nBenefits of Cabs for Passengers:")
    for benefit in benefits:
        print(f"- {benefit}")



#5 part
def compare_transport_modes():
    plt.bar(transport_modes, daily_users, color=['blue', 'green', 'orange'])
    plt.title('Daily Users of Different Transport Modes in Pune')
    plt.ylabel('Number of Users (in millions)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


#6 part
def plot_pie_chart():
    plt.figure(figsize=(7, 7))
    plt.pie(daily_users, labels=transport_modes, autopct='%1.1f%%', startangle=90, colors=['blue', 'green', 'orange'])
    plt.title('Percentage of Daily Users by Transport Mode')
    plt.show()



def plot_line_chart():
    plt.plot(transport_modes, daily_users, marker='o', color='red', linestyle='--')
    plt.title('Daily Users Trend for Transport Modes in Pune')
    plt.xlabel('Transport Modes')
    plt.ylabel('Number of Users (in millions)')
    plt.grid(True)
    plt.show()



def calculate_increase_percentage():
    percentage_increase = (cab_increase / (cab_count - cab_increase)) * 100
    print(f"\nCab Count Increase Percentage: {percentage_increase:.2f}%")



while True:
    print("\n--- Cab Usage Analysis in Pune ---")
    print("1. Display Reasons for Increased Cab Usage")
    print("2. Display Benefits of Cabs")
    print("3. Compare Transport Modes (Bar Chart)")
    print("4. Show Transport Mode Percentages (Pie Chart)")
    print("5. Show Daily Users Trend (Line Chart)")
    print("6. Calculate Cab Count Increase Percentage")
    print("7. Exit")
    


    choice = input("Enter your choice: ")
    


    if choice == '1':
        display_reasons()
    elif choice == '2':
        display_benefits()
    elif choice == '3':
        compare_transport_modes()
    elif choice == '4':
        plot_pie_chart()
    elif choice == '5':
        plot_line_chart()
    elif choice == '6':
        calculate_increase_percentage()
    elif choice == '7':
        print("Exiting... Thank you!")
        break
    else:
        print("Invalid choice. Please try again.")