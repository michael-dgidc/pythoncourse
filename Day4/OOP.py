class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"I am {self.name}.")


class Student(Person):  # Inheritance
    def introduce(self):  # Method overriding
        print(f"I am {self.name}, a student.")


class Teacher(Person):  # Inheritance
    def introduce(self):  # Method overriding
        print(f"I am {self.name}, a teacher.")


# Objects of different classes
people = [
    Student("Alice", 20),
    Teacher("Bob", 40),
    Person("John", 30)
]

# Polymorphism
for person in people:
    person.introduce()