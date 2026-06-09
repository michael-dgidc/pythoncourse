# ============================================
# PASSWORD VALIDATOR PROGRAM
# ============================================
# This program validates a password based on specific requirements:
# 1. Must be at least 8 characters long
# 2. Must contain at least one lowercase letter
# 3. Must contain at least one uppercase letter
# 4. Must contain at least one digit (number)
# 5. Must contain at least one special character (!@#$%^&*)

import re  # import re module - provides regular expression pattern matching functions


def validate_password_strength(user_password_input):
    # Function to validate if a password meets all security requirements
    # Parameter: user_password_input - the password string to validate
    # Returns: True if password is valid, False otherwise
    
    # Check if password length is at least 8 characters
    if len(user_password_input) < 8:
        return False  # password too short, return False
    
    # Check if password contains at least one lowercase letter (a-z)
    if not re.search("[a-z]", user_password_input):
        return False  # no lowercase letter found, return False
    
    # Check if password contains at least one uppercase letter (A-Z)
    if not re.search("[A-Z]", user_password_input):
        return False  # no uppercase letter found, return False
    
    # Check if password contains at least one digit/number (0-9)
    if not re.search("[0-9]", user_password_input):
        return False  # no digit found, return False
    
    # Check if password contains at least one special character (!@#$%^&*_+-=)
    if not re.search("[!@#$%^&*_+\-=\[\]{};:,.<>?]", user_password_input):
        return False  # no special character found, return False
    
    # If all checks pass, password meets all requirements
    return True  # all requirements met, return True


# ============================================
# MAIN PROGRAM
# ============================================
print("--- Password Validator ---")  # display program title
user_password = input("Create a new password: ")  # prompt user and store password in variable

# Call the validate_password_strength function and check the result
if validate_password_strength(user_password):
    print("✓ Valid password! Your password meets all security requirements.")  # success message
else:
    print("✗ Invalid password! Please try again.")  # failure message
    print("Password must have: 8+ characters, uppercase, lowercase, number, and special character (!@#$%^&*_+-=[]{}etc)")  # requirements reminder
