# Import get_string
from cs50 import get_string

# Ask user for input
text = get_string("Text: ")


letters = 0.00
words = 1.00
sentences = 0.00

for i in text:
    # Calculate the words
    if i == " ":
        words += 1.00
    # Calculate the sentences
    elif i == "." or i == "!" or i == "?":
        sentences += 1.00
    # Calculate the letters
    elif i.isalpha():
        letters += 1.00

# Calculate the needed values
L = letters / words * 100
S = sentences / words * 100

# Calculate the result
result = round((0.0588 * L) - (0.296 * S) - 15.8)

# Print it (16+ , 1-)
if result < 1:
    print("Before Grade 1")
elif result > 16:
    print("Grade 16+")
else:
    print(f"Grade {result}")