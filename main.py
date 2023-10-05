import parse as prs
import logging as log
import sys


def read_from_stdin():
    program = sys.stdin.read()
    lines = program.splitlines()
    var_dict = {}
    for line in lines:
        if line.startswith("//"):
            continue
        prs.handle_line(line, var_dict)


def read_from_file(filename):
    try:
        prs.readFile(filename)
    except ValueError as ve:
        log.warning(ve)
        print(ve)
    except Exception as e:
        log.warning(f"Could not read and parse {filename}. Error: {e}")


if __name__ == "__main__":
    log.basicConfig(filename="file.log", encoding="utf-8", level=log.DEBUG)
    log.info("Starting Normal Procedure")

    # check if there's any input from stdin
    if not sys.stdin.isatty():  # if stdin is being used (piped or redirected)
        try:
            log.info("Reading from stdin")
            read_from_stdin()
        except Exception as e:
            log.warning(f"Could not parse input from stdin. Error: {e}")
    elif len(sys.argv) > 1:  # if there's a filename argument
        FILENAME = sys.argv[1]
        try:
            log.info(f"Reading {FILENAME}")
            read_from_file(FILENAME)
        except Exception as e:
            log.warning(f"Could not read and parse {FILENAME}. Error: {e}")
    else:
        print("Please provide a program via stdin or specify a filename as an argument.")
        sys.exit(1)
