# Python Script to Output the First Argument to the Console
# Python Version: 3.11 (latest stable version as of October 2023)

"""
prompt for AI deep seek
Create a script for use the Python Library Yahoo Finance API with the following characteristics
    1. Take the first argument that was specified when the program started and output it to the console
"""

import sys

# Check if at least one argument is provided
if len(sys.argv) < 2:
    print("Error: No argument provided.")
    print("Usage: python script.py <argument>")
    sys.exit(1)

# Get the first argument
first_argument = sys.argv[1]

# Output the first argument to the console
print(f"The first argument is: {first_argument}")

"""
python script.py Hello
"""