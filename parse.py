def ends_with_dot_autum(file_name: str) -> bool:
    return file_name.endswith(".autum")


def print_statement(line: str, variables: dict) -> None:
    line = line[2:].strip()
    if line in variables:  # Check if the variable exists in the dictionary
        print(variables[line])
    elif line.startswith('"') and line.endswith('"'):  # Check if it is a string
        print(line[1:-1])  # Print the string without quotes
    else:
        print("Variable(s) not found in dictionary")


def handle_if_statement(line: str, variables: dict) -> bool:
    return parse_if_statement(line, variables)


def handle_else_statement(line: str, variables: dict) -> None:
    if not parse_if_statement(line, variables):
        return


def handle_assignment(line: str, variables: dict) -> None:
    key, val = line.split("=")
    variables[key.strip()] = val.strip()


def handle_line(line: str, variables: dict) -> None:
    line = line.lstrip()
    if line.startswith("pr"):
        print_statement(line, variables)
    elif line.startswith("if"):
        if handle_if_statement(line, variables):
            return
    elif line.startswith("else"):
        handle_else_statement(line, variables)
    elif "=" in line:
        handle_assignment(line, variables)
    else:
        print(f"Invalid Syntax: {line}")


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

                return eval(f"{x} {final_operator} {y}")

    print("Invalid if statement")
    return False


def readFile(file: str) -> None:
    if not ends_with_dot_autum(file):
        raise ValueError(f"File {file} does not have the expected .autum extension")

    var_dict = {}
    comment_prefix = "//"

    with open(file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith(comment_prefix):
                continue
            handle_line(line, var_dict)
