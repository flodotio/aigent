from functions.get_file_content import get_file_content

print(f"{get_file_content("calculator", "lorem.txt")}")

print(f"{get_file_content("calculator", "main.py")}")

print(f"{get_file_content("calculator", "pkg/calculator.py")}")

print(f"{get_file_content("calculator", "/bin/cat")}")

print(f"{get_file_content("calculator", "pkg/does_not_exist.py")}")