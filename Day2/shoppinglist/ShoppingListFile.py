# create a shopping list and save it to a file with formatted text
shopping_items = ["milk", "eggs", "bread", "butter"]  # initial list
more_items = ["cheese", "yogurt", "fruit", "vegetables"]  # second list
combined_items = shopping_items + more_items  # combine lists
combined_items.append("juice")  # add one more item
combined_items.append("cereal")  # add another item
combined_items.remove("bread")  # remove an item from the list
combined_items.sort()  # sort the items alphabetically
combined_items.reverse()  # reverse the sorted items

output_file = "shopping_list.txt"  # file path for saving the formatted list
with open(output_file, "w") as file:  # open the file for writing
    file.write("Shopping List Summary\n")  # write a header line
    file.write("=====================\n")  # write a separator
    for index, item in enumerate(combined_items, start=1):  # iterate through each item
        file.write(f"{index}. {item}\n")  # write each item with a number
    file.write("\n")  # blank line before summary
    file.write("Summary of operations:\n")  # write summary header
    file.write("1. Created two shopping lists.\n")
    file.write("2. Combined both shopping lists.\n")
    file.write("3. Added juice and cereal.\n")
    file.write("4. Removed bread.\n")
    file.write("5. Sorted the list alphabetically.\n")
    file.write("6. Reversed the sorted list.\n")

print(f"Formatted shopping list written to {output_file}")  # notify the user