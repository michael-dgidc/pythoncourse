""""Sample script code for the Python criteria assessment.

This code includes:
- 2.1 Decisions with 'if', 'elif' & 'else'
- 2.2 Built-in Python functions like 'int()', 'len()', 'sum()', 'max()', 'min()' and 'sorted()'
- 2.3 Loops using both 'for' and 'while'
- 3.1 Defining functions which group a set of actions together
- 4.1 Executing the Python program
- 4.3 Standard library modules for the Python programming language, i.e., 'datetime', 'random' & 'statistics'
"""

import datetime
import random
import statistics


def validate_integer_input(prompt, minimum=None, maximum=None):
    """Get user input for an integer till they provide a valid one."""
    while True:
        user_input = input(prompt).strip()

        if not user_input:
            print("Please enter something.")

            continue

        if not user_input.lstrip("+").lstrip("-").isdigit():
            print("That doesn't seem to be a valid integer. Please try again.")

            continue

        number = int(user_input)

        if minimum and number < minimum:
            print(f"That number is too low. Please try again. The lowest is {minimum}")

            continue
        if maximum and number > maximum:
            print(f"That number is too high. Please try again. The highest is {maximum}")

            continue
        return number


def get_random_integers(amount, minimum=-10, maximum=20):
    """Generate random integers using the random module"""
    integers = []

    for _ in range(amount):
        integers.append(random.randint(minimum, maximum))

    return integers


def categorize_integers(integers):
    """Categorize integers with decisions"""
    positives = []
    negatives = []
    zeros = 0

    for integer in integers:
        if integer > 0:
            positives.append(integer)
        elif integer < 0:
            negatives.append(integer)
        else:
            zeros += 1

    return positives, negatives, zeros


def display_results(person, integers, positives, negatives, zeros):
    """Display the results using built-in functions and statistical calculations."""
    print()  # blank line for better readability
    print(f"Hello {person}! This is your number summary:")

    print("Numbers:", integers)
    print(f"Total numbers: {len(integers)}")
    print(f"Positives: {len(positives)}")
    print(f"Negatives: {len(negatives)}")
    print(f"Zeros: {zeros}")

    if integers:
        print(f"Min number: {min(integers)}")
        print(f"Max number: {max(integers)}")
        print(f"Sorted numbers: {sorted(integers)}")
        print(f"Their sum: {sum(integers)}")
        print(f"Their average: {statistics.mean(integers):.2f}")

    if len(positives) > len(negatives):
        print("The majority of your numbers are positives.")
    elif len(negatives) > len(positives):
        print("The majority of your numbers are negatives.")
    else:
        print("You have equal numbers of positives and negatives.")


def main():
    """Define the main function for our program."""
    print("Sample program for decisions, loops, functions and modules.")
    script_start_time = datetime.datetime.now()
    print(f"Script start time: {script_start_time:%Y-%m-%d %H:%M:%S}")

    person = input("What's your name? ") or "Student