#!/usr/bin/env python3
"""Simple profile creator demonstrating:
- two or more data types: string, int, float, boolean
- a data structure: list and dict
- two or more operators: assignment, arithmetic, comparison, logical, membership, identity
- collects gender, height, weight, and calculates BMI
Comments mark where each is used.  
"""

# using a list and a dict data structure to store multiple profiles
profiles_list = []  # using assignment operator (=) to assign an empty list
profiles_dict = {}  # using assignment operator (=) to assign an empty dict

def input_bool(prompt):
    """Read a boolean-like response from the user."""
    val = input(prompt).strip().lower()
    # using membership operator 'in' to check allowed true values
    return val in ('y', 'yes', 'true', '1')  # returns a boolean data type


def create_profile():
    # using string data type for the name
    name = input('Name: ').strip()  # using assignment operator to assign the input to `name`

    # using int data type for age (convert from string to int)
    age_input = input('Age: ').strip()
    try:
        age = int(age_input)  # using int() to create an integer value
    except ValueError:
        print('Invalid age, please enter a number')
        return

    # using string data type for gender
    gender = input('Gender (male/female/other): ').strip()  # joe mange comment: gender stored as string

    # using float data type for height in meters
    height_input = input('Height in meters (e.g. 1.75): ').strip()
    try:
        height = float(height_input)  # using float() to create a float value
    except ValueError:
        print('Invalid height, please enter a number like 1.75')
        return

    # using float data type for weight in kilograms
    weight_input = input('Weight in kilograms (e.g. 70.5): ').strip()
    try:
        weight = float(weight_input)  # using float() to create a float value
    except ValueError:
        print('Invalid weight, please enter a number like 70.5')
        return

    # using boolean data type via helper
    is_active = input_bool('Is active? (y/n): ')

    # compute BMI using arithmetic operators
    if height <= 0 or weight <= 0:  # using comparison operator
        print('Height and weight must be positive values')
        return
    bmi = weight / (height * height)  # using division and multiplication # joe mange comment: calculate BMI

    # using a dict data structure to hold one profile
    profile = {
        'name': name,  # string
        'age': age,    # int
        'gender': gender,  # string
        'height': height,  # float
        'weight': weight,  # float
        'bmi': bmi,  # float
        'active': is_active  # boolean
    }

    # add profile to the list (data structure operation)
    profiles_list.append(profile)  # using list append method

    # add profile to the dict keyed by name (data structure operation)
    # if the name already exists, create a unique key by appending an index
    key = name
    if key in profiles_dict:  # using membership operator 'in'
        idx = 1
        while f"{key}_{idx}" in profiles_dict:  # membership check in a loop
            idx += 1
        key = f"{key}_{idx}"
    profiles_dict[key] = profile  # using assignment to set dict entry

    # using arithmetic operator to compute years to retirement
    years_to_retire = 65 - age  # subtraction

    # using comparison operator and logical operator to determine status
    if age >= 18 and is_active:  # using >= (comparison) and and (logical)
        status = 'Adult active user'
    elif age >= 18 and not is_active:  # using not (logical)
        status = 'Adult inactive user'
    else:
        status = 'Minor user'

    # determine BMI category using comparison operators
    if bmi < 18.5:
        bmi_status = 'Underweight'
    elif bmi < 25:
        bmi_status = 'Normal weight'
    elif bmi < 30:
        bmi_status = 'Overweight'
    else:
        bmi_status = 'Obese'

    # using membership operator to check if 'admin' appears in the name
    if 'admin' in name.lower():  # using 'in' (membership)
        profile['role'] = 'admin'  # using assignment to set a new dict key

    # using identity operator to compare to None (example)
    if profile.get('role') is None:  # using 'is' (identity)
        profile['role'] = 'user'

    print(f"Created profile for {name}. {years_to_retire} years to retirement. Status: {status}. BMI: {bmi:.1f} ({bmi_status})")


def list_profiles():
    if not profiles_list:
        print('No profiles yet')
        return
    for i, p in enumerate(profiles_list, start=1):
        # using string formatting to display values of different data types
        print(f"{i}. {p['name']} - age: {p['age']} - gender: {p['gender']} - height: {p['height']} - weight: {p['weight']} - BMI: {p['bmi']:.1f} - active: {p['active']} - role: {p.get('role')}")


def list_profiles_dict():
    if not profiles_dict:
        print('No profiles in dict yet')
        return
    for key, p in profiles_dict.items():
        # display the dict key and profile
        print(f"{key}: {p['name']} - age: {p['age']} - gender: {p['gender']} - height: {p['height']} - weight: {p['weight']} - BMI: {p['bmi']:.1f} - active: {p['active']} - role: {p.get('role')}")


def main():
    while True:
        print('\nProfile Creator')
        print('1) Create profile')
        print('2) List profiles (list)')
        print('3) List profiles (dict)')
        print('4) Exit')
        choice = input('Choose an option: ').strip()

        # using comparison operators to check choice
        if choice == '1':
            create_profile()
        elif choice == '2':
            list_profiles()
        elif choice == '3':
            list_profiles_dict()
        elif choice == '4':
            break
        else:
            print('Invalid option, try again')


if __name__ == '__main__':
    main()
