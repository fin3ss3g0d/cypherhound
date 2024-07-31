from colorama import Fore, Style

red = Fore.RED + Style.BRIGHT
default = Style.BRIGHT
reset = Style.RESET_ALL
green = Style.BRIGHT + Fore.GREEN
yellow = Style.BRIGHT + Fore.YELLOW

def log_command_invalid(e):
    print(f'{red}[-] Invalid command: {e}{reset}')


def log_error(e):
    print(f'{red}[-] Error: {e}{reset}')


def log_no_results():
    print(f'{red}[-] No results from cypher{reset}')


def log_invalid_option(option):
    print(f'{red}[-] Invalid option: {option}{reset}')


def log_successful_export(path):
    print(f'{green}[+] Successful export to: {path}{reset}')


def log_config_not_set(c):
    print(f'{red}[-] {c} is not set!{reset}')


def log_successful_set(i, r):
    print(f'{green}[+] {i} set to {r} successfully!{reset}')
