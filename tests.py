from functions.get_files_content import get_file_contents
from functions.write_files import write_file
from functions.run_python import run_python


def run_tests():
    
    result = get_file_contents('calculator','main.py')
    print(result)
    
    result = write_file('calculator','test_write.txt', 'Hello, World!')
    print(result)
    
    result = run_python('calculator','test_write.txt')
    print(result)
    
    result = run_python("calculator", "main.py")
    print(result)

    result = run_python("calculator", "tests.py")
    print(result)

    result = run_python("calculator", "../main.py")
    print(result)

    result = run_python("calculator", "nonexistent.py")
    print(result)
    
    
    # result = run_python("calculator", "main.py")
    # print(result)
    
    # result = run_python("calculatir", "main.py", ["3 + 5"])
    # print(result)
    
    
    # result = run_python("calculator", "tests.py")
    # print(result)
    
    # result = run_python("calculator", "../main.py")
    # print(result)
    
    # result = run_python("calculator", "nonexistent.py")
    # print(result)
    
if __name__ == "__main__":
    run_tests()