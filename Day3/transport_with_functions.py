# ============================================
# TRANSPORT EXAMPLE WITH FUNCTIONS
# ============================================
# This example demonstrates using functions to provide
# welcome messages based on transport mode

# Define a function for car welcome
def welcome_car():
    print("Welcome to your CAR!")  # function for car
    print("You have chosen a comfortable personal vehicle.")  # car specific message
    print("Enjoy the freedom of the open road!")  # additional car message

# Define a function for taxi welcome
def welcome_taxi():
    print("Welcome to your TAXI!")  # function for taxi
    print("You have chosen a convenient ride service.")  # taxi specific message
    print("Our driver will take care of you!")  # additional taxi message

# Define a function for bus welcome
def welcome_bus():
    print("Welcome to the BUS!")  # function for bus
    print("You have chosen an eco-friendly transport option.")  # bus specific message
    print("Enjoy traveling with other passengers!")  # additional bus message

# Define a function that selects transport based on input
def select_transport(choice):
    # choice parameter receives the user's transport selection
    if choice == "1":  # if choice is 1
        welcome_car()  # call the car welcome function
    elif choice == "2":  # elif choice is 2
        welcome_taxi()  # call the taxi welcome function
    elif choice == "3":  # elif choice is 3
        welcome_bus()  # call the bus welcome function
    else:  # if choice is invalid
        print("Invalid choice! Please enter 1, 2, or 3")  # error message

# Main program
print("\n--- Transport Selection Using Functions ---")
transport_choice = input("Enter 1 for Car, 2 for Taxi, 3 for Bus: ")  # get user input
select_transport(transport_choice)  # call function to handle selection and welcome
print("Thank you for using our transport service!")  # closing message
