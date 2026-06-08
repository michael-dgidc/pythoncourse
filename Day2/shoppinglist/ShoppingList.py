# initial list
l1 = ["milk", "eggs", "bread", "butter"]
# second list
l2 = ["cheese", "yogurt", "fruit", "vegetables"]
combined_list = l1 + l2
print("Combined Shopping List:", combined_list)
# add more items to the list
combined_list.append("juice")
combined_list.append("cereal")
print("Updated Shopping List:", combined_list)
# remove an item from the list
combined_list.remove("bread")
print("Shopping List after removing bread:", combined_list)
# sort the list alphabetically
combined_list.sort()
print("Sorted Shopping List:", combined_list)
# reverse the list
combined_list.reverse()
print("Reversed Shopping List:", combined_list)
# check if an item is in the list
if "milk" in combined_list:
    print("Milk is in the shopping list.")
else:
    print("Milk is not in the shopping list.")
