from . import bcolors


def print_fail(msg: str) -> None:
    print(f"{bcolors.colors.FAIL}FAIL: {msg}{bcolors.colors.ENDC}")


def print_done(msg: str) -> None:
    print(f"{bcolors.colors.OKGREEN}DONE: {msg}{bcolors.colors.ENDC}")


def print_warning(msg: str) -> None:
    print(f"{bcolors.colors.WARNING}WARNING: {msg}{bcolors.colors.ENDC}")
