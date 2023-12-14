from escpos.printer import Serial
import random
import string

def generate_key(length=6):
    characters = string.ascii_uppercase + string.digits
    key = ''.join(random.choice(characters) for _ in range(length))
    return key

KEY=generate_key()
print(KEY)

p = Serial("COM7", baudrate=57600)
p.profile.profile_data["media"]["width"]["pixel"] = 300

# p.set(align='left', bold=False, double_width=False, double_height=False)
# p.text("*********************\n")
# p.control("LF")
# p.set(align='center')
# p.image('C:\\Users\\rfon2\\Downloads\\test3.png', True, True, fragment_height=960, center=True)
# p.control("LF")
# p.set(align='center', bold=False, double_width=True, double_height=True)

p.text("Mgcil Drinking Slot\nMachine Voucher\n")
p.set(align='center', bold=True, double_width=True, double_height=True)
p.control("LF")
p.text("wah46.00 $\n")
p.control("LF")

p.barcode("{B012ABCDabcd", "CODE128 ", height=120, width=3, align_ct=True, function_type="B")
p.set(align='left', bold=False, double_width=False, double_height=False)
p.control("LF")
p.text("*********************\n")
p.cut()


