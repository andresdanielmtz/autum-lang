import re

# open file with termination .aut


def ends_with_dot_aut(file_name: str) -> bool:
    return file_name.endswith(".aut")

def print_statement(line: str, variables: dict) -> None:
    line = line[2:].strip()
    if line not in variables:
        print(line)
    else:
        print(variables[line])


def parse_if_statement(line: str, variables: dict) -> bool:
    line = line[2:].strip()
    operator = [">", "<", ">=", "<=", "==", "!=", "!", "="]
    operator_match = re.search(r"(.*[><]=?|==|!=)\s*(.+)", line)

    if bool(operator_match):
        lhs = ""
        final_operator = ""
        rhs = (
            operator_match.group(2).strip()
            if len(operator_match.groups()) >= 2
            else None
        )
        
        for char in line:
            if len(final_operator) <= 1:
                if char in operator:
                    final_operator += char
                else:
                    lhs += char
        lhs = lhs.strip()[0]

        # print(lhs)
        # print(rhs)
        # print(final_operator)

        if lhs in variables and (rhs is None or rhs in variables):
            x = variables[lhs]
            y = variables[rhs] if rhs else None

            # Perform the comparison based on the operator
            return eval(f"{x} {final_operator} {y}")

        else:
            print("Variable(s) not found in dictionary")
            return False

    else:
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

