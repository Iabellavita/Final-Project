import subprocess as sub
from concurrent.futures import ProcessPoolExecutor

list_bomb = ["https://icanhazip.com/",
             "https://icanhazip.com/",
             "https://icanhazip.com/",
             "https://icanhazip.com/",
             "https://icanhazip.com/",
             "https://icanhazip.com/",
             "https://icanhazip.com/",
             "https://icanhazip.com/",
             "https://icanhazip.com/",
             "https://icanhazip.com/",
             "https://icanhazip.com/",
             "https://icanhazip.com/",
             "https://icanhazip.com/",
             "https://icanhazip.com/",
             "https://icanhazip.com/",
             "https://icanhazip.com/",
             "https://icanhazip.com/"]


def ex_command(site: str):
    command = 'ping'.split(' ')
    command.append(site)
    sub.call(command)


def main():
    with ProcessPoolExecutor(max_workers=len(list_bomb)) as ex:
        ex.map(ex_command, list_bomb)


if __name__ == '__main__':
    main()
