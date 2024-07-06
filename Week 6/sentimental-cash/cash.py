# Import get_float function from CS50 lib
from cs50 import get_float

# Ask user to enter a valid number and ask until user gives
while True:
    money = get_float("Change owed: ")
    if money > 0:
        break

# Assign an int for count the number of metals
# check for 0.25 0.10 0.05 0.01 in order and extract from total

# for quarters
hmq = int(money / 0.25)
money = round(money - (hmq * 0.25), 2)

# for dimes
hmd = int(money / 0.10)
money = round(money - (hmd * 0.10), 2)

# for nickels
hmn = int(money / 0.05)
money = round(money - (hmn * 0.05), 2)

# for pennies
hmp = int(money * 100)

coins = hmq + hmd + hmn + hmp

print(coins)