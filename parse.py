import re

# open file with termination .aut


def ends_with_dot_aut(file_name: str) -> bool:
    return file_name.endswith(".aut")


def print_statement(line: str, variables: dict) -> None:
    line = line[2:].strip()
    if line in variables:  # Check if the variable exists in the dictionary
        print(variables[line])
    elif line.startswith('"') and line.endswith('"'):  # Check if it is a string
        print(line[1:-1])  # Print the string without quotes
    else:
        print("Variable(s) not found in dictionary")


def parse_if_statement(line: str, variables: dict) -> bool:
    line = line[2:].strip()
    operator = [">", "<", ">=", "<=", "==", "!=", "!", "="]

    for op in operator:
        if op in line:
            lhs, final_operator, rhs = map(str.strip, line.partition(op))

            if lhs in variables:
                x = variables[lhs]

                if rhs in variables:
                    y = variables[rhs]
                else:
                    y = rhs  # If RHS is not a variable, use the direct value
                evaluation = eval(f"{x} {final_operator} {y}")

                return evaluation  # Evaluates the entire operation
                

            else:
                print(f"\nLHS: {lhs} \nFINAL_OPERATOR: {final_operator} \nRHS: {rhs}")
                print("Variable(s) not found in dictionary")
                return False

    print("Invalid if statement")
    return False



def check_else(abstraction_level: int) -> bool:
    return abstraction_level == -1


def readFile(file: str) -> None:
    if not ends_with_dot_aut(file):
        return

    var_dict = {}
    abstraction_level = 0
    comment_prefix = "//"

    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if ("\t" in line) or abstraction_level < 0:
                line = comment_prefix
            else:
                line = line.lstrip()
            # print("line: ", line)
            # print("Abstraction Level: ", abstraction_level)

            if line.startswith("pr"):
                print_statement(line, var_dict)

            elif line.startswith("if"):
                if parse_if_statement(line, var_dict):
                    abstraction_level = 1
                else:
                    abstraction_level = -1

            elif line.startswith("else") and abstraction_level == -1:
                if not parse_if_statement(line, var_dict):
                    abstraction_level = 1
                else:
                    abstraction_level = -1

            elif line.startswith(comment_prefix):
                continue

            elif "=" in line:
                key, val = line.split("=")
                var_dict[key.strip()] = val.strip()
            else:
                print(f"Invalid Syntax: {line}")
