"""
NOTE: This file MUST be run with ADMINISTRATOR PRIVILEGES to work

command:

MacOs:

copy and paste --> sudo python3 configure_ip.py

Linux:

copy and paste --> su python configure_ip.py


Windows (CMD Terminal):

highly recommended to install gsudo (https://github.com/gerardog/gsudo)

gsudo command:

copy and paste --> sudo python configure_ip.py

"""
# imports
import os
import sys
import platform

# functions 
def Windows():
    winpath = os.path.join(os.environ['WINDIR'], "System32", "Drivers", "etc", "hosts")
    print(winpath)

    with open(winpath, 'a') as f:
        f.writelines(['127.0.0.1       routelookup.io\n', '127.0.0.1       application.routelookup.io'])

def Linux():
    linpath = os.path.join(os.path.expanduser('~'), '..', '..', 'etc', 'hosts')
    print(linpath)

    with open(linpath, 'a') as f:
        f.writelines(['127.0.0.1       routelookup.io\n', '127.0.0.1       application.routelookup.io'])


def MacOs():
    macpath = os.path.join(os.path.expanduser('~'), '..', '..', 'private', 'etc', 'hosts')
    print(macpath)

    with open(macpath, 'a') as f:
        f.writelines(['127.0.0.1       routelookup.io\n', '127.0.0.1       application.routelookup.io'])

if __name__ == '__main__':
    system = platform.system()

    if system == 'Windows':
        Windows()
    elif system == 'Linux':
        Linux()
    elif system == 'Darwin':
        MacOs()
    else:
        print("Not in a currently supported system")
        sys.exit(0)

    print("process complete")
    sys.exit(0)
    