from functions.get_files_content import get_file_contents
from functions.write_files import write_file
from functions.run_python import run_python


def test():
    result = run_python("calculator", "main.py")
    print(result)

    result = run_python("calculator", "tests.py")
    print(result)

    result = run_python("calculator", "../main.py")
    print(result)

    result = run_python("calculator", "nonexistent.py")
    print(result)


if __name__ == "__main__":
    test()
