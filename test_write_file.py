from functions.write_file import write_file
case_1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print(case_1)
case_2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
print(case_2)
case_3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print(case_3)