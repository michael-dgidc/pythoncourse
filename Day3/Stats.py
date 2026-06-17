#Uses for loop, decision making, operators, and built-in function
#Program to find the average of numbers
numbers = [15, 20, 35, 45, 55]
total_sum = 0
list_size = len(numbers)

for i in numbers:  # Loop will run 5 times as there are 5 numbers in the array
    total_sum += i
average = total_sum/list_size
print("The average is:", average)

#Program to check whether number is even or odd
for i in numbers:  #Decision-making through for loop
    if i%2 == 0:
        print("Even number:", i)
    else:
        print("Odd number:", i)

# ============================================
# CHALLENGE SOLUTION: Create array of numbers 9-50 divisible by 2
# ============================================
print("\n--- Challenge: Numbers between 9-50 divisible by 2 ---")
divisible_by_2 = []  # create an empty array to store numbers divisible by 2

# for loop to iterate through numbers from 9 to 50
for number in range(9, 51):  # range(9, 51) generates numbers 9 to 50 inclusive
    if number % 2 == 0:  # decision making: check if number is divisible by 2 (remainder is 0)
        divisible_by_2.append(number)  # if divisible by 2, add number to array using append()

print("Numbers between 9 to 50 divisible by 2:", divisible_by_2)  # display the resulting array
print("Total count:", len(divisible_by_2))  # built-in function len() to count elements
