# FROM HERE
# https://stackoverflow.com/questions/4033723/how-do-i-access-command-line-arguments

import sys

print(sys.argv)

# Get the first argument
first_argument = sys.argv[1]

# Output the first argument to the console
print(f"The first argument is: {first_argument}")