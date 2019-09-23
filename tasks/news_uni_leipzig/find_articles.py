#!/bin/python3

input_file = open("wdt_2019-07-08_deu.source", "r")
file_lines = input_file.readlines()

# for line in file_lines:
#     if not line.strip():
#         print("empty string")
#     else:
#         print("\n")

for line in file_lines:
    if not line.strip():
        print("empty string")
    else:
        print(len(line.split()))


