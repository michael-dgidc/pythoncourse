#!/usr/bin/env python3
"""Simple profile creator demonstrating:
- two or more data types: string, int, float, boolean
- a data structure: list and dict
- two or more operators: assignment, arithmetic, comparison, logical, membership, identity
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

    # using float data type for balance
    balance_input = input('Balance (e.g. 123.45): ').strip()
    try:
        balance = float(balance_input)  # using float() to create a float value
    except ValueError:
        balance = 0.0  # using assignment operator to set default

    # using boolean data type via helper
    is_active = input_bool('Is active? (y/n): ')

    # using a dict data structure to hold one profile
    profile = {
        'name': name,  # string
        'age': age,    # int
        'balance': balance,  # float
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

    # using membership operator to check if 'admin' appears in the name
    if 'admin' in name.lower():  # using 'in' (membership)
        profile['role'] = 'admin'  # using assignment to set a new dict key

    # using identity operator to compare to None (example)
    if profile.get('role') is None:  # using 'is' (identity)
        profile['role'] = 'user'

    print(f"Created profile for {name}. {years_to_retire} years to retirement. Status: {status}")


def list_profiles():
    if not profiles_list:
        print('No profiles yet')
        return
    for i, p in enumerate(profiles_list, start=1):
        # using string formatting to display values of different data types
        print(f"{i}. {p['name']} - age: {p['age']} - balance: {p['balance']} - active: {p['active']} - role: {p.get('role')}")


def list_profiles_dict():
    if not profiles_dict:
        print('No profiles in dict yet')
        return
    for key, p in profiles_dict.items():
        # display the dict key and profile
        print(f"{key}: {p['name']} - age: {p['age']} - balance: {p['balance']} - active: {p['active']} - role: {p.get('role')}")


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
