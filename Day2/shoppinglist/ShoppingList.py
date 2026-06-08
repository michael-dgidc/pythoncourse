# Initial list
l1 = ["milk", "eggs", "bread", "butter"]  # Define the first shopping list
# Second list
l2 = ["cheese", "yogurt", "fruit", "vegetables"]  # Define the second shopping list
combined_list = l1 + l2  # Combine both lists in one list
print("Combined Shopping List:", combined_list)  # Print combined list
# Adding more items to the list
combined_list.append("juice")  # Add 'juice' to the end of the combined list
combined_list.append("cereal")  # Add 'cereal' to the end of the combined list
print("Updated Shopping List:", combined_list)  # Print list after addition of more items
# Removing an item from the list
combined_list.remove("bread")  # Remove 'bread' from combined list
print("Shopping List after removing 'bread':", combined_list)  # Print list after removing an item
# Sorting the list
combined_list.sort()  # Sort the combined list alphabetically in ascending order
print("Sorted Shopping List:", combined_list)  # Print sorted list
# Reversing the list
combined_list.reverse()  # Reverse the order of elements in the list
print("Reversed Shopping List:", combined_list)  # Print reversed list
# Removing the last element in the list using pop()
popped_item = combined_list.pop()  # Remove the last element from the list
print("Popped item:", popped_item)  # Print popped item
print("Shopping List after removing the last item:", combined_list)  # Print the updated list
# Check if an item is in the list
if "milk" in combined_list:  # Check if 'milk' is in combined list
    print("Milk is in the shopping list.")  # Confirmation if 'milk' is in the combined list
else:
    print("Milk is not in the shopping list.")  # Absence notice if 'milk' is not in the combined list

# Summary of performed operations
# 1. Created two shopping lists, l1 and l2
# 2. Combined l1 and l2 into combined_list
# 3. Added "juice" and "cereal" to combined_list
# 4. Removed "bread" from combined_list
# 5. Sorted combined_list alphabetically
# 6. Reversed the sorted combined_list
# 7. Removed the last item from combined_list with pop()
# 8. Checked whether "milk" is in the final list