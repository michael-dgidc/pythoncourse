# DataTypesDemo.py
# Demonstrates creation, initialization, and type-checking of common Python data types.

def show(name, value):
    # prints a readable representation and the type name of `value`
    print(f"{name}: {value!r} (type: {type(value).__name__})")

# Numeric types
int_var = 42  # integer literal assigned to `int_var`
float_var = 3.14159  # floating-point literal assigned to `float_var`
complex_var = 2 + 3j  # complex number with real=2 and imag=3

# Text and boolean
str_var = "hello, world"  # string assigned to `str_var`
bool_var = True  # boolean True assigned to `bool_var`

# Sequence types
list_var = [1, "two", 3.0]  # list containing mixed-type elements
tuple_var = (1, 2, 3)  # immutable tuple of integers
range_var = range(5)  # range object representing 0..4

# Set types
set_var = {1, 2, 3}  # unordered unique collection (set)
frozenset_var = frozenset([1, 2, 3])  # immutable set (frozenset)

# Mapping
dict_var = {"a": 1, "b": 2}  # dict mapping string keys to integer values

# Binary types
bytes_var = b"bytes"  # immutable bytes literal
bytearray_var = bytearray(b"mutable")  # mutable sequence of bytes
memoryview_var = memoryview(b"mem")  # memoryview referencing a bytes object

# Special
none_var = None  # NoneType value representing 'no value'

# Display all variables with their types and values
show("int_var", int_var)
show("float_var", float_var)
show("complex_var", complex_var)
show("str_var", str_var)
show("bool_var", bool_var)
show("list_var", list_var)
show("tuple_var", tuple_var)
show("range_var", range_var)
show("set_var", set_var)
show("frozenset_var", frozenset_var)
show("dict_var", dict_var)
show("bytes_var", bytes_var)
show("bytearray_var", bytearray_var)
show("memoryview_var", memoryview_var)
show("none_var", none_var)

# Example: check types using isinstance for a few select variables
print()  # blank line for readability in output
print("Type checks:")
print("list_var is list:", isinstance(list_var, list))  # True if list_var is a list
print("dict_var is dict:", isinstance(dict_var, dict))  # True if dict_var is a dict
print("int_var is int:", isinstance(int_var, int))  # True if int_var is an int
print("str_var is str:", isinstance(str_var, str))  # True if str_var is a str

# Summary of demonstrations:
# 1. Creation: defined examples for numbers, text, sequences, sets, mappings, binary types, and None.
# 2. Initialization: each variable assigned an idiomatic literal or constructor.
# 3. Inspection: `show()` prints value and its type using `type(...).__name__`.
# 4. Type checks: `isinstance()` used to verify runtime types for common containers.
# 5. Notes: `list` is mutable, `tuple` and `frozenset` are immutable, `bytes` is immutable while `bytearray` is mutable.
