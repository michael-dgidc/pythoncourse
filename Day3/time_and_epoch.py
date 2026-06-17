# ============================================
# CURRENT TIME AND EPOCH PROGRAM
# ============================================
# Using modules and functions built in python
# The purpose of this program is:
# - To demonstrate use of the time module for date and time operations.
# - To demonstrate use of built-in functions.
# - Gives the user the ability to choose their preferred way of date format.
# - Demonstrates epoch time and how it works.

import time  # import the time module - contains various operations for time


# Function to display time in UK format (DD-MM-YYYY HH:MM:SS)
def display_uk_time():
    # Function will display current time in UK format
    now = time.localtime()  # built-in function used to store current time in variable
    uk_formatted_time = time.strftime("%d-%m-%Y %H:%M:%S", now)  # formatting the time in UK format

    print("\n--- UK Date Format ---")  # section header
    print("Local date and time (UK format):", uk_formatted_time)  # printing the current date/time in UK format


# Function to display time in US format (MM-DD-YYYY HH:MM:SS)
def display_us_time():
    # Function will display current time in US format
    now = time.localtime()  # built-in function used to store current time in variable
    us_formatted_time = time.strftime("%m-%d-%Y %H:%M:%S", now)  # formatting the time in US format
    
    print("\n--- US Date Format ---")  # section header
    print("Local date and time (US format):", us_formatted_time)  # printing the current date/time in US format


# Function to display epoch time
def display_epoch_time():
    # Function prints out the seconds since epoch
    seconds = time.time()  # built-in function that stores seconds since the epoch

    print("\n--- Epoch Information ---")  # section header
    print("Epoch is the beginning time from which time is measured (1st Jan 1970, 00:00:00 UTC in Python)")  # explanation of epoch time
    print("Seconds since epoch =", seconds)  # printing the seconds since epoch
    print()  # line space


# Function to make decision according to the choice made by the user
def select_time_format(user_choice):
    # Function takes a parameter of user choice and calls the required function accordingly
    # Parameter: user_choice - user input (1 for UK, 2 for US)

    if user_choice == "1":  # if user choice is 1 then
        display_uk_time()  # call the function to display time in UK format
    elif user_choice == "2":  # elif user choice is 2 then
        display_us_time()  # call the function to display time in US format
    else:  # else if user chooses something else then
        print("Invalid choice! Please enter 1 or 2")  # show error message


# ============================================
# MAIN PROGRAM
# ============================================
print("=== Current Time and Epoch Program ===")  # displaying the title
print("Select your date format preference:")  # giving instruction to the user
print("1 - UK Format (DD-MM-YYYY HH:MM:SS)")  # option 1 description
print("2 - US Format (MM-DD-YYYY HH:MM:SS)")  # option 2 description
print()  # line space

time_format_choice = input("Enter your choice (1 or 2): ")  # taking the input from user
select_time_format(time_format_choice)  # function call to process the user input

# Display epoch info for all users
display_epoch_time()  # calling the epoch info function

print("Thank you for using the Time and Epoch Program!")  # closing message

# CHALLENGE: Make these into user-defined functions (COMPLETED - done)
# CHALLENGE: Add line spaces between outputs (COMPLETED - added print() for line spacing throughout)