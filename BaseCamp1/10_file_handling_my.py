# Mode	What It Does
# "r"	Read (default) → file must exist
# "w"	Write → creates new or overwrites existing file
# "a"	Append → add to the end of file
# "x"	Create → makes a new file, error if exists
# "b"	Binary (for images, etc.)

#Read all content
file = open("example.txt", "r")
content = file.read()
print(content)
file.close() 
#always close the file, 
# otherwise The operating system still thinks the file is being used.
# Every open file takes up system resources

#Read line by line
file = open("example.txt", "r")
for line in file:
    print(line.strip())  # strip removes \n
file.close()


#Read into a list
file = open("example.txt", "r")
lines = file.readlines()
print(lines)  # gives you a list of lines
file.close()
print('=' * 20)

# Writing to a File
# Overwrite (w)
file = open("example.txt", "w")
file.write("Hello, this is a new file!\n")
file.write("Second line here.")
file.close()


# ⚠️ Warning: "w" erases old content.
# Append (a)
file = open("example.txt", "a")
file.write("\nAdding a new line at the end.")
file.close()


# There is better way to handle files using 'with' statement
# It automatically takes care of closing the file

with open("example.txt", "r") as file:
    content = file.read()
    print(content)


with open("example.txt", "a") as file:
    file.write("\nAppending a new line to the file.")
    

# 🚀 7. Bonus – Check if File Exists Before Opening
# Sometimes, you want to avoid errors:
import os

if os.path.exists("notes.txt"):
    with open("notes.txt", "r") as file:
        print(file.read())
else:
    print("File does not exist.")
    

print("workbook".center(20, '='))
#WorkBook

# Python File Handling Practice Exercises
# Level 1 – Basics

# Create a file

# Write a Python program to create a file called myfile.txt.

# Inside it, write the text:

# Hello Python!
# I’m learning file handling.


# Read the whole file

# Open myfile.txt in read mode.

# Print all its content at once.

# Read line by line

# Open the same file.

# Print each line separately (remove the \n at the end).

# Append text

# Add this line at the end of myfile.txt:

# This line was appended later.


# Check file exists

# Use Python to check if myfile.txt exists before opening it.

# If it doesn’t exist, print: "File not found!".

# Level 2 – Intermediate

# Count lines in a file

# Count how many lines are in myfile.txt.

# Print: "This file has X lines."

# Save user input to file

# Ask the user to type 3 sentences.

# Save them into a file called diary.txt.

# Read file into a list

# Open diary.txt.

# Store each line in a list and print the list.

# Copy content from one file to another

# Read all content from myfile.txt.

# Write it into a new file copy.txt.

# Word counter

# Read myfile.txt.

# Count how many words it contains.

# Print the number.

# Level 3 – Small Project

# 📂 Mini Diary App

# Create a Python program called diary.py.

# Features:

# Each time the program runs, ask the user: "Write your diary entry:".

# Save the entry into diary.txt with today’s date.

# Then ask: "Do you want to read all past entries? (yes/no)".

# If yes, print the whole diary.

with open("myfile.txt", 'w') as file:
    file.write("Hello Python!\n")
    file.write("I'm learning file handling.\n")

with open("myfile.txt", 'r') as file:
    print("heelo")
    print(file.read()) #pointer is at the end after read
        
    # Go back to start of file
    file.seek(0)

    print("\nLine by line:")
    for line in file:
        print(line.strip())
    for line in file: # nothing will be printed as pointer is at the end
        print(line.strip())


with open("myfile.txt", 'a') as file:
    file.write("This line is appended.\n")
    file.write("Appending another line.\n")
print("Appended lines.")

if os.path.exists("myfile.txt"):
    with open("myfile.txt", 'r') as file:
        print("\nFinal file content:")
        print(file.read())
else:   
    print("File not found!")    


with open("example.txt", 'r') as file:
    file_list = file.readlines()
    print('This file has X lines:', len(file_list))
    
for i in range(3):
    user_input = input("Enter something: ")
    with open("diary.txt", 'a') as file:
        file.write(user_input + '\n')