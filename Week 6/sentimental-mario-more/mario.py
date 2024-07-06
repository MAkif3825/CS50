# Ask a number until they give number between 1 and 8
while True:
    try:
        h = int(input("Height: "))
        if 1 <= h <= 8:
            break
    # If user types non-int value, handle it
    except ValueError:
        print("", end="")

for j in range(1, h + 1):
    print(" " * (h - j), end="")
    print("#" * j, end="  ")
    print("#" * j)

