# ============================================
# SMILEY AND SAD FACE DISPLAY PROGRAM
# ============================================
# This program demonstrates using functions to display
# ASCII art faces based on user input

# Function to display a smiley face
def display_smiley_face():
    # Function draws a happy smiley face using ASCII art
    print("\n--- Smiley Face ---")  # display section header
    print("     ___________     ")  # top border
    print("    /           \\    ")  # upper curve
    print("   |  o     o   |   ")  # eyes
    print("   |             |   ")  # space
    print("   |   \\  _  /   |   ")  # happy smile
    print("    \\           /    ")  # lower curve
    print("     ~~~~~~~~~~~     ")  # bottom border
    print("   ✨ I'm happy! ✨")  # message for smiley with emojis
    print()  # blank line for spacing

# Function to display a sad face
def display_sad_face():
    # Function draws a sad face using ASCII art
    print("\n--- Sad Face ---")  # display section header
    print("     ___________     ")  # top border
    print("    /           \\    ")  # upper curve
    print("   |  o     o   |   ")  # eyes
    print("   |             |   ")  # space
    print("   |   /  ‾  \\   |   ")  # sad frown
    print("    \\           /    ")  # lower curve
    print("     ~~~~~~~~~~~     ")  # bottom border
    print("   😢 I'm sad... 😢")  # message for sad face with emojis
    print()  # blank line for spacing

# Function to handle user selection and render appropriate face
def select_face_option(user_choice):
    # Function takes user choice and calls appropriate face display function
    # Parameter: user_choice - user's input (1 for smiley, 2 for sad)
    
    if user_choice == "1":  # if user enters 1
        display_smiley_face()  # call function to display smiley
    elif user_choice == "2":  # elif user enters 2
        display_sad_face()  # call function to display sad face
    else:  # if user enters anything else
        print("Invalid choice! Please enter 1 or 2")  # error message

# ============================================
# MAIN PROGRAM
# ============================================
print("=== Face Display Program ===")  # display program title
print("Select which face you want to see:")  # prompt instruction
print("1 - Smiley Face :)")  # option 1 description
print("2 - Sad Face :(")  # option 2 description
print()  # blank line for spacing

face_choice = input("Enter your choice (1 or 2): ")  # get user input and store in variable
select_face_option(face_choice)  # call function to process user choice and display face

print("Thanks for using the Face Display Program!")  # closing message
