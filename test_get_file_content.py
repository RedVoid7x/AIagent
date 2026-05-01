from functions.get_file_contents import get_file_content
from config import MAX_CHARS
contents = get_file_content("calculator", "lorem.txt")
check_length = len(contents)
check_truncation = contents.endswith(f"{MAX_CHARS} characters]")
print(check_length, check_truncation)

print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat")) #(this should return an error string)
print(get_file_content("calculator", "pkg/does_not_exist.py")) #(this should return an error string)