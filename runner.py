import os
import subprocess
import sys


class cc:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():
    """
    Runner for local competitive programming.

    Each question must be in a folder. Each folder must contain
    a python file and text files for input and expected output.
    
    For the text files, the following structure is expected:
    'X.in' for input and 'X.out' for output. X can be anything as
    long as both .in and .out have the same name.
    """
    timeout = 10
    if len(sys.argv) == 3: 
        timeout = int(sys.argv[2])

    ex_folders = sorted(
        list(filter(os.path.isdir, os.listdir(os.getcwd())))
    )

    for folder in ex_folders:
        files = sorted(os.listdir(f"{os.getcwd()}/{folder}"))
        inputs = []
        outputs = []
        exec = None

        for file in files:
            if "in" in file:
                inputs.append(file)
            elif "out" in file:
                outputs.append(file)
            elif ".py" in file:
                exec = file
        if not exec:
            print("Python file not found")
            break
        if len(inputs) != len(outputs):
            print(f"Uneven IO files for folder {folder}")
            break

        ok = True
        failed = 0

        for position, _ in enumerate(inputs):
            input_file = open(f"{folder}/{inputs[position]}")
            output_file = open(f"{folder}/{outputs[position]}")
            expected_value = output_file.read()
            subprocess_value = subprocess.run(
                ["python3", f"{folder}/{exec}"],
                stdin=input_file, capture_output=True, timeout=timeout
            )
            return_value = subprocess_value.stdout.decode()
            if expected_value != return_value:
                failed += 1
                ok = False
                print(f"{cc.FAIL}F - Expected {repr(expected_value)} but got {repr(return_value)}{cc.RESET}")
            else:
                print(f"{cc.OK}.{cc.RESET}")
        print(f"{cc.OK}All tests ({len(inputs)}) passed for {cc.BOLD}{folder}{cc.RESET}" if ok else f"{cc.FAIL}Not all tests ({failed}/{len(inputs)}) passed for {cc.BOLD}{folder}{cc.RESET}")

main()
