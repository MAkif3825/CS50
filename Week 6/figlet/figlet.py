import sys
import random

from pyfiglet import Figlet
figlet = Figlet()



length = len(sys.argv)
list = figlet.getFonts()

if length == 1:
    rand = random.randint(0, len(list) - 1)
    figlet.setFont(font = list[rand])
    print(figlet.renderText(input("Input: ")))
elif length == 3:
    if sys.argv[1] == "-f" or sys.argv[1] == "--font":
        if sys.argv[2] in list:
            figlet.setFont(font = sys.argv[2])
            print(figlet.renderText(input("Input: ")))
        else:
            print("Invalid usage")
            sys.exit(1)
    else:
        print("Invalid usage")
        sys.exit(1)
else:
    print("Invalid usage")
    sys.exit(1)
