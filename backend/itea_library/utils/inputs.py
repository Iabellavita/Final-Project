from . import logprint


def input_numeric(msg: str):
    while True:
        inp = input(msg)
        if inp.isnumeric():
            return int(inp)
        else:
            logprint.print_fail('invalid input!')
            input('Press Enter to continue...')
