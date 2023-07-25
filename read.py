import parse as prs
import logging as log

if __name__ == "__main__":
    FILENAME = "code_example.aut"

    log.basicConfig(filename="file.log", encoding="utf-8", level=log.DEBUG)
    log.info("Starting Normal Procedure")

    try:
        log.info(f"Reading {FILENAME}")
        prs.readFile(FILENAME)
    except:
        log.warning("Could not perform PARSE -> READFILE.")
