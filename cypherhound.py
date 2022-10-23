#!/usr/bin/python3
# Author: Dylan Evans|fin3ss3g0d
import argparse
import terminal
import readline
import sys
import signal
import log


def signal_handler(sig, frame):
    sys.exit(0)


banner = """
  /$$$$$$                      /$$                          
 /$$__  $$                    | $$                          
| $$  \__/ /$$   /$$  /$$$$$$ | $$$$$$$   /$$$$$$   /$$$$$$ 
| $$      | $$  | $$ /$$__  $$| $$__  $$ /$$__  $$ /$$__  $$
| $$      | $$  | $$| $$  \ $$| $$  \ $$| $$$$$$$$| $$  \__/
| $$    $$| $$  | $$| $$  | $$| $$  | $$| $$_____/| $$      
|  $$$$$$/|  $$$$$$$| $$$$$$$/| $$  | $$|  $$$$$$$| $$      
 \______/  \____  $$| $$____/ |__/  |__/ \_______/|__/      
           /$$  | $$| $$                                    
          |  $$$$$$/| $$                                    
           \______/ |__/
 /$$   /$$                                     /$$          
| $$  | $$                                    | $$          
| $$  | $$  /$$$$$$  /$$   /$$ /$$$$$$$   /$$$$$$$          
| $$$$$$$$ /$$__  $$| $$  | $$| $$__  $$ /$$__  $$          
| $$__  $$| $$  \ $$| $$  | $$| $$  \ $$| $$  | $$          
| $$  | $$| $$  | $$| $$  | $$| $$  | $$| $$  | $$          
| $$  | $$|  $$$$$$/|  $$$$$$/| $$  | $$|  $$$$$$$          
|__/  |__/ \______/  \______/ |__/  |__/ \_______/          

        (Author: Dylan Evans|fin3ss3g0d)
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Python terminal app that runs various Neo4j cyphers on BloodHound data sets.")
    parser.add_argument("-u", "--user", help="Neo4j username", required=True)
    parser.add_argument("-p", "--pwd", help="Neo4j password", required=True)
    args = parser.parse_args()
    readline.set_completer(terminal.Completer(terminal.OPTIONS).complete)
    readline.parse_and_bind('tab: complete')
    signal.signal(signal.SIGINT, signal_handler)
    print(f'{log.default}{banner}{log.reset}')
    terminal.input_loop(args.user, args.pwd)
