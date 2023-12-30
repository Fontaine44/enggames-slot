from escpos.printer import Serial
from settings import *
from time import sleep


def wah_parser(text):
    text = text.replace('5', 'wah').replace('7', '(wahwah)')
    return text

def print_ticket(player):
    try:
        parsed_amount = wah_parser(str(player.balance))
        parsed_sips = wah_parser(str(player.sips))
        parsed_chugs = wah_parser(str(player.chugs))

        p = Serial(PRINTER_PORT, baudrate=57600)

        p.set(align='center', bold=False, double_width=True, double_height=True)
        p.text("*********************\n")
        p.control("LF")
        p.set(align='center')
        p.image(MGCIL_LOGO_PATH, True, True, fragment_height=960, center=True)
        p.control("LF")
        p.set(align='center', bold=False, double_width=True, double_height=True)

        p.text("Mgcil Drinking Slot\nMachine Coupon\n")
        p.set(align='center', bold=True, double_width=True, double_height=True)
        p.control("LF")
        p.text(f"{parsed_amount} $\n")
        p.control("LF")

        p.text("  ")
        p.qr(player.id, size=10, native=True)
        p.control("LF")

        p.set(align='center', normal_textsize=True, bold=False, double_width=False, double_height=False)
        p.text(f"STATS:   sips: {parsed_sips}   chugs: {parsed_chugs}\n")
        p.control("LF")

        p.set(align='center', bold=False, double_width=True, double_height=True)
        p.text("*********************\n")
        p.cut()
    
    except Exception as e:
        print("Failed to print voucher")
        print(e)
        sleep(2)
