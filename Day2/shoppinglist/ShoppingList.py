# initial list
l1 = ["milk", "eggs", "bread", "butter"]  # define the first shopping list
# second list
l2 = ["cheese", "yogurt", "fruit", "vegetables"]  # define the second shopping list
combined_list = l1 + l2  # combine both lists into one list
print("Combined Shopping List:", combined_list)  # display the combined list
# add more items to the list
combined_list.append("juice")  # add juice to the end of the combined list
combined_list.append("cereal")  # add cereal to the end of the combined list
print("Updated Shopping List:", combined_list)  # display the list after adding items
# remove an item from the list
combined_list.remove("bread")  # remove bread from the combined list
print("Shopping List after removing bread:", combined_list)  # display list after removal
# sort the list alphabetically
combined_list.sort()  # sort the list in ascending alphabetical order
print("Sorted Shopping List:", combined_list)  # display the sorted list
# reverse the list
combined_list.reverse()  # reverse the order of items in the list
print("Reversed Shopping List:", combined_list)  # display the reversed list
# remove the last item using pop
popped_item = combined_list.pop()  # remove and capture the last item in the list
print("Popped item:", popped_item)  # display the removed item
print("Shopping List after pop:", combined_list)  # display the list after popping the last item
# check if an item is in the list
if "milk" in combined_list:  # test whether milk is present in the list
    print("Milk is in the shopping list.")  # print confirmation if milk exists
else:
    print("Milk is not in the shopping list.")  # print absence notice if milk is missing

# Summary of operations:
# 1. Created two shopping lists, l1 and l2.
# 2. Combined l1 and l2 into combined_list.
# 3. Added "juice" and "cereal" to combined_list.
# 4. Removed "bread" from combined_list.
# 5. Sorted combined_list alphabetically.
# 6. Reversed the sorted combined_list.
# 7. Removed the last item from combined_list with pop().
# 8. Checked whether "milk" is still in the final list.
