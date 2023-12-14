from escpos.printer import Serial
from settings import *
from time import sleep


def wah_parser(text):
    # TODO: parse wah/wahwah here
    return text

def print_ticket(key, amount, sips, chugs):
    try:
        parsed_amount = wah_parser(str(amount))
        parsed_sips = wah_parser(str(sips))
        parsed_chugs = wah_parser(str(chugs))

        p = Serial(PRINTER_PORT, baudrate=57600)

        p.set(align='left', bold=False, double_width=False, double_height=False)
        p.text("*********************\n")
        p.control("LF")
        p.set(align='center')
        p.image('C:\\Users\\rfon2\\Downloads\\test3.png', True, True, fragment_height=960, center=True)
        p.control("LF")
        p.set(align='center', bold=False, double_width=True, double_height=True)

        p.text("Mgcil Drinking Slot\nMachine Voucher\n")
        p.set(align='center', bold=True, double_width=True, double_height=True)
        p.control("LF")
        p.text(f"{parsed_amount} $\n")
        p.control("LF")

        p.qr(key, size=10, native=True)
        p.control("LF")

        p.set(align='center', normal_textsize=True, bold=False, double_width=False, double_height=False)
        p.text(f"STATS:   sips: {parsed_sips}   chugs: {parsed_chugs}\n")
        p.control("LF")

        p.set(align='center', bold=False, double_width=True, double_height=True)
        p.text("*********************\n")
        p.cut()
    
    except:
        print("Failed to print voucher")
        sleep(2)
