#!/usr/bin/env python3
"""Beginner-friendly profile creator with no functions.
Includes:
- data types: string, int, float, boolean
- data structures: list and dict
- operators: assignment, arithmetic, comparison, logical, membership, identity
All uses are commented where they appear.
"""

# Using assignment operator to create data structures
profiles_list = []  # list data structure
profiles_dict = {}  # dict data structure

print('Beginner Profile Creator (no functions)')

while True:
    print('\nMenu:')
    print('1) Create profile')
    print('2) List profiles (list)')
    print('3) List profiles (dict)')
    print('4) Exit')
    choice = input('Choose an option: ').strip()

    # using comparison operator to check the choice
    if choice == '1':
        # using string data type for name
        name = input('Name: ').strip()  # assignment

        # using int data type for age (convert from string)
        age_input = input('Age: ').strip()
        try:
            age = int(age_input)  # int()
        except ValueError:
            print('Invalid age, skipping profile creation')
            continue

        # using float data type for balance
        balance_input = input('Balance (e.g. 100.50): ').strip()
        try:
            balance = float(balance_input)  # float()
        except ValueError:
            balance = 0.0  # assignment to default float

        # using boolean via membership check
        active_input = input('Is active? (y/n): ').strip().lower()
        is_active = active_input in ('y', 'yes', 'true', '1')  # membership operator -> boolean

        # create a profile dict (data structure)
        profile = {
            'name': name,      # string
            'age': age,        # int
            'balance': balance,# float
            'active': is_active# boolean
        }

        # add to list (data structure) using list append
        profiles_list.append(profile)  # assignment via method call

        # add to dict keyed by name; if duplicate, add numeric suffix
        key = name
        # using membership operator 'in' to check existing keys
        if key in profiles_dict:
            idx = 1
            # using membership in loop to find unused key
            while f"{key}_{idx}" in profiles_dict:
                idx += 1  # using arithmetic operator to increment
            key = f"{key}_{idx}"

        profiles_dict[key] = profile  # using assignment to set dict entry

        # arithmetic operator to compute years to retirement
        years_to_retire = 65 - age

        # using comparison and logical operators to set status
        if age >= 18 and is_active:
            status = 'Adult active user'
        elif age >= 18 and not is_active:
            status = 'Adult inactive user'
        else:
            status = 'Minor user'

        # membership operator to check for substring in name
        if 'admin' in name.lower():
            profile['role'] = 'admin'  # assignment to dict key
        else:
            # identity operator example: compare to None
            if profile.get('role') is None:
                profile['role'] = 'user'

        print(f"Created profile for {name}. {years_to_retire} years to retirement. Status: {status}")

    elif choice == '2':
        if not profiles_list:  # using logical operator 'not'
            print('No profiles in list')
        else:
            for i, p in enumerate(profiles_list, start=1):
                # demonstrate values of different data types
                print(f"{i}. {p['name']} - age: {p['age']} - balance: {p['balance']} - active: {p['active']} - role: {p.get('role')}")

    elif choice == '3':
        if not profiles_dict:
            print('No profiles in dict')
        else:
            for k, p in profiles_dict.items():
                print(f"{k}: {p['name']} - age: {p['age']} - balance: {p['balance']} - active: {p['active']} - role: {p.get('role')}")

    elif choice == '4':
        break
    else:
        print('Invalid option, try again')

print('Goodbye')
