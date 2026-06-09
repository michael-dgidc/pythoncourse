# Simple script to read a student name and exam percentage score.
# It then displays the entered name and computed grade.

name = input('Enter your name: ').strip()

try:
    percentage = float(input('Enter your exam percentage mark (e.g. 75): ').strip())
except ValueError:
    print('Invalid percentage input. Please enter a numeric value.')
    raise SystemExit(1)

if percentage >= 80:
    grade = 'A'
elif percentage >= 70:
    grade = 'B'
elif percentage >= 60:
    grade = 'C'
elif percentage >= 50:
    grade = 'D'
elif percentage >= 40:
    grade = 'E'
else:
    grade = 'F'

print(f'Name: {name}')
print(f'Percentage: {percentage}%')
print(f'Grade awarded: {grade}')
