# ============================================
# IF/ELIF/ELSE EXAMPLE: Transport Selection
# ============================================
print("\n--- Select Your Transport Option ---")
transport_choice = input("Enter 1 for Car, 2 for Taxi, 3 for Bus: ")  # Get user input

# Use if/elif/else to select transport based on user input
if transport_choice == "1":  # if user enters 1
    print("You selected: CAR")  # print car
    print("Enjoy your car ride!")  # additional message for car
elif transport_choice == "2":  # elif user enters 2
    print("You selected: TAXI")  # print taxi
    print("Enjoy your taxi ride!")  # additional message for taxi
elif transport_choice == "3":  # elif user enters 3
    print("You selected: BUS")  # print bus
    print("Enjoy your bus ride!")  # additional message for bus
else:  # if none of the above options (invalid input)
    print("Invalid choice! Please enter 1, 2, or 3")  # error message
